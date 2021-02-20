# -*- encoding: utf-8 -*-
# Copyright (c) 2021 Stephen Bunn <stephen@bunn.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""The Megu 4chan plugin.

This package should expose only the plugins implemented by the package.
"""

from .plugins import ThreadPlugin

__all__ = ["ThreadPlugin"]
