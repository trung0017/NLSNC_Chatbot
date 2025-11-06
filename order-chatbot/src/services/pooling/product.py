from typing import List, Dict, Optional
from src.config.database import get_db_connection

class ProductService:
    def __init__(self):
        self.db = get_db_connection()
        self.cursor = self.db.cursor(dictionary=True)

    def get_all_products(self) -> List[Dict]:
        query = """
        SELECT p.*, c.name as category_name 
        FROM products p
        JOIN categories c ON p.category_id = c.id
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_product_by_id(self, product_id: int) -> Optional[Dict]:
        query = """
        SELECT p.*, c.name as category_name 
        FROM products p
        JOIN categories c ON p.category_id = c.id
        WHERE p.id = %s
        """
        self.cursor.execute(query, (product_id,))
        return self.cursor.fetchone()

    def search_products(self, keyword: str) -> List[Dict]:
        query = """
        SELECT p.*, c.name as category_name 
        FROM products p
        JOIN categories c ON p.category_id = c.id
        WHERE MATCH(p.name, p.description) AGAINST(%s IN NATURAL LANGUAGE MODE)
        """
        self.cursor.execute(query, (keyword,))
        return self.cursor.fetchall()

    def update_stock(self, product_id: int, quantity: int) -> bool:
        query = """
        UPDATE products 
        SET stock = stock - %s 
        WHERE id = %s AND stock >= %s
        """
        self.cursor.execute(query, (quantity, product_id, quantity))
        self.db.commit()
        return self.cursor.rowcount > 0 