"""Contains constants for global package use."""

import re

API_DOMAIN = "a.4cdn.org"
IMAGE_DOMAIN = "i.4cdn.org"

THREAD_PATTERN = re.compile(
    r"^https?:\/\/(?:(?:www|boards)\.)?4chan(?:nel)?\.org\/(?P<board>\w+)\/thread/(?P<thread>\d+)"
)
