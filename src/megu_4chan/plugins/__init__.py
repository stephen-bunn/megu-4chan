# -*- encoding: utf-8 -*-
# Copyright (c) 2021 Stephen Bunn <stephen@bunn.io>
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

"""Contains the various plugins implemented by the package.

This module should expose the implemented plugins.
"""

from megu_4chan.plugins.thread import ThreadPlugin

__all__ = ["ThreadPlugin"]
