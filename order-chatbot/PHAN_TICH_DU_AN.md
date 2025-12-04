# PHÂN TÍCH CHI TIẾT DỰ ÁN ORDER CHATBOT

## 📋 TỔNG QUAN DỰ ÁN

**Order Chatbot** là một hệ thống chatbot thông minh được xây dựng để tư vấn và hỗ trợ đặt hàng laptop. Dự án sử dụng Google Gemini Pro (AI model) kết hợp với FastAPI backend và giao diện web PHP.

### Mục đích chính:
- Tư vấn sản phẩm laptop thông minh dựa trên nhu cầu và ngân sách
- Tự động nhận diện khoảng giá từ tin nhắn người dùng
- Hỗ trợ đặt hàng và quản lý giỏ hàng
- Tích hợp thông tin khuyến mãi
- Lưu trữ lịch sử chat
- Xử lý câu hỏi thường gặp tự động

---

## 🏗️ KIẾN TRÚC HỆ THỐNG

### 1. Kiến trúc tổng thể

```
┌─────────────────┐
│   Frontend      │  PHP Web Interface
│   (web/)        │  - index.php
│                 │  - JavaScript (main.js)
│                 │  - CSS (style.css)
└────────┬────────┘
         │ HTTP/REST API
         ▼
┌─────────────────┐
│   Backend API   │  FastAPI (src/api/routes.py)
│   (src/api/)    │  - POST /chat
│                 │  - GET /
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Chatbot Core   │  ChatbotChain (src/chatbot/chain.py)
│  (src/chatbot/) │  - Xử lý tin nhắn
│                 │  - Trích xuất thông tin
│                 │  - Tạo phản hồi
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌──────────────┐
│ Gemini │ │  Database    │
│   Pro  │ │  (MySQL)     │
└────────┘ └──────────────┘
```

### 2. Cấu trúc thư mục chi tiết

```
order-chatbot/
├── config/                 # Cấu hình hệ thống
│   ├── database.py        # Kết nối database cũ
│   └── google_cloud.py    # Cấu hình Google Cloud
│
├── database/              # Scripts và dữ liệu database
│   ├── schema.sql         # Schema database chính
│   ├── sample_data.sql    # Dữ liệu mẫu
│   ├── scraper_tgdd.py    # Scraper dữ liệu từ TGDD
│   └── statistics.py      # Thống kê dữ liệu
│
├── src/                   # Source code Python
│   ├── main.py           # Entry point ứng dụng
│   │
│   ├── api/              # API Layer
│   │   └── routes.py     # FastAPI routes
│   │
│   ├── chatbot/          # Chatbot Core
│   │   ├── chain.py      # ChatbotChain - Logic chính
│   │   ├── database_utils.py  # Utilities database
│   │   ├── faq_handler.py     # Xử lý FAQ
│   │   ├── prompts.py          # Templates prompts
│   │   ├── response_formatter.py  # Format responses
│   │   ├── training_data.py      # Training data
│   │   └── utils.py              # Utilities
│   │
│   └── services/         # Business Logic Layer
│       ├── database.py   # Database service (connection pool)
│       └── pooling/
│           └── product.py # Product service
│
└── web/                   # Frontend
    ├── index.php         # Trang chủ
    ├── assets/
    │   ├── css/style.css
    │   └── js/main.js
    └── includes/         # PHP includes
        ├── config.php
        ├── database.php
        └── ...
```

---

## 🔧 CÔNG NGHỆ SỬ DỤNG

### Backend:
- **Python 3.8+**
- **FastAPI**: Framework web hiện đại, hiệu năng cao
- **Uvicorn**: ASGI server
- **Google Gemini Pro**: AI model cho chatbot
- **MySQL**: Database chính
- **mysql-connector-python**: MySQL connector với connection pooling

### Frontend:
- **PHP**: Server-side rendering
- **JavaScript (Vanilla)**: Xử lý tương tác
- **CSS**: Styling

### Thư viện Python chính:
- `langchain`: Framework cho LLM applications
- `google-generativeai`: SDK cho Google Gemini
- `pydantic`: Data validation
- `python-dotenv`: Quản lý biến môi trường

---

## 📊 CẤU TRÚC DATABASE

### Các bảng chính:

1. **customers**: Thông tin khách hàng
   - id, name, email, phone, address, password
   - created_at, updated_at

2. **categories**: Danh mục sản phẩm (hierarchical)
   - id, name, description, parent_id

3. **products**: Sản phẩm laptop
   - id, category_id, name, description, price, stock
   - image_url, status, created_at, updated_at

4. **carts & cart_items**: Giỏ hàng
   - carts: id, customer_id
   - cart_items: id, cart_id, product_id, quantity

5. **orders & order_items**: Đơn hàng
   - orders: id, customer_id, order_number, total_amount
   - shipping_address, payment_method, status
   - order_items: id, order_id, product_id, quantity, price

6. **chat_history**: Lịch sử chat
   - id, customer_id, message, is_bot, created_at

7. **promotions**: Khuyến mãi
   - id, code, discount_type, discount_value
   - start_date, end_date, min_order_amount, usage_limit

8. **product_reviews**: Đánh giá sản phẩm
   - id, product_id, customer_id, rating, comment

9. **faqs**: Câu hỏi thường gặp
   - id, question, answer, category

10. **training_data**: Dữ liệu training chatbot
    - id, input_text, response_text, category

---

## 🔄 LUỒNG XỬ LÝ CHÍNH

### 1. Luồng xử lý tin nhắn (Message Processing Flow)

```
User Input
    │
    ▼
[FastAPI /chat endpoint]
    │
    ▼
[ChatbotChain.generate_response()]
    │
    ├─► [Extract Product Info]
    │   └─► Regex patterns:
    │       - Price ranges (15-20 triệu)
    │       - Laptop models (Dell Inspiron, MSI GF63...)
    │       - Usage purposes (gaming, đồ họa, văn phòng...)
    │
    ├─► [Check FAQ Handler]
    │   └─► Full-text search trong bảng FAQs
    │
    ├─► [Get Products from DB]
    │   └─► Search theo:
    │       - Price range
    │       - Category
    │       - Keywords
    │       - Specific model
    │
    ├─► [Format Response]
    │   └─► ResponseFormatter:
    │       - format_product_list()
    │       - format_price_range_response()
    │       - format_purpose_response()
    │       - format_specific_model_info()
    │
    └─► [Return Response]
        └─► JSON response với context
```

### 2. Chi tiết xử lý trong ChatbotChain

#### a) Trích xuất thông tin (`_extract_product_info`)

**Patterns được nhận diện:**

1. **Price Patterns:**
   - `15-20 triệu`, `khoảng 15-20 triệu`
   - `từ 15-20 triệu`, `tầm 15-20 triệu`
   - `dưới 15 triệu`, `khoảng 15 triệu`

2. **Purpose Patterns:**
   - Lập trình: `lập trình`, `coding`, `dev`, `developer`
   - Gaming: `game`, `gaming`, `chơi game`
   - Đồ họa: `đồ họa`, `thiết kế`, `design`, `photoshop`
   - Văn phòng: `văn phòng`, `office`, `học tập`

3. **Laptop Model Patterns:**
   - Dell: Inspiron, Vostro, Latitude, XPS, G15, Alienware
   - Lenovo: IdeaPad, ThinkPad, Legion, Yoga
   - HP: Pavilion, Envy, EliteBook, Victus, OMEN
   - ASUS: VivoBook, ZenBook, TUF, ROG, ExpertBook
   - Acer: Aspire, Nitro, Predator, Swift, Spin
   - MSI: GF, GL, GS, GE, GP, Prestige, Modern, Katana, Sword, Raider, Stealth

4. **Upgrade Patterns:**
   - RAM upgrade: `nâng ram`, `up ram`, `thêm ram`
   - Storage upgrade: `nâng ổ cứng`, `up ssd`
   - General: `nâng cấp được không`

#### b) Tìm kiếm sản phẩm (`_get_products`)

**Thứ tự ưu tiên:**
1. Tìm theo model cụ thể (nếu có)
2. Tìm theo khoảng giá
3. Tìm theo category
4. Tìm theo keywords

#### c) Format phản hồi (`ResponseFormatter`)

**Các loại format:**
- `format_price_range_response()`: Khi có khoảng giá
- `format_purpose_response()`: Khi có mục đích sử dụng
- `format_purpose_with_price_and_details()`: Khi có cả giá và mục đích
- `format_specific_model_info()`: Khi hỏi về model cụ thể
- `format_greeting()`: Lời chào
- `format_error_with_suggestions()`: Lỗi với gợi ý

---

## 🎯 TÍNH NĂNG CHÍNH

### 1. Tư vấn sản phẩm thông minh

**Khả năng:**
- ✅ Nhận diện khoảng giá từ ngôn ngữ tự nhiên
- ✅ Phân tích mục đích sử dụng
- ✅ Tìm kiếm sản phẩm theo nhiều tiêu chí
- ✅ Đề xuất sản phẩm phù hợp với scoring system
- ✅ Hiển thị thông tin chi tiết sản phẩm

**Ví dụ:**
```
User: "Tôi cần laptop gaming tầm 20-25 triệu"
Bot: 
  - Trích xuất: purpose=gaming, price_range=[20M-25M]
  - Tìm sản phẩm: Filter products by gaming category + price
  - Format: Danh sách laptop gaming trong khoảng giá
```

### 2. Xử lý câu hỏi về model cụ thể

**Khả năng:**
- ✅ Nhận diện brand và model từ tin nhắn
- ✅ Tìm kiếm chính xác model trong database
- ✅ Hiển thị thông số kỹ thuật chi tiết
- ✅ Tư vấn về khả năng nâng cấp

**Ví dụ:**
```
User: "Chi tiết về MSI GF63"
Bot:
  - Detect: brand=MSI, model=GF63
  - Search: Tìm "MSI GF63" trong database
  - Response: Thông số kỹ thuật đầy đủ
```

### 3. Context Management

**Khả năng:**
- ✅ Lưu trữ context theo session
- ✅ Nhớ sản phẩm đã đề cập trước đó
- ✅ Xử lý câu hỏi follow-up dựa trên context

**Ví dụ:**
```
User: "Laptop gaming 20 triệu"
Bot: [Hiển thị danh sách]
User: "Nâng cấp RAM được không?"
Bot: [Dựa vào context, trả lời về laptop đã đề cập]
```

### 4. FAQ Handler

**Khả năng:**
- ✅ Full-text search trong bảng FAQs
- ✅ Relevance scoring
- ✅ Trả lời tự động các câu hỏi thường gặp

### 5. Response Formatting

**Khả năng:**
- ✅ Format giá tiền (VND)
- ✅ Extract và format thông số kỹ thuật
- ✅ Tạo phản hồi có cấu trúc, dễ đọc
- ✅ Gợi ý tiếp theo cho người dùng

---

## 🔌 API ENDPOINTS

### 1. `GET /`
**Mục đích:** Health check
**Response:**
```json
{
  "status": "Chatbot API is running"
}
```

### 2. `POST /chat`
**Mục đích:** Xử lý tin nhắn từ người dùng

**Request Body:**
```json
{
  "message": "Tôi cần laptop gaming 20 triệu",
  "customer_id": 1,  // Optional
  "context": {}      // Optional
}
```

**Response:**
```json
{
  "response": "Dạ, trong khoảng giá 20,000,000đ...",
  "context": {
    "last_products": [...],
    "purposes": ["gaming"],
    "price_range": [20000000, 25000000]
  }
}
```

---

## 🗄️ DATABASE SERVICES

### 1. DatabaseUtils (src/chatbot/database_utils.py)
- Kết nối database đơn giản (không pooling)
- Methods:
  - `get_products_by_category()`
  - `get_products_by_price_range()`
  - `search_products()`
  - `get_faq_by_category()`

### 2. DatabaseService (src/services/database.py)
- **Singleton pattern** với connection pooling
- **Connection pool:** 5 connections
- Methods:
  - `get_product_by_id()`
  - `search_products()` (full-text search)
  - `get_products_by_category()`
  - `get_products_by_price_range()`
  - `save_chat_history()`
  - `get_chat_history()`

### 3. FAQHandler (src/chatbot/faq_handler.py)
- Connection pooling riêng
- Full-text search với relevance scoring
- Methods:
  - `get_faq_answer()`
  - `get_product_info()`
  - `get_similar_products()`

---

## 🎨 FRONTEND (Web Interface)

### Cấu trúc:
- **index.php**: Trang chủ với chat interface
- **main.js**: 
  - `sendMessage()`: Gửi tin nhắn đến API
  - `appendMessage()`: Hiển thị tin nhắn
  - `showTypingIndicator()`: Hiển thị "đang gõ..."
  - Session management với localStorage

### Flow:
```
User types message
    │
    ▼
[Enter key / Click Send]
    │
    ▼
[showTypingIndicator()]
    │
    ▼
[POST /chat API]
    │
    ▼
[appendMessage(response)]
```

---

## ⚙️ CẤU HÌNH

### Environment Variables (.env):
```env
# Database
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=chatbot_db
DB_PORT=3306

# Legacy MySQL config (cho các module cũ)
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DATABASE=chatbot_db

# Google Gemini
GEMINI_API_KEY=your_api_key_here

# Server
HOST=0.0.0.0
PORT=8000
```

### PHP Config (web/includes/config.php):
```php
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASS = 'Trung@2025'
DB_NAME = 'chatbot_db'
API_URL = 'http://localhost:8000'
```

---

## 🚀 CÁCH CHẠY DỰ ÁN

### 1. Setup Database:
```bash
mysql -u root -p < database/schema.sql
mysql -u root -p < database/sample_data.sql
```

### 2. Setup Python Environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### 3. Cấu hình .env:
```bash
cp env.example .env
# Chỉnh sửa .env với thông tin thực tế
```

### 4. Chạy Backend:
```bash
python src/main.py
# hoặc
uvicorn src.main:app --reload
```

### 5. Chạy Frontend:
- Setup web server (Apache/Nginx) trỏ đến thư mục `web/`
- Hoặc dùng PHP built-in server:
```bash
cd web
php -S localhost:8080
```

---

## 📈 ĐIỂM MẠNH

1. **Kiến trúc rõ ràng:** Tách biệt các layer (API, Business Logic, Database)
2. **AI Integration:** Sử dụng Google Gemini Pro cho xử lý ngôn ngữ tự nhiên
3. **Pattern Recognition:** Regex patterns mạnh mẽ cho trích xuất thông tin
4. **Context Management:** Lưu trữ và sử dụng context hiệu quả
5. **Response Formatting:** Format phản hồi đẹp, dễ đọc
6. **Connection Pooling:** Tối ưu kết nối database
7. **Full-text Search:** Tìm kiếm sản phẩm và FAQ hiệu quả

---

## ⚠️ ĐIỂM CẦN CẢI THIỆN

1. **Inconsistency trong Database Connection:**
   - Có 3 cách kết nối database khác nhau:
     - `DatabaseUtils` (không pooling)
     - `DatabaseService` (có pooling)
     - `FAQHandler` (pooling riêng)
   - **Đề xuất:** Thống nhất sử dụng một service duy nhất

2. **Error Handling:**
   - Một số nơi chỉ `print()` thay vì logging
   - Thiếu error recovery mechanism
   - **Đề xuất:** Sử dụng logging module và retry logic

3. **Session Management:**
   - Session storage đơn giản (in-memory)
   - Không persist khi server restart
   - **Đề xuất:** Sử dụng Redis hoặc database

4. **API Authentication:**
   - Chưa có authentication/authorization
   - **Đề xuất:** Thêm JWT hoặc API key

5. **Testing:**
   - Chưa có unit tests
   - Chưa có integration tests
   - **Đề xuất:** Thêm pytest tests

6. **Documentation:**
   - Một số functions thiếu docstrings
   - **Đề xuất:** Thêm docstrings đầy đủ

7. **Code Duplication:**
   - Một số logic bị lặp lại
   - **Đề xuất:** Refactor thành shared utilities

8. **Frontend:**
   - Chưa có error handling tốt
   - Chưa có loading states rõ ràng
   - **Đề xuất:** Cải thiện UX

---

## 🔮 HƯỚNG PHÁT TRIỂN

1. **Tích hợp Google Gemini tốt hơn:**
   - Sử dụng Gemini để phân tích ngữ cảnh tốt hơn
   - Fine-tuning với dữ liệu training

2. **Thêm tính năng:**
   - Đặt hàng trực tiếp qua chatbot
   - Thanh toán online
   - Tracking đơn hàng
   - Gửi email thông báo

3. **Cải thiện AI:**
   - Sentiment analysis
   - Intent classification tốt hơn
   - Multi-turn conversation handling

4. **Performance:**
   - Caching responses
   - Database indexing
   - CDN cho static files

5. **Monitoring:**
   - Logging system
   - Analytics
   - Error tracking (Sentry)

6. **Security:**
   - Input validation
   - SQL injection prevention (đã có nhưng cần kiểm tra)
   - Rate limiting
   - API authentication

---

## 📝 KẾT LUẬN

Dự án **Order Chatbot** là một hệ thống chatbot tư vấn laptop khá hoàn chỉnh với:
- ✅ Kiến trúc rõ ràng, dễ mở rộng
- ✅ Tích hợp AI (Google Gemini Pro)
- ✅ Xử lý ngôn ngữ tự nhiên tốt
- ✅ Database design hợp lý
- ✅ Frontend đơn giản nhưng đủ dùng

Tuy nhiên, vẫn còn một số điểm cần cải thiện về:
- Code organization (thống nhất database connection)
- Error handling và logging
- Testing
- Security
- Performance optimization

Nhìn chung, đây là một dự án tốt, có tiềm năng phát triển thành một hệ thống thương mại điện tử hoàn chỉnh.

