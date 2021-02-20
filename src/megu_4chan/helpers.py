# -*- encoding: utf-8 -*-
# Copyright (c) 2021 Stephen Bunn <stephen@bunn.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""Contains useful helper functions used throughout the project."""

from base64 import b64decode

from megu.hasher import HashType
from megu.helpers import http_session
from megu.models import Checksum

from .constants import API_DOMAIN, IMAGE_DOMAIN
from .types import Thread


def get_content_id(board: str, post_id: str) -> str:
    """Build a post's content id.

    Args:
        board (str):
            The board the post was pulled from.
        post_id (str):
            The post's existing id.

    Returns:
        str:
            The appropriate content id.
    """

    return f"4chan-{board}-{post_id}"


def get_image_url(board: str, image_id: str, ext: str) -> str:
    """Get an image's hosting url.

    Args:
        board (str):
            The board the image was pulled from.
        image_id (str):
            The image id of the image (pulled from post["tim"]).
        ext (str):
            The extension of the image (pulled from post["ext"]).

    Returns:
        str:
            The appropriate image url.
    """

    return f"https://{IMAGE_DOMAIN}/{board}/{image_id}{ext}"


def get_thumbnail_url(board: str, id: str) -> str:
    """Get an image thumbnail's hosting url.

    Args:
        board (str):
            The board the image was pulled from.
        image_id (str):
            The image id of the image (pulled from post["tim"]).

    Returns:
        str:
            The appropriate image thumbnail url.
    """

    return f"https://{IMAGE_DOMAIN}/{board}/{id}s.jpg"


def get_thread_url(board: str, thread_id: str) -> str:
    """Get a thread's JSON api endpoint.

    Args:
        board (str):
            The board the thread lives in.
        thread_id (str):
            The id of the thread.

    Returns:
        str:
            The appropriate thread's JSON api endpoint.
    """

    return f"https://{API_DOMAIN}/{board}/thread/{thread_id}.json"


def get_thread(board: str, thread_id: str) -> Thread:
    """Get the thread data for a given thread.

    Args:
        board (str):
            The board the thread lives in.
        thread_id (str):
            The id of the thread.

    Raises:
        ValueError:
            If the request to retrieve the thread data fails.

    Returns:
        ~types.Thread:
            The extracted thread data.
    """

    thread_url = get_thread_url(board, thread_id)
    with http_session() as session:
        response = session.get(thread_url)
        if response.status_code not in (200,):
            raise ValueError(f"Failed to get response for thread at {thread_url}")

        response_body: Thread = response.json()
        return response_body


def get_checksum(md5_hash: str) -> Checksum:
    """Produce a Checksum instance for some 4chan encoded md5 hash.

    Args:
        md5_hash (str):
            The encoded md5 hash from a post.

    Returns:
        megu.models.Checksum:
            The appropriate checksum instance for the given hash.
    """

    return Checksum(type=HashType.MD5, hash=b64decode(md5_hash).hex())
