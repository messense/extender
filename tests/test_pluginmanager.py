# -*- coding: utf-8 -*-
import nose
import six
from nose.tools import raises, with_setup
import extender.manager
from extender import PluginManager, Plugin
from extender.plugin import PluginMount


def test_plugins_install():
    plugins = PluginManager()
    plugins.install('extender.plugins')
    assert len(plugins) == 3


def test_plugins_install_with_entry_points():
    plugins = PluginManager(entry_points='extender.plugins')
    assert len(plugins) == 3


def fake_iter_entry_points(entry_points):
    class FakeEP(object):
        name = 'FakeEP'

    return [FakeEP(), FakeEP()]


def setup_func():
    extender.manager.iter_entry_points = fake_iter_entry_points


def teardown_func():
    from pkg_resources import iter_entry_points
    extender.manager.iter_entry_points = iter_entry_points


@with_setup(setup_func, teardown_func)
def test_plugins_install_failed():
    plugins = PluginManager(entry_points='extender.plugins')
    print(plugins.class_list)
    assert len(plugins) == 0


def test_plugins_get():
    plugins = PluginManager()
    plugins.install('extender.plugins')

    assert plugins.get('plugin1') is not None


@raises(KeyError)
def test_plugins_get_with_nonexists_slug():
    plugins = PluginManager()
    plugins.install('extender.plugins')
    plugins.get('test-plugin')


@raises(StopIteration)
def test_plugins_all_with_no_plugins_installed():
    plugins = PluginManager()
    next(plugins.all())


def test_plugins_iteration():
    plugins = PluginManager()
    plugins.install('extender.plugins')
    titles = [p.title for p in plugins]
    assert 'Plugin1' in titles
    assert 'Plugin2' in titles
    assert 'Plugin3' in titles


def test_plugins_enable():
    plugins = PluginManager()
    plugins.install('extender.plugins')

    len1 = len(plugins)
    len2 = sum(1 for i in plugins.all(include_disabled=False))

    assert len1 == 3
    assert len2 == 2


def test_plugins_first():
    plugins = PluginManager()
    plugins.install('extender.plugins')
    msg = plugins.first('test_func1', 'test')
    assert msg == 'test'


def test_plugins_first_with_nonexists_func():
    plugins = PluginManager()
    plugins.install('extender.plugins')
    result = plugins.first('noexists_func')
    assert result is None


def test_plugins_call():
    plugins = PluginManager()
    plugins.install('extender.plugins')
    result = plugins.call('test_func2', 2, 1)
    assert 'a + b = 3' in result
    assert 'a - b = 1' in result
    assert 'a * b = 2' not in result


def test_plugins_call_with_nonexists_func():
    plugins = PluginManager()
    plugins.install('extender.plugins')
    result = plugins.call('noexists_func')
    assert not result


def test_plugins_apply():
    plugins = PluginManager()
    plugins.install('extender.plugins')
    value = plugins.apply('test_func3', 'test')
    assert value == 'Plugin1 Plugin2 test'


def test_plugins_apply_with_nonexists_func():
    plugins = PluginManager()
    plugins.install('extender.plugins')
    value = plugins.apply('noexists_func', 'test')
    assert value == 'test'


class TestPlugin(Plugin):
    title = 'TestPlugin'
    slug = 'testplugin'
    description = 'My awesome plugin!'
    version = '0.0.1'
    priority = 2
    author = 'Your Name'
    author_url = 'https://github.com/yourname/pluginname'

    def test(self):
        return 'test'


class TestGenericPlugin(six.with_metaclass(PluginMount, object)):
    title = 'TestGenericPlugin'

    def test(self):
        return 'test'


def test_plugins_register_with_class():
    plugins = PluginManager()
    plugins.register(TestPlugin)
    assert plugins.first('test') == 'test'


def test_plugins_register_with_instance():
    plugins = PluginManager()
    plugins.register(TestPlugin())
    assert plugins.first('test') == 'test'


def test_plugins_register_generic_plugin_with_class():
    plugins = PluginManager()
    plugins.register(TestGenericPlugin)
    assert plugins.first('test') == 'test'


def test_plugins_unregister_with_slug():
    plugins = PluginManager()
    plugins.install('extender.plugins')

    assert len(plugins) == 3
    plugins.unregister('plugin3')
    assert len(plugins) == 2

    plugins.unregister('pluginnonexists')
    assert len(plugins) == 2


def test_plugins_unregister_with_class():
    plugins = PluginManager()
    plugins.register(TestPlugin)

    assert len(plugins) == 1
    plugins.unregister(TestPlugin)
    assert len(plugins) == 0


def test_plugins_unregister_with_instance():
    plugins = PluginManager()
    plugins.register(TestPlugin)

    assert len(plugins) == 1
    plugins.unregister(TestPlugin())
    assert len(plugins) == 0

if __name__ == '__main__':
    nose.runmodule()
