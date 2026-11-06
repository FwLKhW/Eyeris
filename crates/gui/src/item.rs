use iced::widget::{button, column, container, image, row, text, text_input};
use iced::{Center, Color, Element, Fill};

use crate::{Message, fmt_time};

pub struct Item {
    pub hash: String,
    pub origin: String,
    pub fullname: String,
    pub format: String,
    pub size: u64,
    pub width: u32,
    pub height: u32,
    pub created: u64,
    pub modified: u64,
    pub rating: u8,
    pub tags: Vec<String>,
    /// Text currently typed in the tags input (comma separated).
    pub tags_draft: String,
    pub colors: Vec<Color>,
    pub thumb: image::Handle,
}

pub fn item_view(i: usize, it: &Item) -> Element<'_, Message> {
    // Rating: 5 clickable stars.
    let stars: Vec<Element<'_, Message>> = (1..=5_u8)
        .map(|n| {
            let glyph = if n <= it.rating { "★" } else { "☆" };
            button(text(glyph).size(22.0))
                .padding(2.0)
                .style(button::text)
                .on_press(Message::SetRating(i, n))
                .into()
        })
        .collect();

    let tags = text_input("tags, comma separated (Enter to save)", &it.tags_draft)
        .on_input(move |s| Message::TagsChanged(i, s))
        .on_submit(Message::TagsSubmitted(i));

    let swatches: Vec<Element<'_, Message>> = it
        .colors
        .iter()
        .map(|&c| {
            container(text(""))
                .width(28.0)
                .height(28.0)
                .style(move |_| container::Style::default().background(c))
                .into()
        })
        .collect();

    let info = column![
        text(it.fullname.as_str()).size(18.0),
        text(format!(
            "{} · {}×{} · {} KB",
            it.format,
            it.width,
            it.height,
            it.size / 1024
        ))
        .size(13.0),
        text(format!(
            "created {} · modified {}",
            fmt_time(it.created),
            fmt_time(it.modified)
        ))
        .size(13.0),
        text(format!("origin: {}", it.origin)).size(12.0),
        text(format!("hash: {}", it.hash)).size(11.0),
    ]
    .spacing(3.0)
    .width(Fill);

    let editor = column![row(stars).spacing(2.0), tags, row(swatches).spacing(4.0)]
        .spacing(6.0)
        .width(320.0);

    container(
        row![
            image(it.thumb.clone()).width(96.0).height(96.0),
            info,
            editor
        ]
        .spacing(12.0)
        .align_y(Center),
    )
    .padding(10.0)
    .width(Fill)
    .style(container::bordered_box)
    .into()
}
