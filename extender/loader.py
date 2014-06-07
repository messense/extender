# -*- coding: utf-8 -*-
import sys
import logging
from pkg_resources import iter_entry_points


def install_plugins(entry_points):
    from .plugin import register
    logger = logging.getLogger("extender.loader")
    for ep in iter_entry_points(entry_points):
        try:
            plugin = ep.load()
        except Exception:
            import traceback
            sys.stderr.write("Failed to load plugin %r:\n%s\n" % (ep.name, traceback.format_exc()))
            logger.exception("Failed to load plugin %r:\n" % ep.name)
        else:
            register(plugin)
