# E-Commerce Web Scraper

A Python web scraper for the [WebScraper e-commerce test site](https://webscraper.io/test-sites/e-commerce/static) using Beautiful Soup and the `uv` package manager.

## Project Overview

This project demonstrates:
- **Git workflow**: Proper branching strategy with feature and fix branches
- **Dependency management**: Using `uv` package manager
- **Web scraping**: Beautiful Soup-based extraction from static HTML
- **Data processing**: Cleaning, normalization, and deduplication
- **CSV export**: Structured output files for analysis

## Project Structure

```
project/
├── pyproject.toml                  # Project metadata and dependencies
├── README.md                       # This file
├── data/
│   ├── products.csv               # Complete product dataset
│   └── category_summary.csv        # Summary statistics
├── src/
│   ├── main.py                    # Main entry point
│   └── scraper/
│       ├── __init__.py
│       ├── crawler.py             # Site navigation and discovery
│       ├── parsers.py             # Data extraction
│       ├── exporters.py           # CSV generation
│       └── utils.py               # Helper functions
└── tests/                         # Test directory (for future tests)
```

## Requirements

- Python 3.10+
- `uv` package manager
- Internet connection for scraping

## Setup Instructions

### 1. Prerequisites

Ensure you have Python 3.10+ installed:
```bash
python --version
```

### 2. Clone or Set Up the Project

```bash
cd "C:\Users\Soban Saqib\Desktop\web_scraper"
```

### 3. Initialize uv Project

```bash
uv init
```

### 4. Install Dependencies

Using uv (recommended):
```bash
uv pip install -r requirements.txt
```

Or manually:
```bash
uv pip install requests beautifulsoup4
```

The `pyproject.toml` file already contains all required dependencies.

## Running the Scraper

### Using uv

```bash
uv run src/main.py
```

### Using Python directly

```bash
python src/main.py
```

## Git Workflow

This project follows a structured branching strategy:

### Branches Used

1. **main** - Production-ready code
2. **dev** - Development branch (base for features)
3. **feature/catalog-navigation** - Category and subcategory discovery
4. **feature/product-details** - Product detail page scraping
5. **fix/url-resolution** - URL joining and resolution fixes
6. **fix/deduplication** - Duplicate product removal

### Workflow Steps

```
1. Create repository with main
   └─ Main branch initialized

2. Create dev from main
   └─ Development branch for features

3. Create feature/catalog-navigation
   └─ Implement category/subcategory discovery
   └─ Merge into dev

4. Create feature/product-details
   └─ Implement product detail scraping
   └─ Merge into dev

5. Create fix/url-resolution
   └─ Fix relative URL handling
   └─ Merge into dev

6. Create fix/deduplication
   └─ Implement deduplication logic
   └─ Merge into dev

7. Final testing on dev
   └─ Ensure all features working

8. Merge dev into main
   └─ Production release
```

## Data Extraction

### Products CSV (`products.csv`)

Contains detailed information about each product:

| Column | Description |
|--------|-------------|
| category | Product category name |
| subcategory | Product subcategory name |
| product_title | Product name/title |
| price | Price as displayed (raw) |
| price_numeric | Normalized price (float) |
| product_url | URL to product page |
| image_url | URL to product image |
| description | Product description text |
| rating | Product rating/star value |
| review_count | Number of reviews |
| specification | Key product specification |
| page_reference | Source page identifier |

### Category Summary CSV (`category_summary.csv`)

Aggregated statistics per category:

| Column | Description |
|--------|-------------|
| category | Category name |
| subcategory | Subcategory name |
| total_products | Number of products in this category |
| average_price | Mean product price |
| minimum_price | Lowest product price |
| maximum_price | Highest product price |
| missing_descriptions | Count of products without description |
| description_coverage | Percentage of products with description |

## Technical Implementation

### Crawler (`crawler.py`)

- **`discover_categories()`** - Finds all product categories from main page
- **`discover_subcategories(category_url)`** - Finds subcategories within a category
- **`get_pagination_urls(page_url)`** - Identifies all pages in a paginated listing
- **`get_product_links(listing_url)`** - Extracts links to individual products
- **`crawl()`** - Orchestrates the full site traversal

### Parsers (`parsers.py`)

- **`ListingParser`** - Extracts product cards from listing pages
- **`ProductDetailParser`** - Extracts detailed information from product pages
- Handles missing fields gracefully

### Exporters (`exporters.py`)

- **`CSVExporter.export_products()`** - Writes product data to CSV
- **`CSVExporter.export_category_summary()`** - Generates summary statistics

### Utilities (`utils.py`)

- **URL Handling**: `normalize_url()` joins relative and absolute URLs
- **Text Cleaning**: `clean_text()` normalizes whitespace
- **Price Parsing**: `normalize_price()` converts price strings to floats
- **Deduplication**: `deduplicate_products()` removes duplicates by URL
- **Safe Access**: `safe_get()` handles missing dictionary values

## Key Features

1. **Multi-page Crawling**
   - Discovers and processes pagination
   - Handles varying pagination styles

2. **Category Discovery**
   - Automatically finds all categories
   - Discovers nested subcategories
   - No hardcoded category paths

3. **Detail Page Scraping**
   - Doesn't stop at listings
   - Fetches and parses individual product pages
   - Enriches data with detailed information

4. **URL Resolution**
   - Correctly joins relative and absolute URLs
   - Handles various path formats
   - Validates URL structure

5. **Deduplication**
   - Removes duplicate products by URL
   - Tracks duplicate count
   - Ensures clean final dataset

6. **Data Cleaning**
   - Normalizes prices to numeric format
   - Removes extra whitespace
   - Handles missing fields safely
   - Cleans text content

7. **Error Handling**
   - Continues on missing fields
   - Recovers from network errors
   - Handles unexpected HTML structures
   - Fails gracefully on page load issues

## Assumptions

1. **Static HTML Site** - JavaScript rendering not required
2. **Predictable Structure** - Categories/products follow consistent patterns
3. **No Authentication** - Site accessible without login
4. **Reasonable Load** - Server can handle scraper requests
5. **URL Stability** - Product URLs remain consistent
6. **UTF-8 Encoding** - Pages are UTF-8 encoded

## Limitations

1. **JavaScript-Heavy Sites** - This scraper cannot execute JavaScript
   - Use Selenium/Playwright for dynamic content (not allowed per requirements)
   - Works only on static HTML

2. **Rate Limiting** - Single-threaded with 0.3-0.5s delays
   - Not optimized for very large sites
   - Respects server by adding delays

3. **Data Availability** - Depends on HTML structure
   - Missing fields return empty strings
   - Works with available site structure

4. **Images** - Image URLs extracted but not downloaded
   - Image files not saved locally
   - Only URLs stored in CSV

5. **Session Handling** - No session persistence
   - Each request is independent
   - Doesn't maintain login state

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| requests | ≥2.31.0 | HTTP requests |
| beautifulsoup4 | ≥4.12.0 | HTML parsing |
| pytest | ≥7.4.0 | Testing (optional) |

Install all dependencies:
```bash
uv pip install -r requirements.txt
```

Or install from `pyproject.toml`:
```bash
uv pip install .
```

## Running Tests

```bash
uv run pytest tests/
```

## Output Files

After running the scraper, you'll find:

- **`data/products.csv`** - Detailed product dataset
  - One row per product
  - All extracted fields
  - Ready for analysis

- **`data/category_summary.csv`** - Category statistics
  - One row per category/subcategory combination
  - Aggregated metrics
  - Summary view of data

## Troubleshooting

### No products found
- Check website structure - may have changed
- Verify selectors in `crawler.py`
- Inspect page HTML for correct class names

### Missing data fields
- Some products may not have all fields on the site
- Check website for availability of field
- Empty cells indicate unavailable data

### Network errors
- Check internet connection
- Website may be rate limiting - add delays
- Try running again after a delay

### Permission errors
- Ensure write access to `data/` directory
- Check file permissions on `data/products.csv`

## License

This project is for educational purposes only.

## Author

Student - Quiz No. 1 (Technology and Tools)

## References

- [WebScraper.io Test Site](https://webscraper.io/test-sites/e-commerce/static)
- [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/)
- [Requests Documentation](https://requests.readthedocs.io/)
- [uv Documentation](https://docs.astral.sh/uv/)
