# -*- encoding: utf-8 -*-
# Copyright (c) 2021 Stephen Bunn <stephen@bunn.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""Contains the logic necessary for extracting content from a 4chan thread."""

import re
from datetime import datetime
from mimetypes import guess_type
from pathlib import Path
from typing import Generator

from megu.helpers import http_session
from megu.models import Content, HttpMethod, HttpResource, Manifest, Meta, Url
from megu.plugin import BasePlugin

from ..constants import THREAD_PATTERN
from ..helpers import (
    get_checksum,
    get_content_id,
    get_image_url,
    get_thread,
    get_thumbnail_url,
)


class ThreadPlugin(BasePlugin):
    """4chan thread plugin."""

    name = "4chan Thread"
    domains = {"boards.4chan.org", "boards.4channel.org"}
    pattern = re.compile(THREAD_PATTERN)

    def can_handle(self, url: Url) -> bool:
        """Ensure that the plugin only attempts to process URLs that it can handle.

        Args:
            url (megu.models.Url):
                The URL to check.

        Returns:
            bool:
                True if the plugin can handle the given url, otherwise False.
        """

        return self.pattern.match(url.url) is not None

    def extract_content(self, url: Url) -> Generator[Content, None, None]:
        """Extract 4chan thread content from the given url.

        Args:
            url (megu.models.Url):
                The validated url provided by the user.

        Raises:
            ValueError:
                If something unexpected occurs when extracting groups from the url.

        Yields:
            Generator[megu.models.Content, None, None]:
                The content discovered by the plugin.
        """

        # extract details from the url
        match = self.pattern.match(url.url)
        if not match:
            raise ValueError(f"Failed to match url {url.url}")

        groups = match.groupdict()
        board = groups.get("board", None)
        thread = groups.get("thread", None)

        if not board or not thread:
            raise ValueError(f"Failed to extract board and thread from url {url.url}")

        # iterate over available posts from the given url
        for post in get_thread(board, thread)["posts"]:
            if post.get("filename") is None or post.get("ext") is None:
                continue

            post_id = str(post["no"])
            post_image_id = str(post["tim"])
            post_image_url = get_image_url(
                board,
                post_image_id,
                post["ext"],  # type: ignore
            )
            post_image_type, _ = guess_type(post_image_url)
            post_thumbnail_url = get_thumbnail_url(board, post_image_id)

            if post_image_type is None:
                # XXX: assume image is jpeg is filemagic fails for some reason
                post_image_type = "image/jpeg"

            # construct the available metadata from the given post
            post_meta = Meta(
                id=post_id,
                description=post.get("com"),
                publisher=post.get("name"),
                published_at=(
                    datetime.fromtimestamp(post["time"]) if "time" in post else None
                ),
                filename=post.get("filename"),
                thumbnail=post_thumbnail_url,
            )

            # yield the raw image content
            yield Content(
                id=get_content_id(board, post_id),
                url=url.url,
                quality=1.0,
                size=post["fsize"],
                type=post_image_type,
                resources=[HttpResource(method=HttpMethod.GET, url=post_image_url)],
                meta=post_meta,
                checksums=[get_checksum(post["md5"])],  # type: ignore
                extra=post,
            )

            # yield the image thumbnail content (if available)
            with http_session() as session:
                head_response = session.head(post_thumbnail_url)
                if head_response.status_code in (200,):
                    post_thumbnail_size = head_response.headers.get("content-length")

                    yield Content(
                        id=get_content_id(board, post_id),
                        url=url.url,
                        quality=0.0,
                        size=post_thumbnail_size,
                        type="image/jpeg",
                        resources=[
                            HttpResource(method=HttpMethod.GET, url=post_thumbnail_url)
                        ],
                        meta=post_meta,
                        extra=post,
                    )

    def merge_manifest(self, manifest: Manifest, to_path: Path) -> Path:
        """Merge the downloaded manifest to the appropriate filepath.

        .. important::
            This plugin assumes that only one artifact is downloaded and included in
            the manifest. Since the content from 4chan is not chunked up, we can handle
            fetching the content through a single HttpResource.

        Args:
            manifest (megu.models.Manifest):
                The manifest including the downloaded artifacts.
            to_path (~pathlib.Path):
                The path to merge the file contents to.

        Raises:
            ValueError:
                If the given manifest does have exactly 1 artifact.

        Returns:
            ~pathlib.Path:
                The path the manifest artifacts were merged to (should be *to_path*).
        """

        if len(manifest.artifacts) != 1:
            raise ValueError(
                f"{self.__class__.__name__!s} expects only one artifact, "
                f"received {len(manifest.artifacts)}"
            )

        _, only_artifact = manifest.artifacts[0]
        only_artifact.rename(to_path)

        return to_path
