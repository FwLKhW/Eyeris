#let c-ink = rgb("#0A0A0A")
#let c-text = rgb("#171717")
#let c-muted = rgb("#595959")
#let c-line = rgb("#CFCFCF")
#let c-soft = rgb("#F4F4F4")
#let c-code = rgb("#EAEAEA")

#let body-font = ("Monda", "Plus Jakarta Sans")
#let head-font = ("Plus Jakarta Sans", "Monda")
#let code-font = ("JetBrainsMono NF", "DejaVu Sans Mono")

#set document(
  title: "Eyeris — A Digital Asset Management for the rest of us",
  author: ("Nguyễn Thế Anh", "Châm Duy Khoát"),
  keywords: (
    "digital asset management",
    "image indexing",
    "image tagging",
    "semantic search",
    "vision-language embeddings",
    "Rust",
    "Python",
  ),
)

#set page(
  paper: "a4",
  margin: (x: 2.6cm, top: 3.1cm, bottom: 2.9cm),
  header-ascent: 38%,
  header: [
    #set text(size: 8.5pt, fill: c-muted, font: head-font)
    #stack(
      spacing: 7pt,
      grid(
        columns: (1fr, auto),
        align: (left + horizon, right + horizon),
        text(weight: "bold", fill: c-ink)[#box(baseline: 0.5pt, square(size: 6pt, fill: c-ink)) #h(4pt) Eyeris],
        [A Digital Asset Management for the rest of us],
      ),
      line(length: 100%, stroke: 0.8pt + c-ink),
    )
  ],
  footer: context {
    align(
      right,
      box(
        fill: c-ink,
        inset: (x: 8pt, y: 4pt),
        text(fill: white, size: 8pt, weight: "bold", font: head-font, counter(page).display()),
      ),
    )
  },
)

#set text(font: body-font, size: 10.5pt, fill: c-text, lang: "en", hyphenate: false)
#set par(leading: 1em, spacing: 2em, justify: false)

#show emph: set text(font: head-font, style: "normal")
#show strong: set text(weight: "bold", fill: c-ink)

#show link: it => underline(offset: 2.5pt, stroke: 0.6pt + c-ink, text(fill: c-ink, it))

#set heading(numbering: none)

#show heading.where(level: 1): it => {
  v(4.2em, weak: true)
  block(sticky: true, below: 1.2em)[
    #rect(width: 1.6cm, height: 5pt, fill: c-ink, stroke: none)
    #v(0.7em)
    #text(font: head-font, size: 23pt, weight: "bold", fill: c-ink, tracking: -0.01em, it.body)
  ]
}

#show heading.where(level: 2): it => {
  v(2.8em, weak: true)
  block(
    sticky: true,
    below: 1em,
    text(font: head-font, size: 14pt, weight: "semibold", fill: c-ink, it.body),
  )
  v(1.8em, weak: true)
}

#set list(
  marker: text(fill: c-ink, weight: "bold")[•],
  indent: 0.3em,
  body-indent: 0.8em,
  spacing: 1em,
)
#set enum(
  numbering: n => text(fill: c-ink, weight: "bold", font: head-font)[#n.],
  indent: 0.3em,
  body-indent: 0.8em,
  spacing: 1em,
)

#show raw: set text(font: code-font, size: 1.2em, weight: "semibold")

#show raw.where(block: false): it => highlight(
  fill: c-code,
  extent: 1.5pt,
  top-edge: "ascender",
  bottom-edge: "descender",
  text(fill: c-ink, it),
)

#show raw.where(block: true): it => block(
  width: 100%,
  fill: c-soft,
  stroke: (left: 3pt + c-ink, rest: 0.6pt + c-line),
  inset: 14pt,
  above: 1.8em,
  below: 1.4em,
  it,
)

#set table(
  stroke: (x, y) => (bottom: 0.6pt + c-line),
  inset: (x: 11pt, y: 10pt),
  align: left + horizon,
  fill: (x, y) => if y == 0 { c-ink } else if calc.even(y) { c-soft } else { white },
)
#show table.cell.where(y: 0): set text(fill: white, weight: "bold", font: head-font, size: 0.9em)
#show table: set text(size: 0.92em)
#show table: it => block(
  width: 100%,
  stroke: 0.8pt + c-ink,
  breakable: false,
  above: 2.4em,
  below: 2.4em,
  it,
)

#show figure.caption: it => align(
  center,
  text(font: head-font, size: 0.85em, style: "italic", fill: c-muted, it.body),
)
#show figure: set block(above: 2em, below: 2em)

#let card-img(path, h) = block(
  width: 100%,
  height: h,
  fill: c-soft,
  stroke: 0.6pt + c-line,
  inset: 8pt,
  clip: true,
  image(path, width: 100%, height: 100%, fit: "contain"),
)

#let shot(path, caption: none, h: 10cm) = figure(
  card-img(path, h),
  caption: caption,
  kind: image,
  numbering: none,
  supplement: none,
)

#let cap(body) = align(
  center,
  text(font: head-font, size: 0.85em, style: "italic", fill: c-muted, body),
)

#let failed = text(fill: c-ink, weight: "bold")[(failed)]

#let cover-label(t) = text(
  font: head-font,
  size: 8pt,
  weight: "bold",
  fill: c-ink,
  tracking: 0.14em,
  upper(t),
)

#let chip(t) = box(
  stroke: 0.8pt + c-ink,
  inset: (x: 9pt, y: 4.5pt),
  text(size: 8.5pt, fill: c-ink, t),
)

#page(margin: 0pt, header: none, footer: none)[
  // Hero
  #block(width: 100%, height: 16.5cm, fill: c-ink)[
    #pad(x: 2.6cm, top: 2.8cm)[
      #block(inset: -5pt, image("assets/icon.svg", width: 2.8cm))
      #text(font: head-font, size: 46pt, weight: "extrabold", fill: white, tracking: -0.02em)[Eyeris]
      #line(length: 3cm, stroke: 2pt + white)
      #v(0.35cm)
      #text(font: head-font, size: 17pt, weight: "semibold", fill: white)[A Digital Asset Management for the rest of us]
    ]
  ]

  // Metadata
  #pad(x: 2.6cm, top: 1.5cm)[
    #grid(
      columns: (3.3cm, 1fr),
      inset: (y: 11pt),
      stroke: (x, y) => (bottom: 0.6pt + c-line, top: if y == 0 { 0.8pt + c-ink } else { none }),
      align: (left + top, left + top),
      cover-label("Authors"),
      [
        #link("https://github.com/ForeverWeLearn")[Nguyễn Thế Anh] & #link("https://github.com/sainoman15")[Châm Duy Khoát]
      ],

      cover-label("Course"), [DAP391m],
      cover-label("Supervisor"), [Nguyễn Thị Hoàng Yến],
      cover-label("Date"), [November 2026],
      cover-label("Repository"),
      [
        #link("https://github.com/FwLKhW/Eyeris")[FwLKhW/Eyeris] · Archived on Nov 11, 2026
      ],

      cover-label("Keywords"),
      [
        #set par(leading: 1em)
        #for k in (
          "digital asset management",
          "image indexing",
          "image tagging",
          "semantic search",
          "vision-language embeddings",
          "Rust",
          "Python",
        ) [#chip(k)#h(4pt)]
      ],
    )
  ]
]

#counter(page).update(1)

= About

#block(
  stroke: (left: 4pt + c-ink),
  inset: (left: 16pt, y: 16pt),
  above: 2em,
  below: 2.4em,
  text(
    font: head-font,
    size: 15pt,
    weight: "semibold",
    fill: c-ink,
  )[Personal image collections grow faster than the tools that organize them.],
)

*Eyeris* is an experimental, local-first Digital Asset Management (DAM) system that aims to sit between open-source feature rich tools like #link("https://digikam.org")[*digiKam*] and polished but closed ones like #link("https://eagle.cool")[*Eagle*].

It's designed to stores images in a self-managed _Collection_ (just a plain folder with databases), deduplicates by pixel hash, extracts dominant colors, auto tagging, and semantic search through vision-language embeddings. Reasonable for a 1 month project.

But the system ended up in a terrible hybrid prototype: a *Rust* core handles initial indexing and a desktop GUI, while *Python* handles embeddings, tagging, filtering, and exploratory analysis in notebooks. It works... fine, maybe.

The cost to work in both two languages is headache. Implicit schemas, subprocess calls, and duplicated logic made the design ugly, even XMP metadata write-back never became usable. So badly...

We decided to archive the repository to start a successor with a cleaner architecture.

This report documents what was built, what worked, and what we would do differently.

= 1. Introduction

== 1.1 Motivation

Photographers, designers, and hobbyists have thousands of images. Organize them in folder hierarchy just get harder day by day, and finding "black hair cat girl sleeping chilly on sofa" means scrolling over 10 different folders.

We wanted something simple enough that a collection is just a folder, yet smart and versatile enough to search by meaning and by many image properties.

== 1.2 Goals and Scope

The project aim to archive:

- Self-contained collection without duplicates
- Manage useful metadata (size, dimensions, timestamps, rating, tags, dominant colors)
- Semantic text-to-image search and automatic tagging
- Explore collection easily in a polish UI #failed

Out of scope: RAW formats, video, editing.

= 2. Related Work

Eyeris borrows concepts from #link("https://digikam.org")[*digiKam*] and #link("https://eagle.cool")[*Eagle*], and its implementation are somewhat inspired by them.

#table(
  columns: (auto, 1fr, 1fr, 1.2fr),
  [App], [Strengths], [Weaknesses], [Inspired],
  [*digiKam*],
  [Open source, rich metadata and XMP support],
  [Dense interface, heavy for casual use],
  [XMP, tagging model],

  [*Eagle*],
  [Pleasant UX, library-as-folder model],
  [Proprietary],
  [The _Library_ concept, which became our _Collection_],
)

Further, Eyeris applies *SigLIP 2* and *Perception Encoder* for text-to-image retrieval and auto tagging. Embeddings are stored in *ChromaDB*.

= 3. System Design and Architecture

== 3.1 Design Principles

- *A collection is a folder.*
- *Content-based identity.* Images live in folders named by the hash of their pixels.
- *Local-first.* All models and data are offline, though require download.
- *Metadata portability.* Ratings and tags should live in the image itself via XMP, and both in the database. #failed

== 3.2 Collection Layout

```yaml
<collection>/
├── embeddings/             # ChromaDB store for semantic search
├── images/
│   └── <hash>/
│       ├── <name>.<ext>    # copied original
│       └── thumbnail.png   # 512 px thumbnail
└── index.db                # SQLite, table `images`
```

#shot("assets/imgs/collection-layout.png", caption: [Collection layout on disk], h: 12cm)

== 3.3 Hybrid Architecture: Rust and Python ⊙▃⊙?!

The codebase is roughly 40% Rust and 60% Python.

```
─────────────────────────────────────────────────────────────────────
Language    Files     Lines    Blanks  Comments       Code Complexity
─────────────────────────────────────────────────────────────────────
Rust           17     1,162       165       105        892        145
Python          9       822       178        56        588         77
Jupyter         7     1,606         0         0      1,606          0
```

#cap[Lines of code count, generated using *scc*]

The intent was to use each language where it is strongest: Rust for CPU-bound, parallel, I/O-heavy work; Python for the machine-learning ecosystem and fast notebook-driven experimentation.

#table(
  columns: (auto, auto, 1.3fr, 1.6fr),
  [Layer], [Language], [Responsibility], [Main components],
  [Core],
  [*Rust*],
  [Hashing, color extraction, thumbnails, DB writes],
  [`index`, `hash`, `color`, `thumbnail`, `db`, `collection`, `cli`, `efs`],

  [GUI], [*Rust*], [Browse, import, rate, tag], [`gui` (`iced`)],
  [ML & analysis],
  [*Python*],
  [Embeddings, tagging, filtering, EDA],
  [`embed`, `ss`, `tag/*`, `filter`, `eda`, notebooks],
)

_We won't say that we must do this just because we have no choice. (more in #link(label("devlog1"))[Devlogs \#1])_

== 3.4 Languages Interaction

Python and Rust share no types or process. They communicate in two ways:

+ *Python → Rust via subprocess.* Python call to the compiled `cli` binary to add folder or add images to collection.
+ *Both read and write `index.db` directly.* Rust creates the table; Python queries it with `pandas` and updates with raw SQL.

This was quick to build, but it means the schema exists implicitly, in two languages, with no authority (see Section 6).

= 4. Implementation

== 4.1 Indexing

For each image:

- Collects filesystem metadata
- Reads XMP properties
- Computes pixel hash
- Extracts dominant colors

Images are processed in parallel with `rayon`.

Successfully indexed images are inserted in a single transaction, then copied into `images/<hash>/` and given a thumbnail (also in parallel).

== 4.2 Database Schema

A single `images` table holds all metadata.

#table(
  columns: (auto, auto, 1fr),
  [Column], [Type], [Description],
  [id], [INTEGER], [Primary key],
  [origin], [TEXT], [Original path (slash-normalized)],
  [fullname / name / format], [TEXT], [File name, stem, uppercase extension],
  [size], [INTEGER], [Bytes],
  [width / height], [INTEGER], [Pixels],
  [created / modified], [INTEGER], [Unix timestamps (ms)],
  [rating], [INTEGER], [0–5],
  [tags], [TEXT], [Pipe-separated],
  [hash], [TEXT], [BLAKE3 of pixels, unique],
  [color\_1 … color\_4], [INTEGER], [Dominant colors as packed `0xRRGGBB` (nullable)],
)

Simplify queries at the cost of normalization:

- *Tags* are stored as one pipe-separated string (e.g. `"girl|beach|sunset"`)
- *Dominant colors* are packed into up to four integer columns (`0xRRGGBB` as decimal)

== 4.3 Deduplication by Pixel Hash

The `hash` column is the BLAKE3 digest of the decoded RGBA16 pixel buffer, declared `UNIQUE ON CONFLICT IGNORE`. Two files with identical pixels collapse into one entry even if their format or compression differs.

This catches EXACT duplicates only.

== 4.4 Color Analysis

#shot("assets/imgs/okmain.png", h: 20cm)

Up to four dominant colors are extracted per image with the `okmain` crate. Which under the hood using K-Means on OKLAB color space.

#shot("assets/imgs/filter-dominant-color.png", caption: [Filter by a green color], h: 18cm)

On the Python side, colors are converted to the OKLCH color space, where hue is grouped into ten named bands (red … pink) and low-chroma colors are classified as black, gray, or white by lightness. This is used for color filtering, lightness buckets.

== 4.5 Semantic Search and Tagging

#figure(
  grid(
    columns: (1fr, 1fr, 1fr),
    column-gutter: 8pt,
    card-img("assets/imgs/ss-anime-girl.png", 9cm),
    card-img("assets/imgs/ss-flowers.png", 9cm),
    card-img("assets/imgs/ss-airplane.png", 9cm),
  ),
  caption: [Example semantic-search results for several text queries],
  kind: image,
  numbering: none,
  supplement: none,
)

Images are embedded with a Perception Encoder model (loaded through LibreYOLO) and stored in a ChromaDB collection using cosine distance. A text query is embedded with the same model, and return results above a similarity threshold.

#shot("assets/imgs/tag-most-suit.png", caption: [Assign most suit tag for images], h: 14cm)

Some tagging strategies:

#table(
  columns: (1.3fr, 1.2fr, 1.4fr, 1.3fr),
  [Approach], [Type], [Output], [Notes],
  [YOLO classifier],
  [Closed-set (ImageNet 1000 classes)],
  [Top-5 classes, filtered above 0.5 confidence],
  [Simple, but limited vocabulary],

  [Perception Encoder & SigLIP 2], [Open-set, multi-label], [Tags above 0.65], [Flexible, but compute heavy (embed)],
)

== 4.6 Filtering and EDA

Filtering is expressed as an `ImageFilter` (a `TypedDict` whose conditions combined with AND): name, format, size, dimensions, orientation, rating, tags (any/all/has), timestamps, and color proximity.

The EDA module adds derived features (megapixels, aspect ratio snapped to common ratios, resolution tier, hour and weekday of creation, source folder) and a set of analyses:

- Data audit (null rates, ranges, suspicious timestamps)
- Format share of files, format share of disk
- Tag co-occurrence
- Near-duplicate detection by embedding cosine similarity
- Rating prediction: ridge regression from embeddings to rating
- ... and some fun!

#shot("assets/imgs/eda-rating-correlation.png", caption: [Rating correlation], h: 9cm)

#shot("assets/imgs/eda-color-distribution.png", caption: [Color distribution], h: 11cm)

#shot("assets/imgs/eda-resolution.png", caption: [Resolution], h: 11cm)

#shot("assets/imgs/eda-top-tags.png", caption: [Top tags], h: 11cm)

== 4.7 Desktop GUI

#shot("assets/imgs/gui.png", caption: [Made in Rust using Iced], h: 12cm)

The GUI is built with `iced`. It lists images with thumbnails, metadata, swatches of dominant colors, a five-star rating control, and a comma-separated tag editor. It can open a collection and import images or whole folders. Edits are saved to the database on interaction.

= 5. Evaluation and Results

Eyeris was built as an exploratory prototype, so evaluation is mostly qualitative.

== 5.1 Search and Tagging Quality

Qualitatively, free-text queries ("a picture of forest", "thunder storm") return plausible top results at low thresholds, while abstract or stylistic queries are less reliable.

Closed-set YOLO tags are precise on common objects but miss anything outside their vocabulary.

SigLIP 2 and Perception Encoder tagging are more flexible but sensitive to thresholds and to how candidate tags are phrased.

No formal precision/recall study was done.

== 5.2 Collection Insights

The EDA notebook is the most useful part of the project. For example:

- finding a share of storage taken by a few large PNGs
- finding clusters of bulk-copied timestamps
- finding near-duplicate pairs or semantically similar pairs

= 6. Limitations and Lessons Learned

== 6.1 Known Limitations

- *XMP write-back is unstable.* The `xmp` crate can read and write a custom `eyeris` namespace (`Rating`, `Tags`) via `xmp_toolkit`, but writing proved unreliable across files and formats. Ratings and tags currently live only in `index.db`. This undermines the original portability goal. <xmp>
- *Implicit, duplicated schema.* The table is created in Rust, queried in Python, and re-queried in the GUI with hand-written SQL.
- *Fragile consistency.* Embeddings are keyed by database row id, and thumbnails are generated after the DB insert; a failure in between leaves the stores out of sync.
- *String-encoded tags.* The pipe-separated format blocks characters and complicates queries.
- *Subprocess coupling.* Python depends on a hard-coded path to `target/release/cli`.
- *Limited formats.* Only JPEG, PNG and WEBP, although can accepts more extensions.

== 6.2 Architectural Weaknesses

The root problem was not either language but the seam between them. There was no single source of truth: no shared schema, no shared domain model, and no API boundary, only a file and a binary.

Each new feature (tags, filters, GUI edits) touched the database from a different place, so the same knowledge was re-implemented several times. We concluded that patching this would cost more than redesigning it.

== 6.3 What Worked Well

- Content-addressed folders made deduplication nearly free.
- Strict lints in Rust caught many edge cases early.
- Notebooks made it cheap to try models and analyses.

== 6.4 Lessons Learned

+ Don't use Rust with Python (or Python with Rust) in this way! (subprocess, no contract)
+ Remember lesson 1.

= 7. Project Status and Future Work

== 7.1 Archived

The repository was archived on November 11, 2026.

The current architecture is so poorly designed to be growth. And continuing to build on it would make our brain explode.

We planned to move the development to a new repository with a cleaner design.

== 7.2 Plan

The successor would entirely written in Rust and will have:

- A reliable metadata strategy, with XMP either fixed or replaced by a well-tested sidecar approach.
- Semantic search and tagging integrated seamlessly into the workflow.
- A normalized tag model.
- A polish UI!

New repository: \*not started yet ლ(・﹏・ლ)\*

= 8. Conclusion

Eyeris showed that a local-first collection, pixel-hash deduplication, and embedding-based search can be combined into a useful DAM prototype with modest code.

It also showed how quickly an unstructured hybrid architecture become broken. The most valuable outcome is the set of design lessons that will shape the successor project.

= Acknowledgments

Thanks to the maintainers of #link("https://github.com/LibreYOLO/libreyolo")[LibreYOLO], Perception Encoder, SigLIP 2, ChromaDB, `iced`, `xmp_toolkit`, `rayon`, `rusqlite`, and `okmain`, and to Professor Nguyễn Thị Hoàng Yến.

= References

+ digiKam. #link("https://digikam.org/")
+ Eagle. #link("https://eagle.cool/")
+ BLAKE3. #link("https://github.com/BLAKE3-team/BLAKE3")
+ Björn Ottosson. #link("https://bottosson.github.io/posts/oklab/")[A perceptual color space for image processing] (Oklab).
+ SigLIP 2. #link("https://huggingface.co/blog/siglip2")[SigLIP 2: A better multilingual vision language encoder]
+ Perception Encoder. #link("https://ai.meta.com/research/publications/perception-encoder-the-best-visual-embeddings-are-not-at-the-output-of-the-network/")[Perception Encoder: The best visual embeddings are not at the output of the network]

= Devlogs

== \#1 Rust + Python is just a joke <devlog1>

From the day we present the project idea, we decided to code fully in Python. Because it would be very easy to run ML models and perform data analysis.

One of our friend said, making app with Python will result in terrible performance. Yeah, some true. We said if we have time, we will make a Rust version of it. With ONNX runtime to run ML models, robust data analysis with DuckDB, performance UI with GPUI.

For 2nd university students, it's easy for them to think they can do all the job of an entire department in half a year in a month.

We are. So we chase them all!

Till the day... "Omg! There is only 2 weeks left! We have a broken Rust indexing system, some python script to test some ML models, fragile data analysis functions here and there, a non-sense GUI made using Slint with callback linking broken there and here!"

Less is more. More is less.

We want to do too many things.

The initial design of the UI:

#shot("assets/imgs/initial-design.png", caption: [Initial Design], h: 10cm)

Half cooked using Slint #link("https://github.com/FwLKhW/Eyeris/releases/tag/v0.0.1-preview.2")[Eyeris v0.0.1-preview.2]:

#shot("assets/imgs/gui-slint.png", caption: [Half cooked using Slint], h: 10cm)

And an performance but broken indexing system: #link("https://github.com/FwLKhW/image-indexing-engine")[FwLKhW/image-indexing-engine]

Do all that just to end up in trauma when the time is up. Make many but nothing is made.

What could we do?

The GUI made with Slint seem good, but far from expectation, mostly because the complexity when working with DSL for the fist time. Further more, we already have a fast indexing pipeline in Rust, we just cannot suffer from write a slower one?!.

Not to say, Rust will not help us complete even a prototype, not mention a final stable app. Cannot imagine how in the world we can implement ML + data analysis + GUI in Rust in 2 weeks.

With all we have. We choose the worst but the only possible decision: Rust + Python.

(╥﹏╥)
