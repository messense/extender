# -*- coding: utf-8 -*-
import logging
import six
from threading import local


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
                logger = logging.getLogger('extender.errors')
                logger.exception('Unable to import %s' % cls_path)
                continue
        self.cache = results

        return results


class PluginManager(InstanceManager):
    def __iter__(self):
        return iter(self.all())

    def __len__(self):
        return sum(1 for i in self.all())

    def all(self):
        for plugin in sorted(super(PluginManager, self).all(),
                             key=lambda x: x.get_title()):
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
                logger = logging.getLogger('extender.errors')
                logger.error('Error processing %s() on %r: %s', func_name, plugin.__class__, e, extra={
                    'func_arg': args,
                    'func_kwargs': kwargs,
                }, exc_info=True)
                continue

            if result is not None:
                return result

    def call(self, func_name, *args, **kwargs):
        for plugin in self.all():
            try:
                getattr(plugin, func_name)(*args, **kwargs)
            except Exception as e:
                logger = logging.getLogger('extender.errors')
                logger.error('Error processing %s() on %r: %s', func_name, plugin.__class__, e, extra={
                    'func_arg': args,
                    'func_kwargs': kwargs,
                }, exc_info=True)
                continue

    def register(self, cls):
        self.add('%s.%s' % (cls.__module__, cls.__name__))
        return cls

    def unregister(self, cls):
        self.remove('%s.%s' % (cls.__module__, cls.__name__))
        return cls

plugins = PluginManager()
register = plugins.register
unregister = plugins.unregister


class PluginMount(type):
    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        if IPlugin in bases:
            return new_cls
        if not new_cls.title:
            new_cls.title = new_cls.__name__
        if not new_cls.slug:
            new_cls.slug = new_cls.title.replace(' ', '-').lower()
        return new_cls


class IPlugin(local):
    """
    Plugin interface. Should not be inherited from directly.

    A plugin should be treated as if it were a singleton. The owner does not
    control when or how the plugin gets instantiated, nor is it guaranteed that
    it will happen, or happen more than once.

    All children should allow ``**kwargs`` on all inherited methods.
    """
    # Generic plugin information
    title = None
    slug = None
    description = None
    version = None
    author = None
    author_url = None
    resource_links = ()

    # Global enabled state
    enabled = True
    can_disable = True

    def is_enabled(self):
        """
        Returns a boolean representing if this plugin is enabled.

        If ``project`` is passed, it will limit the scope to that project.
        """
        if not self.enabled:
            return False
        if not self.can_disable:
            return True
        return True

    def get_title(self):
        """
        Returns the general title for this plugin.
        """
        return self.title

    def get_description(self):
        """
        Returns the description for this plugin. This is shown on the plugin configuration
        page.
        """
        return self.description

    def get_resource_links(self):
        """
        Returns a list of tuples pointing to various resources for this plugin.
        """
        return self.resource_links


class Plugin(six.with_metaclass(PluginMount, IPlugin)):
    """
    A plugin should be treated as if it were a singleton. The owner does not
    control when or how the plugin gets instantiated, nor is it guaranteed that
    it will happen, or happen more than once.
    """
    pass
