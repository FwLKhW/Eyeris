from datetime import datetime
from typing import Literal, TypedDict

import numpy as np
import pandas as pd

Orientation = Literal["landscape", "portrait", "square"]

COLOR_COLUMNS = ("color_1", "color_2", "color_3", "color_4")


class ImageFilter(TypedDict, total=False):
    """Every key is optional. Conditions are combined with AND."""

    # Name (case-insensitive substring of `name`)
    name: str

    # Format, e.g. ["PNG", "JPG"] (case-insensitive)
    formats: list[str]

    # File size in bytes
    min_size: int
    max_size: int

    # Dimensions in pixels
    min_width: int
    max_width: int
    min_height: int
    max_height: int
    orientation: Orientation

    # Rating 0..=5
    min_rating: int
    max_rating: int

    # Tags (case-insensitive)
    tags_any: list[str]  # has at least one of these tags
    tags_all: list[str]  # has all of these tags
    has_tags: bool  # True: tagged only, False: untagged only

    # Timestamps
    created_after: datetime
    created_before: datetime
    modified_after: datetime
    modified_before: datetime

    # Dominant color, "#RRGGBB". Match if any of the 4 colors is within
    # `color_distance` (Euclidean distance in RGB, 0..~441) of it.
    color: str
    color_distance: float


def _hex2rgb(value: str) -> tuple[int, int, int]:
    h = value.lstrip("#")
    if len(h) != 6:
        raise ValueError(f"Expected color like '#RRGGBB', got {value!r}")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def _color_distance(df: pd.DataFrame, target: tuple[int, int, int]) -> pd.Series:
    """Smallest RGB distance between `target` and any dominant color of each image."""
    # (n, 4) float array, NaN where the color is NULL
    colors = df[list(COLOR_COLUMNS)].to_numpy(dtype="float64", na_value=np.nan)
    valid = ~np.isnan(colors)

    packed = np.nan_to_num(colors).astype(np.int64)  # 0xRRGGBB
    rgb = np.stack(  # (n, 4, 3)
        [(packed >> 16) & 255, (packed >> 8) & 255, packed & 255], axis=-1
    )

    dist = np.linalg.norm(rgb - np.array(target), axis=-1)  # (n, 4)
    dist[~valid] = np.inf  # NULL color never matches

    return pd.Series(dist.min(axis=1), index=df.index)


def filter_images(df: pd.DataFrame, flt: ImageFilter) -> pd.DataFrame:
    """Return the rows of `df` (from `Collection.images_df()`) matching `flt`."""
    mask = pd.Series(True, index=df.index)

    if (name := flt.get("name")) is not None:
        mask &= df["name"].str.contains(name, case=False, regex=False, na=False)

    if (formats := flt.get("formats")) is not None:
        mask &= df["format"].str.upper().isin([f.upper() for f in formats])

    if (v := flt.get("min_size")) is not None:
        mask &= df["size"] >= v
    if (v := flt.get("max_size")) is not None:
        mask &= df["size"] <= v

    if (v := flt.get("min_width")) is not None:
        mask &= df["width"] >= v
    if (v := flt.get("max_width")) is not None:
        mask &= df["width"] <= v
    if (v := flt.get("min_height")) is not None:
        mask &= df["height"] >= v
    if (v := flt.get("max_height")) is not None:
        mask &= df["height"] <= v

    match flt.get("orientation"):
        case "landscape":
            mask &= df["width"] > df["height"]
        case "portrait":
            mask &= df["width"] < df["height"]
        case "square":
            mask &= df["width"] == df["height"]
        case None:
            pass

    if (v := flt.get("min_rating")) is not None:
        mask &= df["rating"] >= v
    if (v := flt.get("max_rating")) is not None:
        mask &= df["rating"] <= v

    tags_any = flt.get("tags_any")
    tags_all = flt.get("tags_all")
    has_tags = flt.get("has_tags")
    if tags_any is not None or tags_all is not None or has_tags is not None:
        # "a|b|c" -> {"a", "b", "c"}; NULL / "" -> set()
        tag_sets = (
            df["tags"].fillna("").map(lambda s: {t.lower() for t in s.split("|") if t})
        )
        if tags_any is not None:
            wanted = {t.lower() for t in tags_any}
            mask &= tag_sets.map(lambda s: not s.isdisjoint(wanted))
        if tags_all is not None:
            wanted = {t.lower() for t in tags_all}
            mask &= tag_sets.map(lambda s: wanted <= s)
        if has_tags is not None:
            mask &= tag_sets.map(bool) == has_tags

    # `created` / `modified` are Unix timestamps in milliseconds
    for key, column, is_after in (
        ("created_after", "created", True),
        ("created_before", "created", False),
        ("modified_after", "modified", True),
        ("modified_before", "modified", False),
    ):
        if (when := flt.get(key)) is not None:
            ts = pd.to_datetime(df[column], unit="ms")
            mask &= (
                (ts >= pd.Timestamp(when)) if is_after else (ts <= pd.Timestamp(when))
            )

    if (color := flt.get("color")) is not None:
        max_dist = flt.get("color_distance", 60.0)
        mask &= _color_distance(df, _hex2rgb(color)) <= max_dist

    return df[mask]
