use anyhow::Result;
use image::{DynamicImage, GenericImageView};
use rgb::Rgb;

/// # Errors
///
/// The only case this will fail is width or height of the image bigger than 65536.
pub fn extract_colors(img: &DynamicImage) -> Result<Vec<Rgb<u8>>> {
    let (width, height) = img.dimensions();
    let rgb8_img = img.to_rgb8();

    let input = okmain::InputImage::from_bytes(
        u16::try_from(width)?,
        u16::try_from(height)?,
        rgb8_img.as_raw(),
    )?;

    let srgb_colors = okmain::colors(input);

    Ok(srgb_colors)
}

#[must_use]
pub fn rgb2hex(rgb: &Rgb<u8>) -> String {
    format!("#{:02X}{:02X}{:02X}", rgb.r, rgb.g, rgb.b)
}

#[must_use]
#[allow(clippy::arithmetic_side_effects)]
pub fn rgb2dec(rgb: &Rgb<u8>) -> i64 {
    (i64::from(rgb.r) << 16) + (i64::from(rgb.g) << 8) + (i64::from(rgb.b))
}
