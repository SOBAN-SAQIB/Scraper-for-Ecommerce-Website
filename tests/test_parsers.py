"""
Tests for parsers.
"""

import pytest
from unittest.mock import Mock, patch
from scraper.parsers import ProductDetailParser


class TestProductDetailParser:
    """Test product detail parsing."""

    @patch('scraper.parsers.requests.get')
    def test_fetch_and_parse_success(self, mock_get):
        """Test successful parsing of product details."""
        # Mock the response
        mock_response = Mock()
        mock_response.content = '''
        <html>
        <body>
            <h4 class="card-title">Test Product</h4>
            <h4 class="price">$99.99</h4>
            <p class="description">Test description</p>
            <div class="rating">4.5</div>
            <div class="review-count">10 reviews</div>
            <div class="specification">Test specs</div>
            <img class="card-img-top" src="/image.jpg">
        </body>
        </html>
        '''
        mock_get.return_value = mock_response

        result = ProductDetailParser.fetch_and_parse("http://example.com/product", "http://example.com")

        assert result['title'] == "Test Product"
        assert result['price'] == "$99.99"
        assert result['description'] == "Test description"
        assert result['rating'] == "4.5"
        assert result['review_count'] == "10 reviews"
        assert result['specification'] == "Test specs"
        assert result['image_url'] == "http://example.com/image.jpg"

    @patch('scraper.parsers.requests.get')
    def test_fetch_and_parse_missing_fields(self, mock_get):
        """Test parsing with missing fields."""
        mock_response = Mock()
        mock_response.content = '<html><body><h4 class="card-title">Test Product</h4></body></html>'
        mock_get.return_value = mock_response

        result = ProductDetailParser.fetch_and_parse("http://example.com/product", "http://example.com")

        assert result['title'] == "Test Product"
        assert result.get('price', '') == ""
        assert result.get('description', '') == ""

    @patch('scraper.parsers.requests.get')
    def test_fetch_and_parse_request_error(self, mock_get):
        """Test handling of request errors."""
        mock_get.side_effect = Exception("Request failed")

        result = ProductDetailParser.fetch_and_parse("http://example.com/product", "http://example.com")

        assert result is None