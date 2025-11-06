import os
import json
from typing import List, Dict, Tuple
import re

class ConversationLoader:
    """Lớp xử lý và tải dữ liệu hội thoại từ file"""
    
    def __init__(self, data_dir: str = "training_data"):
        """
        Args:
            data_dir: Thư mục chứa các file txt hội thoại
        """
        self.data_dir = data_dir
        self._ensure_data_dir()
    
    def _ensure_data_dir(self):
        """Tạo thư mục data nếu chưa tồn tại"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def load_conversations(self) -> List[Dict[str, str]]:
        """Tải tất cả các cuộc hội thoại từ thư mục data"""
        conversations = []
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.txt'):
                file_path = os.path.join(self.data_dir, filename)
                conversations.extend(self._parse_conversation_file(file_path))
        return conversations
    
    def _parse_conversation_file(self, file_path: str) -> List[Dict[str, str]]:
        """Phân tích file hội thoại thành cặp Q&A
        
        Format file mong đợi:
        User: câu hỏi 1
        Bot: câu trả lời 1
        User: câu hỏi 2
        Bot: câu trả lời 2
        ...
        """
        conversations = []
        current_qa = {'question': '', 'answer': ''}
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith('User:'):
                # Nếu đã có Q&A trước đó thì lưu lại
                if current_qa['question'] and current_qa['answer']:
                    conversations.append(current_qa.copy())
                # Bắt đầu Q&A mới
                current_qa['question'] = line[5:].strip()
                current_qa['answer'] = ''
            elif line.startswith('Bot:'):
                current_qa['answer'] = line[4:].strip()
        
        # Thêm cặp Q&A cuối cùng
        if current_qa['question'] and current_qa['answer']:
            conversations.append(current_qa)
            
        return conversations
    
    def extract_product_mentions(self, text: str) -> List[str]:
        """Trích xuất tên sản phẩm từ text"""
        products = []
        # Thêm các pattern nhận dạng sản phẩm
        patterns = [
            r'(?i)(macbook|dell|hp|lenovo|acer|asus)\s*(?:pro|air|xps|pavilion|thinkpad|aspire)?\s*(?:\d+)?',
            r'(?i)(laptop|máy tính)\s+(?:hiệu\s+)?(apple|dell|hp|lenovo|acer|asus)',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                products.append(match.group().strip())
        
        return list(set(products))  # Loại bỏ trùng lặp
    
    def extract_price_ranges(self, text: str) -> List[Tuple[float, float]]:
        """Trích xuất khoảng giá từ text"""
        price_ranges = []
        patterns = [
            r'(\d+(?:\.\d+)?)\s*(?:đến|tới|-)\s*(\d+(?:\.\d+)?)\s*triệu',
            r'(?:dưới|<)\s*(\d+(?:\.\d+)?)\s*triệu',
            r'(?:trên|>)\s*(\d+(?:\.\d+)?)\s*triệu',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                if len(match.groups()) == 2:
                    min_price = float(match.group(1)) * 1_000_000
                    max_price = float(match.group(2)) * 1_000_000
                    price_ranges.append((min_price, max_price))
                else:
                    price = float(match.group(1)) * 1_000_000
                    if 'dưới' in text or '<' in text:
                        price_ranges.append((0, price))
                    else:
                        price_ranges.append((price, float('inf')))
        
        return price_ranges
    
    def analyze_conversation_patterns(self) -> Dict:
        """Phân tích patterns từ các cuộc hội thoại"""
        conversations = self.load_conversations()
        patterns = {
            'products': {},  # Sản phẩm được nhắc đến
            'price_ranges': [],  # Các khoảng giá
            'common_questions': {},  # Câu hỏi phổ biến
            'requirements': set(),  # Yêu cầu thường gặp
        }
        
        for conv in conversations:
            # Phân tích sản phẩm
            products = self.extract_product_mentions(conv['question'])
            for product in products:
                patterns['products'][product] = patterns['products'].get(product, 0) + 1
            
            # Phân tích giá
            price_ranges = self.extract_price_ranges(conv['question'])
            patterns['price_ranges'].extend(price_ranges)
            
            # Phân tích yêu cầu
            requirements_keywords = {
                'pin': ['pin', 'battery', 'dùng lâu'],
                'performance': ['hiệu năng', 'mạnh', 'nhanh'],
                'display': ['màn hình', 'display'],
                'weight': ['mỏng', 'nhẹ', 'gọn'],
            }
            
            for req, keywords in requirements_keywords.items():
                if any(keyword in conv['question'].lower() for keyword in keywords):
                    patterns['requirements'].add(req)
            
            # Lưu câu hỏi
            patterns['common_questions'][conv['question']] = patterns['common_questions'].get(conv['question'], 0) + 1
        
        return patterns
    
    def save_patterns(self, patterns: Dict, output_file: str = 'conversation_patterns.json'):
        """Lưu patterns phân tích được ra file"""
        # Chuyển set thành list để có thể serialize
        patterns['requirements'] = list(patterns['requirements'])
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(patterns, f, ensure_ascii=False, indent=2)
    
    def load_patterns(self, input_file: str = 'conversation_patterns.json') -> Dict:
        """Tải patterns từ file"""
        if not os.path.exists(input_file):
            return {}
            
        with open(input_file, 'r', encoding='utf-8') as f:
            patterns = json.load(f)
            # Chuyển requirements từ list về set
            patterns['requirements'] = set(patterns['requirements'])
            return patterns 