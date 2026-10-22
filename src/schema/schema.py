from typing import TypedDict

from slint import Image, ListModel


class Library(TypedDict):
    path: str
    name: str


class GalleryImage(TypedDict):
    id: str
    name: str
    width: int
    height: int
    thumbnail: Image


class Timestamps(TypedDict):
    indexed: int
    created: int
    modified: int


class Metadata(TypedDict):
    rating: int
    tags: ListModel[str]
    palette: ListModel[ListModel[float]]
    creator: str


class IndexedImage(TypedDict):
    id: str
    name: str
    path: str
    size: int
    width: int
    height: int
    format: str
    timestamps: Timestamps
    # metadata: Metadata
