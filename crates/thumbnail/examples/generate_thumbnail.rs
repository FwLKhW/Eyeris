use std::path::Path;

use anyhow::{Result, bail};
use thumbnail::generate_thumbnail;

fn main() -> Result<()> {
    let Some(images) = efs::pick_images() else {
        bail!("I need image to generate thumbnail.")
    };

    for image in images {
        generate_thumbnail(Path::new(&image))?;
    }

    Ok(())
}
