# -*- coding: utf-8 -*-
import logging
from .plugin import Plugin
from .manager import PluginManager

__version__ = '0.1.0'

logging.basicConfig()


def safe_execute(func, *args, **kwargs):
    try:
        result = func(*args, **kwargs)
    except Exception as e:
        if hasattr(func, 'im_class'):
            cls = func.im_class
        else:
            cls = func.__class__
        logger = logging.getLogger('extender.errors.plugins')
        logger.error('Error processing %r on %r: %s',
                     func.__name__,
                     cls.__name__,
                     e,
                     extra={
                         'func_module': cls.__module__,
                         'func_args': args,
                         'func_kwargs': kwargs,
                     },
                     exc_info=True
                     )
    else:
        return result
