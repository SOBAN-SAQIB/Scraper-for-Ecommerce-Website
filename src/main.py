"""Simplified scraper - fast version."""

import sys
from pathlib import Path
import time

sys.path.insert(0, str(Path(__file__).parent / 'src'))

from scraper.crawler import Crawler
from scraper.parsers import ProductDetailParser
from scraper.exporters import CSVExporter
from scraper.utils import deduplicate_products


def main():
    print("Starting streamlined scraper...")
    
    # Phase 1: Discover structure
    print("\n[1/4] Discovering categories and product links...")
    crawler = Crawler()
    
    # Just get links from home page and each category
    products_list = []
    base_url = crawler.base_url
    
    categories = crawler.discover_categories()
    print(f"  Found {len(categories)} categories")
    
    for cat_idx, category in enumerate(categories, 1):
        cat_name = category['name']
        cat_url = category['url']
        
        # Just get products from category listing page, don't go through pagination
        products = crawler.get_product_links(cat_url)
        print(f"  [{cat_idx}] {cat_name}: {len(products)} products")
        
        # Also check for subcategories in sidebar
        from bs4 import BeautifulSoup
        import requests
        soup = BeautifulSoup(requests.get(cat_url, headers={'User-Agent': 'Mozilla'}).content, 'html.parser')
        subcat_links = []
        sidebar = soup.find('div', class_='sidebar')
        if sidebar:
            nav_links = sidebar.find_all('a', class_='nav-link')
            subcat_links = [el for el in nav_links if '/static/' in el.get('href', '') 
                           and 'category' not in el.get('class', [])
                           and el.get_text().strip().lower() not in ['home', cat_name.lower()]]
        
        # Get products from first few subcategories
        for subcat_link in subcat_links[:2]:  # Limit to 2 subcategories per category
            subcat_name = subcat_link.get_text().strip()
            subcat_href = subcat_link.get('href', '')
            subcat_url = 'https://webscraper.io' + subcat_href if subcat_href.startswith('/') else subcat_href
            
            subcat_products = crawler.get_product_links(subcat_url)
            print(f"      - {subcat_name}: {len(subcat_products)} products")
            
            for prod in subcat_products:
                products_list.append((cat_name, subcat_name, prod['name'], prod['url']))
            
            time.sleep(0.2)
        
        # Add products from main category
        for prod in products[:5]:  # Limit to 5 initial products to reduce time
            products_list.append((cat_name, "", prod['name'], prod['url']))
        
        time.sleep(0.2)
    
    print(f"  Total products to fetch: {len(products_list)}")
    
    # Phase 2: Fetch details
    print("\n[2/4] Fetching product details...")
    all_products = []
    
    for idx, (category, subcategory, product_name, product_url) in enumerate(products_list, 1):
        if idx % 5 == 1:
            print(f"  Processing {idx}/{len(products_list)}...")
        
        try:
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
        except:
            pass
        
        time.sleep(0.15)
    
    print(f"  Fetched {len(all_products)} product details")
    
    # Phase 3: Deduplicate
    print("\n[3/4] Deduplicating...")
    all_products = deduplicate_products(all_products)
    print(f"  After dedup: {len(all_products)} products")
    
    # Phase 4: Export
    print("\n[4/4] Exporting to CSV...")
    CSVExporter.export_products(all_products, "data/products.csv")
    CSVExporter.export_category_summary(all_products, "data/category_summary.csv")
    
    print("\n✓ Complete!")
    print(f"  Products: {len(all_products)}")
    print(f"  CSVs saved to data/")


if __name__ == "__main__":
    main()