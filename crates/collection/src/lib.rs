use std::path::{Path, PathBuf};

use efs::scan_images;

pub struct Collection {
    pub path: PathBuf,
}

impl Collection {
    pub fn new_from_path(path: &Path) -> Self {
        Self {
            path: path.to_path_buf(),
        }
    }

    pub fn index(&self) {
        let image_paths = scan_images(&self.path);
        for image_path in image_paths {
            println!("Indexing {}", image_path.display());
        }
    }

    pub fn generate_thumbnails(&self) {
        let image_paths = scan_images(&self.path);
        for image_path in image_paths {
            println!("Generating thumbnail for {}", image_path.display());
        }
    }
}
