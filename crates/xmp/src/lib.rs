//
// This crate wraps `xmp_toolkit` to read and write Eyeris custom XMP metadata.
//
// The metadata lives under the custom namespace `http://eyeris.app/xmp/1.0` with the XML prefix
// `eyeris`. For now only two properties are defined:
//
//   * `Rating`  – a single unsigned integer (star rating)
//   * `Tags`    – an ordered array of strings (keywords)
//
// # How the XMP Toolkit is used
//
// The C++ XMP Toolkit (wrapped by `xmp_toolkit`) keeps namespace registrations as *global state*.
// Before any property in the `eyeris` namespace can be addressed by its URI, that URI must be
// registered once with `XmpMeta::register_namespace`. Registration is idempotent, so the helpers
// below register the namespace on every call for simplicity.
//
// Writing follows the [`XmpFile`](xmp_toolkit::XmpFile) workflow:
//
//   1. `XmpFile::new`        – allocate a file handle
//   2. `open_file(.., for_update)` – open the target file for read/write
//   3. `xmp()`               – obtain the `XmpMeta` (create an empty one if absent)
//   4. mutate the `XmpMeta`
//   5. `put_xmp(&meta)`      – stage the new packet
//   6. `try_close()`         – write the packet to disk and close
//
// Updates are lost if the `XmpFile` is dropped without calling `close`/`try_close`.

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

/// Register the `eyeris` namespace with the XMP Toolkit (global state).
///
/// Returns the prefix actually registered for the namespace URI. Registration is idempotent, so
/// calling this repeatedly is safe and cheap.
fn register_eyeris_namespace() -> xmp_toolkit::XmpResult<String> {
    XmpMeta::register_namespace(NS, PREFIX)
}

/// Read the Eyeris custom XMP metadata from a file.
///
/// Returns [`None`] when the file contains no XMP packet at all. When the file has XMP but is
/// missing the `Rating` or `Tags` properties, those fields fall back to their defaults (`0` and an
/// empty vector) rather than failing.
///
/// # Errors
///
/// This function does not return a `Result`; a missing or unreadable XMP packet simply yields
/// `None`. Underlying toolkit failures are converted to `None`.
pub fn read(filepath: &Path) -> Option<CustomXmp> {
    // `XmpMeta::from_file` opens the file read-only, reads the XMP packet, then closes the disk
    // file immediately (read-only mode). It returns an error when there is no XMP in the file.
    let meta = XmpMeta::from_file(filepath).ok()?;

    // Make sure our namespace is registered before addressing properties by URI.
    let _ = register_eyeris_namespace();

    // `Rating` is a simple integer property. `property_i32` reads it and parses the string into an
    // i32; we cast to u8 and default to 0 when the property is absent.
    let rating = meta
        .property_i32(NS, CustomXmp::RATING)
        .map(|value| value.value as u8)
        .unwrap_or(0);

    // `Tags` is an ordered array property. `property_array` returns an iterator over the array
    // items (the toolkit uses 1-based indices internally). Each item's value is one tag string.
    let tags = meta
        .property_array(NS, CustomXmp::TAGS)
        .map(|item| item.value)
        .collect();

    Some(CustomXmp { rating, tags })
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
