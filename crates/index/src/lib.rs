use std::{
    fs,
    path::Path,
    time::{SystemTime, UNIX_EPOCH},
};

use anyhow::{Ok, Result};
use image::GenericImageView;
use rgb::Rgb;

use color::extract_colors;
use hash::blake3_image;

#[derive(Debug, Default)]
pub struct IndexedImage {
    pub name: String,
    pub format: String,
    pub size: u64,
    pub width: u32,
    pub height: u32,
    pub created: u64,
    pub modified: u64,
    pub rating: u8,
    pub tags: Vec<String>,
    pub hash: String,
    pub colors: Vec<Rgb<u8>>,
}

/// # Errors
///
/// Fail when image path does not exist.
/// Or reading system or xmp metadata.
/// Or color extraction.
pub fn indexing_image(img_path: &Path) -> Result<IndexedImage> {
    let name = img_path
        .file_stem()
        .unwrap_or_default()
        .to_str()
        .unwrap_or_default()
        .to_string();
    let format = img_path
        .extension()
        .unwrap_or_default()
        .to_str()
        .unwrap_or_default()
        .to_uppercase();

    let sys_meta = fs::metadata(img_path)?;
    let size = sys_meta.len();
    let created = u64::try_from(
        sys_meta
            .created()
            .unwrap_or_else(|_| SystemTime::now())
            .duration_since(UNIX_EPOCH)
            .unwrap_or_default()
            .as_millis(),
    )?;
    let modified = u64::try_from(
        sys_meta
            .modified()
            .unwrap_or_else(|_| SystemTime::now())
            .duration_since(UNIX_EPOCH)
            .unwrap_or_default()
            .as_millis(),
    )?;

    let img = image::open(img_path)?;
    let (width, height) = img.dimensions();
    let xmp_meta = xmp::read(img_path);
    let hash = blake3_image(&img);
    let colors = extract_colors(&img)?;

    let indexed_image = IndexedImage {
        name,
        format,
        size,
        width,
        height,
        created,
        modified,
        rating: xmp_meta.rating,
        tags: xmp_meta.tags,
        hash,
        colors,
    };

    Ok(indexed_image)
}
