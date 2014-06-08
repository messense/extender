# -*- coding: utf-8 -*-
import nose
from extender import PluginManager


def test_plugins_install():
    plugins = PluginManager()
    plugins.install('extender.plugins')
    msg = plugins.first('test_func1', 'test')
    assert msg == 'test'


def test_plugins_call():
    plugins = PluginManager()
    plugins.install('extender.plugins')
    result = plugins.call('test_func2', 2, 1)
    assert 'a + b = 3' in result
    assert 'a - b = 1' in result


def test_plugins_apply():
    plugins = PluginManager()
    plugins.install('extender.plugins')
    value = plugins.apply('test_func3', 'test')
    assert value == 'Plugin1 Plugin2 test'


def test_safe_execute():
    from extender import safe_execute

    def raise_error(e):
        raise e

    safe_execute(raise_error, KeyError)

if __name__ == '__main__':
    nose.runmodule()