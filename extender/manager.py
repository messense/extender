# -*- coding: utf-8 -*-
import sys
import logging
import six
from pkg_resources import iter_entry_points


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
                logger.exception('Unable to import %s' % cls_path)
                continue
        self.cache = results

        return results


class PluginManager(InstanceManager):

    def __init__(self, class_list=None, instances=True, entry_points=None):
        super(PluginManager, self).__init__(class_list, instances)
        if entry_points:
            self.install(entry_points)

    def __iter__(self):
        return iter(self.all())

    def __len__(self):
        return sum(1 for i in self.all())

    def all(self):
        for plugin in sorted(super(PluginManager, self).all(),
                             key=lambda x: x.priority,
                             reverse=True):
            if not plugin.is_enabled():
                continue
            yield plugin

    def get(self, slug):
        for plugin in self.all():
            if plugin.slug == slug:
                return plugin
        raise KeyError(slug)

    def first(self, func_name, *args, **kwargs):
        for plugin in self.all():
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
        for plugin in self.all():
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
        for plugin in self.all():
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
        self.add('%s.%s' % (cls.__module__, cls.__name__))
        return cls

    def unregister(self, cls):
        if isinstance(cls, six.string_types):
            # unregister plugin by slug
            slug = cls
            try:
                cls = self.get(slug)
            except KeyError:
                logger.error('No plugin named %s' % slug)
                return False
        self.remove('%s.%s' % (cls.__module__, cls.__name__))
        return True

    def install(self, entry_points):
        for ep in iter_entry_points(entry_points):
            try:
                plugin = ep.load()
            except Exception:
                import traceback
                sys.stderr.write("Failed to load plugin %r:\n%s\n" % (ep.name, traceback.format_exc()))
                logger.exception("Failed to load plugin %r:\n" % ep.name)
            else:
                self.register(plugin)
