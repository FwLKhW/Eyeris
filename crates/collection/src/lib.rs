use std::{
    fs,
    path::{Path, PathBuf},
};

use anyhow::{Result, bail};
use db::IndexDB;
use efs::scan_images;
use index::{IndexedImage, index_image};
use thumbnail::generate_thumbnail;

pub struct Collection {
    pub path: PathBuf,
    pub images_path: PathBuf,
    pub index_db_path: PathBuf,
}

impl Collection {
    #[must_use]
    pub fn new_from_path(path: &Path) -> Self {
        Self {
            path: path.to_path_buf(),
            images_path: path.join("images"),
            index_db_path: path.join("index.db"),
        }
    }

    /// # Errors
    ///
    /// Fail when user cancel pick images. Or during indexing or generating thumbnails.
    pub fn add_images(&self) -> Result<()> {
        let Some(image_paths) = efs::pick_images() else {
            bail!("Please choose some images")
        };

        self.index(&image_paths)?;

        Ok(())
    }

    /// # Errors
    ///
    /// Fail when user cancel pick folder. Or during indexing or generating thumbnails.
    pub fn add_folder(&self) -> Result<()> {
        let Some(folder_path) = efs::pick_folder() else {
            bail!("Please choose a folder")
        };

        let image_paths = scan_images(&folder_path);
        self.index(&image_paths)?;

        Ok(())
    }

    /// # Errors
    ///
    /// DB insertion may fail.
    pub fn index(&self, image_paths: &[PathBuf]) -> Result<()> {
        let indexed_images: Vec<IndexedImage> = image_paths
            .iter()
            .filter_map(|i| index_image(i).ok())
            .collect();

        IndexDB::new_from_path(&self.index_db_path).add_images(&indexed_images)?;

        if let Ok(exists) = fs::exists(&self.images_path)
            && !exists
        {
            fs::create_dir(&self.images_path)?;
        }
        for img in &indexed_images {
            let hash_folder_path = self.images_path.join(&img.hash);
            if let Ok(exists) = fs::exists(&hash_folder_path)
                && !exists
            {
                fs::create_dir(&hash_folder_path)?;
            }

            let target_image_path = hash_folder_path.join(&img.fullname);
            if let Ok(exists) = fs::exists(&target_image_path)
                && !exists
            {
                fs::copy(&img.origin, &target_image_path)?;

                println!("Generating thumbnail for {}", target_image_path.display());
                generate_thumbnail(&target_image_path)?;
            } else {
                println!("Image {} already exists", target_image_path.display());
            }
        }

        Ok(())
    }
}
