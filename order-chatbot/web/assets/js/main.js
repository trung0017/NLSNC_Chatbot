async function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Hiển thị tin nhắn người dùng
    appendMessage(message, false);
    input.value = '';

    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                customer_id: getCurrentCustomerId()
            })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        
        // Kiểm tra loại response
        if (data.type === 'error') {
            // Hiển thị thông báo lỗi
            appendMessage(data.response, true, 'error');
        } else {
            // Hiển thị phản hồi bình thường từ chatbot
            appendMessage(data.response, true, 'text');
        }
    } catch (error) {
        console.error('Error:', error);
        appendMessage('Xin lỗi, có lỗi xảy ra!', true, 'error');
    }
}

function appendMessage(message, isBot, type = 'text') {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    
    // Thêm class dựa trên loại tin nhắn
    let className = `message ${isBot ? 'bot' : 'user'}`;
    if (type === 'error') {
        className += ' error';
    }
    messageDiv.className = className;
    
    // Xử lý xuống dòng trong tin nhắn
    const formattedMessage = message.replace(/\n/g, '<br>');
    messageDiv.innerHTML = formattedMessage;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Thêm sự kiện Enter để gửi tin nhắn
document.getElementById('user-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Function lấy customer_id từ session
function getCurrentCustomerId() {
    // Trong thực tế, lấy từ session hoặc localStorage sau khi đăng nhập
    return localStorage.getItem('customer_id');
} 