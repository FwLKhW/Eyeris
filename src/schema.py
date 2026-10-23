from typing import TypedDict


class CollectionSchema(TypedDict):
    path: str
    name: str


class MetadataSchema(TypedDict):
    rating: int
    tags: list[str]
    palette: list[tuple[int]]
    creator: str
    description: str


class IndexedImageSchema(TypedDict):
    id: str
    indexed: int
    path: str
    name: str
    format: str
    size: int
    width: int
    height: int
    created: int
    modified: int
    metadata: MetadataSchema
