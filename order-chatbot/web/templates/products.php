<?php
require_once '../includes/header.php';
require_once '../includes/database.php';

$db = new Database();
$query = "SELECT p.*, c.name as category_name 
          FROM products p
          JOIN categories c ON p.category_id = c.id";
$result = $db->query($query);
$products = $result->fetchAll(PDO::FETCH_ASSOC);
?>

<div class="products-container">
    <h1>Sản phẩm</h1>
    <div class="products-grid">
        <?php foreach ($products as $product): ?>
            <div class="product-card">
                <img src="assets/images/<?php echo $product['image_url']; ?>" alt="<?php echo $product['name']; ?>">
                <h3><?php echo $product['name']; ?></h3>
                <p class="category"><?php echo $product['category_name']; ?></p>
                <p class="price"><?php echo formatCurrency($product['price']); ?></p>
                <p class="stock">Còn <?php echo $product['stock']; ?> sản phẩm</p>
                <button onclick="addToCart(<?php echo $product['id']; ?>)">Thêm vào giỏ hàng</button>
            </div>
        <?php endforeach; ?>
    </div>
</div>

<?php require_once '../includes/footer.php'; ?> 