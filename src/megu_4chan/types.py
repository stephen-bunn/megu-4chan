# -*- encoding: utf-8 -*-
# Copyright (c) 2021 Stephen Bunn <stephen@bunn.io>
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

"""Contains type definitions used throughout the package."""

from typing import List, Optional, TypedDict


class Post(TypedDict):
    """Describes the Post data from the 4chan API."""

    no: int
    resto: int
    sticky: Optional[int]
    closed: Optional[int]
    now: str
    time: int
    name: str
    trip: Optional[str]
    id: Optional[str]
    capcode: Optional[str]
    country: Optional[str]
    country_name: Optional[str]
    sub: Optional[str]
    com: Optional[str]
    tim: Optional[int]
    filename: Optional[str]
    ext: Optional[str]
    fsize: Optional[int]
    md5: Optional[str]
    w: Optional[int]
    h: Optional[int]
    tn_w: Optional[int]
    tn_h: Optional[int]
    filedeleted: Optional[int]
    spoiler: Optional[int]
    custom_spoiler: Optional[int]
    replies: Optional[int]
    images: Optional[int]
    bumplimit: Optional[int]
    imagelimit: Optional[int]
    tag: Optional[str]
    semantic_url: Optional[str]
    since4pass: Optional[int]
    unique_ips: Optional[int]
    m_img: Optional[int]
    archived: Optional[int]
    archived_on: Optional[int]


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
