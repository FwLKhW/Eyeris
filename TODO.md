### EDA

#### Data audit
- [x] Null rate and value range of every column
- [x] Rating: how many images are rated (0 = unrated, not bad)
- [x] Tags: how many images are tagged
- [x] Suspicious timestamps (epoch 0, fallback to "now")

#### Extended properties
- [x] Color group: OKLCH hue into 10 groups (red, green, ...), low chroma into neutral (black, gray, white)
- [x] Lightness bucket: dark / mid / light
- [x] Hour of the day: from timestamp (local time)
- [x] Day of the week: from timestamp (local time)
- [x] Megapixels, resolution tier (720p, 1080p, 4K)
- [x] Aspect ratio: snapped to common ones (16:9, 4:3, 1:1, 9:16)
- [x] Source folder: from `origin`

#### Basic
- [x] Formats (PNG, JPG, WEBP):
    - [x] Most common: bar chart
    - [x] Share of files vs share of disk space: side-by-side bar chart
    - [x] Bytes per pixel by format
- [x] Orientation (landscape / portrait / square): bar chart
- [x] Rating distribution (rated images only): bar chart
- [x] Top tags: bar chart
- [x] Collection growth over time: cumulative line chart
- [x] When I collect images: hour x weekday heatmap
- [x] Disk Pareto: how much space the top 1% of files take

#### Relationships & Behavioral
- [x] Tags co-occurrence matrix: use lift / PMI, not raw counts
- [x] Too big/small images (outliers): width x height, log axes, show thumbnails of extremes
- [x] Too old images (outliers): show thumbnails
- [x] Color group distribution, split by lightness
- [x] Rating correlation with other properties (Spearman or grouped means)

#### Embeddings (Chroma)
- [x] Near-duplicates: cosine similarity above ~0.95
- [x] Taste profile: predict rating from embeddings, surface unrated images likely to be good

#### Fun part
- [x] The color of you: based on most appeared color
- [x] Eyeris Wrapped card: top hue, average lightness, night owl or morning person, busiest day, favorite format, top tag
- [x] Collection barcode: dominant colors of all images sorted by hue as one strip

#### Helpers
- [x] `src/eda.py`: one function adds all extended properties to the dataframe
- [x] `contact_sheet(df, n)`: thumbnail grid, to show real images in outlier charts
