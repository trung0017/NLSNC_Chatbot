import re
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from difflib import SequenceMatcher

logger = logging.getLogger(__name__)

def format_price(price: float) -> str:
    """Format price in Vietnamese currency format"""
    try:
        return f"{price:,.0f}đ"
    except (ValueError, TypeError) as e:
        logger.error(f"Error formatting price: {e}")
        return "Đang cập nhật"

def extract_product_info(text: str) -> Dict[str, Any]:
    """Extract product information from text with enhanced pattern matching"""
    patterns = {
        'price': [
            r'(\d+(?:\.\d+)?)\s*(?:đ|VND|k|nghìn|triệu)',
            r'giá\s*(?:là|:)?\s*(\d+(?:\.\d+)?)',
        ],
        'quantity': [
            r'(\d+)\s*(?:cái|chiếc|sản phẩm)',
            r'số\s*lượng\s*(?:là|:)?\s*(\d+)',
        ],
        'product_name': [
            r'(?:mua|đặt|order)\s+(.+?)(?:\s+giá|\s+số lượng|$)',
            r'sản\s*phẩm\s*(?:là|:)?\s*(.+?)(?:\s+giá|\s+số lượng|$)',
        ],
        'color': [
            r'màu\s+(.+?)(?:\s|$)',
            r'color\s*(?:là|:)?\s*(.+?)(?:\s|$)',
        ],
        'size': [
            r'size\s*(?:là|:)?\s*(.+?)(?:\s|$)',
            r'kích\s*(?:thước|cỡ)\s*(?:là|:)?\s*(.+?)(?:\s|$)',
        ]
    }
    
    result = {}
    for key, pattern_list in patterns.items():
        for pattern in pattern_list:
            match = re.search(pattern, text, re.IGNORECASE | re.UNICODE)
            if match:
                result[key] = match.group(1).strip()
                break
    
    return result

def format_chat_history(history: List[Dict[str, Any]], max_length: int = 10) -> str:
    """Format chat history with timestamps and limited length"""
    formatted = []
    for msg in history[-max_length:]:  # Only keep last max_length messages
        sender = "🤖 Bot" if msg['is_bot'] else "👤 Khách"
        timestamp = msg.get('created_at', datetime.now()).strftime("%H:%M")
        formatted.append(f"[{timestamp}] {sender}: {msg['message']}")
    return "\n".join(formatted)

def normalize_text(text: str) -> str:
    """Normalize Vietnamese text for better matching"""
    text = text.lower()
    # Remove diacritics
    patterns = {
        '[àáảãạăắằẳẵặâấầẩẫậ]': 'a',
        '[đ]': 'd',
        '[èéẻẽẹêếềểễệ]': 'e',
        '[ìíỉĩị]': 'i',
        '[òóỏõọôốồổỗộơớờởỡợ]': 'o',
        '[ùúủũụưứừửữự]': 'u',
        '[ỳýỷỹỵ]': 'y'
    }
    for pattern, replace in patterns.items():
        text = re.sub(pattern, replace, text)
    return text

def calculate_text_similarity(text1: str, text2: str) -> float:
    """Calculate similarity between two texts"""
    text1 = normalize_text(text1)
    text2 = normalize_text(text2)
    return SequenceMatcher(None, text1, text2).ratio()

def extract_contact_info(text: str) -> Dict[str, str]:
    """Extract contact information from text"""
    patterns = {
        'phone': r'(?:0|\+84)\d{9,10}',
        'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        'address': r'(?:địa\s*chỉ|address)[:\s]+(.+?)(?:\.|$)',
        'name': r'(?:tên|name)[:\s]+([^,\n]+)',
    }
    
    result = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE | re.UNICODE)
        if match:
            # For address and name, get the captured group
            if key in ['address', 'name']:
                result[key] = match.group(1).strip()
            else:
                result[key] = match.group(0).strip()
    
    return result

def parse_price_range(text: str) -> Optional[Tuple[float, float]]:
    """Parse price range from text"""
    try:
        # Match patterns like "từ 1tr đến 2tr", "1-2 triệu", "dưới 5 triệu", etc.
        patterns = [
            r'(?:từ|>)\s*(\d+(?:\.\d+)?)\s*(?:đến|tới|-)\s*(\d+(?:\.\d+)?)\s*(?:tr|triệu|m|k|nghìn)?',
            r'(?:dưới|<)\s*(\d+(?:\.\d+)?)\s*(?:tr|triệu|m|k|nghìn)',
            r'(?:trên|>)\s*(\d+(?:\.\d+)?)\s*(?:tr|triệu|m|k|nghìn)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                if len(match.groups()) == 2:  # Range
                    min_price = float(match.group(1))
                    max_price = float(match.group(2))
                    return (min_price * 1_000_000, max_price * 1_000_000)
                else:  # Single value
                    price = float(match.group(1))
                    if 'dưới|<' in pattern:
                        return (0, price * 1_000_000)
                    else:  # trên|>
                        return (price * 1_000_000, float('inf'))
        
        return None
    except (ValueError, TypeError) as e:
        logger.error(f"Error parsing price range: {e}")
        return None

def format_product_features(features: List[str]) -> str:
    """Format product features as a bulleted list"""
    return "\n".join([f"• {feature}" for feature in features])

def validate_phone_number(phone: str) -> bool:
    """Validate Vietnamese phone number format"""
    pattern = r'^(?:0|\+84)(?:3[2-9]|5[2689]|7[06-9]|8[1-689]|9[0-9])[0-9]{7}$'
    return bool(re.match(pattern, phone))

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def clean_html(text: str) -> str:
    """Remove HTML tags from text"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text) 