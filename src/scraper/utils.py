"""
Utility functions for the scraper.
# Fix: Improved deduplication logic
"""

import re
from typing import List, Dict


def normalize_price(price_str: str) -> float:
    """
    Extract numeric price from price string.
    
    Args:
        price_str: Price string like "$123.45"
        
    Returns:
        Numeric price or 0.0 if not found
    """
    if not price_str:
        return 0.0
    
    # Remove currency symbols and extract number
    match = re.search(r'[\d,]+\.?\d*', price_str.replace(',', ''))
    if match:
        try:
            return float(match.group().replace(',', ''))
        except ValueError:
            pass
    return 0.0


def deduplicate_products(products: List[Dict]) -> List[Dict]:
    """
    Remove duplicate products based on URL.
    
    Args:
        products: List of product dictionaries
        
    Returns:
        Deduplicated list
    """
    seen_urls = set()
    deduplicated = []
    
    for product in products:
        url = product.get('product_url', '')
        if not url or url not in seen_urls:
            if url:
                seen_urls.add(url)
            deduplicated.append(product)
    
    return deduplicated