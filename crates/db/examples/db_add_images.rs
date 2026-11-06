use anyhow::Result;
use db::IndexDB;
use index::IndexedImage;

fn main() -> Result<()> {
    let db = rfd::FileDialog::new()
        .add_filter("Sqlite3 Database", &["db", "sqlite3"])
        .pick_file();

    if let Some(db) = db {
        let db = IndexDB::new_from_path(&db);
        db.add_images(&[IndexedImage::default(), IndexedImage::default()])?;
    }

    Ok(())
}
