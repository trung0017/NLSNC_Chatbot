-- Cập nhật tên danh mục cho phù hợp
UPDATE categories 
SET name = 'Gaming'
WHERE name LIKE '%gaming%' OR name LIKE '%game%';

UPDATE categories 
SET name = 'Văn phòng'
WHERE name LIKE '%văn phòng%' OR name LIKE '%office%';

UPDATE categories 
SET name = 'Đồ họa'
WHERE name LIKE '%đồ họa%' OR name LIKE '%design%' OR name LIKE '%graphics%';

UPDATE categories 
SET name = 'Mỏng nhẹ'
WHERE name LIKE '%mỏng nhẹ%' OR name LIKE '%ultrabook%';

-- Cập nhật category_id cho sản phẩm
UPDATE products p
SET category_id = (SELECT id FROM categories WHERE name = 'Gaming')
WHERE 
    p.name LIKE '%gaming%' 
    OR p.name LIKE '%msi%'
    OR p.name LIKE '%rog%'
    OR p.description LIKE '%gtx%'
    OR p.description LIKE '%rtx%';

UPDATE products p
SET category_id = (SELECT id FROM categories WHERE name = 'Văn phòng')
WHERE 
    p.name LIKE '%vivobook%'
    OR p.name LIKE '%thinkpad%'
    OR p.name LIKE '%latitude%';

UPDATE products p
SET category_id = (SELECT id FROM categories WHERE name = 'Đồ họa')
WHERE 
    p.name LIKE '%creator%'
    OR p.name LIKE '%studio%'
    OR p.description LIKE '%đồ họa%';

UPDATE products p
SET category_id = (SELECT id FROM categories WHERE name = 'Mỏng nhẹ')
WHERE 
    p.name LIKE '%slim%'
    OR p.name LIKE '%air%'
    OR p.description LIKE '%mỏng nhẹ%'; 