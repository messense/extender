# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from extender import Plugin
import plugin1


class TestPlugin1(Plugin):
    title = 'Plugin1'
    slug = 'plugin1'
    description = 'My awesome plugin!'
    version = plugin1.__version__
    priority = 1

    author = 'Your Name'
    author_url = 'https://github.com/yourname/pluginname'

    def test_func1(self, msg):
        return msg

    def test_func2(self, a, b):
        print('a - b = %i' % (a - b))

    def test_func3(self, value):
        return 'Plugin1 %s' % value
