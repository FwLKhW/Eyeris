from typing import TypedDict


class CollectionSchema(TypedDict):
    path: str
    name: str


class IndexedImageSchema(TypedDict):
    id: str
    path: str
    name: str
    format: str
    size: int
    width: int
    height: int
    indexed: int
    created: int
    modified: int
    rating: int
    tags: list[str]
    creator: str
    description: str
    palette: list[tuple[int, int, int]]
