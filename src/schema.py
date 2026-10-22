from typing import TypedDict


class Library(TypedDict):
    path: str
    name: str


class GalleryImage(TypedDict):
    id: str
    name: str
    width: int
    height: int


class Timestamps(TypedDict):
    indexed: int
    created: int
    modified: int


class Metadata(TypedDict):
    rating: int
    tags: list[str]
    palette: list[tuple[float]]
    creator: str
    description: str


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
