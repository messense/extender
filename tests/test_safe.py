# -*- coding: utf-8 -*-
import nose


def test_safe_execute():
    from extender import safe_execute

    def raise_error(e):
        raise e

    safe_execute(raise_error, KeyError)

if __name__ == '__main__':
    nose.runmodule()