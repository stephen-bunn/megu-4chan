# -*- encoding: utf-8 -*-
# Copyright (c) 2021 Stephen Bunn <stephen@bunn.io>
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

"""Contains type definitions used throughout the package."""

from typing import List, TypedDict


class Post(TypedDict):
    """Describes the Post data from the 4chan API."""

    no: int
    resto: int
    sticky: int | None
    closed: int | None
    now: str
    time: int
    name: str
    trip: str | None
    id: str | None
    capcode: str | None
    country: str | None
    country_name: str | None
    sub: str | None
    com: str | None
    tim: int | None
    filename: str | None
    ext: str | None
    fsize: int | None
    md5: str | None
    w: int | None
    h: int | None
    tn_w: int | None
    tn_h: int | None
    filedeleted: int | None
    spoiler: int | None
    custom_spoiler: int | None
    replies: int | None
    images: int | None
    bumplimit: int | None
    imagelimit: int | None
    tag: str | None
    semantic_url: str | None
    since4pass: int | None
    unique_ips: int | None
    m_img: int | None
    archived: int | None
    archived_on: int | None


class Thread(TypedDict):
    """Describes the Thread data from the 4chan API."""

    posts: List[Post]


class CatalogPage(TypedDict):
    """Describes the CatalogPage data from the 4chan API."""

    page: int
    threads: List[Thread]


class Catalog(TypedDict):
    """Describes the Catalog data from the 4chan API."""

    pages: List[CatalogPage]
