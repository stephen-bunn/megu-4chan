# -*- encoding: utf-8 -*-
# Copyright (c) 2021 Stephen Bunn <stephen@bunn.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""Contains constants for global package use."""

API_DOMAIN = "a.4cdn.org"
IMAGE_DOMAIN = "i.4cdn.org"

DOMAIN_PATTERN = r"^https?:\/\/(?:(?:www|boards)\.)?4chan(?:nel)?\.org"
BOARD_PATTERN = DOMAIN_PATTERN + r"\/(?P<board>\w+)"
THREAD_PATTERN = BOARD_PATTERN + r"\/thread/(?P<thread>\d+)"
