use std::{
    fs,
    path::Path,
    time::{SystemTime, UNIX_EPOCH},
};

use anyhow::{Ok, Result};
use image::GenericImageView;
use rgb::Rgb;

use color::extract_colors;
use hash::blake3_hash;
use xmp;

#[derive(Debug)]
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
/// Path does not exist.
/// Image path isn't a child of root.
/// Or failed reading system metadata and xmp metadata.
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

    let indexed_image = IndexedImage {
        name,
        format,
        size,
        width: u32::try_from(width)?,
        height: u32::try_from(height)?,
        created,
        modified,
        rating: xmp_meta.rating,
        tags: xmp_meta.tags,
        hash: blake3_hash(&img),
        colors: extract_colors(&img)?,
    };

    Ok(indexed_image)
}
