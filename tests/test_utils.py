import string
from base64 import b64encode

import pytest
from httpx import Response
from hypothesis import given
from hypothesis.strategies import text
from megu.models import ContentChecksum
from respx import MockRouter
from tests.conftest import TEST_THREAD_BOARD, TEST_THREAD_ID

from megu_4chan.constants import API_DOMAIN, IMAGE_DOMAIN
from megu_4chan.utils import (
    get_checksum,
    get_content_id,
    get_image_url,
    get_thread,
    get_thread_url,
    get_thumbnail_url,
)

from .strategies import DEFAULT_NAME_STRAT


@given(DEFAULT_NAME_STRAT, DEFAULT_NAME_STRAT)
def test_get_content_id(board: str, post_id: str):
    assert get_content_id(board, post_id) == f"4chan-{board}-{post_id}"


@given(DEFAULT_NAME_STRAT, DEFAULT_NAME_STRAT, DEFAULT_NAME_STRAT)
def test_get_image_url(board: str, image_id: str, ext: str):
    assert get_image_url(board, image_id, ext) == f"https://{IMAGE_DOMAIN}/{board}/{image_id}{ext}"


@given(DEFAULT_NAME_STRAT, DEFAULT_NAME_STRAT)
def test_get_thubmnail_url(board: str, id: str):
    assert get_thumbnail_url(board, id) == f"https://{IMAGE_DOMAIN}/{board}/{id}s.jpg"


@given(DEFAULT_NAME_STRAT, DEFAULT_NAME_STRAT)
def test_get_thread_url(board: str, thread_id: str):
    assert (
        get_thread_url(board, thread_id) == f"https://{API_DOMAIN}/{board}/thread/{thread_id}.json"
    )


def test_get_thread(respx_mock: MockRouter, thread_api_url: str):
    respx_mock.get(thread_api_url).mock(return_value=Response(200, content=b'{"test": "test"}'))
    assert get_thread(TEST_THREAD_BOARD, TEST_THREAD_ID) == {"test": "test"}


def test_get_thread_raises_ValueError_for_error_response(
    respx_mock: MockRouter, thread_api_url: str
):
    respx_mock.get(thread_api_url).mock(return_value=Response(404))
    with pytest.raises(ValueError) as error:
        get_thread(TEST_THREAD_BOARD, TEST_THREAD_ID)
        assert f"Failed to get response for thread at {thread_api_url}" in str(error)


@given(text("abcdef" + string.digits, min_size=32, max_size=32))
def test_get_checksum(content: str):
    assert get_checksum(b64encode(bytes.fromhex(content)).decode("utf-8")) == ContentChecksum(
        "md5", content
    )
