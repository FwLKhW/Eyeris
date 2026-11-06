use std::path::Path;

use anyhow::{Context, Result, bail};
use image::imageops::FilterType;

/// Create 512px bound `thumbnail.png` in the same folder as source image.
///
/// # Errors
///
/// Failed if image not exists or save thumbnail fail.
pub fn generate_thumbnail(img_path: &Path) -> Result<()> {
    let Some(parent) = img_path.parent() else {
        bail!("can not get parent of image")
    };

    let thumbnail_save_path = parent.join("thumbnail.png");
    if thumbnail_save_path.exists() {
        return Ok(());
    }

    let img = image::open(img_path)
        .with_context(|| format!("failed open image {}", img_path.display()))?;

    let thumbnail = img.resize(512, 512, FilterType::Lanczos3);

    thumbnail.save(&thumbnail_save_path).with_context(|| {
        format!(
            "failed save thumbnail for {} at {}",
            img_path.display(),
            thumbnail_save_path.display()
        )
    })?;

    Ok(())
}
