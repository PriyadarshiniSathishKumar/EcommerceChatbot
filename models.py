"""
Database Models for ShopMate AI E-commerce Chatbot

This module defines all database models using SQLAlchemy ORM:
- User: Customer accounts with authentication
- Product: E-commerce product catalog
- CartItem: Shopping cart management
- ChatSession: Chat conversation sessions
- ChatMessage: Individual chat messages
"""

from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    """
    User model for customer accounts and authentication.
    
    Handles user registration, login, password security, and relationships
    to shopping cart items and chat sessions.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))  # Stores hashed password for security
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # One-to-many relationships
    cart_items = db.relationship('CartItem', backref='user', lazy=True, cascade='all, delete-orphan')
    chat_sessions = db.relationship('ChatSession', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """
        Hash and store user password securely using Werkzeug.
        
        Args:
            password (str): Plain text password to hash
        """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """
        Verify user password against stored hash.
        
        Args:
            password (str): Plain text password to verify
            
        Returns:
            bool: True if password matches, False otherwise
        """
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Product(db.Model):
    """
    Product model for e-commerce catalog.
    
    Stores product information including pricing, categorization, ratings,
    and inventory details for the shopping experience.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)  # Product name/title
    description = db.Column(db.Text)  # Detailed product description
    price = db.Column(db.Float, nullable=False)  # Product price in USD
    category = db.Column(db.String(50), nullable=False)  # Electronics, Books, Textiles
    rating = db.Column(db.Float, default=4.0)  # Average customer rating (1-5)
    image_url = db.Column(db.String(500))  # Product image URL
    stock = db.Column(db.Integer, default=10)  # Available inventory count
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Product creation timestamp
    
    def __repr__(self):
        return f'<Product {self.title}>'

class CartItem(db.Model):
    """
    Shopping cart item model linking users to products.
    
    Tracks individual items in user shopping carts with quantities
    and timestamps for cart management functionality.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # References User.id
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)  # References Product.id
    quantity = db.Column(db.Integer, default=1)  # Number of items in cart
    added_at = db.Column(db.DateTime, default=datetime.utcnow)  # When item was added
    
    # Relationship to access product details
    product = db.relationship('Product', backref='cart_items')
    
    def __repr__(self):
        return f'<CartItem {self.product.title} x{self.quantity}>'

class ChatSession(db.Model):
    """
    Chat session model for tracking user conversations.
    
    Each user can have multiple chat sessions, each with a unique token
    for maintaining conversation context and history.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # References User.id
    session_token = db.Column(db.String(100), unique=True, nullable=False)  # Unique session identifier
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Session start time
    
    # One-to-many relationship with chat messages
    messages = db.relationship('ChatMessage', backref='session', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<ChatSession {self.session_token}>'

class ChatMessage(db.Model):
    """
    Individual chat message model for conversation history.
    
    Stores both user input and bot responses with timestamps
    for complete conversation tracking and replay functionality.
    """
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('chat_session.id'), nullable=False)  # References ChatSession.id
    message = db.Column(db.Text, nullable=False)  # Message content (user input or bot response)
    sender = db.Column(db.String(10), nullable=False)  # Either 'user' or 'bot'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Message creation time
    
    def __repr__(self):
        return f'<ChatMessage {self.sender}: {self.message[:50]}>'
