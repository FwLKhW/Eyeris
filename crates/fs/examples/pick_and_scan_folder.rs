use efs::{pick_folder, scan_images};

fn main() {
    let folder = pick_folder();

    if let Some(folder) = folder {
        println!("Selected {}\n", folder.display());

        let images = scan_images(&folder);

        println!("Images to be indexed:");
        for image in images {
            println!("{}", image.display());
        }
    }
}
