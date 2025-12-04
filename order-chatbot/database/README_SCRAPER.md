# Hướng Dẫn Sử Dụng Web Scraper - Thegioididong.com

## Tổng Quan

Script này được sử dụng để cào dữ liệu laptop từ website thegioididong.com và lưu vào database MySQL.

## Các File Đã Tạo

1. **scraper_tgdd.py**: Script Python để cào dữ liệu từ thegioididong.com
2. **tgdd_products.sql**: File SQL chứa 20 sản phẩm laptop đã được cào
3. **tgdd_products_extended.sql**: File SQL mở rộng với thông tin chi tiết hơn

## Cài Đặt

### 1. Cài đặt dependencies

```bash
pip install playwright mysql-connector-python python-dotenv
playwright install chromium
```

### 2. Cấu hình database

Đảm bảo file `.env` đã được cấu hình đúng:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=chatbot_db
DB_PORT=3306
```

## Sử Dụng

### Cách 1: Sử dụng file SQL đã có

```bash
# Import file SQL vào database
mysql -u root -p chatbot_db < tgdd_products_extended.sql
```

### Cách 2: Chạy script Python để cào thêm dữ liệu

```bash
# Chạy script scraper
python scraper_tgdd.py
```

Script sẽ:
- Cào dữ liệu từ 3 trang đầu của thegioididong.com
- Lấy thông tin chi tiết của mỗi sản phẩm
- Lưu vào file `tgdd_products.json` và `tgdd_products.sql`

### Cách 3: Sử dụng MCP Playwright (Đã thử nghiệm)

Đã sử dụng MCP Playwright server để cào dữ liệu trực tiếp từ browser và tạo file SQL.

## Dữ Liệu Đã Cào

### Thống kê
- **Tổng số sản phẩm**: 20 sản phẩm unique
- **Phân loại**:
  - Laptop Văn Phòng: 15 sản phẩm
  - Laptop Mỏng Nhẹ: 3 sản phẩm
  - Laptop Gaming: 2 sản phẩm

### Thông tin sản phẩm
Mỗi sản phẩm bao gồm:
- Tên sản phẩm
- Giá bán
- Mô tả/Thông số kỹ thuật
- Hình ảnh
- Category ID
- Stock (mặc định: 10)
- Status (mặc định: 'active')

## Cấu Trúc Database

### Bảng products
```sql
CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    category_id INT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    image_url VARCHAR(255),
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
);
```

### Categories
- Category ID 5: Laptop Gaming
- Category ID 6: Laptop Văn Phòng
- Category ID 7: Laptop Đồ Họa
- Category ID 8: Laptop Mỏng Nhẹ

## Cải Thiện

### Để cào nhiều sản phẩm hơn:

1. **Tăng số trang**: Thay đổi `max_pages` trong script
```python
products = await scraper.run(max_pages=10)  # Cào 10 trang
```

2. **Cào theo category**: Truy cập các URL category cụ thể
- https://www.thegioididong.com/laptop-gaming
- https://www.thegioididong.com/laptop-do-hoa
- https://www.thegioididong.com/laptop-mong-nhe

3. **Cào theo giá**: Truy cập các URL filter giá
- https://www.thegioididong.com/laptop?p=duoi-10-trieu
- https://www.thegioididong.com/laptop?p=10-15-trieu
- https://www.thegioididong.com/laptop?p=15-20-trieu

### Để cải thiện chất lượng dữ liệu:

1. **Lấy thông tin chi tiết hơn**: Truy cập từng trang sản phẩm để lấy thông số kỹ thuật đầy đủ
2. **Parse thông số kỹ thuật**: Trích xuất CPU, RAM, Storage, GPU từ description
3. **Xử lý hình ảnh**: Lưu hình ảnh local hoặc sử dụng CDN
4. **Xử lý lỗi**: Thêm error handling và retry mechanism

## Lưu Ý

1. **Rate limiting**: Đừng cào quá nhanh để tránh bị block
2. **Robots.txt**: Kiểm tra robots.txt của website trước khi cào
3. **Terms of Service**: Đảm bảo việc cào dữ liệu tuân thủ Terms of Service
4. **Dữ liệu**: Dữ liệu cào được chỉ để phục vụ mục đích học tập và nghiên cứu

## Troubleshooting

### Lỗi: "Cannot connect to database"
- Kiểm tra file `.env` đã được cấu hình đúng
- Đảm bảo MySQL đang chạy
- Kiểm tra quyền truy cập database

### Lỗi: "Playwright browser not found"
- Chạy: `playwright install chromium`
- Kiểm tra PATH environment variable

### Lỗi: "Timeout waiting for page"
- Tăng timeout trong script
- Kiểm tra kết nối internet
- Thử lại sau vài phút

## Kết Quả

Sau khi chạy script, bạn sẽ có:
- File `tgdd_products.json`: Dữ liệu JSON
- File `tgdd_products.sql`: Dữ liệu SQL để import vào database
- 20+ sản phẩm laptop với thông tin đầy đủ

## Liên Hệ

Nếu có vấn đề hoặc câu hỏi, vui lòng tạo issue trên GitHub repository.

---

**Chúc bạn sử dụng thành công! 🎉**

