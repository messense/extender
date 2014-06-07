# -*- coding: utf-8 -*-
import sys
from pkg_resources import iter_entry_points


def install_plugins(entry_points):
    from .plugin import register

    for ep in iter_entry_points(entry_points):
        try:
            plugin = ep.load()
        except Exception:
            import sys
            import traceback

            sys.stderr.write("Failed to load app %r:\n%s\n" % (ep.name, traceback.format_exc()))
        else:
            register(plugin)
