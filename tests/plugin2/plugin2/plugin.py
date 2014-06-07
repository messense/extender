# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from extender import Plugin
import plugin2


class TestPlugin2(Plugin):
    title = 'Plugin2'
    slug = 'plugin2'
    description = 'My awesome plugin!'
    version = plugin2.__version__
    priority = 2

    author = 'Your Name'
    author_url = 'https://github.com/yourname/pluginname'

    def test_func1(self, msg):
        return msg

    def test_func2(self, a, b):
        print('a + b = %i' % (a + b))

    def test_func3(self, value):
        return 'Plugin2 %s' % value
