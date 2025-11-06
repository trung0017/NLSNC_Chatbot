<?php 
// Lấy đường dẫn tuyệt đối đến thư mục gốc
define('ROOT_PATH', dirname(dirname(__FILE__)));

// Include file config
require_once ROOT_PATH . '/includes/config.php';
?>
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chatbot Đặt Hàng</title>
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
    <header>
        <nav>
            <ul>
                <li><a href="index.php">Trang chủ</a></li>
                <li><a href="templates/products.php">Sản phẩm</a></li>
                <li><a href="templates/cart.php">Giỏ hàng</a></li>
            </ul>
        </nav>
    </header>
    <main> 