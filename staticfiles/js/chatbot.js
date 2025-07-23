// Chatbot JavaScript Functions - Simplified Version
console.log('Loading chatbot.js...');

let chatMessages, messageInput, sendButton, typingIndicator, modeIndicator;
let currentMode = 'chat';

window.API_KEY = ''; 
window.API_URL = 'https://api.groq.com/openai/v1/chat/completions';
window.MODEL_NAME = 'llama-3.1-8b-instant';

console.log('Constants initialized');
console.log('window.API_KEY defined:', typeof window.API_KEY !== 'undefined');


document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing...');
    
    // Initialize DOM elements
    chatMessages = document.getElementById('chatMessages');
    messageInput = document.getElementById('messageInput');
    sendButton = document.getElementById('sendButton');
    typingIndicator = document.getElementById('typingIndicator');
    modeIndicator = document.getElementById('modeIndicator');
    
    // Check essential DOM elements
    if (!chatMessages || !messageInput || !sendButton) {
        console.error('Essential DOM elements not found!');
        addErrorMessage('Lỗi: Không tìm thấy các phần tử giao diện cần thiết!');
        return;
    }
    
    console.log('DOM elements initialized successfully');
    
    // Load API key from backend
    loadAPIKey().then(() => {
        initializeChatbot();
    }).catch(error => {
        console.error('Failed to load API key:', error);
        // Initialize chatbot in demo mode
        addErrorMessage(' API Key không khả dụng. Chatbot đang chạy ở chế độ demo. Vui lòng cấu hình API key để sử dụng đầy đủ tính năng.');
        initializeChatbot();
    });
});

// Load API key from backend securely
async function loadAPIKey() {
    try {
        // Try to load from backend first
        const response = await fetch('/api/get-groq-config/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            if (data.success && data.api_key) {
                window.API_KEY = data.api_key;
                console.log('API key loaded from backend successfully');
                return;
            }
        }
        
        // If backend fails, try meta tag
        const metaApiKey = document.querySelector('meta[name="groq-api-key"]');
        if (metaApiKey && metaApiKey.getAttribute('content')) {
            window.API_KEY = metaApiKey.getAttribute('content');
            console.log('API key loaded from meta tag');
            return;
        }
        
        // Last fallback: use a demo mode or throw error
        console.warn('No API key found, using demo mode');
        window.API_KEY = 'demo-mode';
        throw new Error('No valid API key found. Please configure your Groq API key.');
        
    } catch (error) {
        console.error('Error loading API key:', error);
        throw error;
    }
}

// Initialize chatbot after API key is loaded
function initializeChatbot() {
    // Add event listeners for feature cards
    document.querySelectorAll('.feature-card').forEach(card => {
        card.addEventListener('click', function() {
            const mode = this.getAttribute('data-mode');
            if (mode) {
                selectMode(mode);
            }
        });
    });
    
    // Add event listener for send button
    if (sendButton) {
        sendButton.addEventListener('click', sendMessage);
    }
    
    // Add event listener for test API button
    const testApiButton = document.getElementById('testApiButton');
    if (testApiButton) {
        testApiButton.addEventListener('click', function() {
            this.disabled = true;
            this.textContent = ' Testing...';
            testAPIConnection().finally(() => {
                this.disabled = false;
                this.textContent = ' Test API Connection';
            });
        });
    }
    
    // Add event listeners for input
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    messageInput.addEventListener('input', function() {
        sendButton.disabled = !this.value.trim();
    });
    
    // Initialize button state
    sendButton.disabled = !messageInput.value.trim();
    
    // Auto-focus input
    messageInput.focus();
    
    // Validate API key
    console.log('Validating API key...');
    if (!validateAPIKey()) {
        console.error('API key validation failed!');
        addErrorMessage('Lỗi: API key không hợp lệ!');
        return;
    }
    
    // Initialize with chat mode
    selectMode('chat');
    
    // Initialize API status indicator
    initializeAPIStatus();
    
    // Test API connection
    if (window.API_KEY && window.API_KEY !== 'YOUR_GROQ_API_KEY_HERE' && window.API_KEY !== 'demo-mode') {
        setTimeout(testAPIConnection, 1000);
    }
    
    console.log('Chatbot initialized successfully!');
}

// Get CSRF token from cookie or meta tag
function getCookie(name) {
    // First try to get from meta tag
    if (name === 'csrftoken') {
        const metaTag = document.querySelector('meta[name="csrf-token"]');
        if (metaTag) {
            return metaTag.getAttribute('content');
        }
    }
    
    // Fallback to cookie method
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Add error message to chat
function addErrorMessage(message) {
    if (chatMessages) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'message error-message';
        errorDiv.innerHTML = `
            <div class="message-content">
                <i class="fas fa-exclamation-triangle"></i> ${message}
            </div>
            <div class="message-time">${getCurrentTime()}</div>
        `;
        chatMessages.appendChild(errorDiv);
        scrollToBottom();
    } else {
        // Fallback to console if chatMessages not available
        console.error('Chat Error:', message);
        alert('Lỗi: ' + message);
    }
}

// Send message function
function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;
    
    console.log('Sending message:', message);
    
    // Add user message to chat
    addMessageToChat(message, 'user');
    
    // Clear input
    messageInput.value = '';
    sendButton.disabled = true;
    
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


function getAIPrompt(message, mode) {
    const prompts = {
        chat: `Bạn là một trợ lý AI chuyên về lập trình Python và Perl. Hãy trả lời câu hỏi sau bằng tiếng Việt một cách chi tiết và dễ hiểu, tập trung vào việc giải thích khái niệm, cung cấp ví dụ code cụ thể khi cần thiết: ${message}`,
        
        review: `Bạn là một chuyên gia review code Python và Perl. Hãy phân tích đoạn code sau và đưa ra:
1. Những điểm tốt trong code
2. Những lỗi hoặc vấn đề cần sửa
3. Gợi ý cải thiện hiệu năng và cấu trúc
4. Best practices nên áp dụng
Trả lời bằng tiếng Việt: ${message}`,
        
        assessment: `Bạn là một hệ thống đánh giá năng lực lập trình. Dựa vào thông tin học tập sau, hãy:
1. Đánh giá mức độ hiểu biết hiện tại
2. Xác định điểm mạnh và điểm yếu
3. Đề xuất lộ trình học tập tiếp theo
4. Gợi ý bài tập phù hợp với trình độ
Trả lời bằng tiếng Việt: ${message}`,
        
        quiz: `Bạn là một hệ thống tạo câu hỏi tự động. Hãy tạo ra một bộ câu hỏi (3-5 câu) về chủ đề sau:
1. Câu hỏi trắc nghiệm với 4 lựa chọn
2. Câu hỏi tự luận ngắn
3. Bài tập coding thực hành
4. Đáp án chi tiết cho từng câu
Chủ đề: ${message}. Trả lời bằng tiếng Việt.`
    };
    
    return prompts[mode] || prompts.chat;
}

// Mode selection
function selectMode(mode) {
    currentMode = mode;

    

    document.querySelectorAll('.feature-card').forEach(card => {
        card.style.opacity = '0.7';
        card.style.transform = 'scale(1)';
        card.style.boxShadow = 'none';
    });
    
    // Highlight active feature card
    const modeMap = {
        'chat': 0,
        'review': 1, 
        'assessment': 2,
        'quiz': 3
    };
    
    const activeCard = document.querySelectorAll('.feature-card')[modeMap[mode]];
    if (activeCard) {
        activeCard.style.opacity = '1';
        activeCard.style.transform = 'scale(1.05)';
        activeCard.style.boxShadow = '0 4px 12px rgba(0,0,0,0.3)';
    }
    
    // Update mode indicator and placeholder
    const modeTexts = {
        chat: 'Chế độ: Trò chuyện thông thường',
        review: 'Chế độ: Review code - Paste code để phân tích',
        assessment: 'Chế độ: Đánh giá năng lực',
        quiz: 'Chế độ: Tạo câu hỏi - Nhập chủ đề'
    };
    
    const placeholders = {
        chat: 'Nhập câu hỏi về Python hoặc Perl...',
        review: 'Paste code Python/Perl để review và phân tích...',
        assessment: 'Mô tả bài học đã học hoặc kỹ năng muốn đánh giá...',
        quiz: 'Nhập chủ đề để tạo câu hỏi (VD: Python OOP, Perl Regex)...'
    };
    
    if (modeIndicator) {
        modeIndicator.textContent = modeTexts[mode];
    }
    
    if (messageInput) {
        messageInput.placeholder = placeholders[mode];
    }
    
    // Add mode-specific intro message
    const modeIntros = {
        chat: 'Chế độ Hỗ trợ học tập đã được kích hoạt! Hỏi tôi bất cứ điều gì về Python và Perl.',
        review: 'Chế độ Review Code đã sẵn sàng! Paste code của bạn để tôi phân tích và đưa ra gợi ý cải thiện.',
        assessment: 'Chế độ Đánh giá năng lực đã kích hoạt! Mô tả những gì bạn đã học để tôi đánh giá và đề xuất lộ trình.',
        quiz: 'Chế độ Tạo Quiz đã sẵn sàng! Cho tôi biết chủ đề để tạo câu hỏi và bài tập phù hợp.'
    };
    
    
    if (chatMessages && chatMessages.children.length === 0) {
        addMessageToChat(modeIntros[mode], 'ai');
    }
    
    // Focus input
    if (messageInput) {
        messageInput.focus();
    }
}


async function sendToAI(message) {
    console.log('sendToAI called with:', message);
    console.log('window.API_KEY available:', typeof window.API_KEY !== 'undefined');
    
    // Check if API key is available
    if (typeof window.API_KEY === 'undefined' || !window.API_KEY || window.API_KEY === 'demo-mode') {
        console.warn('API_KEY is not available, showing demo response');
        showTypingIndicator();
        
        // Demo response after a short delay
        setTimeout(() => {
            hideTypingIndicator();
            const demoResponse = ` **Demo Mode Response**

Xin chào! Tôi là AI Assistant hỗ trợ học tập Python và Perl.

**Tin nhắn của bạn:** "${message}"

**Chế độ hiện tại:** ${currentMode}

 **Lưu ý:** Đây là chế độ demo. Để sử dụng AI thực, vui lòng:
1. Cấu hình API key Groq hợp lệ
2. Kiểm tra kết nối internet
3. Liên hệ quản trị viên nếu vấn đề vẫn tiếp tục

**Các tính năng có sẵn trong demo:**
-  Giao diện chatbot
-  Chuyển đổi chế độ
-  AI thực tế (cần API key)`;
            
            addFormattedMessageToChat(demoResponse, 'ai');
            setTimeout(() => addFollowUpSuggestions(currentMode), 1000);
        }, 1500);
        return;
    }
    
    showTypingIndicator();
    
    try {
        const prompt = getAIPrompt(message, currentMode);
        console.log('Sending request to Groq API...');
        
        const response = await fetch(window.API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${window.API_KEY}`
            },
            body: JSON.stringify({
                model: window.MODEL_NAME,
                messages: [
                    {
                        role: "user",
                        content: prompt
                    }
                ],
                temperature: 0.7,
                max_tokens: 1024
            })
        });

        console.log('Response status:', response.status);
        const data = await response.json();
        
        if (response.ok && data.choices && data.choices[0] && data.choices[0].message) {
            const aiResponse = data.choices[0].message.content;
            hideTypingIndicator();
            addFormattedMessageToChat(aiResponse, 'ai');
            
            
            setTimeout(() => addFollowUpSuggestions(currentMode), 1000);
        } else if (data.error) {
            throw new Error(`API Error: ${data.error.message || data.error.type || JSON.stringify(data.error)}`);
        } else {
            throw new Error('Không thể nhận được phản hồi từ AI');
        }
    } catch (error) {
        console.error('Lỗi khi gọi API:', error);
        hideTypingIndicator();
        
        let errorMessage = 'Xin lỗi, đã có lỗi xảy ra: ';
        if (error.message.includes('model')) {
            errorMessage += 'Model đã được cập nhật, hãy thử lại.';
        } else if (error.message.includes('rate_limit')) {
            errorMessage += 'Đã vượt quá giới hạn requests, thử lại sau 1 phút.';
        } else {
            errorMessage += error.message;
        }
        
        addMessageToChat(errorMessage, 'ai');
    }
}


async function testAPIConnection() {
    console.log('Testing API connection...');
    
    // Skip test if in demo mode
    if (!window.API_KEY || window.API_KEY === 'demo-mode') {
        console.log('Demo mode detected, skipping API test');
        addMessageToChat(' Chế độ demo được kích hoạt. Hãy thử gửi tin nhắn!', 'ai');
        return;
    }
    
    try {
        const response = await fetch(window.API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${window.API_KEY}`
            },
            body: JSON.stringify({
                model: window.MODEL_NAME,
                messages: [
                    {
                        role: "user",
                        content: "Hello, test message"
                    }
                ],
                max_tokens: 10,
                temperature: 0.1
            })
        });
        
        const data = await response.json();
        
        if (response.ok && data.choices && data.choices[0]) {
            console.log('API connection successful!');
            addMessageToChat(' AI đã sẵn sàng! Bạn có thể bắt đầu trò chuyện.', 'ai');
            updateAPIStatus('success', 'API connection successful');
        } else {
            const errorMsg = data.error?.message || data.error?.type || 'Unknown error';
            throw new Error(`API Error: ${errorMsg}`);
        }
    } catch (error) {
        console.error('API test failed:', error);
        
        let userMessage = ' Không thể kết nối API. ';
        if (error.message.includes('Invalid API Key') || error.message.includes('401')) {
            userMessage += 'API Key không hợp lệ hoặc đã hết hạn. Vui lòng kiểm tra lại API key.';
        } else if (error.message.includes('rate_limit') || error.message.includes('429')) {
            userMessage += 'Đã vượt quá giới hạn API. Vui lòng thử lại sau.';
        } else if (error.message.includes('network') || error.name === 'TypeError') {
            userMessage += 'Lỗi kết nối mạng. Vui lòng kiểm tra internet.';
        } else {
            userMessage += `Lỗi: ${error.message}`;
        }
        
        addMessageToChat(userMessage, 'ai');
        
        // Update API status and switch to demo mode on API failure
        updateAPIStatus('error', `API Error: ${error.message}`);
        window.API_KEY = 'demo-mode';
        console.log('Switched to demo mode due to API failure');
    }
}

// Validate API key
function validateAPIKey() {
    console.log('Validating API key...');
    
    if (typeof window.API_KEY === 'undefined') {
        console.error('API_KEY is not defined!');
        return false;
    }
    
    // Allow demo mode
    if (window.API_KEY === 'demo-mode') {
        console.log('Demo mode detected');
        return true;
    }
    
    console.log('- Key length:', window.API_KEY.length);
    console.log('- Key starts with gsk_:', window.API_KEY.startsWith('gsk_'));
    console.log('- API URL:', window.API_URL);
    console.log('- Model:', window.MODEL_NAME);
    
    if (window.API_KEY.length !== 56) {
        console.warn('API key length seems incorrect. Groq keys should be 56 characters.');
    }
    
    if (!window.API_KEY.startsWith('gsk_')) {
        console.warn('API key should start with "gsk_"');
    }
    
    return true;
}

// Add follow-up suggestions
function addFollowUpSuggestions(mode) {
    const suggestions = {
        chat: [
            'Giải thích thêm về chủ đề này',
            'Cho ví dụ thực tế',
            'So sánh với ngôn ngữ khác'
        ],
        review: [
            'Tối ưu hóa code này',
            'Kiểm tra security issues',
            'Refactor theo best practices'
        ],
        assessment: [
            'Đề xuất bài tập luyện tập',
            'Tạo lộ trình học chi tiết',
            'Đánh giá lại sau 1 tuần'
        ],
        quiz: [
            'Tạo thêm câu hỏi nâng cao',
            'Tạo bài tập thực hành',
            'Giải thích đáp án chi tiết'
        ]
    };
    
    const followUpDiv = document.createElement('div');
    followUpDiv.className = 'follow-up-suggestions';
    followUpDiv.innerHTML = `
        <p><strong>Tiếp tục với:</strong></p>
        <div class="suggestion-buttons">
            ${suggestions[mode].map(suggestion => 
                `<button class="suggestion-btn small" onclick="sendQuickMessage('${suggestion}')">${suggestion}</button>`
            ).join('')}
        </div>
    `;
    
    chatMessages.appendChild(followUpDiv);
    scrollToBottom();
}

// Enhanced message display
function addFormattedMessageToChat(message, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    // Enhanced formatting with syntax highlighting
    const formattedMessage = formatMessageAdvanced(message);
    messageContent.innerHTML = formattedMessage;
    
    const messageTime = document.createElement('div');
    messageTime.className = 'message-time';
    messageTime.textContent = getCurrentTime();
    
    messageDiv.appendChild(messageContent);
    messageDiv.appendChild(messageTime);
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}


function formatMessageAdvanced(text) {
    
    text = text.replace(/```(\w+)?\n([\s\S]*?)```/g, (match, lang, code) => {
        const language = lang || 'text';
        return `<div class="code-block">
            <div class="code-header">
                <span class="code-lang">${language}</span>
                <button class="copy-btn" onclick="copyCode(this)">Copy</button>
            </div>
            <pre><code class="language-${language}">${code.trim()}</code></pre>
        </div>`;
    });
    
    
    text = text.replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>');
    
    
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    
    text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
    
    
    text = text.replace(/\n/g, '<br>');
    
    return text;
}

// Copy code function
function copyCode(button) {
    const codeBlock = button.parentElement.nextElementSibling;
    const code = codeBlock.textContent;
    
    navigator.clipboard.writeText(code).then(() => {
        button.textContent = 'Copied!';
        setTimeout(() => {
            button.textContent = 'Copy';
        }, 2000);
    });
}

// Show typing indicator
function showTypingIndicator() {
    if (typingIndicator) {
        typingIndicator.style.display = 'flex';
        scrollToBottom();
    }
}

// Hide typing indicator
function hideTypingIndicator() {
    if (typingIndicator) {
        typingIndicator.style.display = 'none';
    }
}

// Get current time
function getCurrentTime() {
    try {
        const now = new Date();
        return now.toLocaleTimeString('vi-VN', {
            hour: '2-digit',
            minute: '2-digit'
        });
    } catch (error) {
        console.error('Error getting current time:', error);
        const now = new Date();
        return now.getHours().toString().padStart(2, '0') + ':' + 
               now.getMinutes().toString().padStart(2, '0');
    }
}

// Scroll to bottom
function scrollToBottom() {
    if (chatMessages) {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

console.log('Chatbot script loaded successfully!');

// Global error handler
window.addEventListener('error', function(event) {
    console.error('Global JavaScript Error:', event.error);
    console.error('Error details:', {
        message: event.message,
        filename: event.filename,
        lineno: event.lineno,
        colno: event.colno
    });
    
    // Show user-friendly error message
    if (typeof addErrorMessage === 'function') {
        addErrorMessage('Đã xảy ra lỗi JavaScript. Vui lòng refresh trang và thử lại.');
    }
});

// Global function to make selectMode available
window.selectMode = selectMode;
window.sendMessage = sendMessage;
window.sendQuickMessage = sendQuickMessage;

// API Status Indicator
function updateAPIStatus(status, message) {
    const statusColors = {
        'success': '#4CAF50',
        'error': '#f44336',
        'warning': '#ff9800',
        'info': '#2196F3'
    };
    
    const testApiButton = document.getElementById('testApiButton');
    if (testApiButton) {
        testApiButton.style.background = statusColors[status] || '#666';
        if (message) {
            testApiButton.title = message;
        }
    }
}

// Initialize API status on load
function initializeAPIStatus() {
    if (window.API_KEY && window.API_KEY !== 'demo-mode') {
        updateAPIStatus('info', 'API Key loaded, click to test connection');
    } else {
        updateAPIStatus('warning', 'Demo mode - No API key available');
    }
}
