# -*- encoding: utf-8 -*-
# Copyright (c) 2021 Stephen Bunn <stephen@bunn.io>
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

"""The Megu 4chan plugin.

This package should expose only the plugins implemented by the package.
"""

from megu import register_plugin

from megu_4chan.plugins import ThreadPlugin

register_plugin(ThreadPlugin)

__all__ = ["ThreadPlugin"]
