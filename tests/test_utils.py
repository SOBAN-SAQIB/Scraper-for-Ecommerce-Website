"""
Tests for utility functions.
"""

import pytest
from scraper.utils import normalize_price, deduplicate_products


class TestNormalizePrice:
    """Test price normalization."""

    def test_valid_price_dollar(self):
        """Test normalizing $123.45"""
        assert normalize_price("$123.45") == 123.45

    def test_valid_price_no_symbol(self):
        """Test normalizing 123.45"""
        assert normalize_price("123.45") == 123.45

    def test_price_with_commas(self):
        """Test normalizing $1,234.56"""
        assert normalize_price("$1,234.56") == 1234.56

    def test_invalid_price(self):
        """Test invalid price returns 0.0"""
        assert normalize_price("invalid") == 0.0

    def test_empty_price(self):
        """Test empty string returns 0.0"""
        assert normalize_price("") == 0.0


class TestDeduplicateProducts:
    """Test product deduplication."""

    def test_deduplicate_unique_products(self):
        """Test deduplication with unique products."""
        products = [
            {'product_url': 'url1', 'title': 'Product 1'},
            {'product_url': 'url2', 'title': 'Product 2'},
        ]
        result = deduplicate_products(products)
        assert len(result) == 2
        assert result == products

    def test_deduplicate_duplicate_products(self):
        """Test deduplication with duplicates."""
        products = [
            {'product_url': 'url1', 'title': 'Product 1'},
            {'product_url': 'url1', 'title': 'Product 1'},
            {'product_url': 'url2', 'title': 'Product 2'},
        ]
        result = deduplicate_products(products)
        assert len(result) == 2
        assert result[0]['product_url'] == 'url1'
        assert result[1]['product_url'] == 'url2'

    def test_deduplicate_no_url(self):
        """Test deduplication with missing URL."""
        products = [
            {'title': 'Product 1'},
            {'title': 'Product 2'},
        ]
        result = deduplicate_products(products)
        assert len(result) == 2