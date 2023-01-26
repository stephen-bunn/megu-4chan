from pathlib import Path
from unittest.mock import MagicMock

import pytest
from hypothesis import assume, given
from hypothesis.provisional import urls
from megu.models import URL

from megu_4chan.constants import THREAD_PATTERN
from megu_4chan.thread import ThreadPlugin


def test_ThreadPlugin_name():
    assert ThreadPlugin().name == "4chan Thread"


def test_ThreadPlugin_domains():
    assert ThreadPlugin().domains == {"boards.4chan.org", "boards.4channel.org"}


def test_ThreadPlugin_can_handle(thread_board_url: str):
    assert ThreadPlugin.can_handle(URL(thread_board_url)) == True


@given(urls())
def test_ThreadPlugin_iter_content_raises_ValueError_for_invalid_url(url: str):
    assume(not THREAD_PATTERN.match(url))
    with pytest.raises(ValueError):
        next(ThreadPlugin().iter_content(URL(url)))


def test_ThreadPlugin_write_content():
    artifact_path = MagicMock()
    to_path = Path()
    ThreadPlugin().write_content(("test", [("test", artifact_path)]), to_path)
    artifact_path.rename.assert_called_once_with(to_path)


def test_ThreadPlugin_write_content_raises_ValueError_for_multiple_artifacts():
    with pytest.raises(ValueError):
        ThreadPlugin().write_content(("test", []), Path())

    with pytest.raises(ValueError):
        ThreadPlugin().write_content(("test", [("test1", Path()), ("test2", Path())]), Path())
