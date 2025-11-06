import mysql.connector
from mysql.connector import pooling
import logging
from typing import List, Dict, Optional, Tuple
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseService:
    _instance = None
    _pool = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseService, cls).__new__(cls)
            cls._initialize_pool()
        return cls._instance
    
    @classmethod
    def _initialize_pool(cls):
        if cls._pool is None:
            try:
                dbconfig = {
                    "host": os.getenv("DB_HOST", "localhost"),
                    "user": os.getenv("DB_USER", "root"),
                    "password": os.getenv("DB_PASSWORD", ""),
                    "database": os.getenv("DB_NAME", "chatbot_db"),
                    "port": int(os.getenv("DB_PORT", "3306"))
                }
                
                cls._pool = mysql.connector.pooling.MySQLConnectionPool(
                    pool_name="mypool",
                    pool_size=5,
                    **dbconfig
                )
                logging.info("Database connection pool initialized successfully")
            except Exception as e:
                logging.error(f"Error initializing database pool: {str(e)}")
                raise
    
    def get_connection(self):
        try:
            return self._pool.get_connection()
        except Exception as e:
            logging.error(f"Error getting database connection: {str(e)}")
            raise

    def get_product_by_id(self, product_id: int) -> Optional[Dict]:
        """Get product details by ID"""
        query = """
        SELECT p.*, c.name as category_name,
               COALESCE(AVG(pr.rating), 0) as avg_rating,
               COUNT(pr.id) as review_count
        FROM products p
        JOIN categories c ON p.category_id = c.id
        LEFT JOIN product_reviews pr ON p.id = pr.product_id
        WHERE p.id = %s AND p.status = 'active'
        GROUP BY p.id
        """
        return self._execute_query(query, (product_id,), single=True)
    
    def search_products(self, keyword: str, limit: int = 5) -> List[Dict]:
        """Search products using fulltext search"""
        query = """
        SELECT p.*, c.name as category_name,
               COALESCE(AVG(pr.rating), 0) as avg_rating,
               COUNT(pr.id) as review_count
        FROM products p
        JOIN categories c ON p.category_id = c.id
        LEFT JOIN product_reviews pr ON p.id = pr.product_id
        WHERE MATCH(p.name, p.description) AGAINST(%s IN NATURAL LANGUAGE MODE)
        AND p.status = 'active'
        GROUP BY p.id
        LIMIT %s
        """
        return self._execute_query(query, (keyword, limit))
    
    def get_products_by_category(self, category_id: int, limit: int = 5) -> List[Dict]:
        """Get products by category"""
        query = """
        SELECT p.*, c.name as category_name,
               COALESCE(AVG(pr.rating), 0) as avg_rating,
               COUNT(pr.id) as review_count
        FROM products p
        JOIN categories c ON p.category_id = c.id
        LEFT JOIN product_reviews pr ON p.id = pr.product_id
        WHERE p.category_id = %s AND p.status = 'active'
        GROUP BY p.id
        LIMIT %s
        """
        return self._execute_query(query, (category_id, limit))
    
    def get_products_by_price_range(self, min_price: float, max_price: float, limit: int = 5) -> List[Dict]:
        """Get products within price range"""
        query = """
        SELECT p.*, c.name as category_name,
               COALESCE(AVG(pr.rating), 0) as avg_rating,
               COUNT(pr.id) as review_count
        FROM products p
        JOIN categories c ON p.category_id = c.id
        LEFT JOIN product_reviews pr ON p.id = pr.product_id
        WHERE p.price BETWEEN %s AND %s AND p.status = 'active'
        GROUP BY p.id
        LIMIT %s
        """
        return self._execute_query(query, (min_price, max_price, limit))

    def get_faq_answer(self, question: str) -> Optional[Dict]:
        """Get FAQ answer using fulltext search"""
        query = """
        SELECT *
        FROM faqs
        WHERE MATCH(question) AGAINST(%s IN NATURAL LANGUAGE MODE)
        ORDER BY MATCH(question) AGAINST(%s IN NATURAL LANGUAGE MODE) DESC
        LIMIT 1
        """
        return self._execute_query(query, (question, question), single=True)

    def save_chat_history(self, customer_id: Optional[int], message: str, is_bot: bool = False) -> None:
        """Save chat message to history"""
        query = """
        INSERT INTO chat_history (customer_id, message, is_bot)
        VALUES (%s, %s, %s)
        """
        self._execute_query(query, (customer_id, message, is_bot), fetch=False)

    def get_chat_history(self, customer_id: Optional[int], limit: int = 10) -> List[Dict]:
        """Get recent chat history"""
        query = """
        SELECT *
        FROM chat_history
        WHERE customer_id = %s
        ORDER BY created_at DESC
        LIMIT %s
        """
        return self._execute_query(query, (customer_id, limit))

    def save_feedback(self, customer_id: Optional[int], message: str, feedback: str) -> None:
        """Save user feedback"""
        query = """
        INSERT INTO feedback (customer_id, message, feedback)
        VALUES (%s, %s, %s)
        """
        self._execute_query(query, (customer_id, message, feedback), fetch=False)

    def get_active_promotions(self) -> List[Dict]:
        """Get currently active promotions"""
        query = """
        SELECT *
        FROM promotions
        WHERE status = 'active'
        AND start_date <= CURRENT_TIMESTAMP
        AND end_date >= CURRENT_TIMESTAMP
        AND (usage_limit IS NULL OR used_count < usage_limit)
        """
        return self._execute_query(query)
    
    def _execute_query(self, query: str, params: tuple = None, single: bool = False, fetch: bool = True):
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params)
            
            if fetch:
                if single:
                    result = cursor.fetchone()
                else:
                    result = cursor.fetchall()
                return result
            else:
                conn.commit()
                
        except Exception as e:
            if conn:
                conn.rollback()
            logging.error(f"Database query error: {str(e)}")
            raise
        finally:
            if conn:
                conn.close() 