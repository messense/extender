# -*- coding: utf-8 -*-
import nose
from extender import safe_execute


def test_safe_execute():
    def test(msg):
        return msg
    assert safe_execute(test, 'test') == 'test'


def test_safe_execute_with_exception():
    def raise_error(e):
        raise e

    safe_execute(raise_error, KeyError)


class TestSafeExecute(object):

    def normal(self, msg):
        return msg

    def raise_error(e):
        raise e


def test_safe_execute_with_instance_method():
    test = TestSafeExecute()
    msg = safe_execute(test.normal, 'test')
    assert msg == 'test'

    safe_execute(test.raise_error, KeyError)

if __name__ == '__main__':
    nose.runmodule()
