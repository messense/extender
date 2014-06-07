# -*- coding: utf-8 -*-
from extender import Plugin
import plugin1


class TestPlugin1(Plugin):
    title = 'Plugin1'
    slug = 'plugin1'
    description = 'My awesome plugin!'
    version = plugin1.__version__

    author = 'Your Name'
    author_url = 'https://github.com/yourname/pluginname'

    def test_func(self, msg):
        return msg
