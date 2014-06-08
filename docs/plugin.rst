.. _plugin:

Write your plugin
=================

Plugin layout
-------------

A plugins layout generally looks like the following ::


    setup.py
    pluginname/
    pluginname/__init__.py
    pluginname/plugin.py


The __init__.py file should contain no plugin logic, and at most, a ``__version__ = ‘x.x.x’`` line.
For example, if you want to pull the version using pkg_resources (which is what we recommend), your file might contain ::

    try:
    __version__ = __import__('pkg_resources') \
        .get_distribution(__name__).version
    except Exception:
        __version__ = 'unknown'

Plugin class
------------

Inside of plugin.py, you’ll declare your Plugin class ::

    # -*- coding: utf-8 -*-
    from extender import Plugin
    import plugin1


    class PluginName(Plugin):
        title = 'Plugin Name'
        slug = 'pluginname'
        description = 'My awesome plugin!'
        version = plugin1.__version__

        author = 'Your Name'
        author_url = 'https://github.com/yourname/pluginname'

        def test_func(self, msg):
            return msg

You should provider at least ``title``, ``version`` attributes in your plugin class and define whatever method as you wish.

Register your plugin
--------------------

You can register your plugin via entry_points in your setup.py ::

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
    from setuptools import setup

    setup(
        name='pluginname',
        version='0.0.1',
        author='Your name',
        author_email='Your Email address',
        url='https://github.com/yourname/pluginname',
        packages=[
            'pluginname'
        ],
        description='plugin description',
        install_requires=[
            'extender',
        ],
        include_package_data=True,
        entry_points={
            'extender.plugins': [
                'pluginname = pluginname.plugin:PluginName',
            ]
        },
    )

You can change entry_points key ``extender.plugins`` to whatever you want.

That’s it! Users will be able to install your plugin via ``python setup.py install``.
And your plugin will be registered to that entry_points automatically, then you can install/load all these awesome plugins in your code.
