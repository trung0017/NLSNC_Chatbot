from typing import List, Dict, Optional
import mysql.connector
from datetime import datetime
from decimal import Decimal

class DatabaseUtils:
    def __init__(self, db_config: Dict):
        self.db_config = db_config
        self.conn = None
        self.cursor = None

    def connect(self):
        """Kết nối đến database"""
        try:
            self.conn = mysql.connector.connect(**self.db_config)
            self.cursor = self.conn.cursor(dictionary=True)
        except Exception as e:
            raise Exception(f"Lỗi kết nối database: {str(e)}")

    def disconnect(self):
        """Đóng kết nối database"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def _format_category_name(self, category_name: Optional[str]) -> str:
        """Format tên danh mục cho phù hợp"""
        if not category_name:
            return "Laptop"
        
        # Mapping các tên danh mục
        category_mapping = {
            'gaming': 'Laptop Gaming',
            'văn phòng': 'Laptop Văn phòng',
            'đồ họa': 'Laptop Đồ họa',
            'mỏng nhẹ': 'Laptop Mỏng nhẹ'
        }
        
        # Tìm mapping phù hợp
        name = category_name.lower()
        for key, value in category_mapping.items():
            if key in name:
                return value
                
        return "Laptop"

    def get_products_by_category(self, category_id: int) -> List[Dict]:
        """Lấy sản phẩm theo category"""
        query = """
        SELECT 
            p.*,
            c.name as category_name,
            c.id as category_id
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE p.category_id = %s AND p.status = 'active'
        ORDER BY p.price ASC
        """
        try:
            self.cursor.execute(query, (category_id,))
            results = self.cursor.fetchall()
            # Format category names
            for result in results:
                result['category_name'] = self._format_category_name(result.get('category_name'))
            return results
        except Exception as e:
            print(f"Error in get_products_by_category: {str(e)}")
            return []

    def get_products_by_price_range(self, min_price: float, max_price: float, category_id: Optional[int] = None) -> List[Dict]:
        """Lấy sản phẩm theo khoảng giá"""
        try:
            if category_id:
                query = """
                SELECT 
                    p.*,
                    c.name as category_name,
                    c.id as category_id
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.id
                WHERE p.price BETWEEN %s AND %s 
                AND p.category_id = %s 
                AND p.status = 'active'
                ORDER BY p.price ASC
                """
                self.cursor.execute(query, (min_price, max_price, category_id))
            else:
                query = """
                SELECT 
                    p.*,
                    c.name as category_name,
                    c.id as category_id
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.id
                WHERE p.price BETWEEN %s AND %s 
                AND p.status = 'active'
                ORDER BY p.price ASC
                """
                self.cursor.execute(query, (min_price, max_price))
            
            results = self.cursor.fetchall()
            # Format category names
            for result in results:
                result['category_name'] = self._format_category_name(result.get('category_name'))
            return results
            
        except Exception as e:
            print(f"Error in get_products_by_price_range: {str(e)}")
            return []

    def get_active_promotions(self) -> List[Dict]:
        """Lấy các khuyến mãi đang hoạt động"""
        current_time = datetime.now()
        query = """
        SELECT * FROM promotions 
        WHERE status = 'active'
        AND start_date <= %s 
        AND end_date >= %s
        AND used_count < usage_limit
        ORDER BY min_order_amount ASC
        """
        self.cursor.execute(query, (current_time, current_time))
        return self.cursor.fetchall()

    def get_product_details(self, product_id: int) -> Optional[Dict]:
        """Lấy chi tiết sản phẩm"""
        query = """
        SELECT 
            p.*,
            c.name as category_name,
            c.id as category_id
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE p.id = %s AND p.status = 'active'
        """
        try:
            self.cursor.execute(query, (product_id,))
            result = self.cursor.fetchone()
            if result:
                result['category_name'] = self._format_category_name(result.get('category_name'))
            return result
        except Exception as e:
            print(f"Error in get_product_details: {str(e)}")
            return None

    def search_products(self, keyword: str) -> List[Dict]:
        """Tìm kiếm sản phẩm theo từ khóa"""
        search_term = f"%{keyword}%"
        query = """
        SELECT 
            p.*,
            c.name as category_name,
            c.id as category_id
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE (p.name LIKE %s OR p.description LIKE %s)
        AND p.status = 'active'
        ORDER BY p.price ASC
        """
        try:
            self.cursor.execute(query, (search_term, search_term))
            results = self.cursor.fetchall()
            # Format category names
            for result in results:
                result['category_name'] = self._format_category_name(result.get('category_name'))
            return results
        except Exception as e:
            print(f"Error in search_products: {str(e)}")
            return []

    def get_category_info(self, category_id: int) -> Optional[Dict]:
        """Lấy thông tin category"""
        query = "SELECT * FROM categories WHERE id = %s"
        self.cursor.execute(query, (category_id,))
        return self.cursor.fetchone()

    def get_faq_by_category(self, category: str) -> List[Dict]:
        """Lấy FAQ theo category"""
        query = "SELECT * FROM faqs WHERE category = %s"
        self.cursor.execute(query, (category,))
        return self.cursor.fetchall()

    def get_training_data_by_category(self, category: str) -> List[Dict]:
        """Lấy training data theo category"""
        query = "SELECT * FROM training_data WHERE category = %s"
        self.cursor.execute(query, (category,))
        return self.cursor.fetchall()

    def get_latest_products(self, limit: int = 5) -> List[Dict]:
        """Lấy các laptop mới nhất (sắp xếp theo created_at DESC)"""
        query = """
        SELECT 
            p.*,
            c.name as category_name,
            c.id as category_id
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE p.status = 'active'
        ORDER BY p.created_at DESC
        LIMIT %s
        """
        try:
            self.cursor.execute(query, (limit,))
            results = self.cursor.fetchall()
            # Format category names
            for result in results:
                result['category_name'] = self._format_category_name(result.get('category_name'))
            return results
        except Exception as e:
            print(f"Error in get_latest_products: {str(e)}")
            return []

    def get_windows_laptops(self, limit: int = 5) -> List[Dict]:
        """Lấy các laptop Windows (không phải Mac)"""
        query = """
        SELECT 
            p.*,
            c.name as category_name,
            c.id as category_id
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE p.status = 'active'
        AND (p.name NOT LIKE '%Mac%' AND p.name NOT LIKE '%MacBook%')
        AND (p.description NOT LIKE '%Mac%' OR p.description IS NULL)
        ORDER BY p.price ASC
        LIMIT %s
        """
        try:
            self.cursor.execute(query, (limit,))
            results = self.cursor.fetchall()
            for result in results:
                result['category_name'] = self._format_category_name(result.get('category_name'))
            return results
        except Exception as e:
            print(f"Error in get_windows_laptops: {str(e)}")
            return []

    def get_mac_laptops(self, limit: int = 5) -> List[Dict]:
        """Lấy các laptop Mac (MacBook)"""
        query = """
        SELECT 
            p.*,
            c.name as category_name,
            c.id as category_id
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE p.status = 'active'
        AND (p.name LIKE '%Mac%' OR p.name LIKE '%MacBook%')
        ORDER BY p.price ASC
        LIMIT %s
        """
        try:
            self.cursor.execute(query, (limit,))
            results = self.cursor.fetchall()
            for result in results:
                result['category_name'] = self._format_category_name(result.get('category_name'))
            return results
        except Exception as e:
            print(f"Error in get_mac_laptops: {str(e)}")
            return []

    def get_products_by_chip(self, chip_name: str, limit: int = 5) -> List[Dict]:
        """Lấy các laptop theo chip (M3, M4, M4 Pro, etc.)"""
        query = """
        SELECT 
            p.*,
            c.name as category_name,
            c.id as category_id
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE p.status = 'active'
        AND (p.name LIKE %s OR p.description LIKE %s)
        ORDER BY p.price ASC
        LIMIT %s
        """
        try:
            search_term = f"%{chip_name}%"
            self.cursor.execute(query, (search_term, search_term, limit))
            results = self.cursor.fetchall()
            for result in results:
                result['category_name'] = self._format_category_name(result.get('category_name'))
            return results
        except Exception as e:
            print(f"Error in get_products_by_chip: {str(e)}")
            return [] 