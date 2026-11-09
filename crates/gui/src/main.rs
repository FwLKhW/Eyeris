//! Eyeris GUI: edit `Rating` and `Tags`.
//!
//! Usage: `cargo r -p gui -- <collection_folder>` or press "Open collection".

use std::path::Path;

use collection::Collection;
use gui::{Item, Message, item_view, load_collection, parse_tags, report, save_rating, save_tags};
use iced::widget::{button, column, row, scrollable, text};
use iced::{Center, Element, Fill};

#[derive(Default)]
struct Gui {
    collection: Option<Collection>,
    items: Vec<Item>,
    status: String,
}

fn main() -> iced::Result {
    iced::application(Gui::new, Gui::update, Gui::view)
        .title("Eyeris")
        .run()
}

impl Gui {
    fn new() -> Self {
        let mut gui = Self {
            status: "Open a collection folder".to_string(),
            ..Self::default()
        };
        if let Some(path) = std::env::args().nth(1) {
            gui.open_collection(Path::new(&path));
        }
        gui
    }

    fn open_collection(&mut self, path: &Path) {
        let c = Collection::new_from_path(path);
        self.status = match load_collection(&c) {
            Ok(items) => {
                let n = items.len();
                self.items = items;
                format!("{n} images in {}", path.display())
            }
            Err(e) => format!("Error: {e:#}"),
        };
        self.collection = Some(c);
    }

    fn update(&mut self, message: Message) {
        match message {
            Message::OpenCollection => {
                if let Some(folder) = efs::pick_folder() {
                    self.open_collection(&folder);
                }
            }
            Message::AddImages => {
                if let Some(collection) = &self.collection {
                    if let Err(err) = collection.add_images() {
                        self.status = format!("Error: {}", err);
                    }
                }
            }
            Message::AddFolder => {
                if let Some(collection) = &self.collection {
                    if let Err(err) = collection.add_folder() {
                        self.status = format!("Error: {}", err);
                    }
                }
            }
            Message::Reload => {
                if let Some(path) = self.collection.as_ref().map(|c| c.path.clone()) {
                    self.open_collection(&path);
                }
            }
            Message::SetRating(i, rating) => {
                let (Some(c), Some(it)) = (&self.collection, self.items.get_mut(i)) else {
                    return;
                };
                // Clicking the current rating again clears it.
                it.rating = if it.rating == rating { 0 } else { rating };
                self.status = report(
                    save_rating(c, it),
                    &format!("Saved rating of {}", it.fullname),
                );
            }
            Message::TagsChanged(i, draft) => {
                if let Some(it) = self.items.get_mut(i) {
                    it.tags_draft = draft;
                }
            }
            Message::TagsSubmitted(i) => {
                let (Some(c), Some(it)) = (&self.collection, self.items.get_mut(i)) else {
                    return;
                };
                it.tags = parse_tags(&it.tags_draft);
                it.tags_draft = it.tags.join(", ");
                self.status = report(save_tags(c, it), &format!("Saved tags of {}", it.fullname));
            }
        }
    }

    fn view(&self) -> Element<'_, Message> {
        let header = row![
            button("Open collection").on_press(Message::OpenCollection),
            button("Reload").on_press_maybe(self.collection.as_ref().map(|_| Message::Reload)),
            button("Import images")
                .on_press_maybe(self.collection.as_ref().map(|_| Message::AddImages)),
            button("Import folder")
                .on_press_maybe(self.collection.as_ref().map(|_| Message::AddFolder)),
            text(self.status.as_str()),
        ]
        .spacing(10.0)
        .align_y(Center);

        let list = column(
            self.items
                .iter()
                .enumerate()
                .map(|(i, it)| item_view(i, it)),
        )
        .spacing(8.0)
        .padding(8.0);

        column![header, scrollable(list).height(Fill)]
            .spacing(10.0)
            .padding(10.0)
            .into()
    }
}
