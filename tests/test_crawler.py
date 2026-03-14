"""
Tests for crawler.
"""

import pytest
from unittest.mock import Mock, patch
from scraper.crawler import Crawler


class TestCrawler:
    """Test web crawling functionality."""

    @patch('scraper.crawler.requests.Session')
    def test_discover_categories(self, mock_session):
        """Test category discovery."""
        mock_response = Mock()
        mock_response.content = '''
        <html>
        <body>
            <div class="sidebar">
                <a class="category-link" href="/computers">Computers</a>
                <a class="category-link" href="/phones">Phones</a>
            </div>
        </body>
        </html>
        '''
        mock_session_instance = Mock()
        mock_session_instance.get.return_value = mock_response
        mock_session.return_value = mock_session_instance

        crawler = Crawler()
        categories = crawler.discover_categories()

        assert len(categories) == 2
        assert categories[0]['name'] == 'Computers'
        assert categories[0]['url'] == 'https://webscraper.io/computers'
        assert categories[1]['name'] == 'Phones'

    @patch('scraper.crawler.requests.Session')
    def test_get_product_links_single_page(self, mock_session):
        """Test product link collection from single page."""
        mock_response = Mock()
        mock_response.content = '''
        <html>
        <body>
            <div class="card">
                <a class="title" href="/product1">Product 1</a>
            </div>
            <div class="card">
                <a class="title" href="/product2">Product 2</a>
            </div>
        </body>
        </html>
        '''
        mock_session_instance = Mock()
        mock_response_empty = Mock()
        mock_response_empty.content = '<html><body></body></html>'
        mock_session_instance.get.side_effect = [mock_response, mock_response_empty]
        mock_session.return_value = mock_session_instance

        crawler = Crawler()
        products = crawler.get_product_links("https://webscraper.io/category")

        assert len(products) == 2
        assert products[0]['name'] == 'Product 1'
        assert products[0]['url'] == 'https://webscraper.io/product1'

    @patch('scraper.crawler.requests.Session')
    def test_get_product_links_pagination(self, mock_session):
        """Test product link collection with pagination."""
        # First page
        mock_response1 = Mock()
        mock_response1.content = '''
        <html>
        <body>
            <div class="card">
                <a class="title" href="/product1">Product 1</a>
            </div>
        </body>
        </html>
        '''
        # Second page (empty)
        mock_response2 = Mock()
        mock_response2.content = '<html><body></body></html>'

        mock_session_instance = Mock()
        mock_session_instance.get.side_effect = [mock_response1, mock_response2]
        mock_session.return_value = mock_session_instance

        crawler = Crawler()
        products = crawler.get_product_links("https://webscraper.io/category")

        assert len(products) == 1
        assert products[0]['name'] == 'Product 1'