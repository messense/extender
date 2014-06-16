# -*- coding: utf-8 -*-
import sys
import logging
import six
from pkg_resources import iter_entry_points

logging.basicConfig()
logger = logging.getLogger('extender.manager')


class InstanceManager(object):

    def __init__(self, class_list=None, instances=True):
        self.cache = None
        class_list = class_list or []
        self.class_list = None
        self.instances = instances
        self.update(class_list)

    def get_class_list(self):
        return self.class_list

    def add(self, class_path):
        self.cache = None
        self.class_list.append(class_path)

    def remove(self, class_path):
        self.cache = None
        self.class_list.remove(class_path)

    def update(self, class_list):
        """
        Updates the class list and wipes the cache.
        """
        self.cache = None
        self.class_list = class_list

    def all(self):
        """
        Returns a list of cached instances.
        """
        class_list = list(self.get_class_list())
        if not class_list:
            self.cache = []
            return []

        if self.cache is not None:
            return self.cache

        results = []
        for cls_path in class_list:
            module_name, class_name = cls_path.rsplit('.', 1)
            try:
                module = __import__(module_name, {}, {}, class_name)
                cls = getattr(module, class_name)
                if self.instances:
                    results.append(cls())
                else:
                    results.append(cls)
            except Exception:
                logger.exception('Unable to import {cls}'.format(cls=cls_path))
                continue
        self.cache = results

        return results


class PluginManager(InstanceManager):

    def __init__(self, entry_points=None, class_list=None, instances=True):
        super(PluginManager, self).__init__(class_list, instances)
        if entry_points:
            self.install(entry_points)

    def __iter__(self):
        return iter(self.all())

    def __len__(self):
        return sum(1 for i in self.all())

    def all(self, include_disabled=True):
        for plugin in sorted(super(PluginManager, self).all(),
                             key=lambda x: x.priority,
                             reverse=True):
            if not plugin.is_enabled() and not include_disabled:
                continue
            yield plugin

    def get(self, slug):
        for plugin in self.all():
            if plugin.slug == slug:
                return plugin
        raise KeyError(slug)

    def first(self, func_name, *args, **kwargs):
        for plugin in self.all(include_disabled=False):
            try:
                result = getattr(plugin, func_name)(*args, **kwargs)
            except Exception as e:
                logger.error(
                    'Error processing %s() on %r: %s',
                    func_name,
                    plugin.__class__,
                    e,
                    extra={
                        'func_arg': args,
                        'func_kwargs': kwargs,
                    },
                    exc_info=True
                )
                continue

            if result is not None:
                return result

    def call(self, func_name, *args, **kwargs):
        result = []
        for plugin in self.all(include_disabled=False):
            saved_result = result
            try:
                result.append(getattr(plugin, func_name)(*args, **kwargs))
            except Exception as e:
                result = saved_result  # rollback
                logger.error(
                    'Error calling %s() on %r: %s',
                    func_name,
                    plugin.__class__,
                    e,
                    extra={
                        'func_arg': args,
                        'func_kwargs': kwargs,
                    },
                    exc_info=True
                )
                continue
        return result

    def apply(self, func_name, value, *args, **kwargs):
        for plugin in self.all(include_disabled=False):
            saved_value = value
            try:
                value = getattr(plugin, func_name)(value, *args, **kwargs)
            except Exception as e:
                value = saved_value  # rollback
                logger.error(
                    'Error applying %s() on %r: %s',
                    func_name,
                    plugin.__class__,
                    e,
                    extra={
                        'func_arg': args,
                        'func_kwargs': kwargs,
                    },
                    exc_info=True
                )
                continue
        return value

    def register(self, cls):
        if not hasattr(cls, '__name__'):
            # class instance
            cls = cls.__class__
        self.add('{module}.{name}'.format(
            module=cls.__module__,
            name=cls.__name__
        ))
        return cls

    def unregister(self, cls):
        if isinstance(cls, six.string_types):
            # unregister plugin by slug
            slug = cls
            try:
                cls = self.get(slug)
            except KeyError:
                logger.error('No plugin named %s.', slug)
                return
        if not hasattr(cls, '__name__'):
            # class instance
            cls = cls.__class__
        self.remove('{module}.{name}'.format(
            module=cls.__module__,
            name=cls.__name__
        ))
        return cls

    def install(self, entry_points):
        for ep in iter_entry_points(entry_points):
            try:
                plugin = ep.load()
            except Exception:
                logger.exception("Failed to load plugin %r.", ep.name)
            else:
                self.register(plugin)
