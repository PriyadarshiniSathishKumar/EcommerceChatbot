// Chat functionality for ShopMate AI

let chatContainer;
let messageInput;
let sendButton;
let typingIndicator;
let isProcessing = false;

// Initialize chat functionality
function initializeChat() {
    // Get DOM elements
    chatContainer = document.getElementById('chatMessages');
    messageInput = document.getElementById('messageInput');
    sendButton = document.getElementById('sendBtn');
    typingIndicator = document.getElementById('typingIndicator');
    
    // Set up event listeners
    setupEventListeners();
    
    // Scroll to bottom of chat
    scrollToBottom();
    
    // Focus on input
    messageInput.focus();
    
    console.log('Chat initialized successfully');
}

function setupEventListeners() {
    // Message form submission
    const messageForm = document.getElementById('messageForm');
    messageForm.addEventListener('submit', handleMessageSubmit);
    
    // Enter key to send message
    messageInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            messageForm.dispatchEvent(new Event('submit'));
        }
    });
    
    // Auto-resize textarea (if converted to textarea later)
    messageInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = this.scrollHeight + 'px';
    });
    
    // Voice input button (placeholder for future implementation)
    const voiceBtn = document.getElementById('voiceBtn');
    if (voiceBtn) {
        voiceBtn.addEventListener('click', handleVoiceInput);
    }
}

async function handleMessageSubmit(e) {
    e.preventDefault();
    
    const message = messageInput.value.trim();
    if (!message || isProcessing) {
        return;
    }
    
    // Clear input and disable form
    messageInput.value = '';
    setProcessingState(true);
    
    // Add user message to chat
    addMessageToChat(message, 'user');
    
    // Show typing indicator
    showTypingIndicator();
    
    try {
        // Send message to backend
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Hide typing indicator
        hideTypingIndicator();
        
        // Add bot response to chat
        addBotResponseToChat(data.bot_response);
        
        // Update cart count if needed
        updateCartCount();
        
    } catch (error) {
        console.error('Error sending message:', error);
        hideTypingIndicator();
        
        // Show error message
        addMessageToChat(
            "Sorry, I'm having trouble connecting right now. Please try again in a moment.",
            'bot',
            'error'
        );
        
        // Show notification
        if (window.ShopMateApp) {
            window.ShopMateApp.showNotification('Failed to send message. Please try again.', 'error');
        }
    }
    
    setProcessingState(false);
}

function addMessageToChat(message, sender, type = 'normal') {
    const messageContainer = document.createElement('div');
    messageContainer.className = `message ${sender}-message`;
    
    const timestamp = new Date().toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
    });
    
    if (sender === 'user') {
        messageContainer.innerHTML = `
            <div class="flex justify-end">
                <div class="bg-indigo-600 text-white rounded-2xl rounded-tr-sm px-4 py-3 max-w-md shadow-lg">
                    <p class="whitespace-pre-wrap">${escapeHtml(message)}</p>
                    <div class="text-xs text-indigo-200 mt-1">${timestamp}</div>
                </div>
                <div class="w-8 h-8 bg-indigo-600 rounded-full flex items-center justify-center ml-3 flex-shrink-0">
                    <i class="fas fa-user text-white text-sm"></i>
                </div>
            </div>
        `;
    } else {
        const bgColor = type === 'error' ? 'bg-red-50 border-red-200' : 'bg-white border';
        const textColor = type === 'error' ? 'text-red-700' : '';
        
        messageContainer.innerHTML = `
            <div class="flex">
                <div class="w-8 h-8 bg-gray-600 rounded-full flex items-center justify-center mr-3 flex-shrink-0">
                    <i class="fas fa-robot text-white text-sm"></i>
                </div>
                <div class="${bgColor} rounded-2xl rounded-tl-sm px-4 py-3 max-w-md shadow-lg ${textColor}">
                    <div class="prose prose-sm max-w-none">
                        ${formatMessage(message)}
                    </div>
                    <div class="text-xs text-gray-500 mt-1">${timestamp}</div>
                </div>
            </div>
        `;
    }
    
    chatContainer.appendChild(messageContainer);
    scrollToBottom();
}

function addBotResponseToChat(response) {
    const messageContainer = document.createElement('div');
    messageContainer.className = 'message bot-message';
    
    const timestamp = new Date().toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
    });
    
    messageContainer.innerHTML = `
        <div class="flex">
            <div class="w-8 h-8 bg-gray-600 rounded-full flex items-center justify-center mr-3 flex-shrink-0">
                <i class="fas fa-robot text-white text-sm"></i>
            </div>
            <div class="bg-white rounded-2xl rounded-tl-sm px-4 py-3 max-w-md shadow-lg border">
                <div class="prose prose-sm max-w-none">
                    ${formatBotMessage(response)}
                </div>
                <div class="text-xs text-gray-500 mt-1">${timestamp}</div>
            </div>
        </div>
    `;
    
    chatContainer.appendChild(messageContainer);
    
    // Add product cards if products are included
    if (response.products && response.products.length > 0) {
        addProductCards(response.products);
    }
    
    scrollToBottom();
}

function formatBotMessage(response) {
    let message = response.message;
    
    // Convert markdown-style formatting to HTML
    message = message.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    message = message.replace(/\*(.*?)\*/g, '<em>$1</em>');
    message = message.replace(/\n/g, '<br>');
    
    // Convert links to clickable buttons
    message = message.replace(/\[Add to Cart\]\(javascript:addToCart\((\d+)\)\)/g, 
        '<button class="add-to-cart-btn mt-2" onclick="addToCart($1)">Add to Cart</button>');
    
    return message;
}

function addProductCards(products) {
    const productsContainer = document.createElement('div');
    productsContainer.className = 'products-grid mt-4';
    
    products.forEach(product => {
        const productCard = document.createElement('div');
        productCard.className = 'product-card';
        productCard.innerHTML = `
            <div class="bg-white border rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow duration-200">
                <h4 class="font-medium text-gray-900 mb-2">${escapeHtml(product.title)}</h4>
                <p class="text-lg font-bold text-indigo-600 mb-3">$${product.price.toFixed(2)}</p>
                <button class="add-to-cart-btn w-full bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg transition-colors duration-200 text-sm font-medium" 
                        onclick="addToCart(${product.id})">
                    <i class="fas fa-cart-plus mr-2"></i>Add to Cart
                </button>
            </div>
        `;
        productsContainer.appendChild(productCard);
    });
    
    const messageContainer = document.createElement('div');
    messageContainer.className = 'message bot-message';
    messageContainer.innerHTML = `
        <div class="flex">
            <div class="w-8 h-8 bg-gray-600 rounded-full flex items-center justify-center mr-3 flex-shrink-0">
                <i class="fas fa-robot text-white text-sm"></i>
            </div>
            <div class="max-w-2xl">
                ${productsContainer.outerHTML}
            </div>
        </div>
    `;
    
    chatContainer.appendChild(messageContainer);
    scrollToBottom();
}

async function addToCart(productId) {
    try {
        const response = await fetch('/api/add-to-cart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                product_id: productId,
                quantity: 1 
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.success) {
            // Update cart count
            updateCartCount();
            
            // Show success message
            if (window.ShopMateApp) {
                window.ShopMateApp.showNotification(data.message, 'success');
            }
            
            // Add confirmation message to chat
            addMessageToChat(`✅ ${data.message}`, 'bot');
        }
        
    } catch (error) {
        console.error('Error adding to cart:', error);
        if (window.ShopMateApp) {
            window.ShopMateApp.showNotification('Failed to add item to cart', 'error');
        }
    }
}

async function updateCartCount() {
    try {
        const response = await fetch('/api/cart-count');
        const data = await response.json();
        
        const cartCountElement = document.getElementById('cartCount');
        if (cartCountElement) {
            cartCountElement.textContent = data.count;
            
            // Add pulse animation
            cartCountElement.classList.add('pulse-animation');
            setTimeout(() => {
                cartCountElement.classList.remove('pulse-animation');
            }, 2000);
        }
    } catch (error) {
        console.error('Error updating cart count:', error);
    }
}

function showTypingIndicator() {
    if (typingIndicator) {
        typingIndicator.classList.remove('hidden');
        scrollToBottom();
    }
}

function hideTypingIndicator() {
    if (typingIndicator) {
        typingIndicator.classList.add('hidden');
    }
}

function setProcessingState(processing) {
    isProcessing = processing;
    sendButton.disabled = processing;
    messageInput.disabled = processing;
    
    if (processing) {
        sendButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    } else {
        sendButton.innerHTML = '<i class="fas fa-paper-plane"></i>';
        messageInput.focus();
    }
}

function scrollToBottom() {
    setTimeout(() => {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }, 100);
}

function formatMessage(message) {
    // Basic message formatting
    return message.replace(/\n/g, '<br>');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Voice input placeholder
function handleVoiceInput() {
    if (window.ShopMateApp) {
        window.ShopMateApp.showNotification('Voice input coming soon!', 'info');
    }
}

// Export chat history
async function exportChatHistory() {
    try {
        const messages = document.querySelectorAll('.message');
        let chatHistory = 'ShopMate AI Chat History\n';
        chatHistory += '=' .repeat(30) + '\n\n';
        
        messages.forEach(message => {
            const isUser = message.classList.contains('user-message');
            const sender = isUser ? 'You' : 'ShopMate AI';
            const content = message.querySelector('p, .prose')?.textContent || '';
            const timestamp = message.querySelector('.text-xs')?.textContent || '';
            
            if (content.trim()) {
                chatHistory += `[${timestamp}] ${sender}: ${content}\n\n`;
            }
        });
        
        // Create and download file
        const blob = new Blob([chatHistory], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `shopmate-chat-${new Date().toISOString().split('T')[0]}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        if (window.ShopMateApp) {
            window.ShopMateApp.showNotification('Chat history exported successfully!', 'success');
        }
        
    } catch (error) {
        console.error('Error exporting chat:', error);
        if (window.ShopMateApp) {
            window.ShopMateApp.showNotification('Failed to export chat history', 'error');
        }
    }
}

// Clear chat history
async function clearChatHistory() {
    try {
        const response = await fetch('/api/clear-chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (response.ok) {
            // Clear messages from DOM
            const messages = chatContainer.querySelectorAll('.message');
            messages.forEach(msg => msg.remove());
            
            // Add welcome message
            addMessageToChat(
                `👋 **Hello!**\n\nWelcome back to ShopMate AI! I'm here to help you find amazing products.\n\nYou can try:\n• "Show me electronics"\n• "Find books under $30"\n• "Search for headphones"\n• "Show my cart"\n\nWhat are you looking for today? 🛍️`,
                'bot'
            );
            
            if (window.ShopMateApp) {
                window.ShopMateApp.showNotification('Chat history cleared!', 'success');
            }
        }
        
    } catch (error) {
        console.error('Error clearing chat:', error);
        if (window.ShopMateApp) {
            window.ShopMateApp.showNotification('Failed to clear chat history', 'error');
        }
    }
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter to send message
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        document.getElementById('messageForm').dispatchEvent(new Event('submit'));
    }
    
    // Escape to clear input
    if (e.key === 'Escape' && messageInput) {
        messageInput.value = '';
        messageInput.blur();
    }
});

// Auto-save draft messages
let draftTimeout;
if (messageInput) {
    messageInput.addEventListener('input', function() {
        clearTimeout(draftTimeout);
        draftTimeout = setTimeout(() => {
            localStorage.setItem('shopmate-draft', this.value);
        }, 500);
    });
    
    // Restore draft on load
    const draft = localStorage.getItem('shopmate-draft');
    if (draft) {
        messageInput.value = draft;
    }
    
    // Clear draft on send
    document.getElementById('messageForm')?.addEventListener('submit', function() {
        localStorage.removeItem('shopmate-draft');
    });
}

// Export functions for global access
window.addToCart = addToCart;
window.exportChatHistory = exportChatHistory;
window.clearChatHistory = clearChatHistory;
window.initializeChat = initializeChat;
