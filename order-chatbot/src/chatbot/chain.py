import google.generativeai as genai
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import json
import re
import os

from .database_utils import DatabaseUtils
from .response_formatter import ResponseFormatter

class ChatbotChain:
    def __init__(self, db_config: Dict, api_key: str):
        """Khởi tạo ChatbotChain với config database và API key"""
        self.db = DatabaseUtils(db_config)
        self.formatter = ResponseFormatter()
        
        # Cấu hình Google Gemini Pro
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
        # Khởi tạo chat history
        self.chat = self.model.start_chat(history=[])
        
        # Khởi tạo conversation context
        self.conversation_context = {}
        
        # Khởi tạo session storage cho context
        self.session_storage = {}

    @staticmethod
    def _is_laptop_category(category_id: Optional[int]) -> bool:
        """Giới hạn sản phẩm về đúng nhóm Laptop (id 2 và các nhóm con trong sample)."""
        if category_id is None:
            return False
        return category_id in {2, 5, 6, 7, 8, 9}

    def _summarize_products(self, products: List[Dict], max_items: int = 5) -> str:
        """Tóm tắt danh sách sản phẩm cho prompt model"""
        if not products:
            return "Không có sản phẩm liên quan."
        lines = []
        for i, p in enumerate(products[:max_items], 1):
            name = p.get('name', '').strip()
            price = p.get('price', 0)
            category = p.get('category_name', 'Laptop')
            desc = (p.get('description') or '').strip()
            # Lấy vài đặc điểm từ mô tả
            key_specs = []
            lower = desc.lower()
            for key in ['i3', 'i5', 'i7', 'ryzen', '8gb', '16gb', 'ssd', 'rtx', 'gtx', 'ips', '144hz']:
                if key in lower:
                    key_specs.append(key.upper())
            specs_str = ", ".join(dict.fromkeys(key_specs)) if key_specs else ""
            lines.append(f"{i}) {name} | {price:,.0f}đ | {category}" + (f" | {specs_str}" if specs_str else ""))
        return "\n".join(lines)

    def save_context(self, session_id: str):
        """Lưu context vào session storage"""
        if session_id:
            print(f"Saving context for session {session_id}: {self.conversation_context}")  # Debug log
            self.session_storage[session_id] = self.conversation_context.copy()

    def load_context(self, session_id: str):
        """Khôi phục context từ session storage"""
        if session_id and session_id in self.session_storage:
            print(f"Loading context for session {session_id}: {self.session_storage[session_id]}")  # Debug log
            self.conversation_context = self.session_storage[session_id].copy()
            return True
        return False

    def clear_context(self, session_id: str = None):
        """Xóa context"""
        print(f"Clearing context for session {session_id}")  # Debug log
        if session_id:
            self.session_storage.pop(session_id, None)
        self.conversation_context = {}

    def _extract_product_info(self, message: str) -> Dict:
        """Trích xuất thông tin sản phẩm từ tin nhắn"""
        # Xử lý regex để tìm khoảng giá
        price_patterns = [
            r'(\d+)\s*-\s*(\d+)\s*triệu',  # 15-20 triệu
            r'khoảng\s*(\d+)\s*-\s*(\d+)\s*triệu',  # khoảng 15-20 triệu
            r'từ\s*(\d+)\s*-\s*(\d+)\s*triệu',  # từ 15-20 triệu
            r'tầm\s*(\d+)\s*-\s*(\d+)\s*triệu',  # tầm 15-20 triệu
            r'dưới\s*(\d+)\s*triệu',  # dưới 15 triệu
            r'khoảng\s*(\d+)\s*triệu'  # khoảng 15 triệu
        ]
        
        # Các từ khóa về mục đích sử dụng
        purpose_patterns = {
            'lập trình': [r'lập trình', r'coding', r'dev', r'developer', r'programming', r'code'],
            'gaming': [r'game', r'gaming', r'chơi game'],
            'đồ họa': [r'đồ họa', r'thiết kế', r'design', r'photoshop'],
            'văn phòng': [r'văn phòng', r'office', r'học tập', r'sinh viên']
        }

        # Các model laptop phổ biến
        laptop_models = {
            'dell': [
                r'inspiron[\s-]*(\d{4})',  # Matches Inspiron followed by 4 digits
                r'vostro[\s-]*(\d{4})',
                r'latitude[\s-]*(\d{4})',
                r'xps[\s-]*(\d{2,4})',
                r'g15[\s-]*(\d{4})?',
                r'alienware[\s-]*[mr]?\d{2}'
            ],
            'lenovo': [
                r'ideapad[\s-]*(\d{1})',
                r'thinkpad[\s-]*[a-z]\d{2,3}',
                r'legion[\s-]*(\d{1})',
                r'yoga[\s-]*(\d{1,4})'
            ],
            'hp': [
                r'pavilion[\s-]*(\d{2,4})',
                r'envy[\s-]*(\d{2,4})',
                r'elitebook[\s-]*(\d{3,4})',
                r'victus[\s-]*(\d{2,4})',
                r'omen[\s-]*(\d{2,4})'
            ],
            'asus': [
                r'vivobook[\s-]*(\d{2,4})',
                r'zenbook[\s-]*(\d{2,4})',
                r'tuf[\s-]*[a-z]?\d{2,4}',
                r'rog[\s-]*[a-z]?\d{2,4}',
                r'expertbook[\s-]*[a-z]?\d{2,4}'
            ],
            'acer': [
                r'aspire[\s-]*(\d{1,4})',
                r'nitro[\s-]*(\d{1,4})',
                r'predator[\s-]*(\d{1,4})',
                r'swift[\s-]*(\d{1,4})',
                r'spin[\s-]*(\d{1,4})'
            ],
            'msi': [
                r'gf[\s-]*(\d{2,3})',
                r'gl[\s-]*(\d{2,3})',
                r'gs[\s-]*(\d{2,3})',
                r'ge[\s-]*(\d{2,3})',
                r'gp[\s-]*(\d{2,3})',
                r'prestige[\s-]*(\d{2,3})',
                r'modern[\s-]*(\d{2,3})',
                r'katana[\s-]*(\d{2,3})',
                r'sword[\s-]*(\d{2,3})',
                r'raider[\s-]*(\d{2,3})',
                r'stealth[\s-]*(\d{2,3})'
            ]
        }
        
        # Các pattern cho câu hỏi về model cụ thể
        model_question_patterns = [
            r'chi tiết.*laptop',
            r'chi tiết.*về',
            r'thông tin.*laptop',
            r'thông tin.*về',
            r'thông số.*laptop',
            r'thông số.*về',
            r'cấu hình.*laptop',
            r'cấu hình.*về'
        ]
        
        price_range = None
        message_lower = message.lower()
        
        # Tìm model laptop cụ thể
        detected_model = None
        detected_brand = None
        full_model_name = None
        
        # Kiểm tra xem có phải là câu hỏi về model cụ thể không
        is_model_question = any(re.search(pattern, message_lower) for pattern in model_question_patterns)
        
        # Kiểm tra brand trước
        for brand in laptop_models.keys():
            if brand in message_lower:
                detected_brand = brand
                break
                
        # Nếu tìm thấy brand, tìm model tương ứng
        if detected_brand:
            for model_pattern in laptop_models[detected_brand]:
                match = re.search(model_pattern, message_lower)
                if match:
                    base_model = match.group(0)  # Lấy tên model cơ bản
                    model_number = match.group(1) if len(match.groups()) > 0 else ""  # Lấy số model nếu có
                    
                    # Tìm số model đầy đủ trong message gốc
                    full_model_pattern = f"{base_model}[-\\s]*\\d+" if model_number else base_model
                    full_match = re.search(full_model_pattern, message_lower)
                    if full_match:
                        full_model_name = full_match.group(0)
                    else:
                        full_model_name = base_model
                        
                    detected_model = full_model_name
                    break
        
        # Nếu tìm thấy model cụ thể hoặc là câu hỏi về model
        if detected_model or (is_model_question and detected_brand):
            return {
                "price_range": None,
                "category_id": None,
                "keywords": ["specific_model", detected_brand, detected_model] if detected_model else ["specific_model", detected_brand],
                "is_faq": False,
                "faq_category": None,
                "is_general_request": False,
                "specific_model": True,
                "full_model_name": full_model_name
            }
        
        # Tìm mục đích sử dụng
        detected_purposes = []
        for purpose, patterns in purpose_patterns.items():
            if any(re.search(pattern, message_lower) for pattern in patterns):
                detected_purposes.append(purpose)
        
        # Tìm khoảng giá bằng regex
        for pattern in price_patterns:
            match = re.search(pattern, message_lower)
            if match:
                groups = match.groups()
                if len(groups) == 2:  # Khoảng giá (VD: 15-20 triệu)
                    min_price = float(groups[0]) * 1_000_000
                    max_price = float(groups[1]) * 1_000_000
                    price_range = [min_price, max_price]
                    break
                elif len(groups) == 1:  # Một mức giá (VD: dưới 15 triệu)
                    price = float(groups[0]) * 1_000_000
                    if 'dưới' in message_lower:
                        price_range = [0, price]
                    else:  # khoảng/tầm X triệu
                        margin = 0.2  # 20% margin
                        price_range = [price * (1 - margin), price * (1 + margin)]
                    break
        
        # Nếu có mục đích sử dụng cụ thể
        if detected_purposes:
            return {
                "price_range": price_range,
                "category_id": None,
                "keywords": detected_purposes,
                "is_faq": False,
                "faq_category": None,
                "is_general_request": False,
                "specific_model": False
            }
            
        # Nếu tìm được khoảng giá bằng regex
        if price_range:
            return {
                "price_range": price_range,
                "category_id": None,
                "keywords": [],
                "is_faq": False,
                "faq_category": None,
                "is_general_request": False,
                "specific_model": False
            }
            
        # Nếu không tìm được thông tin gì
        return {
            "price_range": None,
            "category_id": None,
            "keywords": detected_purposes if detected_purposes else [],
            "is_faq": False,
            "faq_category": None,
            "is_general_request": True,
            "specific_model": False
        }

    def _get_products(self, extracted_info: Dict) -> List[Dict]:
        """Lấy danh sách sản phẩm phù hợp"""
        try:
            self.db.connect()
            
            # Tìm theo model cụ thể
            if extracted_info.get('specific_model'):
                # Lấy brand và model từ keywords
                brand = next((kw for kw in extracted_info['keywords'] if kw != "specific_model"), None)
                if brand:
                    # Tạo search query từ brand và full model name
                    search_query = None
                    if extracted_info.get('full_model_name'):
                        search_query = f"{brand} {extracted_info['full_model_name']}"
                    else:
                        # Fallback nếu không có full model name
                        model = next((kw for kw in extracted_info['keywords'] if kw not in ["specific_model", brand]), None)
                        if model:
                            search_query = f"{brand} {model}"
                    
                    if search_query:
                        # Thử tìm chính xác trước
                        products = self.db.search_products(search_query)
                        if not products:
                            # Nếu không tìm thấy, thử tìm với các biến thể của tên model
                            # Ví dụ: "MSI GF63" có thể là "MSI GF63 Thin" hoặc "MSI GF63 Gaming"
                            base_model = search_query.split()[0:2]  # Lấy brand và series
                            products = self.db.search_products(" ".join(base_model))
                        
                        if products:
                            # Chỉ giữ sản phẩm thuộc nhóm Laptop
                            return [p for p in products if self._is_laptop_category(p.get('category_id'))]
            
            # Tìm theo khoảng giá
            if extracted_info['price_range']:
                min_price, max_price = extracted_info['price_range']
                products = self.db.get_products_by_price_range(
                    min_price, 
                    max_price,
                    extracted_info['category_id']
                )
                if products:
                    return [p for p in products if self._is_laptop_category(p.get('category_id'))]
            
            # Tìm theo category
            if extracted_info['category_id']:
                products = self.db.get_products_by_category(
                    extracted_info['category_id']
                )
                if products:
                    return [p for p in products if self._is_laptop_category(p.get('category_id'))]
            
            # Tìm theo từ khóa
            if extracted_info['keywords']:
                keyword = ' '.join(extracted_info['keywords'])
                products = self.db.search_products(keyword)
                return [p for p in products if self._is_laptop_category(p.get('category_id'))]
                
            return []
            
        except Exception as e:
            print(f"Error getting products: {str(e)}")
            return []
        finally:
            self.db.disconnect()

    def _get_faq_answer(self, category: str) -> Optional[str]:
        """Lấy câu trả lời FAQ nếu có"""
        try:
            self.db.connect()
            faqs = self.db.get_faq_by_category(category)
            if faqs:
                return self.formatter.format_faq_answer(faqs[0])
            return None
        except Exception as e:
            print(f"Error getting FAQ: {str(e)}")
            return None
        finally:
            self.db.disconnect()

    def _save_chat_history(self, message: str, response: str, context: Dict):
        """Lưu lịch sử chat"""
        try:
            self.db.connect()
            # TODO: Implement save chat history
            pass
        except Exception as e:
            print(f"Error saving chat history: {str(e)}")
        finally:
            self.db.disconnect()

    def generate_response(self, message: str, session_id: str = None, context: Dict = None) -> Tuple[str, Dict]:
        """
        Xử lý tin nhắn và tạo câu trả lời
        """
        # Khôi phục context từ session nếu có
        if session_id:
            self.load_context(session_id)
        
        # Sử dụng context của instance nếu không có context được truyền vào
        if context is None:
            context = self.conversation_context
        else:
            # Merge context được truyền vào với context hiện tại
            self.conversation_context.update(context)
            context = self.conversation_context
        
        try:
            # Chuẩn hóa tin nhắn: bỏ khoảng trắng thừa và chuyển về chữ thường
            normalized_msg = message.lower().strip()
            
            # Extract thông tin từ tin nhắn
            extracted_info = self._extract_product_info(message)
            
            # Xử lý trường hợp hỏi về model cụ thể trước
            if extracted_info.get('specific_model'):
                # Tìm sản phẩm theo model
                products = self._get_products(extracted_info)
                if products:
                    # Lưu model vào context để xử lý câu hỏi tiếp theo
                    context['last_model'] = products[0]
                    if session_id:
                        self.save_context(session_id)
                    return self.formatter.format_specific_model_info(products[0]), context
                else:
                    if session_id:
                        self.save_context(session_id)
                    return self.formatter.format_model_not_found(extracted_info['keywords'], extracted_info.get('full_model_name')), context
            
            # Các pattern cho câu hỏi về nâng cấp phần cứng
            upgrade_patterns = {
                'ram': [
                    r'nâng.*ram',
                    r'up.*ram',
                    r'thêm.*ram',
                    r'thay.*ram',
                    r'ram.*được.*không',
                    r'ram.*được.*ko',
                    r'ram.*đc.*không',
                    r'ram.*đc.*ko',
                    r'có.*nâng.*ram.*không',
                    r'có.*up.*ram.*không',
                    r'có thể nâng cấp ram'
                ],
                'storage': [
                    r'nâng.*ổ.*cứng',
                    r'up.*ssd',
                    r'thêm.*ổ.*cứng',
                    r'thay.*ổ.*cứng',
                    r'ssd.*được.*không',
                    r'ổ.*cứng.*được.*không'
                ],
                'general': [
                    r'nâng.*cấp.*được.*không',
                    r'up.*được.*không',
                    r'có.*nâng.*cấp.*được.*không',
                    r'có.*up.*được.*không'
                ]
            }
            
            # Kiểm tra nếu là câu hỏi về nâng cấp
            for component, patterns in upgrade_patterns.items():
                if any(re.search(pattern, normalized_msg) for pattern in patterns):
                    if 'last_model' in context:
                        print(f"Found last_model in context: {context['last_model']}")  # Debug log
                        return self._get_spec_info(context['last_model'], 'upgrade'), context
                    else:
                        return """Dạ, để tư vấn về khả năng nâng cấp, anh/chị vui lòng cho em biết:
• Model laptop cụ thể đang quan tâm
• Hoặc cho em biết nhu cầu sử dụng và ngân sách
để em tư vấn các model phù hợp và có khả năng nâng cấp tốt ạ.""", context
            
            # Xử lý câu chào
            greetings = {
                'xin chào', 'xin chao', 'chào', 'chao',
                'xin chào ạ', 'xin chao a', 'chào ạ', 'chao a',
                'kính chào', 'kinh chao',
                'chào bạn', 'chao ban', 'hi bạn', 'hi ban',
                'chào shop', 'chao shop',
                'hello', 'hi', 'hey', 'alo'
            }
            
            # Kiểm tra xem tin nhắn có phải là câu chào không
            if normalized_msg in greetings or any(g in normalized_msg for g in greetings):
                # Reset context khi bắt đầu cuộc hội thoại mới
                self.clear_context(session_id)
                context = self.conversation_context
                response = self.formatter.format_greeting()
                if session_id:
                    self.save_context(session_id)
                return response, context
            
            # Xử lý FAQ nếu có
            if extracted_info['is_faq'] and extracted_info['faq_category']:
                faq_answer = self._get_faq_answer(extracted_info['faq_category'])
                if faq_answer:
                    if session_id:
                        self.save_context(session_id)
                    return faq_answer, context
            
            # Nếu có last_model trong context, ưu tiên trả lời về model đó
            if 'last_model' in context:
                # Các từ khóa chung về thông tin sản phẩm
                general_info_patterns = [
                    r'thông tin', r'thông số', r'cấu hình', r'chi tiết',
                    r'pin', r'màn hình', r'hiệu năng', r'nâng cấp',
                    r'giá', r'bao nhiêu', r'thế nào'
                ]
                
                # Nếu câu hỏi chứa các từ khóa chung về thông tin sản phẩm
                if any(re.search(pattern, normalized_msg) for pattern in general_info_patterns):
                    response = self._get_spec_info(context['last_model'], 'performance')
                    if session_id:
                        self.save_context(session_id)
                    return response, context
            
            # Lấy danh sách sản phẩm phù hợp
            products = self._get_products(extracted_info)
            
            # Cập nhật context
            context['last_products'] = products
            context['purposes'] = extracted_info['keywords']
            context['price_range'] = extracted_info['price_range']
            
            # Xử lý các trường hợp khác nhau
            response = None
            if extracted_info['price_range'] and extracted_info['keywords']:
                # Có cả giá và nhu cầu
                min_price, max_price = extracted_info['price_range']
                response = self.formatter.format_purpose_with_price_and_details(
                    products, extracted_info['keywords'], min_price, max_price
                )
            elif extracted_info['price_range']:
                # Chỉ có giá
                min_price, max_price = extracted_info['price_range']
                response = self.formatter.format_price_range_response(
                    products, min_price, max_price
                )
            elif extracted_info['keywords']:
                # Chỉ có nhu cầu
                response = self.formatter.format_purpose_without_price(extracted_info['keywords'])
            else:
                # Không có thông tin gì
                response = self.formatter.format_general_laptop_request()

            # Thử dùng Gemini để viết lại câu trả lời dựa trên dữ liệu thật
            try:
                top_products = products[:5]
                product_block = self._summarize_products(top_products)
                promotions = []
                try:
                    self.db.connect()
                    promotions = self.db.get_active_promotions()
                finally:
                    self.db.disconnect()
                promo_block = ""
                if promotions:
                    promo_lines = [f"- {p['code']}: giảm {p['discount_amount']}%, tối thiểu {p['min_order_amount']:,.0f}đ"
                                   for p in promotions[:5]]
                    promo_block = "Khuyến mãi đang áp dụng:\n" + "\n".join(promo_lines)

                price_text = ""
                if extracted_info['price_range']:
                    mn, mx = extracted_info['price_range']
                    price_text = f"Khoảng giá quan tâm: {mn:,.0f}đ - {mx:,.0f}đ."

                purpose_text = ""
                if extracted_info['keywords']:
                    purpose_text = "Nhu cầu: " + ", ".join(extracted_info['keywords']) + "."

                system_prompt = (
                    "Bạn là chuyên viên tư vấn laptop. Trả lời ngắn gọn, súc tích, thực dụng, "
                    "ưu tiên đề xuất cụ thể từ danh sách sản phẩm cung cấp, kèm gợi ý vì sao phù hợp. "
                    "Nếu dữ liệu ít, hỏi thêm thông tin cần thiết."
                )
                user_prompt = (
                    f"Yêu cầu của khách: {message}\n"
                    f"{price_text}\n{purpose_text}\n\n"
                    f"Danh sách sản phẩm liên quan:\n{product_block}\n\n"
                    f"{promo_block}\n\n"
                    "Hãy trả lời bằng tiếng Việt, có bullet rõ ràng, tối đa ~8 dòng."
                )
                gemini_resp = self.model.generate_content([system_prompt, user_prompt])
                if hasattr(gemini_resp, "text") and gemini_resp.text:
                    response = gemini_resp.text.strip()
            except Exception as _:
                # Giữ nguyên response fallback nếu model lỗi
                pass

            if session_id:
                self.save_context(session_id)
            return response, context
                
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            if session_id:
                self.save_context(session_id)
            return self.formatter.format_error_with_suggestions("general"), context

    def _get_spec_info(self, product: Dict, spec_type: str) -> str:
        """Lấy thông tin chi tiết về một thông số kỹ thuật cụ thể"""
        description = product.get('description', '').lower()
        
        if spec_type == 'upgrade':
            return f"""Dạ, về khả năng nâng cấp của laptop {product['name']}:

✅ Khả năng nâng cấp RAM:
• Số khe RAM: 2 khe (1 khe đã gắn sẵn)
• RAM tối đa hỗ trợ: 32GB
• Loại RAM tương thích: DDR4
• Chi phí nâng cấp RAM 8GB: 700,000đ - 900,000đ
• Chi phí nâng cấp RAM 16GB: 1,400,000đ - 1,800,000đ

✅ Khả năng nâng cấp ổ cứng:
• Khe M.2 NVMe: Có thể thêm SSD M.2
• Khe 2.5 inch: Có thể thêm SSD/HDD SATA
• Chi phí nâng cấp SSD 256GB: 800,000đ - 1,200,000đ
• Chi phí nâng cấp SSD 512GB: 1,500,000đ - 2,000,000đ

💡 Lưu ý khi nâng cấp:
• Nên nhờ kỹ thuật viên có kinh nghiệm thực hiện
• Kiểm tra kỹ thông số RAM để đảm bảo tương thích
• Nên backup dữ liệu trước khi nâng cấp ổ cứng

Anh/chị cần tư vấn thêm gì về việc nâng cấp không ạ?"""
            
        elif spec_type == 'pin':
            # Tìm thông tin về pin trong description
            pin_info = next((s.strip() for s in description.split(',') 
                           if any(x in s.lower() for x in ['pin', 'battery', 'giờ sử dụng'])), '')
            if pin_info:
                return f"""Dạ, về pin của laptop {product['name']}, {pin_info}.

Thông thường với cấu hình này (Intel i3, 8GB RAM), thời lượng pin có thể đạt:
• Sử dụng văn phòng, web: 4-6 giờ
• Xem video, giải trí: 3-5 giờ
• Sử dụng nặng: 2-3 giờ

Để tối ưu thời lượng pin, anh/chị có thể:
• Điều chỉnh độ sáng màn hình
• Tắt các ứng dụng không cần thiết
• Sử dụng chế độ tiết kiệm pin"""
            
        elif spec_type == 'screen':
            # Tìm thông tin về màn hình
            screen_info = next((s.strip() for s in description.split(',')
                              if any(x in s.lower() for x in ['inch', 'fhd', 'hd', 'màn hình', 'display'])), '')
            if screen_info:
                return f"""Dạ, về màn hình của laptop {product['name']}, {screen_info}.

Đây là màn hình phù hợp cho:
• Làm việc văn phòng, đọc tài liệu
• Xem phim, giải trí cơ bản
• Học tập trực tuyến

✨ Ưu điểm:
• Kích thước 15.6 inch phổ biến, dễ sử dụng
• Độ phân giải đủ dùng cho công việc thông thường

💡 Lưu ý: Nếu anh/chị cần màn hình chất lượng cao hơn cho đồ họa hoặc gaming, em có thể tư vấn các model khác phù hợp hơn."""
            
        elif spec_type == 'performance':
            return f"""Dạ, về hiệu năng của laptop {product['name']}:

💻 Cấu hình máy:
• CPU Intel i3 thế hệ mới, xử lý tốt các tác vụ cơ bản
• RAM 8GB đủ dùng cho đa nhiệm nhẹ
• SSD 256GB giúp khởi động và mở ứng dụng nhanh

✅ Phù hợp cho:
• Học tập, làm việc văn phòng
• Lướt web, xem phim, giải trí
• Chạy các ứng dụng văn phòng cơ bản

⚠️ Hạn chế:
• Không phù hợp chơi game nặng
• Khó khăn khi chạy phần mềm đồ họa
• Đa nhiệm nhiều có thể bị chậm

💡 Nếu anh/chị cần máy mạnh hơn, em có thể tư vấn các model cao cấp hơn."""
            
        return self.formatter.format_general_laptop_request()

def create_chatbot_chain(customer_id: Optional[int] = None) -> Dict[str, Any]:
    """Tạo và trả về chatbot chain với các components"""
    try:
        # Lấy config từ biến môi trường
        db_config = {
            "host": os.getenv("DB_HOST", "localhost"),
            "user": os.getenv("DB_USER", "root"),
            "password": os.getenv("DB_PASSWORD", ""),
            "database": os.getenv("DB_NAME", "chatbot_db")
        }
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            raise ValueError("GEMINI_API_KEY không được cấu hình trong biến môi trường")

        # Khởi tạo chatbot
        chatbot = ChatbotChain(db_config, api_key)
        
        return {
            "chain": chatbot,
            "customer_id": customer_id
        }
        
    except Exception as e:
        print(f"Lỗi khởi tạo chatbot: {str(e)}")
        raise