use std::path::{Path, PathBuf};

use anyhow::{Ok, Result, bail};
use db::IndexDB;
use efs::scan_images;
use index::{IndexedImage, index_image};

pub struct Collection {
    pub path: PathBuf,
}

impl Collection {
    #[must_use]
    pub fn new_from_path(path: &Path) -> Self {
        Self {
            path: path.to_path_buf(),
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
        self.generate_thumbnails(&image_paths)?;

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
        self.generate_thumbnails(&image_paths)?;

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

        IndexDB::new_from_path(&self.path.join(IndexDB::REL_PATH)).add_images(&indexed_images)?;

        Ok(())
    }

    /// # Errors
    pub fn generate_thumbnails(&self, image_paths: &[PathBuf]) -> Result<()> {
        for image_path in image_paths {
            println!("Generating thumbnail for {}", image_path.display());
        }

        Ok(())
    }
}
