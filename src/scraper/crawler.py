"""
Crawler module for discovering categories and product links.
# Feature: Enhanced catalog navigation
# Fix: Improved URL resolution
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from urllib.parse import urljoin


class Crawler:
    """Handles web crawling for the e-commerce site."""
    
    def __init__(self, base_url: str = "https://webscraper.io/test-sites/e-commerce/static"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def discover_categories(self) -> List[Dict]:
        """
        Discover main categories from the home page.
        
        Returns:
            List of category dictionaries with 'name' and 'url'
        """
        try:
            response = self.session.get(f"{self.base_url}/computers")
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find category links in sidebar
            categories = []
            sidebar = soup.find('div', class_='sidebar')
            if sidebar:
                category_links = sidebar.find_all('a', class_='category-link')
                for link in category_links:
                    name = link.get_text().strip()
                    href = link.get('href', '')
                    if href and name:
                        full_url = urljoin(self.base_url, href)
                        categories.append({
                            'name': name,
                            'url': full_url
                        })
            
            # Fallback: hardcoded categories if not found
            if not categories:
                categories = [
                    {'name': 'Computers', 'url': f"{self.base_url}/computers"},
                    {'name': 'Phones', 'url': f"{self.base_url}/phones"}
                ]
            
            return categories
        
        except Exception as e:
            print(f"Error discovering categories: {e}")
            return []
    
    def get_product_links(self, category_url: str) -> List[Dict]:
        """
        Get product links from a category page.
        
        Args:
            category_url: URL of the category page
            
        Returns:
            List of product dictionaries with 'name' and 'url'
        """
        try:
            response = self.session.get(category_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            products = []
            # Find product links
            product_cards = soup.find_all('div', class_='card')
            for card in product_cards:
                link = card.find('a', class_='title')
                if link:
                    name = link.get_text().strip()
                    href = link.get('href', '')
                    if href and name:
                        full_url = urljoin(self.base_url, href)
                        products.append({
                            'name': name,
                            'url': full_url
                        })
            
            return products
        
        except Exception as e:
            print(f"Error getting product links from {category_url}: {e}")
            return []