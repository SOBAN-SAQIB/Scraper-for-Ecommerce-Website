"""
Tests for exporters.
"""

import pytest
import csv
import os
from scraper.exporters import CSVExporter


class TestCSVExporter:
    """Test CSV export functionality."""

    def test_export_products(self, tmp_path):
        """Test exporting products to CSV."""
        products = [
            {
                'category': 'Computers',
                'subcategory': 'Laptops',
                'product_title': 'Test Laptop',
                'price': '$999.99',
                'price_numeric': 999.99,
                'product_url': 'http://example.com/product',
                'image_url': 'http://example.com/image.jpg',
                'description': 'Test description',
                'rating': '4.5',
                'review_count': '10',
                'specification': 'Test specs',
                'page_reference': '1'
            }
        ]

        output_file = tmp_path / "test_products.csv"
        CSVExporter.export_products(products, str(output_file))

        assert output_file.exists()

        with open(output_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        assert len(rows) == 1
        assert rows[0]['category'] == 'Computers'
        assert rows[0]['product_title'] == 'Test Laptop'

    def test_export_category_summary(self, tmp_path):
        """Test exporting category summary to CSV."""
        products = [
            {
                'category': 'Computers',
                'subcategory': 'Laptops',
                'price': '$999.99',
                'description': 'Description'
            },
            {
                'category': 'Computers',
                'subcategory': 'Laptops',
                'price': '$1099.99',
                'description': 'Description 2'
            }
        ]

        output_file = tmp_path / "test_summary.csv"
        CSVExporter.export_category_summary(products, str(output_file))

        assert output_file.exists()

        with open(output_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        assert len(rows) == 1
        assert rows[0]['category'] == 'Computers'
        assert rows[0]['subcategory'] == 'Laptops'
        assert rows[0]['total_products'] == '2'
        assert rows[0]['avg_price'] == '1049.99'
        assert rows[0]['min_price'] == '999.99'
        assert rows[0]['max_price'] == '1099.99'
        assert rows[0]['missing_descriptions'] == '0'
        assert rows[0]['duplicates_removed'] == '0'