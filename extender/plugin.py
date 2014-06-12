# -*- coding: utf-8 -*-
import six
from threading import local


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
    priority = 0
    author = None
    author_url = None
    resource_links = ()

    # Global enabled state
    enabled = True
    can_disable = True

    def is_enabled(self):
        """
        Returns a boolean representing if this plugin is enabled.
        """
        if not self.can_disable:
            return True  # pragma: no cover
        return self.enabled


class PluginMount(type):

    def __new__(mcs, name, bases, attrs):
        new_cls = type.__new__(mcs, name, bases, attrs)
        if IPlugin in bases:
            return new_cls
        if not hasattr(new_cls, 'title'):
            new_cls.title = new_cls.__name__
        if not hasattr(new_cls, 'slug'):
            new_cls.slug = new_cls.title.replace(' ', '-').lower()
        if not hasattr(new_cls, 'priority'):
            new_cls.priority = 0
        if not hasattr(new_cls, 'is_enabled'):
            new_cls.is_enabled = lambda s: True
        return new_cls


class Plugin(six.with_metaclass(PluginMount, IPlugin)):

    """
    A plugin should be treated as if it were a singleton. The owner does not
    control when or how the plugin gets instantiated, nor is it guaranteed that
    it will happen, or happen more than once.
    """
    pass
