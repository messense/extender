# -*- coding: utf-8 -*-
import nose


def test_install_plugins():
    from extender import install_plugins, plugins

    install_plugins('extender.plugins')
    msg = plugins.first('test_func', 'test')
    assert msg == 'test'

if __name__ == '__main__':
    nose.runmodule()