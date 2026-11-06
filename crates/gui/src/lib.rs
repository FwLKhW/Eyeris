pub mod item;

use collection::Collection;
pub use item::{Item, item_view};

use anyhow::Result;
use chrono::DateTime;
use iced::{Color, widget::image};
use rusqlite::{Connection, params};

#[derive(Debug, Clone)]
pub enum Message {
    OpenCollection,
    Reload,
    SetRating(usize, u8),
    TagsChanged(usize, String),
    TagsSubmitted(usize),
}

pub fn dec2color(v: i64) -> Color {
    // `v` is `0xRRGGBB` stored in an i64: the last 3 big-endian bytes are r, g, b.
    let [.., r, g, b] = v.to_be_bytes();
    Color::from_rgb8(r, g, b)
}

pub fn fmt_time(ms: u64) -> String {
    i64::try_from(ms)
        .ok()
        .and_then(DateTime::from_timestamp_millis)
        .map_or_else(
            || "-".to_string(),
            |d| d.format("%Y-%m-%d %H:%M").to_string(),
        )
}

/// "a, b ,, c" -> ["a", "b", "c"]. `|` is the DB separator so it can't live in a tag.
pub fn parse_tags(input: &str) -> Vec<String> {
    input
        .split(',')
        .map(|t| t.trim().replace('|', "/"))
        .filter(|t| !t.is_empty())
        .collect()
}

pub fn report(result: Result<()>, ok: &str) -> String {
    match result {
        Ok(()) => ok.to_string(),
        Err(e) => format!("Error: {e:#}"),
    }
}

pub fn load_collection(c: &Collection) -> Result<Vec<Item>> {
    if !c.index_db_path.exists() {
        return Ok(Vec::new());
    }

    let conn = Connection::open(&c.index_db_path)?;
    let mut stmt = conn.prepare(
        "SELECT hash, origin, fullname, format, size, width, height,
                CAST(created AS INTEGER), CAST(modified AS INTEGER), rating, tags,
                color_1, color_2, color_3, color_4
         FROM images",
    )?;

    let rows = stmt.query_map([], |r| {
        let hash: String = r.get(0)?;
        let tags: Option<String> = r.get(10)?;
        let tags = parse_tags(&tags.unwrap_or_default().replace('|', ","));
        let colors: [Option<i64>; 4] = [r.get(11)?, r.get(12)?, r.get(13)?, r.get(14)?];

        Ok(Item {
            thumb: image::Handle::from_path(c.thumbnail_path(&hash)),
            origin: r.get(1)?,
            fullname: r.get(2)?,
            format: r.get(3)?,
            size: u64::try_from(r.get::<_, i64>(4)?).unwrap_or(0),
            width: u32::try_from(r.get::<_, i64>(5)?).unwrap_or(0),
            height: u32::try_from(r.get::<_, i64>(6)?).unwrap_or(0),
            created: u64::try_from(r.get::<_, i64>(7)?).unwrap_or(0),
            modified: u64::try_from(r.get::<_, i64>(8)?).unwrap_or(0),
            rating: u8::try_from(r.get::<_, i64>(9)?).unwrap_or(0),
            tags_draft: tags.join(", "),
            tags,
            colors: colors.into_iter().flatten().map(dec2color).collect(),
            hash,
        })
    })?;

    Ok(rows.collect::<rusqlite::Result<Vec<_>>>()?)
}

/// Write rating to the collection's copy of the image (XMP) and to IndexDB.
pub fn save_rating(c: &Collection, it: &Item) -> Result<()> {
    xmp::write_rating(&c.image_path(&it.hash, &it.fullname), it.rating)?;
    Connection::open(&c.index_db_path)?.execute(
        "UPDATE images SET rating = ?1 WHERE hash = ?2",
        params![i64::from(it.rating), it.hash],
    )?;
    Ok(())
}

/// Write tags to the collection's copy of the image (XMP) and to IndexDB (`a|b|c`).
pub fn save_tags(c: &Collection, it: &Item) -> Result<()> {
    xmp::write_tags(&c.image_path(&it.hash, &it.fullname), &it.tags)?;
    Connection::open(&c.index_db_path)?.execute(
        "UPDATE images SET tags = ?1 WHERE hash = ?2",
        params![it.tags.join("|"), it.hash],
    )?;
    Ok(())
}
