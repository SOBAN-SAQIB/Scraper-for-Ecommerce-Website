"""
Parsers for extracting product details from HTML.
# Feature: Enhanced product details parsing
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional
from urllib.parse import urljoin


class ProductDetailParser:
    """Parses product detail pages."""
    
    @staticmethod
    def fetch_and_parse(product_url: str, base_url: str) -> Optional[Dict]:
        """
        Fetch and parse a product detail page.
        
        Args:
            product_url: URL of the product page
            base_url: Base URL for relative links
            
        Returns:
            Dictionary with product details or None if failed
        """
        try:
            response = requests.get(product_url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract product details
            details = {}
            
            # Title
            title_elem = soup.find('h4', class_='card-title')
            if title_elem:
                details['title'] = title_elem.get_text().strip()
            
            # Price
            price_elem = soup.find('h4', class_='price')
            if price_elem:
                details['price'] = price_elem.get_text().strip()
            
            # Description
            desc_elem = soup.find('p', class_='description')
            if desc_elem:
                details['description'] = desc_elem.get_text().strip()
            
            # Rating
            rating_elem = soup.find('div', class_='rating')
            if rating_elem:
                details['rating'] = rating_elem.get_text().strip()
            
            # Review count
            review_elem = soup.find('div', class_='review-count')
            if review_elem:
                details['review_count'] = review_elem.get_text().strip()
            
            # Specification
            spec_elem = soup.find('div', class_='specification')
            if spec_elem:
                details['specification'] = spec_elem.get_text().strip()
            
            # Image URL
            img_elem = soup.find('img', class_='card-img-top')
            if img_elem:
                img_src = img_elem.get('src', '')
                if img_src:
                    details['image_url'] = urljoin(base_url, img_src)
            
            return details
        
        except Exception as e:
            print(f"Error parsing {product_url}: {e}")
            return None