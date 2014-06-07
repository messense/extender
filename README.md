extender
========
A simple plug-in/extension system on Python inspired by Sentry project.

[![Build Status](https://travis-ci.org/messense/extender.svg)](https://travis-ci.org/messense/extender)
[![Coverage Status](https://coveralls.io/repos/messense/extender/badge.png)](https://coveralls.io/r/messense/extender)

## Installation
In your terminal run

```bash
pip install https://github.com/messense/extender/archive/master.zip
```

Or simply install it from PyPi by executing

```bash
pip install extender
```

## How to write a plugin

A plugins layout generally looks like the following:

    setup.py
    pluginname/
    pluginname/__init__.py
    pluginname/plugin.py

The __init__.py file should contain no plugin logic, and at most, a `__version__ = ‘x.x.x’` line.
For example, if you want to pull the version using pkg_resources (which is what we recommend), your file might contain:

```python
try:
    __version__ = __import__('pkg_resources') \
        .get_distribution(__name__).version
except Exception:
    __version__ = 'unknown'
```

Inside of plugin.py, you’ll declare your Plugin class:

```python
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
```

And you’ll register it via entry_points in your setup.py:

```python
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
```

You can change entry_points key `extender.plugins` to whatever you want.

That’s it! Users will be able to install your plugin via `pip install <package name>`.

## How to install plugins in your code

```python
from extender import install_plugins

install_plugins('extender.plugins')
```

The `install_plugins` function takes an argument `entry_point` to install all plugins(just some python package)
registered to that entry_point automatically.

## How to invoke a method of plugins

```python
from extender import plugins

""" invoke func_name(1, 2), return the result of the first called method """
result = plugins.first('func_name', 1, 2)
""" invoke func_name(1, msg='hello'), no return """
plugins.call('func_name', 1, msg='hello')
""" invoke hook func_name to modify value by every plugin then return it """
value = plugins.hook('func_name', 1)
```

## LICENSE

The MIT License (MIT)

Copyright (c) 2014 messense

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
