<?php
// Hàm kiểm tra đường dẫn hiện tại
function getCurrentPage() {
    return basename($_SERVER['PHP_SELF']);
}

// Hàm tạo đường dẫn tương đối
function getRelativePath($path) {
    $currentDepth = substr_count(getCurrentPage(), '/');
    $prefix = str_repeat('../', $currentDepth);
    return $prefix . $path;
}

// Hàm format tiền tệ
function formatCurrency($amount) {
    return number_format($amount, 0, ',', '.') . ' đ';
}

// Hàm xử lý lỗi
function handleError($message) {
    error_log($message);
    return [
        'error' => true,
        'message' => 'Có lỗi xảy ra, vui lòng thử lại sau'
    ];
} 