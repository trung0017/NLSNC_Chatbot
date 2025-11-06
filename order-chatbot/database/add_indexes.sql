-- Thêm FULLTEXT index cho bảng products
ALTER TABLE products
ADD FULLTEXT(name, description);

-- Thêm FULLTEXT index cho bảng faqs
ALTER TABLE faqs
ADD FULLTEXT(question);

-- Thêm FULLTEXT index cho bảng training_data
ALTER TABLE training_data
ADD FULLTEXT(input_text); 