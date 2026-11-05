use std::fs;
use std::path::{Path, PathBuf};

#[must_use]
pub fn scan_images(path: &Path) -> Vec<PathBuf> {
    let mut images = Vec::new();
    let mut stack = vec![path.to_path_buf()];

    while let Some(current_dir) = stack.pop() {
        let Ok(entries) = fs::read_dir(current_dir) else {
            continue;
        };

        for entry in entries {
            let Ok(entry) = entry else { continue };

            let file_name = entry.file_name();
            let Some(name_str) = file_name.to_str() else {
                continue;
            };

            if name_str.starts_with('.') {
                continue;
            }

            let Ok(file_type) = entry.file_type() else {
                continue;
            };

            if file_type.is_dir() {
                stack.push(entry.path());
            } else if file_type.is_file()
                && let Some(ext) = entry.path().extension().and_then(|e| e.to_str())
            {
                let ext_lower = ext.to_ascii_lowercase();
                if matches!(ext_lower.as_str(), "jpg" | "jpeg" | "png") {
                    images.push(entry.path());
                }
            }
        }
    }

    images
}
