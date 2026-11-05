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
    pub const REL_PATH: &str = "index.db";

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
                name            TEXT,
                format          TEXT,
                size            INTEGER,
                width           INTEGER,
                height          INTEGER,
                created         INTEGER,
                modified        INTEGER,
                rating          INTEGER,
                tags            TEXT,
                hash            TEXT,
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
                    origin, name, format, size, width, height, created, modified,
                    rating, tags, hash, color_1, color_2, color_3, color_4
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            )?;

            for img in indexed_images {
                let colors_int: Vec<i64> = img.colors.iter().map(rgb2dec).collect();

                stmt.execute(params![
                    img.origin,
                    img.name,
                    img.format,
                    img.size.cast_signed(),
                    img.width.cast_signed(),
                    img.height.cast_signed(),
                    img.created.to_string(),
                    img.modified.to_string(),
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
}
