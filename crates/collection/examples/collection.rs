use collection::Collection;

fn main() {
    let folder = efs::pick_folder();

    if let Some(folder) = folder {
        let collection = Collection::new_from_path(&folder);
        collection.index();
        collection.generate_thumbnails();
    }
}
