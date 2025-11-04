-- Chèn dữ liệu danh mục
INSERT INTO categories (name, description, parent_id) VALUES
('Điện thoại', 'Các loại điện thoại di động', NULL),
('Laptop', 'Máy tính xách tay các loại', NULL),
('Tablet', 'Máy tính bảng các loại', NULL),
('Phụ kiện', 'Phụ kiện điện tử các loại', NULL),
('Laptop Gaming', 'Laptop chuyên game với hiệu năng cao', 2),
('Laptop Văn Phòng', 'Laptop cho công việc văn phòng', 2),
('Laptop Đồ Họa', 'Laptop cho thiết kế và đồ họa', 2),
('Laptop Mỏng Nhẹ', 'Laptop di động với trọng lượng nhẹ', 2),
('Laptop Cao Cấp', 'Laptop cao cấp với cấu hình mạnh', 2);

-- Chèn dữ liệu sản phẩm
INSERT INTO products (category_id, name, description, price, stock, image_url, status) VALUES
(1, 'iPhone 14 Pro Max', 'iPhone 14 Pro Max 256GB, màu đen', 27990000, 50, 'iphone14.jpg', 'active'),
(1, 'Samsung Galaxy S23', 'Samsung Galaxy S23 Ultra 5G 256GB', 23990000, 30, 'samsung-s23.jpg', 'active'),
(2, 'MacBook Pro M2', 'MacBook Pro 14 inch M2 Pro', 52990000, 20, 'macbook-m2.jpg', 'active'),
(2, 'Dell XPS 13', 'Dell XPS 13 Plus 9320 i7 12700H', 49990000, 15, 'dell-xps.jpg', 'active'),
(3, 'iPad Pro M2', 'iPad Pro M2 11 inch WiFi 128GB', 20990000, 25, 'ipad-pro.jpg', 'active'),
(4, 'AirPods Pro 2', 'Tai nghe Apple AirPods Pro 2', 6790000, 100, 'airpods-pro.jpg', 'active'),

-- Laptop Gaming
(5, 'Acer Nitro 5', 'AMD Ryzen 7, RTX 3060, 16GB RAM', 24990000, 30, 'acer-nitro-5.jpg', 'active'),
(5, 'MSI GF63', 'Intel i5, GTX 1650, 8GB RAM', 16990000, 25, 'msi-gf63.jpg', 'active'),
(5, 'Lenovo Legion 5', 'AMD Ryzen 5, RTX 3050Ti, 16GB RAM', 22990000, 20, 'legion-5.jpg', 'active'),
(5, 'ASUS TUF Gaming', 'Intel i7, RTX 3050, 16GB RAM', 21990000, 35, 'asus-tuf.jpg', 'active'),
(5, 'HP Victus', 'AMD Ryzen 5, RTX 3050, 8GB RAM', 19990000, 28, 'hp-victus.jpg', 'active'),

-- Laptop Văn Phòng
(6, 'Dell Inspiron 3511', 'Intel i3, 8GB RAM, 256GB SSD', 12990000, 40, 'dell-3511.jpg', 'active'),
(6, 'HP 15s', 'AMD Ryzen 5, 8GB RAM, 512GB SSD', 14990000, 45, 'hp-15s.jpg', 'active'),
(6, 'Lenovo IdeaPad 3', 'Intel i5, 8GB RAM, 512GB SSD', 13990000, 35, 'ideapad-3.jpg', 'active'),
(6, 'ASUS VivoBook', 'Intel i5, 8GB RAM, 256GB SSD', 15990000, 30, 'vivobook.jpg', 'active'),
(6, 'Acer Aspire 3', 'Intel i3, 4GB RAM, 256GB SSD', 11990000, 50, 'aspire-3.jpg', 'active'),

-- Laptop Đồ Họa
(7, 'MacBook Pro 16', 'M1 Pro, 16GB RAM, 512GB SSD', 52990000, 15, 'macbook-pro-16.jpg', 'active'),
(7, 'Dell XPS 15', 'Intel i9, RTX 3050Ti, 32GB RAM', 49990000, 12, 'xps-15.jpg', 'active'),
(7, 'ASUS ProArt', 'Intel i7, RTX 3070, 32GB RAM', 47990000, 10, 'proart.jpg', 'active'),
(7, 'MSI Creator Z16', 'Intel i7, RTX 3060, 32GB RAM', 45990000, 18, 'creator-z16.jpg', 'active'),
(7, 'Gigabyte AERO', 'Intel i7, RTX 3060, 16GB RAM', 41990000, 20, 'aero.jpg', 'active'),

-- Laptop Mỏng Nhẹ
(8, 'MacBook Air M2', 'M2, 8GB RAM, 256GB SSD', 32990000, 25, 'macbook-air.jpg', 'active'),
(8, 'Dell XPS 13', 'Intel i5, 8GB RAM, 512GB SSD', 29990000, 20, 'xps-13.jpg', 'active'),
(8, 'LG Gram 14', 'Intel i5, 16GB RAM, 512GB SSD', 31990000, 15, 'lg-gram.jpg', 'active'),
(8, 'ASUS ZenBook', 'Intel i7, 16GB RAM, 512GB SSD', 28990000, 22, 'zenbook.jpg', 'active'),
(8, 'Huawei MateBook', 'Intel i5, 8GB RAM, 512GB SSD', 24990000, 28, 'matebook.jpg', 'active');

-- Tạo bảng FAQ
CREATE TABLE faqs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    category VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Chèn dữ liệu FAQ
INSERT INTO faqs (question, answer, category) VALUES
('Làm thế nào để đặt hàng?', 'Để đặt hàng, bạn có thể thực hiện theo các bước sau:\n1. Chọn sản phẩm muốn mua\n2. Thêm vào giỏ hàng\n3. Điền thông tin giao hàng\n4. Chọn phương thức thanh toán\n5. Xác nhận đơn hàng', 'Đặt hàng'),

('Các phương thức thanh toán?', 'Chúng tôi hỗ trợ các phương thức thanh toán:\n- COD (thanh toán khi nhận hàng)\n- Chuyển khoản ngân hàng\n- Ví điện tử MoMo', 'Thanh toán'),

('Chính sách đổi trả?', 'Sản phẩm được đổi trả trong vòng 7 ngày nếu:\n- Sản phẩm còn nguyên vẹn\n- Có đầy đủ hóa đơn và phụ kiện\n- Lỗi do nhà sản xuất', 'Đổi trả'),

('Thời gian giao hàng?', 'Thời gian giao hàng dự kiến:\n- Nội thành: 1-2 ngày\n- Ngoại thành: 2-3 ngày\n- Tỉnh khác: 3-5 ngày', 'Giao hàng'),

('Bảo hành sản phẩm?', 'Chính sách bảo hành:\n- Điện thoại, laptop: 12 tháng\n- Tablet: 12 tháng\n- Phụ kiện: 3-6 tháng\nBảo hành chính hãng tại các trung tâm bảo hành ủy quyền', 'Bảo hành');

-- Tạo bảng training_data cho chatbot
CREATE TABLE training_data (
    id INT PRIMARY KEY AUTO_INCREMENT,
    input_text TEXT NOT NULL,
    response_text TEXT NOT NULL,
    category VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Chèn dữ liệu training
INSERT INTO training_data (input_text, response_text, category) VALUES
('Chào', 'Xin chào! Tôi có thể giúp gì cho bạn?', 'Chào hỏi'),
('Tạm biệt', 'Tạm biệt! Hẹn gặp lại bạn!', 'Chào hỏi'),
('Cảm ơn', 'Không có gì! Rất vui được giúp đỡ bạn!', 'Chào hỏi'),

('Giá iPhone 14', 'iPhone 14 Pro Max 256GB có giá 27.990.000đ', 'Sản phẩm'),
('Còn hàng không', 'Vui lòng cho tôi biết bạn đang quan tâm đến sản phẩm nào?', 'Sản phẩm'),
('Có trả góp không', 'Có, chúng tôi hỗ trợ trả góp qua thẻ tín dụng và công ty tài chính', 'Thanh toán'),

('Địa chỉ shop', 'Địa chỉ cửa hàng: 123 Đường ABC, Quận XYZ, TP.HCM', 'Thông tin'),
('Số điện thoại', 'Hotline: 1900.xxxx', 'Thông tin'),
('Giờ làm việc', 'Cửa hàng mở cửa từ 8h00 - 21h00 các ngày trong tuần', 'Thông tin');

-- Thêm dữ liệu cho bảng customers
INSERT INTO customers (name, email, phone, address, password) VALUES
('Nguyễn Văn An', 'an.nguyen@email.com', '0901234567', 'Hà Nội', SHA2('password123', 256)),
('Trần Thị Bình', 'binh.tran@email.com', '0912345678', 'TP.HCM', SHA2('password123', 256)),
('Lê Văn Cường', 'cuong.le@email.com', '0923456789', 'Đà Nẵng', SHA2('password123', 256)),
('Phạm Thị Dung', 'dung.pham@email.com', '0934567890', 'Hải Phòng', SHA2('password123', 256)),
('Hoàng Văn Em', 'em.hoang@email.com', '0945678901', 'Cần Thơ', SHA2('password123', 256)),
('Ngô Thị Phương', 'phuong.ngo@email.com', '0956789012', 'Huế', SHA2('password123', 256)),
('Đặng Văn Giang', 'giang.dang@email.com', '0967890123', 'Nha Trang', SHA2('password123', 256)),
('Vũ Thị Hương', 'huong.vu@email.com', '0978901234', 'Vũng Tàu', SHA2('password123', 256)),
('Bùi Văn Inh', 'inh.bui@email.com', '0989012345', 'Đà Lạt', SHA2('password123', 256)),
('Lý Thị Kim', 'kim.ly@email.com', '0990123456', 'Quy Nhơn', SHA2('password123', 256));

-- Thêm dữ liệu cho bảng promotions
INSERT INTO promotions (code, discount_type, discount_value, start_date, end_date, min_order_amount, max_discount, usage_limit) VALUES
('WELCOME2024', 'percentage', 10, '2024-01-01', '2024-12-31', 1000000, 1000000, 100),
('TET2024', 'percentage', 20, '2024-01-15', '2024-02-15', 5000000, 2000000, 50),
('SUMMER2024', 'fixed', 500000, '2024-05-01', '2024-08-31', 10000000, 500000, 200),
('BACKTOSCHOOL', 'percentage', 15, '2024-08-01', '2024-09-30', 15000000, 3000000, 150),
('BLACK_FRIDAY', 'percentage', 30, '2024-11-20', '2024-11-30', 20000000, 5000000, 100);

-- Thêm dữ liệu cho bảng training_data
INSERT INTO training_data (input_text, response_text, category) VALUES
-- Câu hỏi về laptop gaming
('Laptop gaming giá bao nhiêu?', 'Chúng tôi có nhiều lựa chọn laptop gaming với các mức giá khác nhau:\n- Acer Nitro 5: 24.990.000đ (RTX 3060, 16GB RAM)\n- MSI GF63: 16.990.000đ (GTX 1650, 8GB RAM)\n- Lenovo Legion 5: 22.990.000đ (RTX 3050Ti, 16GB RAM)\n- ASUS TUF Gaming: 21.990.000đ (RTX 3050, 16GB RAM)\n- HP Victus: 19.990.000đ (RTX 3050, 8GB RAM)\nBạn muốn tìm laptop trong tầm giá nào?', 'Gaming'),

('Laptop chơi game tốt nhất?', 'Dựa trên cấu hình và đánh giá, những laptop gaming tốt nhất hiện tại:\n1. Acer Nitro 5 (24.990.000đ):\n   - CPU: AMD Ryzen 7\n   - GPU: RTX 3060\n   - RAM: 16GB\n   - Thích hợp cho gaming nặng\n2. Lenovo Legion 5 (22.990.000đ):\n   - CPU: AMD Ryzen 5\n   - GPU: RTX 3050Ti\n   - RAM: 16GB\n   - Cân bằng giữa hiệu năng và giá', 'Gaming'),

-- Câu hỏi về laptop văn phòng
('Laptop văn phòng giá rẻ nhất?', 'Các laptop văn phòng giá tốt hiện có:\n1. Acer Aspire 3: 11.990.000đ\n   - CPU: Intel i3\n   - RAM: 4GB\n   - SSD: 256GB\n2. Dell Inspiron 3511: 12.990.000đ\n   - CPU: Intel i3\n   - RAM: 8GB\n   - SSD: 256GB\n3. Lenovo IdeaPad 3: 13.990.000đ\n   - CPU: Intel i5\n   - RAM: 8GB\n   - SSD: 512GB', 'Văn phòng'),

-- Câu hỏi về laptop đồ họa
('Laptop cho thiết kế đồ họa tốt nhất?', 'Các laptop chuyên đồ họa cao cấp:\n1. MacBook Pro 16 (52.990.000đ):\n   - CPU: M1 Pro\n   - RAM: 16GB\n   - SSD: 512GB\n   - Màn hình Retina\n2. Dell XPS 15 (49.990.000đ):\n   - CPU: Intel i9\n   - GPU: RTX 3050Ti\n   - RAM: 32GB\n   - Màn hình 4K\n3. ASUS ProArt (47.990.000đ):\n   - CPU: Intel i7\n   - GPU: RTX 3070\n   - RAM: 32GB\n   - Màn hình màu chuẩn', 'Đồ họa'),

-- Câu hỏi về laptop mỏng nhẹ
('Laptop mỏng nhẹ pin trâu?', 'Các laptop mỏng nhẹ với pin tốt:\n1. MacBook Air M2 (32.990.000đ):\n   - Pin: Đến 18 giờ\n   - Trọng lượng: 1.24kg\n2. LG Gram 14 (31.990.000đ):\n   - Pin: Đến 20.5 giờ\n   - Trọng lượng: 999g\n3. Dell XPS 13 (29.990.000đ):\n   - Pin: Đến 14 giờ\n   - Trọng lượng: 1.27kg', 'Mỏng nhẹ'),

-- Câu hỏi về khuyến mãi
('Có chương trình khuyến mãi nào không?', 'Hiện tại chúng tôi có các chương trình khuyến mãi:\n1. WELCOME2024: Giảm 10% (tối đa 1tr) cho đơn từ 1tr\n2. TET2024: Giảm 20% (tối đa 2tr) cho đơn từ 5tr (15/1 - 15/2)\n3. SUMMER2024: Giảm 500k cho đơn từ 10tr\n4. BACKTOSCHOOL: Giảm 15% (tối đa 3tr) cho đơn từ 15tr\n5. BLACK_FRIDAY: Giảm 30% (tối đa 5tr) cho đơn từ 20tr', 'Khuyến mãi'),

-- Câu hỏi về thanh toán và trả góp
('Mua trả góp như thế nào?', 'Chúng tôi hỗ trợ các hình thức trả góp:\n1. Qua thẻ tín dụng:\n   - Chuyển đổi trả góp 0%\n   - Kỳ hạn 6-12 tháng\n2. Qua công ty tài chính:\n   - Trả trước 20-30%\n   - Kỳ hạn đến 24 tháng\n   - Lãi suất ưu đãi\nYêu cầu: CMND, Hộ khẩu/KT3, Bảng lương', 'Thanh toán'),

-- Câu hỏi về bảo hành
('Chính sách bảo hành laptop?', 'Chính sách bảo hành chi tiết:\n1. Thời gian:\n   - Laptop: 12 tháng\n   - Pin: 6-12 tháng\n   - Phụ kiện: 3-6 tháng\n2. Điều kiện:\n   - Tem bảo hành còn nguyên vẹn\n   - Không có dấu hiệu va đập\n3. Địa điểm: Trung tâm bảo hành ủy quyền\n4. Thời gian xử lý: 3-7 ngày làm việc', 'Bảo hành'),

-- Câu hỏi về giao hàng
('Thời gian giao hàng mất bao lâu?', 'Thời gian giao hàng dự kiến:\n1. Nội thành (HN, HCM):\n   - Giao nhanh: 2-4 giờ\n   - Giao thường: 1-2 ngày\n2. Các tỉnh miền Bắc/Nam:\n   - 2-3 ngày\n3. Các tỉnh miền Trung:\n   - 3-5 ngày\nMiễn phí giao hàng cho đơn từ 2 triệu.', 'Giao hàng'),

-- Câu hỏi về đổi trả
('Điều kiện đổi trả là gì?', 'Chính sách đổi trả trong 7 ngày:\n1. Điều kiện:\n   - Sản phẩm còn nguyên vẹn\n   - Đầy đủ phụ kiện và hộp\n   - Tem bảo hành còn nguyên\n2. Trường hợp đổi trả:\n   - Lỗi kỹ thuật\n   - Sai sản phẩm\n   - Không đúng nhu cầu\n3. Chi phí:\n   - Miễn phí nếu lỗi từ nhà sản xuất\n   - Phí 5% nếu đổi khác mẫu', 'Đổi trả');

-- Thêm dữ liệu cho bảng faqs
INSERT INTO faqs (question, answer, category) VALUES
('Nên chọn laptop hãng nào?', 'Tùy theo nhu cầu sử dụng:\n1. Gaming:\n   - Acer Nitro, Predator\n   - MSI Gaming\n   - Lenovo Legion\n   - ASUS TUF, ROG\n2. Văn phòng:\n   - Dell Inspiron, Latitude\n   - HP Pavilion, ProBook\n   - Lenovo ThinkPad\n3. Đồ họa:\n   - MacBook Pro\n   - Dell XPS\n   - ASUS ProArt\n4. Mỏng nhẹ:\n   - MacBook Air\n   - Dell XPS\n   - LG Gram', 'Tư vấn'),

('So sánh các dòng laptop gaming?', 'So sánh các laptop gaming phổ biến:\n1. Acer Nitro 5 (24.990.000đ):\n   - Ưu: Giá tốt, tản nhiệt tốt\n   - Nhược: Hơi nặng\n2. MSI GF63 (16.990.000đ):\n   - Ưu: Rẻ nhất phân khúc\n   - Nhược: Card đồ họa yếu hơn\n3. Lenovo Legion 5 (22.990.000đ):\n   - Ưu: Cân bằng, bền bỉ\n   - Nhược: Giá cao hơn\n4. ASUS TUF (21.990.000đ):\n   - Ưu: Bền bỉ, giá tốt\n   - Nhược: Màn hình trung bình', 'Gaming'),

('Cấu hình laptop văn phòng tối thiểu?', 'Cấu hình đề xuất cho văn phòng:\n1. Cơ bản (11-13 triệu):\n   - CPU: Intel i3/Ryzen 3\n   - RAM: 8GB\n   - SSD: 256GB\n2. Khuyến nghị (13-15 triệu):\n   - CPU: Intel i5/Ryzen 5\n   - RAM: 8-16GB\n   - SSD: 512GB\n3. Cao cấp (15-20 triệu):\n   - CPU: Intel i7/Ryzen 7\n   - RAM: 16GB\n   - SSD: 512GB-1TB', 'Văn phòng');

-- Thêm dữ liệu cho bảng chat_history
INSERT INTO chat_history (customer_id, message, is_bot) VALUES
(1, 'Tôi muốn mua laptop chơi game', 0),
(1, 'Với nhu cầu chơi game, tôi gợi ý bạn một số mẫu laptop gaming như Acer Nitro 5, MSI GF63, hoặc Lenovo Legion 5. Các máy này đều có cấu hình tốt với card đồ họa RTX series.', 1),
(2, 'Laptop văn phòng giá khoảng 15 triệu', 0),
(2, 'Trong tầm giá 15 triệu, bạn có thể tham khảo các mẫu như HP 15s, Lenovo IdeaPad 3 hoặc ASUS VivoBook. Các máy này đều phù hợp nhu cầu văn phòng với cấu hình ổn định.', 1);

-- Thêm dữ liệu cho bảng orders và order_items
INSERT INTO orders (customer_id, order_number, total_amount, shipping_address, shipping_phone, payment_method, status) VALUES
(1, 'ORD001', 24990000, 'Số 1 Đại Cồ Việt, Hai Bà Trưng, Hà Nội', '0901234567', 'banking', 'delivered'),
(2, 'ORD002', 16990000, '123 Nguyễn Văn Linh, Q7, TP.HCM', '0912345678', 'cod', 'shipping'),
(3, 'ORD003', 52990000, '456 Lê Duẩn, Đà Nẵng', '0923456789', 'momo', 'confirmed');

INSERT INTO order_items (order_id, product_id, quantity, price) VALUES
(1, 1, 1, 24990000),
(2, 2, 1, 16990000),
(3, 11, 1, 52990000); 