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

        conn.execute(
            "CREATE TABLE IF NOT EXISTS images (
                id          INTEGER PRIMARY KEY,
                name        TEXT,
                format      TEXT,
                size        INTEGER,
                width       INTEGER,
                height      INTEGER,
                created     INTEGER,
                modified    INTEGER,
                rating      INTEGER,
                tags        TEXT,
                hash        TEXT,
                color_1     INTEGER,
                color_2     INTEGER,
                color_3     INTEGER,
                color_4     INTEGER
            )",
            [],
        )?;

        let tx = conn.transaction()?;
        {
            let mut stmt = tx.prepare(
                "INSERT OR REPLACE INTO images (
                    id, name, format, size, width, height, created, modified, rating,
                    tags, hash, color_1, color_2, color_3, color_4
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            )?;

            for (id, img) in indexed_images.iter().enumerate() {
                let colors_int: Vec<i64> = img.colors.iter().map(rgb2dec).collect();

                stmt.execute(params![
                    id.cast_signed(),
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
