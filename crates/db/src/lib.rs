use std::path::{Path, PathBuf};

use anyhow::Result;
use rusqlite::{Connection, params};

use color::rgb2dec;
use index::IndexedImage;

/// This struct doesn't hold any database connection.
/// It connect to database on each method call then close.
pub struct IndexDB {
    pub path: PathBuf,
}

impl IndexDB {
    #[must_use]
    pub fn new_from_path(path: &Path) -> Self {
        Self {
            path: path.to_path_buf(),
        }
    }

    /// # Errors
    ///
    /// Returns an error if the database connection fails, table creation fails, or execution fails.
    pub fn add_images(&self, indexed_images: &[IndexedImage]) -> Result<()> {
        let mut conn = Connection::open(&self.path)?;

        conn.execute_batch(
            "CREATE TABLE IF NOT EXISTS images (
                id              INTEGER PRIMARY KEY,
                origin          TEXT,
                fullname        TEXT,
                name            TEXT,
                format          TEXT,
                size            INTEGER,
                width           INTEGER,
                height          INTEGER,
                created         INTEGER,
                modified        INTEGER,
                rating          INTEGER,
                tags            TEXT,
                hash            TEXT UNIQUE ON CONFLICT IGNORE,
                color_1         INTEGER,
                color_2         INTEGER,
                color_3         INTEGER,
                color_4         INTEGER
            ); CREATE INDEX IF NOT EXISTS idx_images_id ON images (id);",
        )?;

        let tx = conn.transaction()?;
        {
            let mut stmt = tx.prepare(
                "INSERT INTO images (
                    origin, fullname, name, format, size, width, height, created, modified,
                    rating, tags, hash, color_1, color_2, color_3, color_4
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            )?;

            for img in indexed_images {
                let colors_int: Vec<i64> = img.colors.iter().map(rgb2dec).collect();

                stmt.execute(params![
                    img.origin,
                    img.fullname,
                    img.name,
                    img.format,
                    img.size.cast_signed(),
                    img.width.cast_signed(),
                    img.height.cast_signed(),
                    img.created.cast_signed(),
                    img.modified.cast_signed(),
                    img.rating.cast_signed(),
                    img.tags.join("|"),
                    img.hash,
                    colors_int.first(),
                    colors_int.get(1),
                    colors_int.get(2),
                    colors_int.get(3),
                ])?;
            }
        }
        tx.commit()?;

        Ok(())
    }

    /// # Errors
    ///
    /// Returns an error if the database connection fails or row mapping fails.
    pub fn get_all_images(&self) -> Result<Vec<IndexedImage>> {
        if !self.path.exists() {
            return Ok(Vec::new());
        }

        let conn = Connection::open(&self.path)?;
        let Ok(mut stmt) = conn.prepare(
            "SELECT origin, fullname, name, format, size, width, height, created, modified, rating, tags, hash FROM images",
        ) else {
            return Ok(Vec::new())
        };

        let rows = stmt.query_map([], |row| {
            let origin: String = row.get(0)?;
            let fullname: String = row.get(1)?;
            let name: String = row.get(2)?;
            let format: String = row.get(3)?;
            let size: i64 = row.get(4)?;
            let width: i64 = row.get(5)?;
            let height: i64 = row.get(6)?;
            let created: i64 = row.get(7)?;
            let modified: i64 = row.get(8)?;
            let rating: i64 = row.get(9)?;
            let tags: String = row.get(10)?;
            let hash: String = row.get(11)?;

            Ok(IndexedImage {
                origin,
                fullname,
                name,
                format,
                size: u64::try_from(size).unwrap_or(0),
                width: u32::try_from(width).unwrap_or(0),
                height: u32::try_from(height).unwrap_or(0),
                created: created.cast_unsigned(),
                modified: modified.cast_unsigned(),
                rating: u8::try_from(rating).unwrap_or(0),
                tags: if tags.is_empty() {
                    Vec::new()
                } else {
                    tags.split('|').map(str::to_string).collect()
                },
                hash,
                colors: Vec::new(),
            })
        })?;

        let mut images = Vec::new();
        for row in rows {
            images.push(row?);
        }

        Ok(images)
    }
}
