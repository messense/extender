.. _manager:

Install and manage plugins
==========================

Setup a plugin manager
----------------------

To install your awesome plugins, you should initialize a ``PluginManager`` first ::

    from extender import PluginManager

    plugins = PluginManager()

Install plugins
---------------

With a instance of ``PluginManager`` class, we can install plugins of a specific entry_points by calling the ``install`` method of ``PluginManager`` ::

    from extender import PluginManager
    plugins = PluginManager()

    plugins.install('extender.plugins')


To setup a plugin manager and install plugins quickly you can do it by ::

    from extender import PluginManager
    plugins = PluginManager('extender.plugins')
    # or
    # plugins = PluginManager(entry_points='extender.plugins')


Use plugins
-----------

You can use ``plugins.call(func_name, *args, **kwargs)`` method to invoke the method `func_name` on every plugin
and return a list of results which contains return value of each invoked method of plugins ::

    from extender import PluginManager
    plugins = PluginManager()

    plugins.install('extender.plugins')

    result_list = plugins.call('say', 1, msg='hello')

To get single value of the first invoked plugin's return value, use ``first`` instead of ``call`` ::

    from extender import PluginManager
    plugins = PluginManager()

    plugins.install('extender.plugins')

    result = plugins.first('say', 1, msg='hello')

If you want to apply some method of plugins on a variable and return the value(maybe modified by plugins), you can use ``apply`` ::

    from extender import PluginManager
    plugins = PluginManager()

    plugins.install('extender.plugins')

    value = "Hello world!"
    value = plugins.apply('greet', value)
