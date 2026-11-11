### EDA

#### Data audit
- [ ] Null rate and value range of every column
- [ ] Rating: how many images are rated (0 = unrated, not bad)
- [ ] Tags: how many images are tagged
- [ ] Suspicious timestamps (epoch 0, fallback to "now")

#### Extended properties
- [ ] Color group: OKLCH hue into 10 groups (red, green, ...), low chroma into neutral (black, gray, white)
- [ ] Lightness bucket: dark / mid / light
- [ ] Hour of the day: from timestamp (local time)
- [ ] Day of the week: from timestamp (local time)
- [ ] Megapixels, resolution tier (720p, 1080p, 4K)
- [ ] Aspect ratio: snapped to common ones (16:9, 4:3, 1:1, 9:16)
- [ ] Source folder: from `origin` (top folders, `Screenshot...` / `IMG_...` patterns)

#### Basic
- [ ] Formats (PNG, JPG, WEBP):
    - [ ] Most common: bar chart
    - [ ] Share of files vs share of disk space: side-by-side bar chart
    - [ ] Bytes per pixel by format
- [ ] Orientation (landscape / portrait / square): bar chart
- [ ] Rating distribution (rated images only): bar chart
- [ ] Top tags: bar chart
- [ ] Collection growth over time: cumulative line chart
- [ ] When I collect images: hour x weekday heatmap
- [ ] Disk Pareto: how much space the top 1% of files take

#### Relationships & Behavioral
- [ ] Tags co-occurrence matrix: use lift / PMI, not raw counts
- [ ] Too big/small images (outliers): width x height, log axes, show thumbnails of extremes
- [ ] Too old images (outliers): show thumbnails
- [ ] Color group distribution, split by lightness
- [ ] Rating correlation with other properties (Spearman or grouped means)

#### Embeddings (Chroma)
- [ ] 2D map of the collection (UMAP / t-SNE), colored by hue, rating or format
- [ ] Clusters, auto-labeled by nearest tags
- [ ] Near-duplicates: cosine similarity above ~0.95
- [ ] Taste profile: predict rating from embeddings, surface unrated images likely to be good

#### Fun part
- [ ] The color of you: based on most appeared color
- [ ] Eyeris Wrapped card: top hue, average lightness, night owl or morning person, busiest day, favorite format, top tag
- [ ] Collection barcode: dominant colors of all images sorted by hue as one strip

#### Helpers
- [ ] `src/eda.py`: one function adds all extended properties to the dataframe
- [ ] `contact_sheet(df, n)`: thumbnail grid, to show real images in outlier charts
