"""
Export scraped data to CSV files.
"""

import csv
from typing import List, Dict
from pathlib import Path
from .utils import normalize_price


class CSVExporter:
    """Export data to CSV format."""
    
    @staticmethod
    def export_products(products: List[Dict], output_path: str = "data/products.csv"):
        """
        Export products to CSV file.
        
        Args:
            products: List of product dictionaries
            output_path: Path to output CSV file
        """
        # Create output directory if it doesn't exist
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        if not products:
            print(f"No products to export")
            return
        
        # Define CSV headers
        fieldnames = [
            'category',
            'subcategory',
            'product_title',
            'price',
            'price_numeric',
            'product_url',
            'image_url',
            'description',
            'rating',
            'review_count',
            'specification',
            'page_reference'
        ]
        
        try:
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for product in products:
                    # Calculate numeric price
                    price_numeric = normalize_price(product.get('price', ''))
                    
                    row = {
                        'category': product.get('category', ''),
                        'subcategory': product.get('subcategory', ''),
                        'product_title': product.get('product_title', ''),
                        'price': product.get('price', ''),
                        'price_numeric': price_numeric if price_numeric else '',
                        'product_url': product.get('product_url', ''),
                        'image_url': product.get('image_url', ''),
                        'description': product.get('description', ''),
                        'rating': product.get('rating', ''),
                        'review_count': product.get('review_count', ''),
                        'specification': product.get('specification', ''),
                        'page_reference': product.get('page_reference', '')
                    }
                    writer.writerow(row)
            
            print(f"Exported {len(products)} products to {output_path}")
        
        except Exception as e:
            print(f"Error exporting products to CSV: {e}")
    
    @staticmethod
    def export_category_summary(products: List[Dict], output_path: str = "data/category_summary.csv"):
        """
        Export category summary statistics.
        
        Args:
            products: List of product dictionaries
            output_path: Path to output CSV file
        """
        # Create output directory if it doesn't exist
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Group products by category-subcategory
        summary_data = {}
        
        for product in products:
            category = product.get('category', 'Unknown')
            subcategory = product.get('subcategory', '')
            key = (category, subcategory)
            
            if key not in summary_data:
                summary_data[key] = {
                    'products': [],
                    'prices': [],
                    'missing_descriptions': 0
                }
            
            summary_data[key]['products'].append(product)
            
            # Collect prices
            price_numeric = normalize_price(product.get('price', ''))
            if price_numeric:
                summary_data[key]['prices'].append(price_numeric)
            
            # Count missing descriptions
            if not product.get('description', '').strip():
                summary_data[key]['missing_descriptions'] += 1
        
        # Generate summary rows
        summary_rows = []
        for (category, subcategory), data in summary_data.items():
            prices = data['prices']
            avg_price = sum(prices) / len(prices) if prices else ''
            min_price = min(prices) if prices else ''
            max_price = max(prices) if prices else ''
            
            row = {
                'category': category,
                'subcategory': subcategory,
                'total_products': len(data['products']),
                'avg_price': f"{avg_price:.2f}" if avg_price else '',
                'min_price': f"{min_price:.2f}" if min_price else '',
                'max_price': f"{max_price:.2f}" if max_price else '',
                'missing_descriptions': data['missing_descriptions'],
                'duplicates_removed': 0  # Placeholder, as deduplication is global
            }
            summary_rows.append(row)
        
        # Sort by category and subcategory
        summary_rows.sort(key=lambda x: (x['category'], x['subcategory']))
        
        # Write to CSV
        fieldnames = [
            'category',
            'subcategory',
            'total_products',
            'avg_price',
            'min_price',
            'max_price',
            'missing_descriptions',
            'duplicates_removed'
        ]
        
        try:
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(summary_rows)
            
            print(f"Exported category summary to {output_path}")
        
        except Exception as e:
            print(f"Error exporting category summary: {e}")