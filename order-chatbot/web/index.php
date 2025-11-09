<?php
require_once 'includes/header.php';
?>

<div class="chat-container">
    <div class="chat-messages" id="chat-messages">
        <!-- Messages will be displayed here -->
    </div>
    
    <div class="chat-input">
        <input type="text" id="user-input" placeholder="Nhập tin nhắn...">
        <button onclick="sendMessage()">Gửi</button>
    </div>
</div>

<script>
function sendMessage() {
    // Xử lý gửi tin nhắn đến API
}
</script>

<?php
require_once 'includes/footer.php';
?> 