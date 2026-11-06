use std::{
    path::{Path, PathBuf},
    time::Instant,
};

use anyhow::Result;
use clap::{Parser, Subcommand};

use collection::Collection;
use colored_text::Colorize;

#[derive(Parser, Debug)]
#[command(version, name = "eyeris", about = "Eyeris is Iris")]
struct Cli {
    /// Folder as a Collection
    #[arg(required = true)]
    collection_path: String,

    #[command(subcommand)]
    command: Commands,
}

#[derive(Debug, Subcommand)]
enum Commands {
    /// Add images or folder
    Add {
        #[command(subcommand)]
        command: AddCommands,
    },
}

#[derive(Debug, Subcommand)]
enum AddCommands {
    /// Pick images
    Images {
        #[arg(required = true)]
        image_paths: Vec<String>,
    },

    /// Pick a folder
    Folder {
        #[arg(required = true)]
        folder_path: String,
    },
}

fn main() -> Result<()> {
    let cli = Cli::parse();

    let start = Instant::now();

    match &cli.command {
        Commands::Add { command } => {
            let collection = Collection::new_from_path(Path::new(&cli.collection_path));

            match command {
                AddCommands::Images { image_paths } => {
                    let image_paths: Vec<PathBuf> = image_paths.iter().map(PathBuf::from).collect();

                    collection.index(&image_paths)?;
                }
                AddCommands::Folder { folder_path } => {
                    let folder_path = PathBuf::from(folder_path);
                    let image_paths = efs::scan_images(&folder_path);

                    collection.index(&image_paths)?;
                }
            }
        }
    }

    println!(
        "\nTake {} seconds\n",
        format!("{}", start.elapsed().as_secs_f32()).green()
    );

    Ok(())
}
