# -*- coding: utf-8 -*-
import nose
from extender.manager import InstanceManager


class TestClass1(object):
    pass


class TestClass2(object):
    pass


def test_manager_with_not_instances():
    manager = InstanceManager(instances=False)
    manager.add('{module}.{name}'.format(
        module=TestClass1.__module__,
        name=TestClass1.__name__
    ))
    manager.add('{module}.{name}'.format(
        module=TestClass2.__module__,
        name=TestClass2.__name__
    ))
    manager.add('non.exists')  ## non exists class

    classes = manager.all()
    assert len(classes) == 2

if __name__ == '__main__':
    nose.runmodule()
