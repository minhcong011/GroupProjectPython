// Chatbot JavaScript Functions - Fixed Version
console.log('Loading chatbot.js...');

// API Configuration - Must be defined first
const API_KEY = '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';
const API_URL = 'https://api.groq.com/openai/v1/chat/completions';
const MODEL_NAME = 'llama-3.1-8b-instant';

// Global variables
let chatMessages, messageInput, sendButton, typingIndicator, modeIndicator;
let currentMode = 'chat';

console.log('API_KEY defined:', typeof API_KEY !== 'undefined');
console.log('API_KEY length:', API_KEY.length);

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing...');
    
    // Initialize DOM elements
    chatMessages = document.getElementById('chatMessages');
    messageInput = document.getElementById('messageInput');
    sendButton = document.getElementById('sendButton');
    typingIndicator = document.getElementById('typingIndicator');
    modeIndicator = document.getElementById('modeIndicator');
    
    // Check if all elements exist
    if (!chatMessages || !messageInput || !sendButton) {
        console.error('Essential DOM elements not found!');
        return;
    }
    
    console.log('DOM elements initialized successfully');
    
    // Add event listeners
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
        return;
    }
    
    // Test API connection
    if (API_KEY && API_KEY !== 'YOUR_GROQ_API_KEY_HERE') {
        setTimeout(testAPIConnection, 1000);
    }
    
    // Initialize with chat mode
    selectMode('chat');
    
    console.log('Chatbot initialized successfully!');
});

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

// Enhanced AI prompt templates
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
    
    // Update feature cards styling
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
    
    // Only add intro if chat is empty
    if (chatMessages && chatMessages.children.length === 0) {
        addMessageToChat(modeIntros[mode], 'ai');
    }
    
    // Focus input
    if (messageInput) {
        messageInput.focus();
    }
}

// Send to AI function
async function sendToAI(message) {
    console.log('sendToAI called with:', message);
    console.log('API_KEY available:', typeof API_KEY !== 'undefined');
    
    if (typeof API_KEY === 'undefined' || !API_KEY) {
        console.error('API_KEY is not defined!');
        addMessageToChat('Lỗi: API_KEY chưa được cấu hình!', 'ai');
        return;
    }
    
    showTypingIndicator();
    
    try {
        const prompt = getAIPrompt(message, currentMode);
        console.log('Sending request to Groq API...');
        
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${API_KEY}`
            },
            body: JSON.stringify({
                model: MODEL_NAME,
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
            
            // Add follow-up suggestions
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

// Test API connection
async function testAPIConnection() {
    console.log('Testing API connection...');
    
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${API_KEY}`
            },
            body: JSON.stringify({
                model: MODEL_NAME,
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
            addMessageToChat('AI đã sẵn sàng! Bạn có thể bắt đầu trò chuyện.', 'ai');
        } else {
            throw new Error(`API Error: ${data.error?.message || JSON.stringify(data)}`);
        }
    } catch (error) {
        console.error('API test failed:', error);
        addMessageToChat('Không thể kết nối API. Vui lòng kiểm tra lại.', 'ai');
    }
}

// Validate API key
function validateAPIKey() {
    console.log('Validating API key...');
    
    if (typeof API_KEY === 'undefined') {
        console.error('API_KEY is not defined!');
        return false;
    }
    
    console.log('- Key length:', API_KEY.length);
    console.log('- Key starts with gsk_:', API_KEY.startsWith('gsk_'));
    console.log('- API URL:', API_URL);
    console.log('- Model:', MODEL_NAME);
    
    if (API_KEY.length !== 56) {
        console.warn('API key length seems incorrect. Groq keys should be 56 characters.');
    }
    
    if (!API_KEY.startsWith('gsk_')) {
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

// Advanced message formatting
function formatMessageAdvanced(text) {
    // Convert code blocks
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
    
    // Convert inline code
    text = text.replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>');
    
    // Convert bold text
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Convert italic text
    text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
    
    // Convert line breaks
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
    const now = new Date();
    return now.toLocaleTimeString('vi-VN', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Scroll to bottom
function scrollToBottom() {
    if (chatMessages) {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

console.log('Chatbot script loaded successfully!');
