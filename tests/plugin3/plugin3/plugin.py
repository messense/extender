# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from extender import Plugin
import plugin2


class TestPlugin3(Plugin):
    title = 'Plugin3'
    slug = 'plugin3'
    description = 'My awesome plugin!'
    version = plugin2.__version__
    priority = 2

    author = 'Your Name'
    author_url = 'https://github.com/yourname/pluginname'

    def is_enabled(self):
        return False

    def test_func1(self, msg):
        return msg

    def test_func2(self, a, b):
        return 'a * b = %i' % (a * b)

    def test_func3(self, value):
        return 'Plugin3 %s' % value
