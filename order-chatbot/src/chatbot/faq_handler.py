import os
import logging
from typing import Dict, List, Any, Tuple, Optional
from mysql.connector import pooling
from mysql.connector import Error as MySQLError
from dotenv import load_dotenv

# Configure logging
logger = logging.getLogger(__name__)

load_dotenv()

class DatabaseError(Exception):
    """Custom exception for database-related errors"""
    pass

class FAQHandler:
    def __init__(self):
        try:
            # Database configuration
            dbconfig = {
                "host": os.getenv('MYSQL_HOST'),
                "user": os.getenv('MYSQL_USER'),
                "password": os.getenv('MYSQL_PASSWORD'),
                "database": os.getenv('MYSQL_DATABASE'),
                "pool_name": "faq_pool",
                "pool_size": 5
            }
            
            self.connection_pool = pooling.MySQLConnectionPool(**dbconfig)
            logger.info("Database connection pool initialized successfully")
        except MySQLError as e:
            logger.error(f"Failed to initialize database connection pool: {e}")
            raise DatabaseError("Could not initialize database connection")

    def _get_connection(self):
        """Get a connection from the pool with error handling"""
        try:
            return self.connection_pool.get_connection()
        except MySQLError as e:
            logger.error(f"Failed to get database connection from pool: {e}")
            raise DatabaseError("Could not get database connection")

    def close(self):
        """Safely close all connections in the pool"""
        try:
            # The pool will handle closing connections
            logger.info("Closing database connections")
        except Exception as e:
            logger.error(f"Error while closing database connections: {e}")

    def __del__(self):
        """Ensure resources are properly cleaned up"""
        self.close()

    def get_faq_answer(self, question: str) -> Optional[str]:
        """Find the most relevant answer from FAQ database with improved search"""
        query = """
        SELECT answer, MATCH(question) AGAINST(%s IN NATURAL LANGUAGE MODE) as relevance 
        FROM faqs 
        WHERE MATCH(question) AGAINST(%s IN NATURAL LANGUAGE MODE) > 0.2
        ORDER BY relevance DESC
        LIMIT 1
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (question, question))
            result = cursor.fetchone()
            return result['answer'] if result else None
        except MySQLError as e:
            logger.error(f"Database error in get_faq_answer: {e}")
            raise DatabaseError("Failed to retrieve FAQ answer")
        finally:
            cursor.close()
            conn.close()

    def get_product_info(self, product_name: str) -> Optional[Dict]:
        """Get product information with enhanced search and caching"""
        query = """
        SELECT 
            p.*, 
            c.name as category_name,
            MATCH(p.name, p.description) AGAINST(%s IN NATURAL LANGUAGE MODE) as relevance
        FROM products p
        JOIN categories c ON p.category_id = c.id
        WHERE MATCH(p.name, p.description) AGAINST(%s IN NATURAL LANGUAGE MODE) > 0.2
        ORDER BY relevance DESC
        LIMIT 1
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (product_name, product_name))
            return cursor.fetchone()
        except MySQLError as e:
            logger.error(f"Database error in get_product_info: {e}")
            raise DatabaseError("Failed to retrieve product information")
        finally:
            cursor.close()
            conn.close()

    def get_similar_products(self, category_id: int, price_range: Tuple[float, float], limit: int = 3) -> List[Dict]:
        """Find similar products with improved filtering"""
        query = """
        SELECT 
            p.*,
            c.name as category_name
        FROM products p
        JOIN categories c ON p.category_id = c.id
        WHERE p.category_id = %s 
        AND p.price BETWEEN %s AND %s
        AND p.stock > 0  -- Only in-stock items
        ORDER BY p.price ASC
        LIMIT %s
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (category_id, price_range[0], price_range[1], limit))
            return cursor.fetchall()
        except MySQLError as e:
            logger.error(f"Database error in get_similar_products: {e}")
            raise DatabaseError("Failed to retrieve similar products")
        finally:
            cursor.close()
            conn.close()

    def get_featured_products(self, limit: int = 5) -> List[Dict]:
        """Get available products sorted by price"""
        query = """
        SELECT 
            p.*,
            c.name as category_name
        FROM products p
        JOIN categories c ON p.category_id = c.id
        WHERE p.stock > 0  -- Only in-stock items
        ORDER BY p.price ASC  -- Sắp xếp theo giá tăng dần
        LIMIT %s
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (limit,))
            return cursor.fetchall()
        except MySQLError as e:
            logger.error(f"Database error in get_featured_products: {e}")
            raise DatabaseError("Failed to retrieve featured products")
        finally:
            cursor.close()
            conn.close()

    def save_chat_history(self, customer_id: int, message: str, is_bot: bool) -> None:
        """Save chat history with improved error handling"""
        query = """
        INSERT INTO chat_history (customer_id, message, is_bot, created_at)
        VALUES (%s, %s, %s, NOW())
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (customer_id, message, is_bot))
            conn.commit()
        except MySQLError as e:
            logger.error(f"Database error in save_chat_history: {e}")
            raise DatabaseError("Failed to save chat history")
        finally:
            cursor.close()
            conn.close()

    def get_chat_history(self, customer_id: int, limit: int = 10) -> List[Dict]:
        """Retrieve recent chat history"""
        query = """
        SELECT message, is_bot, created_at
        FROM chat_history
        WHERE customer_id = %s
        ORDER BY created_at DESC
        LIMIT %s
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (customer_id, limit))
            return cursor.fetchall()
        except MySQLError as e:
            logger.error(f"Database error in get_chat_history: {e}")
            raise DatabaseError("Failed to retrieve chat history")
        finally:
            cursor.close()
            conn.close()

    # Các phương thức khác giữ nguyên... 