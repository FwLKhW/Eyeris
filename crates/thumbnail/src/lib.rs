use std::path::Path;

use anyhow::{Context, Result};
use image::imageops::FilterType;

/// # Errors
///
/// Failed if image not exists or save thumbnail fail.
pub fn generate_thumbnail(
    img_path: &Path,
    thumb_folder_path: &Path,
    thumb_name: &str,
) -> Result<()> {
    let thumbnail_save_path = thumb_folder_path.join(format!("{thumb_name}.png"));
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
