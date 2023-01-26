"""Contains the logic necessary for extracting content from a 4chan thread."""

from datetime import datetime
from mimetypes import guess_type
from pathlib import Path
from typing import Generator

from megu.helpers import http_session
from megu.models import URL, Content, ContentManifest, ContentMetadata, HTTPResource
from megu.plugin import BasePlugin

from megu_4chan.constants import THREAD_PATTERN
from megu_4chan.utils import (
    get_checksum,
    get_content_id,
    get_image_url,
    get_thread,
    get_thumbnail_url,
)


class ThreadPlugin(BasePlugin):
    """4chan thread plugin."""

    @property
    def name(self) -> str:
        """Name of the thread plugin."""

        return "4chan Thread"

    @property
    def domains(self) -> set[str]:
        """Domains handled by the thread plugin."""

        return {"boards.4chan.org", "boards.4channel.org"}

    @classmethod
    def can_handle(cls, url: URL) -> bool:
        """Ensure that the plugin only attempts to process URLs that it can handle.

        Args:
            url (megu.models.URL):
                The URL to check.

        Returns:
            bool:
                True if the plugin can handle the given url, otherwise False.
        """

        return THREAD_PATTERN.match(str(url)) is not None

    def iter_content(self, url: URL) -> Generator[Content, None, None]:
        """Extract 4chan thread content from the given url.

        Args:
            url (megu.models.URL):
                The validated url provided by the user.

        Raises:
            ValueError:
                If something unexpected occurs when extracting groups from the url.

        Yields:
            Generator[megu.models.Content, None, None]:
                The content discovered by the plugin.
        """

        # extract details from the url
        match = THREAD_PATTERN.match(str(url))
        if not match:
            raise ValueError(f"Failed to match url {url}")

        groups = match.groupdict()
        board = groups.get("board", None)
        thread = groups.get("thread", None)

        # I'm unsure if we can ever get the board and the thread if we fail the thread match
        if not board or not thread:  # pragma: no cover
            raise ValueError(f"Failed to extract board and thread from url {url}")

        # iterate over available posts from the given url
        for post in get_thread(board, thread)["posts"]:
            print(post)
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
            post_meta = ContentMetadata(
                id=post_id,
                description=post.get("com"),
                publisher=post.get("name"),
                published_at=(datetime.fromtimestamp(post["time"]) if "time" in post else None),
                filename=post.get("filename"),
                thumbnail=URL(post_thumbnail_url),
            )

            post_image_size = post.get("fsize")
            if post_image_size is None:
                with http_session() as session:
                    post_image_size = session.head(post_image_url).headers.get("Content-Length", 0)

            # yield the raw image content
            yield Content(
                id=get_content_id(board, post_id),
                group=get_content_id(board, post_id),
                name="Post Image",
                url=url,
                quality=1.0,
                size=int(post_image_size),
                type=post_image_type,
                resources=[HTTPResource(method="GET", url=post_image_url)],
                metadata=post_meta,
                checksums=[get_checksum(post["md5"])],  # type: ignore
                extra=dict(post),
            )

            # yield the image thumbnail content (if available)
            with http_session() as session:
                head_response = session.head(post_thumbnail_url)
                if head_response.status_code in (200,):
                    post_thumbnail_size = head_response.headers.get("content-length")

                    yield Content(
                        id=f"{get_content_id(board, post_id)}-thumbnail",
                        group=get_content_id(board, post_id),
                        name="Post Thumbnail",
                        url=url,
                        quality=0.0,
                        size=int(post_thumbnail_size),
                        type="image/jpeg",
                        resources=[HTTPResource(method="GET", url=post_thumbnail_url)],
                        metadata=post_meta,
                        extra=dict(post),
                    )

    def write_content(self, manifest: ContentManifest, to_path: Path) -> Path:
        """Merge the downloaded manifest to the appropriate filepath.

        .. important::
            This plugin assumes that only one artifact is downloaded and included in
            the manifest. Since the content from 4chan is not chunked up, we can handle
            fetching the content through a single HTTPResource.

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

        _, artifacts = manifest
        if len(artifacts) != 1:
            raise ValueError(
                f"{self.__class__.__name__!s} expects only one artifact, "
                f"received {len(artifacts)}"
            )

        _, only_artifact = artifacts[0]
        only_artifact.rename(to_path)

        return to_path
