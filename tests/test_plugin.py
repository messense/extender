# -*- coding: utf-8 -*-
import sys
import nose
try:
    from io import StringIO
except ImportError:
    try:
        from StringIO import StringIO
    except ImportError:
        from cStringIO import StringIO


def test_install_plugins():
    from extender import install_plugins, plugins

    install_plugins('extender.plugins')
    msg = plugins.first('test_func1', 'test')
    assert msg == 'test'

    saved_stdout =sys.stdout
    out = StringIO()
    sys.stdout = out
    plugins.call('test_func2', 2, 1)
    output = out.getvalue()
    sys.stdout = saved_stdout
    assert 'a + b = 3' in output
    assert 'a - b = 1' in output

    value = plugins.hook('test_func3', 'test')
    assert value == 'Plugin1 Plugin2 test'

if __name__ == '__main__':
    nose.runmodule()