from __future__ import annotations

import math
from datetime import datetime
from pathlib import PurePosixPath
from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import to_rgb
from PIL import Image

from src.filter import COLOR_COLUMNS

if TYPE_CHECKING:
    from src.collection import Collection

LOCAL_TZ = datetime.now().astimezone().tzinfo

WEEKDAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]
BUCKETS = ["dark", "mid", "light"]
TIERS = ["<720p", "720p", "1080p", "1440p", "4K+"]

# OKLCH hue centers (degrees) of the 10 main hues.
HUES = {
    "red": 29,
    "orange": 60,
    "yellow": 105,
    "lime": 130,
    "green": 150,
    "cyan": 200,
    "blue": 255,
    "purple": 310,
    "magenta": 345,
    "pink": 5,
}
NEUTRALS = ["black", "gray", "white"]  # low chroma colors have no meaningful hue
GROUPS = [*HUES, *NEUTRALS]
NEUTRAL_CHROMA = 0.04

PALETTE = {
    "red": "#E53935",
    "orange": "#FB8C00",
    "yellow": "#FDD835",
    "lime": "#9CCC65",
    "green": "#43A047",
    "cyan": "#00ACC1",
    "blue": "#1E88E5",
    "purple": "#8E24AA",
    "magenta": "#D81BD0",
    "pink": "#F48FB1",
    "black": "#212121",
    "gray": "#9E9E9E",
    "white": "#EEEEEE",
}

ASPECTS = {
    "1:1": 1,
    "5:4": 5 / 4,
    "4:3": 4 / 3,
    "3:2": 3 / 2,
    "16:10": 16 / 10,
    "16:9": 16 / 9,
    "21:9": 21 / 9,
    "4:5": 4 / 5,
    "3:4": 3 / 4,
    "2:3": 2 / 3,
    "10:16": 10 / 16,
    "9:16": 9 / 16,
}

EXTENDED = [
    "fullname",
    "color_group",
    "bucket",
    "hour",
    "weekday",
    "megapixels",
    "tier",
    "aspect",
    "folder",
]

NUMERIC = [
    "rating",
    "size",
    "width",
    "height",
    "megapixels",
    "bpp",
    "n_tags",
    "lightness",
    "chroma",
    "hour",
]

_M1 = np.array(
    [
        [0.4122214708, 0.5363325363, 0.0514459929],
        [0.2119034982, 0.6806995451, 0.1073969566],
        [0.0883024619, 0.2817188376, 0.6299787005],
    ]
)
_M2 = np.array(
    [
        [0.2104542553, 0.7936177850, -0.0040720468],
        [1.9779984951, -2.4285922050, 0.4505937099],
        [0.0259040371, 0.7827717662, -0.8086757660],
    ]
)


def _packed(df: pd.DataFrame) -> np.ndarray:
    """`(n, 4)` float array of the dominant colors (0xRRGGBB), NaN where NULL."""
    return df[list(COLOR_COLUMNS)].to_numpy(dtype="float64", na_value=np.nan)


def _rgb(packed: np.ndarray) -> np.ndarray:
    v = np.nan_to_num(packed).astype(np.int64)
    return np.stack([(v >> 16) & 255, (v >> 8) & 255, v & 255], axis=-1)


def _oklch(packed: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Packed `0xRRGGBB` -> OKLCH `(lightness 0..1, chroma, hue in degrees)`."""
    srgb = _rgb(packed) / 255
    linear = np.where(srgb <= 0.04045, srgb / 12.92, ((srgb + 0.055) / 1.055) ** 2.4)
    lab = np.cbrt(linear @ _M1.T) @ _M2.T
    light, a, b = lab[..., 0], lab[..., 1], lab[..., 2]
    chroma, hue = np.hypot(a, b), np.degrees(np.arctan2(b, a)) % 360

    null = np.isnan(packed)
    light[null] = chroma[null] = hue[null] = np.nan
    return light, chroma, hue


def _classify(packed: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Packed colors -> `(lightness, chroma, group name)`; group is `None` for NULL."""
    light, chroma, hue = _oklch(packed)

    centers, names = np.array(list(HUES.values())), np.array(list(HUES))
    gap = np.abs((hue[..., None] - centers + 180) % 360 - 180)  # circular distance
    hue_name = names[gap.argmin(axis=-1)]

    neutral = np.select([light < 0.3, light < 0.85], NEUTRALS[:2], NEUTRALS[2])
    group = np.where(chroma < NEUTRAL_CHROMA, neutral, hue_name)
    return (
        light,
        chroma,
        np.where(np.isnan(light), None, group),  # ty: ignore[no-matching-overload]
    )


def color_groups(df: pd.DataFrame) -> pd.DataFrame:
    """Group name of each of the 4 dominant colors (`color_1` .. `color_4`)."""
    return pd.DataFrame(
        _classify(_packed(df))[2], index=df.index, columns=list(COLOR_COLUMNS)
    )


# ---------------------------------------------------------------- features


def _snap_aspect(width: pd.Series, height: pd.Series, tol: float = 0.04) -> np.ndarray:
    """Snap `width / height` to the closest common aspect ratio, or `"other"`."""
    vals = np.array(list(ASPECTS.values()))
    with np.errstate(all="ignore"):
        ratio = (width.to_numpy(float) / height.to_numpy(float))[:, None]
        gap = np.abs(np.log(ratio / vals))
    nearest = gap.argmin(axis=1)
    close = gap[np.arange(len(gap)), nearest] < tol
    return np.where(close, np.array(list(ASPECTS))[nearest], "other")


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add the extended properties (see `EXTENDED`, `NUMERIC`) to `images_df()`."""
    df = df.copy()
    w, h = df["width"], df["height"]

    # Color of the most dominant color
    light, chroma, group = _classify(_packed(df)[:, :1])
    df["lightness"], df["chroma"] = light[:, 0], chroma[:, 0]
    df["color_group"] = pd.Categorical(group[:, 0], categories=GROUPS, ordered=True)
    df["bucket"] = pd.cut(
        df["lightness"], [0, 0.4, 0.75, 1.01], labels=BUCKETS, right=False
    )

    # Time (local)
    for col in ("created", "modified"):
        df[f"{col}_dt"] = pd.to_datetime(df[col], unit="ms", utc=True).dt.tz_convert(
            LOCAL_TZ
        )
    df["hour"] = df["created_dt"].dt.hour
    df["weekday"] = pd.Categorical(
        df["created_dt"].dt.day_name(), categories=WEEKDAYS, ordered=True
    )

    # Geometry
    df["megapixels"] = w * h / 1e6
    df["bpp"] = df["size"] / (w * h).replace(0, np.nan)  # bytes per pixel
    df["orientation"] = np.select([w > h, w < h], ["landscape", "portrait"], "square")
    df["aspect"] = _snap_aspect(w, h)
    df["tier"] = pd.cut(
        df["megapixels"], [0, 0.9, 2.0, 3.6, 8.2, np.inf], labels=TIERS, right=False
    )

    # Source
    df["folder"] = df["origin"].map(lambda p: PurePosixPath(p).parent.name)

    # Tags / rating
    df["tag_list"] = df["tags"].fillna("").map(lambda s: [t for t in s.split("|") if t])
    df["n_tags"] = df["tag_list"].map(len)
    df["rated"] = df["rating"] > 0

    return df


# ---------------------------------------------------------------- stats


def audit(df: pd.DataFrame) -> pd.DataFrame:
    """Null rate (%) plus min / max of every column."""
    nulls = df.isna().mean().mul(100).rename("null_%")
    return pd.concat(
        [nulls, df.select_dtypes("number").agg(["min", "max"]).T], axis=1
    ).round(2)


def share_files_vs_disk(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """Share (%) of files vs share (%) of disk space per value of `col`."""
    files = df[col].value_counts(normalize=True)
    disk = df.groupby(col, observed=True)["size"].sum() / df["size"].sum()
    return pd.DataFrame({"files": files, "disk": disk}).mul(100)


def hour_weekday(df: pd.DataFrame) -> pd.DataFrame:
    """Count of images per weekday (rows) x hour (columns), by creation time."""
    table = pd.crosstab(df["weekday"], df["hour"])
    return table.reindex(index=WEEKDAYS, columns=range(24), fill_value=0)


def pareto(df: pd.DataFrame) -> pd.DataFrame:
    """Cumulative share of disk (%) taken by the biggest files (% of files)."""
    sizes = df["size"].sort_values(ascending=False).to_numpy(dtype="float64")
    return pd.DataFrame(
        {
            "files_%": np.arange(1, len(sizes) + 1) / len(sizes) * 100,
            "disk_%": sizes.cumsum() / sizes.sum() * 100,
        }
    )


def tag_lift(df: pd.DataFrame, top: int = 20) -> pd.DataFrame:
    """log2 lift of the `top` tags: > 0 means they appear together more than by chance."""
    tags = df["tag_list"].explode().dropna()
    if tags.empty:
        raise ValueError("No tags yet. Tag some images first.")

    keep = tags.value_counts().head(top).index
    one = (
        pd.crosstab(tags.index, tags).reindex(columns=keep, fill_value=0).clip(upper=1)
    )
    b = one.to_numpy(dtype="float64")
    n = len(df)

    with np.errstate(all="ignore"):
        lift = np.log2((b.T @ b / n) / np.outer(b.mean(axis=0), b.mean(axis=0)))
    lift[np.isinf(lift)] = np.nan  # never together
    np.fill_diagonal(lift, np.nan)
    return pd.DataFrame(lift, index=keep, columns=keep)


# ---------------------------------------------------------------- show


def _caption(value: object) -> str:
    if isinstance(value, float):
        return f"{value:.2f}"
    if hasattr(value, "strftime"):
        return value.strftime("%Y-%m-%d")  # ty: ignore[call-non-callable]
    return str(value)[:24]


def contact_sheet(
    df: pd.DataFrame, n: int = 5, caption: str = "fullname", cols: int = 5
) -> None:
    """Thumbnail grid of the first `n` rows, captioned with column `caption`."""
    df = df.head(n)
    cols = max(1, min(cols, len(df)))
    rows = max(1, math.ceil(len(df) / cols))

    _, axes = plt.subplots(rows, cols, figsize=(cols * 2.4, rows * 2.7), squeeze=False)
    for ax in axes.ravel():
        ax.axis("off")
    for ax, row in zip(axes.ravel(), df.itertuples(), strict=False):
        ax.imshow(Image.open(row.thumb_path))  # ty: ignore[unresolved-attribute]
        ax.set_title(_caption(getattr(row, caption)), fontsize=8)
    plt.tight_layout()


def swatch(name: str) -> None:
    """Show the color of a group name."""
    plt.figure(figsize=(3, 1))
    plt.imshow([[to_rgb(PALETTE[name])]], aspect="auto")
    plt.axis("off")


def barcode(df: pd.DataFrame, height: int = 40) -> None:
    """Dominant color of every image, sorted by hue, as one strip."""
    packed = df["color_1"].dropna().to_numpy(dtype="float64")
    light, chroma, hue = _oklch(packed)
    colorful = chroma >= NEUTRAL_CHROMA
    order = np.lexsort((light, np.where(colorful, hue, -1.0), colorful))  # grays first

    strip = _rgb(packed)[order] / 255
    plt.figure(figsize=(12, 2))
    plt.imshow(np.repeat(strip[None], height, axis=0), aspect="auto")
    plt.axis("off")


def wrapped(df: pd.DataFrame) -> str:
    """A small 'Spotify Wrapped' style summary of the collection."""
    colors = color_groups(df).stack().value_counts()
    tags = df["tag_list"].explode().value_counts()
    night = df["hour"].isin([22, 23, 0, 1, 2, 3, 4]).mean()
    morning = df["hour"].between(5, 11).mean()
    light = df["lightness"].mean()
    mood = "dark" if light < 0.4 else "bright" if light > 0.7 else "balanced"

    return "\n".join(
        [
            "✨ Eyeris Wrapped ✨",
            f"Images:          {len(df)}",
            f"Color of you:    {colors.index[0]}",
            f"Mood:            {mood} (avg lightness {light:.2f})",
            f"Collector:       {'night owl 🦉' if night >= morning else 'morning person 🐦'}",
            f"Busiest day:     {df['weekday'].mode()[0]}",
            f"Favorite format: {df['format'].mode()[0]}",
            f"Top tag:         {tags.index[0] if len(tags) else '-'}",
        ]
    )


# ---------------------------------------------------------------- embeddings


def load_embeddings(
    collection: Collection, df: pd.DataFrame
) -> tuple[pd.DataFrame, np.ndarray]:
    """Rows of `df` that have an embedding + their unit-norm embeddings `(n, dim)`.

    Row `i` of the returned `X` belongs to row `i` of the returned dataframe.
    """
    res = collection.ss.chroma.get(include=["embeddings"])
    pos = {image_id: i for i, image_id in enumerate(res["ids"])}
    if not pos:
        raise ValueError("No embeddings yet. Run 01_embedding.ipynb first.")

    df = df[df["id"].isin(pos)].reset_index(drop=True)
    x = np.asarray(res["embeddings"], dtype=np.float32)[[pos[i] for i in df["id"]]]
    return df, x / np.linalg.norm(x, axis=1, keepdims=True)


def near_duplicates(
    df: pd.DataFrame, x: np.ndarray, thres: float = 0.95
) -> pd.DataFrame:
    """Pairs of images whose cosine similarity is >= `thres`, most similar first."""
    sims = np.triu(x @ x.T, k=1)
    i, j = np.nonzero(sims >= thres)
    pairs = pd.DataFrame(
        {
            "thumb_a": df["thumb_path"].to_numpy()[i],
            "thumb_b": df["thumb_path"].to_numpy()[j],
            "sim": sims[i, j],
        }
    )
    return pairs.sort_values("sim", ascending=False).reset_index(drop=True)


def show_pairs(pairs: pd.DataFrame, n: int = 5) -> None:
    """Side by side thumbnails of the first `n` pairs of `near_duplicates`."""
    pairs = pairs.head(n)
    _, axes = plt.subplots(
        max(1, len(pairs)), 2, figsize=(5, 2.6 * max(1, len(pairs))), squeeze=False
    )
    for ax in axes.ravel():
        ax.axis("off")
    for axs, row in zip(axes, pairs.itertuples(), strict=False):
        axs[0].imshow(Image.open(row.thumb_a))  # ty: ignore[unresolved-attribute]
        axs[1].imshow(Image.open(row.thumb_b))  # ty: ignore[unresolved-attribute]
        axs[0].set_title(
            f"similarity {row.sim:.3f}",  # ty: ignore[unresolved-attribute]
            fontsize=8,
            loc="left",
        )
    plt.tight_layout()


def taste_profile(
    df: pd.DataFrame, x: np.ndarray, lam: float = 1.0, folds: int = 5
) -> tuple[pd.Series, float]:
    """Ridge regression `embedding -> rating`, fitted on rated images.

    Returns the predicted rating of every image and the Spearman correlation
    of out-of-fold predictions on rated images (how well your taste is predictable).
    """
    y = df["rating"].to_numpy(dtype="float64")
    rated = np.flatnonzero(df["rated"].to_numpy())
    if len(rated) < 20:
        raise ValueError(f"Need at least 20 rated images, found {len(rated)}.")

    def fit_predict(train: np.ndarray, test: np.ndarray) -> np.ndarray:
        xt, mean = x[train], y[train].mean()
        w = np.linalg.solve(
            xt.T @ xt + lam * np.eye(x.shape[1]), xt.T @ (y[train] - mean)
        )
        return x[test] @ w + mean

    parts = np.array_split(np.random.default_rng(0).permutation(rated), folds)
    oof = np.empty(len(df))
    for k, test in enumerate(parts):
        train = np.concatenate([p for i, p in enumerate(parts) if i != k])
        oof[test] = fit_predict(train, test)

    score = pd.Series(oof[rated]).corr(pd.Series(y[rated]), method="spearman")
    return pd.Series(fit_predict(rated, np.arange(len(df))), index=df.index), float(
        score
    )
