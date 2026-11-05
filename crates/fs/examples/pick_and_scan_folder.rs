use efs::{pick_folder, scan_images};

fn main() {
    let folder = pick_folder();

    if let Some(folder) = folder {
        println!("Selected {folder:#?}\n");

        let images = scan_images(&folder);

        println!("Images to be indexed:");
        for i in images {
            println!("{i:#?}")
        }
    }
}
