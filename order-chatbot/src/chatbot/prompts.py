from typing import Dict, List
from langchain.prompts import PromptTemplate

# Main conversation template with enhanced context and personality
DEFAULT_TEMPLATE = """Bạn là một chuyên gia tư vấn bán hàng laptop chuyên nghiệp, nhiệt tình và thân thiện.
Hãy trò chuyện với khách hàng như một người bạn, thấu hiểu nhu cầu và đưa ra lời khuyên phù hợp.

THÔNG TIN SẢN PHẨM LIÊN QUAN:
{product_info}

LỊCH SỬ CHAT:
{chat_history}

YÊU CẦU HIỆN TẠI:
{input}

HƯỚNG DẪN TRẢ LỜI:
1. Nếu có thông tin sản phẩm liên quan, hãy tập trung vào những sản phẩm đó
2. Nếu không có thông tin cụ thể, hãy hỏi thêm về nhu cầu của khách hàng
3. Luôn đưa ra lời khuyên chân thành và chuyên nghiệp
4. Trả lời ngắn gọn, súc tích nhưng đầy đủ thông tin

Trả lời:"""

# Enhanced product template with more detailed information
PRODUCT_TEMPLATE = """
TÊN SẢN PHẨM: {name}
THƯƠNG HIỆU: {brand}
GIÁ: {price:,.0f} VND
DANH MỤC: {category}
CẤU HÌNH:
- CPU: {cpu}
- RAM: {ram}
- Ổ cứng: {storage}
- Card đồ họa: {gpu}
- Màn hình: {screen}
MÔ TẢ: {description}
TÌNH TRẠNG: {"Còn hàng" if stock > 0 else "Hết hàng"}
"""

# Enhanced FAQ template with better organization
FAQ_TEMPLATE = """
CÂU HỎI: {question}
TRẢ LỜI: {answer}
DANH MỤC: {category}
"""

# New template for order processing
ORDER_TEMPLATE = """Thông tin đơn hàng:
🛒 Sản phẩm: {product_name}
💰 Giá: {price}đ
📦 Số lượng: {quantity}
🏷️ Tổng tiền: {total_price}đ

👤 Thông tin khách hàng:
- Tên: {customer_name}
- SĐT: {phone}
- Địa chỉ: {address}

📋 Xác nhận đơn hàng:
{order_confirmation}

Bạn có muốn xác nhận đặt hàng không?"""

# New template for customer support
SUPPORT_TEMPLATE = """Yêu cầu hỗ trợ:
📝 Vấn đề: {issue}
🔍 Mức độ ưu tiên: {priority}

Các bước xử lý:
{resolution_steps}

Bạn cần hỗ trợ thêm gì không?"""

# Initialize prompt templates
default_prompt = PromptTemplate(
    input_variables=["context", "chat_history", "input"],
    template=DEFAULT_TEMPLATE
)

product_prompt = PromptTemplate(
    input_variables=[
        "product_name", "price", "stock", "category", 
        "description", "promotions", "features", 
        "warranty_shipping"
    ],
    template=PRODUCT_TEMPLATE
)

faq_prompt = PromptTemplate(
    input_variables=["category", "faq_list", "question"],
    template=FAQ_TEMPLATE
)

order_prompt = PromptTemplate(
    input_variables=[
        "product_name", "price", "quantity", "total_price",
        "customer_name", "phone", "address", "order_confirmation"
    ],
    template=ORDER_TEMPLATE
)

support_prompt = PromptTemplate(
    input_variables=["issue", "priority", "resolution_steps"],
    template=SUPPORT_TEMPLATE
)

def format_product_info(product: dict) -> str:
    """Format product information using the template"""
    return PRODUCT_TEMPLATE.format(**product)

def format_faq_answer(faq: dict) -> str:
    """Format FAQ answer using the template"""
    return FAQ_TEMPLATE.format(**faq)

def format_price_range(min_price: float, max_price: float) -> str:
    """Format price range in Vietnamese currency"""
    if min_price == 0:
        return f"dưới {max_price:,.0f} VND"
    elif max_price == float('inf'):
        return f"trên {min_price:,.0f} VND"
    else:
        return f"từ {min_price:,.0f} VND đến {max_price:,.0f} VND" 