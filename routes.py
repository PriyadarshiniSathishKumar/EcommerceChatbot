"""
Flask routes for ShopMate AI - Interactive E-commerce Sales Chatbot

This module handles all web routes including:
- User authentication (login, register, logout)
- Chat interface and API endpoints
- Product search and cart management
- Session management and user interactions
"""

from flask import render_template, request, redirect, url_for, session, flash, jsonify
from app import app, db
from models import User, Product, CartItem, ChatSession, ChatMessage
import uuid
import re
from datetime import datetime

@app.route('/')
def index():
    """
    Home page route - displays the landing page with features and call-to-action.
    
    Returns:
        Rendered index.html template
    """
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login - both GET (show form) and POST (process login).
    
    POST: Validates credentials and creates user session
    GET: Displays login form
    
    Returns:
        Redirect to chat on success, login form on failure/GET
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Find user by username
        user = User.query.filter_by(username=username).first()
        
        # Verify credentials
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('chat'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle user registration - creates new user account.
    
    POST: Validates input and creates new user
    GET: Displays registration form (handled by login.html template)
    
    Returns:
        Redirect to chat on success, login form on failure/GET
    """
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('login.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return render_template('login.html')
        
        # Create new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        # Auto-login after registration
        session['user_id'] = new_user.id
        session['username'] = new_user.username
        flash('Registration successful!', 'success')
        return redirect(url_for('chat'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """
    Handle user logout - clears session and redirects to home.
    
    Returns:
        Redirect to index page with logout confirmation
    """
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/chat')
def chat():
    """
    Main chat interface route - displays chat UI with history and cart info.
    Requires user authentication.
    
    Returns:
        Rendered chat.html template with messages and cart count
        Redirect to login if not authenticated
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Create or get chat session for this user
    session_token = session.get('chat_token')
    if not session_token:
        # Generate new session token
        session_token = str(uuid.uuid4())
        session['chat_token'] = session_token
        
        # Create new chat session in database
        chat_session = ChatSession(
            user_id=session['user_id'],
            session_token=session_token
        )
        db.session.add(chat_session)
        db.session.commit()
    
    # Get existing chat history for this session
    chat_session = ChatSession.query.filter_by(session_token=session_token).first()
    if chat_session:
        messages = ChatMessage.query.filter_by(session_id=chat_session.id).order_by(ChatMessage.timestamp).all()
    else:
        messages = []
    
    # Get current cart items count for display
    cart_count = CartItem.query.filter_by(user_id=session['user_id']).count()
    
    return render_template('chat.html', messages=messages, cart_count=cart_count)

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """
    API endpoint for processing chat messages.
    Handles user input, generates bot responses, and saves conversation history.
    
    Returns:
        JSON response with user message, bot response, and timestamp
        401 if not authenticated, 400 if message is empty
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({'error': 'Empty message'}), 400
    
    # Get current chat session
    session_token = session.get('chat_token')
    chat_session = ChatSession.query.filter_by(session_token=session_token).first()
    
    if not chat_session:
        return jsonify({'error': 'No chat session found'}), 400
    
    # Save user message to database
    user_msg = ChatMessage(
        session_id=chat_session.id,
        message=user_message,
        sender='user'
    )
    db.session.add(user_msg)
    
    # Process message and generate bot response using NLP logic
    bot_response = process_chat_message(user_message, session['user_id'])
    
    # Save bot response to database
    bot_msg = ChatMessage(
        session_id=chat_session.id,
        message=bot_response['message'],
        sender='bot'
    )
    db.session.add(bot_msg)
    db.session.commit()
    
    return jsonify({
        'user_message': user_message,
        'bot_response': bot_response,
        'timestamp': datetime.utcnow().isoformat()
    })

def process_chat_message(message, user_id):
    """Process user message and return appropriate bot response"""
    message_lower = message.lower()
    
    # Greeting patterns
    if any(word in message_lower for word in ['hello', 'hi', 'hey', 'start']):
        return {
            'message': "Hi there! 👋 Welcome to ShopMate AI! I'm here to help you find amazing products. You can try:\n\n• 'Show me electronics'\n• 'Find books under $20'\n• 'Search for headphones'\n• 'Show my cart'\n\nWhat are you looking for today?",
            'type': 'greeting'
        }
    
    # Search patterns
    if any(word in message_lower for word in ['show', 'find', 'search', 'looking', 'want']):
        return search_products(message_lower, user_id)
    
    # Cart patterns
    if any(word in message_lower for word in ['cart', 'basket', 'added']):
        return show_cart(user_id)
    
    # Add to cart patterns - handled via frontend addToCart function
    if 'add to cart' in message_lower:
        return {
            'message': "I can help you add items to your cart! When I show you products, just click the 'Add to Cart' button on any item you like.",
            'type': 'help'
        }
    
    # Price filter patterns
    if any(word in message_lower for word in ['under', 'below', 'less than', 'cheaper']):
        return filter_by_price(message_lower, user_id)
    
    # Category patterns
    categories = ['electronics', 'books', 'textiles', 'clothing', 'accessories']
    for category in categories:
        if category in message_lower:
            return get_products_by_category(category, user_id)
    
    # Help patterns
    if any(word in message_lower for word in ['help', 'what can you do', 'commands']):
        return {
            'message': "I can help you with:\n\n🛍️ **Product Search:**\n• 'Show me electronics'\n• 'Find books under $25'\n• 'Search for wireless headphones'\n\n🛒 **Shopping Cart:**\n• 'Show my cart'\n• 'Add [product] to cart'\n\n📊 **Filters & Sorting:**\n• 'Sort by price low to high'\n• 'Filter electronics under $100'\n\n💬 **Other Commands:**\n• 'Clear chat' - Start fresh\n• 'Help' - Show this menu\n\nJust tell me what you're looking for!",
            'type': 'help'
        }
    
    # Default response
    return {
        'message': "I'm not sure I understand that. Try asking me to:\n• Show products by category\n• Search for specific items\n• Check your cart\n• Filter by price\n\nType 'help' for more options!",
        'type': 'default'
    }

def search_products(query, user_id):
    """
    Search products based on user query using keyword matching and category filters.
    
    Args:
        query (str): User's search query in lowercase
        user_id (int): ID of the user making the search
        
    Returns:
        dict: Response containing search results or error message
    """
    # Extract search terms from the query
    search_terms = re.findall(r'\b\w+\b', query)
    
    # Start with base query - get all products
    products_query = Product.query
    category_found = False
    search_applied = False
    
    # Apply category filters first
    for term in search_terms:
        if term in ['electronics', 'electronic', 'tech', 'gadget', 'gadgets']:
            products_query = products_query.filter(Product.category == 'Electronics')
            category_found = True
            search_applied = True
            break
        elif term in ['books', 'book', 'reading', 'novel', 'textbook']:
            products_query = products_query.filter(Product.category == 'Books')
            category_found = True
            search_applied = True
            break
        elif term in ['textiles', 'textile', 'clothing', 'clothes', 'shirt', 'jacket', 'scarf']:
            products_query = products_query.filter(Product.category == 'Textiles')
            category_found = True
            search_applied = True
            break
    
    # If no category found, search by product title keywords
    if not category_found:
        title_conditions = []
        for term in search_terms:
            # Skip common words that don't help with product search
            if term not in ['show', 'me', 'find', 'search', 'for', 'the', 'a', 'an', 'get', 'want', 'need', 'looking', 'some']:
                title_conditions.append(Product.title.ilike(f'%{term}%'))
                search_applied = True
        
        # Apply title search conditions with OR logic
        if title_conditions:
            from sqlalchemy import or_
            products_query = products_query.filter(or_(*title_conditions))
    
    # If no search terms applied, show random products
    if not search_applied:
        products = Product.query.limit(6).all()
    else:
        products = products_query.limit(6).all()
    
    # Return results
    if products:
        products_html = format_products_html(products)
        return {
            'message': f"Here are some great products I found for you:\n\n{products_html}",
            'type': 'products',
            'products': [{'id': p.id, 'title': p.title, 'price': p.price} for p in products]
        }
    else:
        return {
            'message': "Sorry, I couldn't find any products matching your search. Try:\n• 'Show me electronics'\n• 'Find books'\n• 'Search for textiles'",
            'type': 'no_results'
        }

def get_products_by_category(category, user_id):
    """Get products by category"""
    category_map = {
        'electronics': 'Electronics',
        'books': 'Books',
        'textiles': 'Textiles',
        'clothing': 'Textiles',
        'accessories': 'Textiles'
    }
    
    db_category = category_map.get(category, category.title())
    products = Product.query.filter_by(category=db_category).limit(6).all()
    
    if products:
        products_html = format_products_html(products)
        return {
            'message': f"Here are some great {category} for you:\n\n{products_html}",
            'type': 'products',
            'products': [{'id': p.id, 'title': p.title, 'price': p.price} for p in products]
        }
    else:
        return {
            'message': f"Sorry, no {category} available right now. Try browsing other categories!",
            'type': 'no_results'
        }

def filter_by_price(query, user_id):
    """Filter products by price"""
    # Extract price from query
    price_match = re.search(r'\$?(\d+)', query)
    if price_match:
        max_price = float(price_match.group(1))
        products = Product.query.filter(Product.price <= max_price).limit(6).all()
        
        if products:
            products_html = format_products_html(products)
            return {
                'message': f"Here are products under ${max_price}:\n\n{products_html}",
                'type': 'products',
                'products': [{'id': p.id, 'title': p.title, 'price': p.price} for p in products]
            }
    
    return {
        'message': "I couldn't understand the price range. Try: 'Show me products under $50'",
        'type': 'error'
    }

def format_products_html(products):
    """Format products for display in chat"""
    html = ""
    for product in products:
        html += f"🛍️ **{product.title}**\n"
        html += f"💰 ${product.price:.2f} | ⭐ {product.rating}/5\n"
        html += f"📦 {product.category}\n"
        html += f"[Add to Cart](javascript:addToCart({product.id}))\n\n"
    return html

def show_cart(user_id):
    """Show user's cart contents"""
    cart_items = db.session.query(CartItem, Product).join(Product).filter(CartItem.user_id == user_id).all()
    
    if not cart_items:
        return {
            'message': "Your cart is empty! 🛒\n\nStart shopping by asking me to show you products:\n• 'Show me electronics'\n• 'Find books'\n• 'Search for headphones'",
            'type': 'empty_cart'
        }
    
    total = sum(item.CartItem.quantity * item.Product.price for item in cart_items)
    cart_html = "🛒 **Your Cart:**\n\n"
    
    for item in cart_items:
        cart_html += f"• {item.Product.title} x{item.CartItem.quantity} - ${item.Product.price * item.CartItem.quantity:.2f}\n"
    
    cart_html += f"\n💰 **Total: ${total:.2f}**\n\n"
    cart_html += "Ready to checkout? Just let me know!"
    
    return {
        'message': cart_html,
        'type': 'cart',
        'total': total
    }

@app.route('/api/add-to-cart', methods=['POST'])
def add_to_cart():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    # Check if product exists
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    # Check if item already in cart
    existing_item = CartItem.query.filter_by(
        user_id=session['user_id'],
        product_id=product_id
    ).first()
    
    if existing_item:
        existing_item.quantity += quantity
    else:
        cart_item = CartItem(
            user_id=session['user_id'],
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(cart_item)
    
    db.session.commit()
    
    # Get updated cart count
    cart_count = CartItem.query.filter_by(user_id=session['user_id']).count()
    
    return jsonify({
        'success': True,
        'message': f'{product.title} added to cart!',
        'cart_count': cart_count
    })

@app.route('/api/cart-count')
def get_cart_count():
    if 'user_id' not in session:
        return jsonify({'count': 0})
    
    count = CartItem.query.filter_by(user_id=session['user_id']).count()
    return jsonify({'count': count})

@app.route('/api/clear-chat', methods=['POST'])
def clear_chat():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Clear current chat session messages
    session_token = session.get('chat_token')
    if session_token:
        chat_session = ChatSession.query.filter_by(session_token=session_token).first()
        if chat_session:
            ChatMessage.query.filter_by(session_id=chat_session.id).delete()
            db.session.commit()
    
    return jsonify({'success': True})
