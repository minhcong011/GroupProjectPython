// Chatbot JavaScript Functions
let chatMessages = document.getElementById('chatMessages');
let messageInput = document.getElementById('messageInput');
let sendButton = document.getElementById('sendButton');
let typingIndicator = document.getElementById('typingIndicator');

// API Configuration
const API_KEY = 'YOUR_GOOGLE_GEMINI_API_KEY_HERE'; // Thay thế bằng API key thực tế
const API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent';

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    // Auto-focus input
    messageInput.focus();
});

// Send message function
function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;
    
    // Add user message to chat
    addMessageToChat(message, 'user');
    
    // Clear input
    messageInput.value = '';
    
    // Send to AI
    sendToAI(message);
}

// Send quick message
function sendQuickMessage(message) {
    addMessageToChat(message, 'user');
    sendToAI(message);
}

// Add message to chat
function addMessageToChat(message, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.textContent = message;
    
    const messageTime = document.createElement('div');
    messageTime.className = 'message-time';
    messageTime.textContent = getCurrentTime();
    
    messageDiv.appendChild(messageContent);
    messageDiv.appendChild(messageTime);
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// Send to AI function
async function sendToAI(message) {
    showTypingIndicator();
    
    try {
        const response = await fetch(`${API_URL}?key=${API_KEY}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                contents: [{
                    parts: [{
                        text: `Bạn là một trợ lý AI chuyên về lập trình Python và Perl. Hãy trả lời câu hỏi sau bằng tiếng Việt một cách chi tiết và dễ hiểu, tập trung vào việc giải thích khái niệm, cung cấp ví dụ code cụ thể khi cần thiết: ${message}`
                    }]
                }]
            })
        });

        const data = await response.json();
        
        if (data.candidates && data.candidates[0] && data.candidates[0].content) {
            const aiResponse = data.candidates[0].content.parts[0].text;
            hideTypingIndicator();
            addFormattedMessageToChat(aiResponse, 'ai');
        } else {
            throw new Error('Không thể nhận được phản hồi từ AI');
        }
    } catch (error) {
        console.error('Lỗi khi gọi API:', error);
        hideTypingIndicator();
        addMessageToChat('Xin lỗi, đã có lỗi xảy ra khi kết nối với AI. Vui lòng thử lại sau.', 'ai');
    }
}

// Add formatted message to chat (for AI responses)
function addFormattedMessageToChat(message, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    // Format the message with basic markdown support
    const formattedMessage = formatMessage(message);
    messageContent.innerHTML = formattedMessage;
    
    const messageTime = document.createElement('div');
    messageTime.className = 'message-time';
    messageTime.textContent = getCurrentTime();
    
    messageDiv.appendChild(messageContent);
    messageDiv.appendChild(messageTime);
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// Format message with basic markdown
function formatMessage(text) {
    // Convert code blocks
    text = text.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');
    
    // Convert inline code
    text = text.replace(/`([^`]+)`/g, '<code>$1</code>');
    
    // Convert bold text
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Convert italic text
    text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
    
    // Convert line breaks
    text = text.replace(/\n/g, '<br>');
    
    return text;
}

// Show typing indicator
function showTypingIndicator() {
    typingIndicator.style.display = 'flex';
    scrollToBottom();
}

// Hide typing indicator
function hideTypingIndicator() {
    typingIndicator.style.display = 'none';
}

// Get current time
function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString('vi-VN', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Scroll to bottom
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Handle button states
messageInput.addEventListener('input', function() {
    sendButton.disabled = !this.value.trim();
});

// Initialize button state
sendButton.disabled = !messageInput.value.trim();
