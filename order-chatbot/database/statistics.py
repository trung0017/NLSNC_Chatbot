#!/usr/bin/env python3
"""
Script để thống kê dữ liệu sản phẩm sau khi cào từ thegioididong.com
"""

import re
import json
from collections import defaultdict
from typing import Dict, List

class ProductStatistics:
    def __init__(self):
        self.products = []
        self.categories = defaultdict(int)
        self.brands = defaultdict(int)
        self.price_ranges = defaultdict(int)
        self.processors = defaultdict(int)
        
    def parse_sql_file(self, filename: str) -> List[Dict]:
        """Parse file SQL để lấy danh sách sản phẩm"""
        products = []
        
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Tìm tất cả các INSERT statements
        pattern = r"\((\d+),\s*'([^']+)',\s*'([^']*)',\s*(\d+),\s*\d+,\s*'([^']*)',\s*'([^']+)'\)"
        matches = re.findall(pattern, content)
        
        for match in matches:
            category_id, name, description, price, image_url, status = match
            products.append({
                'category_id': int(category_id),
                'name': name,
                'description': description,
                'price': int(price),
                'image_url': image_url,
                'status': status
            })
        
        return products
    
    def extract_brand(self, name: str) -> str:
        """Trích xuất brand từ tên sản phẩm"""
        name_lower = name.lower()
        brands = ['hp', 'dell', 'lenovo', 'asus', 'acer', 'msi', 'apple', 'macbook', 'lg', 'huawei', 'gigabyte']
        
        for brand in brands:
            if brand in name_lower:
                if brand == 'macbook':
                    return 'Apple'
                return brand.upper()
        return 'Other'
    
    def extract_processor(self, description: str) -> str:
        """Trích xuất processor từ description"""
        if not description:
            return 'Unknown'
        
        desc_lower = description.lower()
        
        # Intel processors
        if 'intel core i9' in desc_lower or 'i9' in desc_lower:
            return 'Intel Core i9'
        elif 'intel core i7' in desc_lower or 'i7' in desc_lower:
            return 'Intel Core i7'
        elif 'intel core i5' in desc_lower or 'i5' in desc_lower:
            return 'Intel Core i5'
        elif 'intel core i3' in desc_lower or 'i3' in desc_lower:
            return 'Intel Core i3'
        elif 'intel core 5' in desc_lower or 'core 5' in desc_lower:
            return 'Intel Core 5'
        elif 'intel' in desc_lower:
            return 'Intel Other'
        
        # AMD processors
        if 'amd ryzen 9' in desc_lower or 'ryzen 9' in desc_lower:
            return 'AMD Ryzen 9'
        elif 'amd ryzen 7' in desc_lower or 'ryzen 7' in desc_lower:
            return 'AMD Ryzen 7'
        elif 'amd ryzen 5' in desc_lower or 'ryzen 5' in desc_lower:
            return 'AMD Ryzen 5'
        elif 'amd ryzen 3' in desc_lower or 'ryzen 3' in desc_lower:
            return 'AMD Ryzen 3'
        elif 'amd' in desc_lower or 'ryzen' in desc_lower:
            return 'AMD Other'
        
        # Apple processors
        if 'apple m5' in desc_lower or 'm5' in desc_lower:
            return 'Apple M5'
        elif 'apple m4' in desc_lower or 'm4' in desc_lower:
            return 'Apple M4'
        elif 'apple m2' in desc_lower or 'm2' in desc_lower:
            return 'Apple M2'
        elif 'apple m1' in desc_lower or 'm1' in desc_lower:
            return 'Apple M1'
        elif 'apple' in desc_lower:
            return 'Apple Other'
        
        return 'Unknown'
    
    def categorize_price(self, price: int) -> str:
        """Phân loại giá theo khoảng"""
        if price < 10000000:
            return 'Dưới 10 triệu'
        elif price < 15000000:
            return '10 - 15 triệu'
        elif price < 20000000:
            return '15 - 20 triệu'
        elif price < 25000000:
            return '20 - 25 triệu'
        elif price < 30000000:
            return '25 - 30 triệu'
        elif price < 40000000:
            return '30 - 40 triệu'
        else:
            return 'Trên 40 triệu'
    
    def get_category_name(self, category_id: int) -> str:
        """Lấy tên category từ ID"""
        category_names = {
            1: 'Điện thoại',
            2: 'Laptop',
            3: 'Tablet',
            4: 'Phụ kiện',
            5: 'Laptop Gaming',
            6: 'Laptop Văn Phòng',
            7: 'Laptop Đồ Họa',
            8: 'Laptop Mỏng Nhẹ',
            9: 'Laptop Cao Cấp'
        }
        return category_names.get(category_id, f'Category {category_id}')
    
    def analyze(self, products: List[Dict]):
        """Phân tích danh sách sản phẩm"""
        self.products = products
        
        for product in products:
            # Thống kê category
            category_name = self.get_category_name(product['category_id'])
            self.categories[category_name] += 1
            
            # Thống kê brand
            brand = self.extract_brand(product['name'])
            self.brands[brand] += 1
            
            # Thống kê giá
            price_range = self.categorize_price(product['price'])
            self.price_ranges[price_range] += 1
            
            # Thống kê processor
            processor = self.extract_processor(product['description'])
            self.processors[processor] += 1
    
    def generate_report(self) -> str:
        """Tạo báo cáo thống kê"""
        report = []
        report.append("=" * 80)
        report.append("BÁO CÁO THỐNG KÊ DỮ LIỆU SẢN PHẨM")
        report.append("=" * 80)
        report.append("")
        
        # Tổng số sản phẩm
        report.append(f"📊 TỔNG SỐ SẢN PHẨM: {len(self.products)}")
        report.append("")
        
        # Thống kê theo category
        report.append("📁 THỐNG KÊ THEO DANH MỤC:")
        report.append("-" * 80)
        for category, count in sorted(self.categories.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(self.products)) * 100
            report.append(f"  {category:30s}: {count:3d} sản phẩm ({percentage:5.1f}%)")
        report.append("")
        
        # Thống kê theo brand
        report.append("🏷️  THỐNG KÊ THEO THƯƠNG HIỆU:")
        report.append("-" * 80)
        for brand, count in sorted(self.brands.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(self.products)) * 100
            report.append(f"  {brand:30s}: {count:3d} sản phẩm ({percentage:5.1f}%)")
        report.append("")
        
        # Thống kê theo giá
        report.append("💰 THỐNG KÊ THEO KHOẢNG GIÁ:")
        report.append("-" * 80)
        price_order = [
            'Dưới 10 triệu', '10 - 15 triệu', '15 - 20 triệu', '20 - 25 triệu',
            '25 - 30 triệu', '30 - 40 triệu', 'Trên 40 triệu'
        ]
        for price_range in price_order:
            if price_range in self.price_ranges:
                count = self.price_ranges[price_range]
                percentage = (count / len(self.products)) * 100
                report.append(f"  {price_range:30s}: {count:3d} sản phẩm ({percentage:5.1f}%)")
        report.append("")
        
        # Thống kê theo processor
        report.append("⚙️  THỐNG KÊ THEO BỘ XỬ LÝ:")
        report.append("-" * 80)
        for processor, count in sorted(self.processors.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(self.products)) * 100
            report.append(f"  {processor:30s}: {count:3d} sản phẩm ({percentage:5.1f}%)")
        report.append("")
        
        # Giá trung bình
        if self.products:
            avg_price = sum(p['price'] for p in self.products) / len(self.products)
            min_price = min(p['price'] for p in self.products)
            max_price = max(p['price'] for p in self.products)
            report.append("💵 THỐNG KÊ GIÁ:")
            report.append("-" * 80)
            report.append(f"  Giá trung bình: {avg_price:,.0f}đ")
            report.append(f"  Giá thấp nhất: {min_price:,.0f}đ")
            report.append(f"  Giá cao nhất: {max_price:,.0f}đ")
            report.append("")
        
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def compare_with_original(self, original_file: str, new_file: str):
        """So sánh dữ liệu ban đầu và dữ liệu mới"""
        original_products = self.parse_sql_file(original_file)
        new_products = self.parse_sql_file(new_file)
        
        print("=" * 80)
        print("SO SÁNH DỮ LIỆU BAN ĐẦU VÀ DỮ LIỆU MỚI")
        print("=" * 80)
        print(f"\n📦 Dữ liệu ban đầu (sample_data.sql): {len(original_products)} sản phẩm")
        print(f"📦 Dữ liệu mới (tgdd_products_extended.sql): {len(new_products)} sản phẩm")
        print(f"📦 Tổng cộng: {len(original_products) + len(new_products)} sản phẩm")
        print("\n" + "=" * 80)
        
        # Phân tích dữ liệu ban đầu
        print("\n📊 THỐNG KÊ DỮ LIỆU BAN ĐẦU:")
        print("-" * 80)
        original_stats = ProductStatistics()
        original_stats.analyze(original_products)
        print(original_stats.generate_report())
        
        # Phân tích dữ liệu mới
        print("\n📊 THỐNG KÊ DỮ LIỆU MỚI:")
        print("-" * 80)
        new_stats = ProductStatistics()
        new_stats.analyze(new_products)
        print(new_stats.generate_report())
        
        # Tổng hợp
        print("\n📊 THỐNG KÊ TỔNG HỢP (BAN ĐẦU + MỚI):")
        print("-" * 80)
        all_products = original_products + new_products
        combined_stats = ProductStatistics()
        combined_stats.analyze(all_products)
        print(combined_stats.generate_report())
        
        return combined_stats

def main():
    stats = ProductStatistics()
    
    # So sánh dữ liệu
    combined_stats = stats.compare_with_original(
        'sample_data.sql',
        'tgdd_products_extended.sql'
    )
    
    # Lưu báo cáo vào file
    report = combined_stats.generate_report()
    with open('statistics_report.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("\n✅ Báo cáo đã được lưu vào file: statistics_report.txt")

if __name__ == "__main__":
    main()

