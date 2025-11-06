from typing import List, Dict, Optional
from decimal import Decimal

class ResponseFormatter:
    @staticmethod
    def format_price(price: Decimal) -> str:
        """Format giá tiền sang dạng VND"""
        return f"{price:,.0f}đ"

    @staticmethod
    def format_product_info(product: Dict) -> str:
        """Format thông tin sản phẩm"""
        return f"""
• {product['name']}
  - Giá: {ResponseFormatter.format_price(product['price'])}
  - Danh mục: {product['category_name']}
  - Mô tả: {product['description']}
"""

    @staticmethod
    def format_product_list(products: List[Dict], show_category: bool = True) -> str:
        """Format danh sách sản phẩm"""
        if not products:
            return "Không tìm thấy sản phẩm phù hợp."
            
        result = ["💻 Các laptop phù hợp trong tầm giá:"]
        for i, product in enumerate(products, 1):
            specs = []
            description = product['description'].lower()
            
            # Extract CPU info
            if 'cpu' in description or 'intel' in description or 'ryzen' in description:
                cpu_info = next((s.strip() for s in description.split(',') 
                               if any(x in s.lower() for x in ['cpu', 'intel', 'ryzen', 'core', 'amd'])), '')
                if cpu_info:
                    # Capitalize CPU brands and models
                    cpu_info = cpu_info.replace('intel', 'Intel').replace('ryzen', 'Ryzen').replace('amd', 'AMD')
                    specs.append(cpu_info)
            
            # Extract RAM
            if 'ram' in description:
                ram_info = next((s.strip() for s in description.split(',') if 'ram' in s.lower()), '')
                if ram_info:
                    # Capitalize RAM
                    ram_info = ram_info.replace('ram', 'RAM').replace('gb', 'GB')
                    specs.append(ram_info)
            
            # Extract Storage
            if 'ssd' in description or 'hdd' in description:
                storage_info = next((s.strip() for s in description.split(',') 
                                   if 'ssd' in s.lower() or 'hdd' in s.lower()), '')
                if storage_info:
                    # Capitalize storage types
                    storage_info = storage_info.replace('ssd', 'SSD').replace('hdd', 'HDD').replace('gb', 'GB')
                    specs.append(storage_info)
            
            # Extract GPU if gaming laptop
            if 'gaming' in product.get('category_name', '').lower():
                gpu_info = next((s.strip() for s in description.split(',')
                               if any(x in s.lower() for x in ['gtx', 'rtx', 'graphics', 'gpu'])), '')
                if gpu_info:
                    # Capitalize GPU models
                    gpu_info = gpu_info.upper().replace('GTX', 'NVIDIA GTX').replace('RTX', 'NVIDIA RTX')
                    specs.append(gpu_info)
                
            # Capitalize product name and brand
            name_parts = product['name'].split()
            brand_models = {
                'asus': 'ASUS',
                'msi': 'MSI',
                'hp': 'HP',
                'dell': 'DELL',
                'lenovo': 'Lenovo',
                'acer': 'Acer',
                'vivobook': 'VivoBook',
                'zenbook': 'ZenBook',
                'thinkpad': 'ThinkPad',
                'ideapad': 'IdeaPad',
                'pavilion': 'Pavilion',
                'victus': 'Victus',
                'omen': 'OMEN',
                'tuf': 'TUF',
                'rog': 'ROG',
                'gf63': 'GF63',
                'gf65': 'GF65',
                'gs66': 'GS66',
                'gl65': 'GL65',
                'nitro': 'Nitro',
                'predator': 'Predator',
                'swift': 'Swift',
                'aspire': 'Aspire'
            }
            
            capitalized_name = []
            for word in name_parts:
                word_lower = word.lower()
                if word_lower in brand_models:
                    capitalized_name.append(brand_models[word_lower])
                else:
                    # Capitalize other words normally
                    capitalized_name.append(word.upper() if len(word) <= 3 else word.title())
            
            product_info = [
                f"{i}. {' '.join(capitalized_name)}",
                f"💰 Giá: {ResponseFormatter.format_price(product['price'])}",
            ]
            
            if show_category and product.get('category_name'):
                product_info.append(f"📑 Loại: {product['category_name']}")
                
            if specs:
                product_info.append(f"🔧 Cấu hình: {' | '.join(filter(None, specs))}")
                
            result.append('\n'.join(product_info))
            
        return '\n\n'.join(result)

    @staticmethod
    def format_promotion_info(promotion: Dict) -> str:
        """Format thông tin khuyến mãi"""
        return f"""
• Mã khuyến mãi: {promotion['code']}
  - Giảm giá: {promotion['discount_amount']}%
  - Đơn hàng tối thiểu: {ResponseFormatter.format_price(promotion['min_order_amount'])}
  - Hiệu lực đến: {promotion['end_date'].strftime('%d/%m/%Y')}
"""

    @staticmethod
    def format_promotions_list(promotions: List[Dict]) -> str:
        """Format danh sách khuyến mãi"""
        if not promotions:
            return "Hiện không có khuyến mãi nào đang áp dụng."
        
        result = "Các khuyến mãi đang áp dụng:\n"
        for promo in promotions:
            result += ResponseFormatter.format_promotion_info(promo)
        return result

    @staticmethod
    def format_faq_answer(faq: Dict) -> str:
        """Format câu trả lời FAQ"""
        return f"""
Câu hỏi: {faq['question']}
Trả lời: {faq['answer']}
"""

    @staticmethod
    def format_error_message(error: str) -> str:
        """Format thông báo lỗi"""
        return f"⚠️ Có lỗi xảy ra: {error}"

    @staticmethod
    def format_greeting(customer_name: Optional[str] = None) -> str:
        """Format lời chào"""
        if customer_name:
            return f"""Xin chào {customer_name}! 👋

Tôi là trợ lý tư vấn laptop thông minh. Tôi có thể giúp bạn:
• Tư vấn chọn laptop phù hợp với nhu cầu
• Tìm kiếm laptop theo khoảng giá mong muốn
• Giải đáp thắc mắc về sản phẩm và dịch vụ
• Cập nhật thông tin khuyến mãi mới nhất

Bạn cần tư vấn về vấn đề gì ạ?"""
        
        return """Xin chào bạn! 👋

Tôi là trợ lý tư vấn laptop thông minh. Tôi có thể giúp bạn:
• Tư vấn chọn laptop phù hợp với nhu cầu
• Tìm kiếm laptop theo khoảng giá mong muốn
• Giải đáp thắc mắc về sản phẩm và dịch vụ
• Cập nhật thông tin khuyến mãi mới nhất

Bạn cần tư vấn về vấn đề gì ạ?"""

    @staticmethod
    def format_no_result() -> str:
        """Format thông báo không có kết quả"""
        return "Xin lỗi, tôi không tìm thấy thông tin phù hợp với yêu cầu của bạn."

    @staticmethod
    def format_suggestion() -> str:
        """Format gợi ý cho người dùng"""
        return """
Bạn có thể thử:
• Nói rõ nhu cầu sử dụng laptop (học tập, gaming, đồ họa...)
• Cho biết khoảng giá mong muốn
• Hỏi về tính năng cụ thể (pin, màn hình, CPU...)
• Xem các khuyến mãi đang có
""" 

    @staticmethod
    def format_price_range_response(products: List[Dict], min_price: int, max_price: int) -> str:
        """Format câu trả lời hoàn chỉnh cho tìm kiếm theo khoảng giá"""
        # Format opening message
        opening = f"Dạ, trong khoảng giá {ResponseFormatter.format_price(min_price)} - {ResponseFormatter.format_price(max_price)}, em có một số laptop phù hợp như bên dưới."
        
        # Get product list
        product_list = ResponseFormatter.format_product_list(products)
        
        # Format closing message with detailed suggestions
        closing = """
Để tư vấn chi tiết hơn, anh/chị cho em biết thêm mục đích sử dụng laptop ạ:

📚 Học tập, văn phòng:
• Xử lý văn bản, Excel, PowerPoint
• Học online, lập trình cơ bản
• Thời lượng pin cao, gọn nhẹ

🎮 Chơi game:
• Game online, offline nhẹ
• Game nặng (AAA titles)
• Stream, quay video gaming

🎨 Đồ họa, sáng tạo:
• Chỉnh sửa ảnh, video
• Thiết kế đồ họa 2D/3D
• Render, làm phim

💼 Doanh nghiệp:
• Bảo mật cao
• Độ bền, độ ổn định
• Kết nối doanh nghiệp

Anh/chị cho em biết nhu cầu chính để em tư vấn phù hợp nhất ạ."""
        
        # Combine all parts
        return f"{opening}\n\n{product_list}\n{closing}" 

    @staticmethod
    def format_purpose_response(products: List[Dict], purposes: List[str]) -> str:
        """Format câu trả lời dựa trên mục đích sử dụng"""
        if not products:
            return "Xin lỗi, hiện tại không có sản phẩm nào phù hợp với nhu cầu của bạn."
            
        # Format opening message based on purposes
        purpose_str = " và ".join(purposes)
        
        # Tạo gợi ý cấu hình dựa trên mục đích sử dụng
        config_suggestions = []
        if 'đồ họa' in purposes:
            config_suggestions.extend([
                "• CPU: Intel Core i7/i9 hoặc AMD Ryzen 7/9 để xử lý tốt các tác vụ đồ họa",
                "• RAM: Tối thiểu 16GB để đa nhiệm tốt",
                "• Card đồ họa: NVIDIA GTX/RTX để render nhanh",
                "• Màn hình: Độ phủ màu tốt (100% sRGB) cho thiết kế"
            ])
        if 'game' in purposes or 'gaming' in purposes:
            config_suggestions.extend([
                "• Card đồ họa rời NVIDIA GTX/RTX cho gaming mượt mà",
                "• Tản nhiệt tốt để chơi game thời gian dài",
                "• Màn hình tần số quét cao (144Hz) cho gaming"
            ])
            
        # Loại bỏ các gợi ý trùng lặp
        config_suggestions = list(dict.fromkeys(config_suggestions))
        
        opening = f"""Dạ, với nhu cầu {purpose_str}, em xin tư vấn một số laptop phù hợp. 

💻 Cấu hình đề xuất:
{chr(10).join(config_suggestions)}

🔍 Dưới đây là các laptop phù hợp với nhu cầu của anh/chị:"""
        
        # Filter and sort products based on purposes
        filtered_products = []
        for product in products:
            score = 0
            desc_lower = product['description'].lower()
            category_lower = product.get('category_name', '').lower()
            
            # Score for gaming laptops
            if 'game' in purposes or 'gaming' in purposes:
                if 'gaming' in category_lower:
                    score += 3
                if any(gpu in desc_lower for gpu in ['gtx', 'rtx', 'graphics']):
                    score += 2
                    
            # Score for graphics/design laptops
            if 'đồ họa' in purposes or 'thiết kế' in purposes:
                if 'đồ họa' in category_lower:
                    score += 3
                if any(gpu in desc_lower for gpu in ['gtx', 'rtx', 'graphics']):
                    score += 2
                if any(cpu in desc_lower for cpu in ['i7', 'ryzen 7', 'i9', 'ryzen 9']):
                    score += 1
                    
            if score > 0:
                filtered_products.append((product, score))
                
        # Sort by score and price
        filtered_products.sort(key=lambda x: (-x[1], x[0]['price']))
        sorted_products = [p[0] for p in filtered_products]
        
        # Get product list
        product_list = ResponseFormatter.format_product_list(sorted_products)
        
        # Format closing message with specific suggestions
        closing = """
💡 Để tư vấn chi tiết hơn, anh/chị cho em biết thêm:
• Các phần mềm đồ họa sẽ sử dụng (Photoshop, Premiere, AutoCAD...)
• Các game thường chơi (online/offline, tên game cụ thể)
• Yêu cầu về màn hình (độ phân giải, tần số quét, độ phủ màu)
• Nhu cầu di chuyển và thời lượng pin mong muốn

Em sẽ gợi ý các model phù hợp nhất với nhu cầu của anh/chị."""
        
        # Combine all parts
        return f"{opening}\n\n{product_list}\n{closing}" 

    @staticmethod
    def format_error_with_suggestions(error_type: str = "extract_info") -> str:
        """Format thông báo lỗi với gợi ý phù hợp"""
        error_messages = {
            "extract_info": "Xin lỗi, em chưa hiểu rõ yêu cầu của anh/chị.",
            "no_products": "Xin lỗi, hiện tại không có sản phẩm nào phù hợp với yêu cầu.",
            "invalid_price": "Xin lỗi, khoảng giá không hợp lệ.",
            "general": "Xin lỗi, có lỗi xảy ra khi xử lý yêu cầu."
        }
        
        suggestions = {
            "extract_info": """
Để em có thể tư vấn tốt hơn, anh/chị vui lòng cho em biết:
• Mục đích sử dụng laptop (học tập, gaming, đồ họa...)
• Khoảng giá mong muốn
• Các tính năng quan trọng (pin, màn hình, CPU...)
• Thương hiệu ưa thích (nếu có)""",
            "no_products": """
Anh/chị có thể thử:
• Điều chỉnh khoảng giá
• Thay đổi yêu cầu về cấu hình
• Xem các sản phẩm tương tự
• Để lại thông tin để được tư vấn khi có hàng""",
            "invalid_price": """
Anh/chị vui lòng:
• Nhập khoảng giá hợp lệ (ví dụ: 15-20 triệu)
• Sử dụng đơn vị tiền tệ (triệu, tr)
• Không sử dụng ký tự đặc biệt""",
            "general": """
Anh/chị có thể:
• Thử lại sau ít phút
• Làm mới trang
• Liên hệ hỗ trợ nếu vẫn gặp lỗi"""
        }
        
        error_msg = error_messages.get(error_type, error_messages["general"])
        suggestion = suggestions.get(error_type, suggestions["general"])
        
        return f"{error_msg}\n{suggestion}" 

    @staticmethod
    def format_purpose_without_price(purposes: List[str]) -> str:
        """Format câu trả lời khi có nhu cầu nhưng chưa có thông tin về giá"""
        # Format opening message based on purposes
        purpose_str = " và ".join(purposes)
        
        # Tạo gợi ý cấu hình dựa trên mục đích sử dụng
        config_suggestions = []
        
        # Xử lý riêng cho lập trình
        if 'lập trình' in purposes:
            message = f"""Dạ, với nhu cầu lập trình, em xin tư vấn sơ bộ về cấu hình phù hợp:

💻 Cấu hình đề xuất cho lập trình:
• CPU: Intel Core i5/i7 hoặc AMD Ryzen 5/7 thế hệ mới
• RAM: Tối thiểu 16GB để chạy các IDE và nhiều ứng dụng
• SSD: 512GB trở lên cho tốc độ đọc/ghi nhanh
• Màn hình: Full HD, tấm nền IPS, kích thước 14-15.6 inch
• Pin: Tối thiểu 6-8 tiếng để làm việc liên tục

💰 Về mức giá, laptop cho lập trình thường có các phân khúc:
• Phổ thông (15-20 triệu): Đủ dùng cho sinh viên, lập trình cơ bản
• Tầm trung (20-30 triệu): Phù hợp cho developer chuyên nghiệp
• Cao cấp (Trên 30 triệu): Cho các dự án nặng, đa nhiệm cao

🔍 Để tư vấn chi tiết hơn, anh/chị vui lòng cho em biết thêm:
• Ngôn ngữ lập trình và công nghệ sử dụng
• Có cần chạy máy ảo hay docker không
• Nhu cầu di chuyển và thời lượng pin mong muốn
• Khoảng giá dự kiến của anh/chị

Em sẽ gợi ý các model phù hợp nhất với nhu cầu của anh/chị."""
            return message
        
        # Xử lý các nhu cầu khác
        if 'đồ họa' in purposes:
            config_suggestions.extend([
                "• CPU: Intel Core i7/i9 hoặc AMD Ryzen 7/9 để xử lý tốt các tác vụ đồ họa",
                "• RAM: Tối thiểu 16GB để đa nhiệm tốt",
                "• Card đồ họa: NVIDIA GTX/RTX để render nhanh",
                "• Màn hình: Độ phủ màu tốt (100% sRGB) cho thiết kế"
            ])
        if 'gaming' in purposes:
            config_suggestions.extend([
                "• Card đồ họa rời NVIDIA GTX/RTX cho gaming mượt mà",
                "• Tản nhiệt tốt để chơi game thời gian dài",
                "• Màn hình tần số quét cao (144Hz) cho gaming"
            ])
        if 'văn phòng' in purposes:
            config_suggestions.extend([
                "• CPU: Intel Core i3/i5 hoặc AMD Ryzen 3/5",
                "• RAM: 8GB trở lên để đa nhiệm tốt",
                "• Màn hình: Full HD, tấm nền IPS",
                "• Pin: Tối thiểu 6 tiếng làm việc"
            ])
            
        # Loại bỏ các gợi ý trùng lặp
        config_suggestions = list(dict.fromkeys(config_suggestions))
        
        # Format message
        message = f"""Dạ, với nhu cầu {purpose_str}, em xin tư vấn sơ bộ về cấu hình phù hợp:

💻 Cấu hình đề xuất:
{chr(10).join(config_suggestions)}

💰 Về mức giá, thông thường laptop phù hợp với nhu cầu này sẽ có các phân khúc:
• Phân khúc phổ thông: 15-20 triệu
• Phân khúc tầm trung: 20-30 triệu
• Phân khúc cao cấp: Trên 30 triệu

Anh/chị cho em biết khoảng giá mong muốn để em tư vấn các model cụ thể ạ."""
        
        return message 

    @staticmethod
    def format_purpose_with_price_and_details(products: List[Dict], purposes: List[str], min_price: int, max_price: int) -> str:
        """Format câu trả lời khi có cả thông tin về giá và nhu cầu"""
        try:
            # Format opening message
            purpose_str = " và ".join(purposes)
            opening = f"""Dạ, trong khoảng giá {ResponseFormatter.format_price(min_price)} - {ResponseFormatter.format_price(max_price)}, em có một số laptop phù hợp cho nhu cầu {purpose_str} của anh/chị."""
            
            # Filter and sort products
            filtered_products = []
            for product in products:
                if min_price <= product['price'] <= max_price:
                    score = 0
                    desc_lower = product['description'].lower()
                    category_lower = product.get('category_name', '').lower()
                    
                    # Score for gaming laptops
                    if 'game' in purposes or 'gaming' in purposes:
                        if 'gaming' in category_lower:
                            score += 3
                        if any(gpu in desc_lower for gpu in ['gtx', 'rtx', 'graphics']):
                            score += 2
                            
                    # Score for graphics/design laptops
                    if 'đồ họa' in purposes or 'thiết kế' in purposes:
                        if 'đồ họa' in category_lower:
                            score += 3
                        if any(gpu in desc_lower for gpu in ['gtx', 'rtx', 'graphics']):
                            score += 2
                        if any(cpu in desc_lower for cpu in ['i7', 'ryzen 7', 'i9', 'ryzen 9']):
                            score += 1
                            
                    if score > 0:
                        filtered_products.append((product, score))
            
            # Sort by score and price
            filtered_products.sort(key=lambda x: (-x[1], x[0]['price']))
            sorted_products = [p[0] for p in filtered_products]
            
            # Get product list
            if not sorted_products:
                return ResponseFormatter.format_error_with_suggestions("no_products")
                
            product_list = ResponseFormatter.format_product_list(sorted_products)
            
            # Format closing message with specific suggestions
            if 'đồ họa' in purposes:
                closing = """
💡 Để tư vấn chi tiết hơn, anh/chị cho em biết thêm:
• Các phần mềm đồ họa sẽ sử dụng (Photoshop, Illustrator, Premiere...)
• Yêu cầu về màn hình (độ phân giải, độ phủ màu)
• Nhu cầu di chuyển và thời lượng pin mong muốn"""
            elif 'game' in purposes or 'gaming' in purposes:
                closing = """
💡 Để tư vấn chi tiết hơn, anh/chị cho em biết thêm:
• Các game thường chơi (online/offline, tên game cụ thể)
• Yêu cầu về màn hình (độ phân giải, tần số quét)
• Thời gian chơi game liên tục"""
            else:
                closing = """
💡 Để tư vấn chi tiết hơn, anh/chị cho em biết thêm:
• Các tác vụ thường xuyên sử dụng
• Yêu cầu về màn hình và thời lượng pin
• Nhu cầu di chuyển thường xuyên không"""
            
            # Combine all parts
            return f"{opening}\n\n{product_list}\n{closing}"
            
        except Exception as e:
            print(f"Error in format_purpose_with_price_and_details: {str(e)}")
            return ResponseFormatter.format_error_with_suggestions("general") 

    @staticmethod
    def format_general_laptop_request() -> str:
        """Format câu trả lời cho yêu cầu chung về laptop"""
        return """Dạ, để tư vấn laptop phù hợp nhất, anh/chị vui lòng cho em biết:

💻 Mục đích sử dụng: học tập/gaming/đồ họa/lập trình
💰 Khoảng giá mong muốn
🎯 Yêu cầu đặc biệt (nếu có)

Em sẽ gợi ý ngay các sản phẩm phù hợp ạ!"""

    @staticmethod
    def format_specific_model_info(product: Dict) -> str:
        """Format thông tin chi tiết về một model laptop cụ thể"""
        # Extract thông tin từ description
        specs = []
        description = product.get('description', '').lower()
        
        # Extract CPU info
        if 'cpu' in description or 'intel' in description or 'ryzen' in description:
            cpu_info = next((s.strip() for s in description.split(',') 
                            if any(x in s.lower() for x in ['cpu', 'intel', 'ryzen', 'core', 'amd'])), '')
            if cpu_info:
                # Capitalize CPU brands and models
                cpu_info = (cpu_info.replace('intel', 'Intel')
                          .replace('ryzen', 'Ryzen')
                          .replace('amd', 'AMD')
                          .replace('core', 'Core'))
                specs.append(f"• CPU: {cpu_info}")
        
        # Extract RAM
        if 'ram' in description:
            ram_info = next((s.strip() for s in description.split(',') if 'ram' in s.lower()), '')
            if ram_info:
                # Capitalize RAM
                ram_info = ram_info.replace('ram', 'RAM').replace('gb', 'GB')
                specs.append(f"• RAM: {ram_info}")
        
        # Extract Storage
        if 'ssd' in description or 'hdd' in description:
            storage_info = next((s.strip() for s in description.split(',') 
                               if 'ssd' in s.lower() or 'hdd' in s.lower()), '')
            if storage_info:
                # Capitalize storage types
                storage_info = storage_info.replace('ssd', 'SSD').replace('hdd', 'HDD').replace('gb', 'GB')
                specs.append(f"• Ổ cứng: {storage_info}")
        
        # Extract GPU
        gpu_info = next((s.strip() for s in description.split(',')
                        if any(x in s.lower() for x in ['gtx', 'rtx', 'graphics', 'gpu', 'vga', 'intel uhd'])), '')
        if gpu_info:
            # Capitalize GPU models
            gpu_info = (gpu_info.upper()
                       .replace('GTX', 'NVIDIA GTX')
                       .replace('RTX', 'NVIDIA RTX')
                       .replace('GRAPHICS', 'Graphics')
                       .replace('VGA', 'Card đồ họa')
                       .replace('INTEL UHD', 'Intel UHD'))
            specs.append(f"• Card đồ họa: {gpu_info}")
        
        # Extract Screen info
        screen_info = next((s.strip() for s in description.split(',')
                          if any(x in s.lower() for x in ['inch', 'fhd', 'uhd', 'oled', 'ips', 'màn hình'])), '')
        if screen_info:
            screen_info = (screen_info.replace('fhd', 'FHD')
                         .replace('uhd', 'UHD')
                         .replace('oled', 'OLED')
                         .replace('ips', 'IPS'))
            specs.append(f"• Màn hình: {screen_info}")
        
        # Extract OS info
        os_info = next((s.strip() for s in description.split(',')
                       if any(x in s.lower() for x in ['windows', 'win', 'linux', 'ubuntu'])), '')
        if os_info:
            os_info = os_info.replace('win', 'Windows')
            specs.append(f"• Hệ điều hành: {os_info}")
        
        # Extract Weight info
        weight_info = next((s.strip() for s in description.split(',')
                          if any(x in s.lower() for x in ['kg', 'nặng', 'trọng lượng'])), '')
        if weight_info:
            specs.append(f"• Trọng lượng: {weight_info}")
        
        # Format response
        response = f"""Dạ, em xin gửi thông tin chi tiết về laptop {product['name']}:

💻 Thông số kỹ thuật:
{chr(10).join(specs)}

💰 Giá bán: {ResponseFormatter.format_price(product['price'])}
📑 Danh mục: {product.get('category_name', 'Laptop')}

✨ Điểm nổi bật:
• Thiết kế gọn nhẹ, phù hợp di chuyển
• Màn hình Full HD sắc nét
• Bàn phím êm ái, thoải mái khi gõ
• Tản nhiệt hiệu quả, ít nóng máy
• Pin đủ dùng cho công việc văn phòng

👍 Phù hợp cho:
• Học tập, làm việc văn phòng cơ bản
• Lướt web, xem phim, giải trí
• Sử dụng các ứng dụng văn phòng

🔍 Để tư vấn chi tiết hơn, anh/chị vui lòng cho em biết:
• Mục đích sử dụng chính của anh/chị
• Các tính năng quan trọng cần có
• Khoảng giá mong muốn

Em sẽ tư vấn thêm các model phù hợp với nhu cầu của anh/chị."""

        return response

    @staticmethod
    def format_model_not_found(keywords: List[str], full_model_name: Optional[str] = None) -> str:
        """Format thông báo khi không tìm thấy model laptop"""
        brand = next((kw for kw in keywords if kw != "specific_model"), None)
        model = next((kw for kw in keywords if kw not in ["specific_model", brand]), None)
        
        if brand and (model or full_model_name):
            # Sử dụng tên model đầy đủ nếu có
            model_name = full_model_name if full_model_name else model
            # Clean up model name - remove regex patterns
            clean_model = model_name.replace(r'\s*', ' ').strip()
            display_name = f"{brand.upper()} {clean_model.upper()}"
            
            return f"""Dạ, hiện tại em chưa tìm thấy thông tin về model {display_name} trong hệ thống.

Để em có thể tư vấn chính xác hơn, anh/chị vui lòng cho em biết:
• Mục đích sử dụng laptop
• Khoảng giá mong muốn
• Các tính năng quan trọng cần có

Em sẽ gợi ý các model phù hợp với nhu cầu của anh/chị."""
        else:
            return ResponseFormatter.format_general_laptop_request() 