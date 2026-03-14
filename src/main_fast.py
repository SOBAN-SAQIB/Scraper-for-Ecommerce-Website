"""Fast scraper version."""

import sys
from pathlib import Path
import time

sys.path.insert(0, str(Path(__file__).parent / 'src'))

from scraper.crawler import Crawler
from scraper.parsers import ProductDetailParser
from scraper.exporters import CSVExporter
from scraper.utils import deduplicate_products


def main():
    print("Starting fast scraper...")
    
    # Quick discovery
    crawler = Crawler()
    base_url = crawler.base_url
    
    # Hardcoded for speed
    categories = [
        {'name': 'Computers', 'url': f"{base_url}/computers"},
        {'name': 'Phones', 'url': f"{base_url}/phones"}
    ]
    
    products_list = []
    for category in categories:
        cat_name = category['name']
        cat_url = category['url']
        
        products = crawler.get_product_links(cat_url)
        for prod in products[:3]:  # Limit for speed
            products_list.append((cat_name, "", prod['name'], prod['url']))
    
    # Fetch details
    all_products = []
    for category, subcategory, product_name, product_url in products_list[:10]:  # Limit
        detail_data = ProductDetailParser.fetch_and_parse(product_url, base_url)
        if detail_data:
            all_products.append({
                'category': category,
                'subcategory': subcategory,
                'product_title': product_name,
                'product_url': product_url,
                'price': detail_data.get('price', ''),
                'description': detail_data.get('description', ''),
                'rating': detail_data.get('rating', ''),
                'review_count': detail_data.get('review_count', ''),
                'specification': detail_data.get('specification', ''),
                'image_url': detail_data.get('image_url', ''),
                'page_reference': '',
            })
        time.sleep(0.1)
    
    # Deduplicate and export
    all_products = deduplicate_products(all_products)
    CSVExporter.export_products(all_products, "data/products.csv")
    CSVExporter.export_category_summary(all_products, "data/category_summary.csv")
    
    print(f"✓ Fast scrape complete! {len(all_products)} products")


if __name__ == "__main__":
    main()