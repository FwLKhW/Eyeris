use anyhow::Result;
use collection::Collection;

fn main() -> Result<()> {
    let folder = efs::pick_folder();

    if let Some(folder) = folder {
        let collection = Collection::new_from_path(&folder);
        collection.add_images()?;
    }

    Ok(())
}
