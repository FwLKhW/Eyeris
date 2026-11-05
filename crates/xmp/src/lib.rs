//
// This crate wraps `xmp_toolkit` to read and write Eyeris custom XMP metadata.
//
// The metadata lives under the custom namespace `http://eyeris.app/xmp/1.0` with the XML prefix
// `eyeris`. For now only two properties are defined:
//
//   * `Rating`  – a single unsigned integer (star rating)
//   * `Tags`    – an ordered array of strings (keywords)
//

use std::path::Path;

use anyhow::Result;
use xmp_toolkit::{OpenFileOptions, XmpFile, XmpMeta, XmpValue};

/// The XML namespace URI for the Eyeris custom XMP properties.
pub const NS: &str = "http://eyeris.app/xmp/1.0";
/// The XML namespace prefix for the Eyeris custom XMP properties.
pub const PREFIX: &str = "eyeris";

/// Holds the Eyeris custom XMP properties read from (or to be written to) a file.
#[derive(Debug, Default)]
pub struct CustomXmp {
    /// Star rating, typically `0..=5`. Stored as a simple integer property.
    pub rating: u8,
    /// Keywords/tags. Stored as an ordered array property so tag order is preserved.
    pub tags: Vec<String>,
}

impl CustomXmp {
    /// Property name for the rating.
    pub const RATING: &str = "Rating";
    /// Property name for the tags array.
    pub const TAGS: &str = "Tags";
}

fn register_eyeris_namespace() -> xmp_toolkit::XmpResult<String> {
    XmpMeta::register_namespace(NS, PREFIX)
}

/// Read the Eyeris custom XMP metadata from a file.
///
/// Returns default empty `CustomXmp` when the file miss or wrong properties.
pub fn read(filepath: &Path) -> CustomXmp {
    let Ok(meta) = XmpMeta::from_file(filepath) else {
        return CustomXmp::default();
    };

    let _ = register_eyeris_namespace();

    let rating = meta
        .property_i32(NS, CustomXmp::RATING)
        .map(|value| value.value as u8)
        .unwrap_or(0);

    let tags = meta
        .property_array(NS, CustomXmp::TAGS)
        .map(|item| item.value)
        .collect();

    CustomXmp { rating, tags }
}

/// Write the `Rating` property into a file's XMP metadata.
///
/// Creates the XMP packet if the file has none. Because the file is opened for update, the change
/// is persisted to disk when the file is closed (`try_close`).
///
/// # Errors
///
/// Returns an error if the file cannot be opened, the XMP packet cannot be created/staged, or the
/// file cannot be closed and written.
pub fn write_rating(filepath: &Path, rating: u8) -> Result<()> {
    let _ = register_eyeris_namespace();

    let mut file = XmpFile::new()?;
    file.open_file(filepath, OpenFileOptions::default().for_update())?;

    // Reuse the existing XMP packet when present, otherwise start from an empty packet so we can
    // write metadata into files that previously had none.
    let mut meta = match file.xmp() {
        Some(meta) => meta,
        None => XmpMeta::new()?,
    };

    // XMP stores everything as strings; `set_property_i32` converts the integer for us.
    meta.set_property_i32(NS, CustomXmp::RATING, &XmpValue::new(i32::from(rating)))?;

    file.put_xmp(&meta)?;
    file.try_close()?;
    Ok(())
}

/// Write the `Tags` array property into a file's XMP metadata.
///
/// Any previously written `Tags` array is removed first, then the supplied tags are appended in
/// order as an ordered array (`rdf:Seq`), so tag order is preserved. Creates the XMP packet if the
/// file has none. The change is persisted to disk when the file is closed (`try_close`).
///
/// # Errors
///
/// Returns an error if the file cannot be opened, the XMP packet cannot be created/staged, an
/// array item cannot be appended, or the file cannot be closed and written.
pub fn write_tags(filepath: &Path, tags: &Vec<String>) -> Result<()> {
    let _ = register_eyeris_namespace();

    let mut file = XmpFile::new()?;
    file.open_file(filepath, OpenFileOptions::default().for_update())?;

    let mut meta = match file.xmp() {
        Some(meta) => meta,
        None => XmpMeta::new()?,
    };

    // Remove any previously written tags so the file stores exactly the supplied list.
    let _ = meta.delete_property(NS, CustomXmp::TAGS);

    if !tags.is_empty() {
        // Describe the array as ordered so it serializes as an `rdf:Seq` (preserves item order).
        let array_name = XmpValue::new(CustomXmp::TAGS.to_string())
            .set_is_array(true)
            .set_is_ordered(true);

        // `append_array_item` creates the array if necessary and appends after the last item.
        // XMP array indices are 1-based, but appending does not require an explicit index.
        for tag in tags {
            meta.append_array_item(NS, &array_name, &XmpValue::new(tag.clone()))?;
        }
    }

    file.put_xmp(&meta)?;
    file.try_close()?;
    Ok(())
}
