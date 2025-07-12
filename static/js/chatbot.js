// Chatbot JavaScript Functions - Enhanced for CS466 Project
let chatMessages = document.getElementById('chatMessages');
let messageInput = document.getElementById('messageInput');
let sendButton = document.getElementById('sendButton');
let typingIndicator = document.getElementById('typingIndicator');
let modeIndicator = document.getElementById('modeIndicator');

// Current mode tracking
let currentMode = 'chat'; // chat, review, assessment, quiz

// API Configuration - Using Groq API (Free alternative)
 // Lấy từ https://console.groq.com/keys
const API_URL = 'https://api.groq.com/openai/v1/chat/completions';
const MODEL_NAME = 'llama-3.1-8b-instant'; // Updated to available model

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    // Auto-focus input
    messageInput.focus();
    
    // Test API if key is configured
    if (API_KEY !== 'YOUR_GROQ_API_KEY_HERE') {
        setTimeout(testAPIConnection, 1000);
    }
    
    // Validate API key
    validateAPIKey();
    
    // Initialize with chat mode
    selectMode('chat');
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

// Enhanced AI prompt templates for different modes
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

// Mode selection functions
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
    
    // Update tool buttons
    document.querySelectorAll('.tool-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Update mode indicator and placeholder
    const modeTexts = {
        chat: ' Chế độ: Trò chuyện thông thường',
        review: ' Chế độ: Review code - Paste code để phân tích',
        assessment: ' Chế độ: Đánh giá năng lực',
        quiz: ' Chế độ: Tạo câu hỏi - Nhập chủ đề'
    };
    
    const placeholders = {
        chat: 'Nhập câu hỏi về Python hoặc Perl...',
        review: 'Paste code Python/Perl để review và phân tích...',
        assessment: 'Mô tả bài học đã học hoặc kỹ năng muốn đánh giá...',
        quiz: 'Nhập chủ đề để tạo câu hỏi (VD: Python OOP, Perl Regex)...'
    };
    
    modeIndicator.textContent = modeTexts[mode];
    messageInput.placeholder = placeholders[mode];
    
    // Add mode-specific intro message
    const modeIntros = {
        chat: ' Chế độ Hỗ trợ học tập đã được kích hoạt! Hỏi tôi bất cứ điều gì về Python và Perl.',
        review: ' Chế độ Review Code đã sẵn sàng! Paste code của bạn để tôi phân tích và đưa ra gợi ý cải thiện.',
        assessment: ' Chế độ Đánh giá năng lực đã kích hoạt! Mô tả những gì bạn đã học để tôi đánh giá và đề xuất lộ trình.',
        quiz: ' Chế độ Tạo Quiz đã sẵn sàng! Cho tôi biết chủ đề để tạo câu hỏi và bài tập phù hợp.'
    };
    
    // Only add intro if chat is empty
    if (chatMessages.children.length === 0) {
        addMessageToChat(modeIntros[mode], 'ai');
    }
    
    // Focus input
    messageInput.focus();
}

// Toggle features panel
function toggleFeatures() {
    const panel = document.getElementById('featuresPanel');
    panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
}

// Switch tabs in features panel
function switchTab(tab) {
    selectMode(tab);
    
    // Update tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    event.target.classList.add('active');
}

// Attach code function
function attachCode() {
    selectMode('review');
    
    // Add code template if input is empty
    if (!messageInput.value.trim()) {
        messageInput.value = '```python\n# Paste your code here\n\n```';
        // Position cursor between the code blocks
        messageInput.setSelectionRange(20, 20);
    }
}

// Send to AI function (Groq API) - Enhanced with debugging
async function sendToAI(message) {
    showTypingIndicator();
    
    try {
        const prompt = getAIPrompt(message, currentMode);
        console.log('Sending request to Groq API...', { prompt: prompt.substring(0, 100) + '...', model: MODEL_NAME });
        
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
                max_tokens: 1024 // Reduced for faster response
            })
        });

        console.log('Response status:', response.status);
        const data = await response.json();
        console.log('Response received:', data.choices ? ' Success' : ' No choices');
        
        if (response.ok && data.choices && data.choices[0] && data.choices[0].message) {
            const aiResponse = data.choices[0].message.content;
            hideTypingIndicator();
            addFormattedMessageToChat(aiResponse, 'ai');
            
            // Add follow-up suggestions based on mode
            setTimeout(() => addFollowUpSuggestions(currentMode), 1000);
        } else if (data.error) {
            throw new Error(`API Error: ${data.error.message || data.error.type || JSON.stringify(data.error)}`);
        } else {
            throw new Error('Không thể nhận được phản hồi từ AI');
        }
    } catch (error) {
        console.error(' Lỗi khi gọi API:', error);
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

// Test API connection (Groq) - Enhanced debugging
async function testAPIConnection() {
    const testButton = document.querySelector('.status-indicator');
    if (!testButton) return;
    
    testButton.textContent = ' Testing...';
    testButton.className = 'status-indicator loading';
    
    try {
        console.log('Testing Groq API connection...', { url: API_URL, key: API_KEY.substring(0, 10) + '...', model: MODEL_NAME });
        
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
        
        console.log('Test response status:', response.status);
        const data = await response.json();
        console.log('Test response data:', data);
        
        if (response.ok && data.choices && data.choices[0]) {
            testButton.textContent = ' Llama 3.1-8B';
            testButton.className = 'status-indicator online';
            console.log(' API connection successful!');
            addMessageToChat(' AI đã sẵn sàng! Bạn có thể bắt đầu trò chuyện.', 'ai');
        } else {
            throw new Error(`API Error: ${data.error?.message || JSON.stringify(data)}`);
        }
    } catch (error) {
        console.error(' API test failed:', error);
        testButton.textContent = ' Lỗi API';
        testButton.className = 'status-indicator offline';
        
        // Show helpful error message
        let errorMessage = 'Không thể kết nối API. ';
        if (error.message.includes('model')) {
            errorMessage += 'Lỗi model đã được sửa, hãy refresh trang.';
        } else if (error.message.includes('401')) {
            errorMessage += 'API key không hợp lệ.';
        } else if (error.message.includes('429')) {
            errorMessage += 'Đã vượt quá giới hạn requests.';
        } else {
            errorMessage += error.message;
        }
        
        addMessageToChat(`🔍 ${errorMessage}`, 'ai');
    }
}

// Manual API key validation
function validateAPIKey() {
    console.log('API Key validation:');
    console.log('- Key length:', API_KEY.length);
    console.log('- Key starts with gsk_:', API_KEY.startsWith('gsk_'));
    console.log('- API URL:', API_URL);
    console.log('- Model:', MODEL_NAME);
    
    if (API_KEY.length !== 56) {
        console.warn(' API key length seems incorrect. Groq keys should be 56 characters.');
    }
    
    if (!API_KEY.startsWith('gsk_')) {
        console.warn(' API key should start with "gsk_"');
    }
}

// Call validation on load
document.addEventListener('DOMContentLoaded', function() {
    // ...existing code...
    
    // Validate API key
    validateAPIKey();
    
    // ...existing code...
});

// Add follow-up suggestions based on mode
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
        <p><strong> Tiếp tục với:</strong></p>
        <div class="suggestion-buttons">
            ${suggestions[mode].map(suggestion => 
                `<button class="suggestion-btn small" onclick="sendQuickMessage('${suggestion}')">${suggestion}</button>`
            ).join('')}
        </div>
    `;
    
    chatMessages.appendChild(followUpDiv);
    scrollToBottom();
}

// Enhanced message display with code highlighting
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

// Advanced message formatting with syntax highlighting
function formatMessageAdvanced(text) {
    // Convert code blocks with language detection
    text = text.replace(/```(\w+)?\n([\s\S]*?)```/g, (match, lang, code) => {
        const language = lang || 'text';
        return `<div class="code-block">
            <div class="code-header">
                <span class="code-lang">${language}</span>
                <button class="copy-btn" onclick="copyCode(this)"> Copy</button>
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
    
    // Convert numbered lists
    text = text.replace(/^\d+\.\s(.+)$/gm, '<li class="numbered-item">$1</li>');
    
    // Convert bullet points
    text = text.replace(/^[-•]\s(.+)$/gm, '<li class="bullet-item">$1</li>');
    
    // Convert line breaks
    text = text.replace(/\n/g, '<br>');
    
    return text;
}

// Copy code function
function copyCode(button) {
    const codeBlock = button.parentElement.nextElementSibling;
    const code = codeBlock.textContent;
    
    navigator.clipboard.writeText(code).then(() => {
        button.textContent = ' Copied!';
        setTimeout(() => {
            button.innerHTML = ' Copy';
        }, 2000);
    });
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
