# 🤖 ShopMate AI - Intelligent E-commerce Sales Chatbot

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.0+-blue.svg)](https://tailwindcss.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3.0+-orange.svg)](https://sqlite.org/)

An intelligent, interactive sales chatbot that transforms the shopping experience by seamlessly guiding users from product search to purchase through natural conversation.

## 🌟 Features

### 🧠 Intelligent Chat Interface
- **Natural Language Processing**: Chat naturally like you would with a friend
- **Smart Product Discovery**: AI understands your preferences and suggests relevant products
- **Context-Aware Responses**: Maintains conversation context for better user experience
- **Real-time Typing Indicators**: Visual feedback during bot processing

### 🛍️ E-commerce Functionality
- **Product Search & Filtering**: Search by keywords, category, price range
- **Shopping Cart Management**: Add, view, and manage cart items within chat
- **100+ Mock Products**: Books, Electronics, and Textiles categories
- **Rich Product Cards**: Images, descriptions, ratings, and pricing

### 🎨 Beautiful User Interface
- **WhatsApp/Slack-style Chat UI**: Familiar and intuitive design
- **Dark/Light Mode Toggle**: Customizable theme preferences
- **Mobile-First Responsive Design**: Perfect on any device
- **Smooth Animations**: AOS animations and custom transitions
- **Professional Aesthetic**: Clean, modern e-commerce design

### 🔐 User Management
- **Secure Authentication**: Password hashing with Werkzeug
- **Session Management**: Persistent user sessions
- **User Registration/Login**: Simple account creation process
- **Chat History**: Persistent conversation tracking

### 📊 Advanced Features
- **Chat Export**: Download conversation history as text
- **Clear Chat**: Reset conversation anytime
- **Cart Notifications**: Real-time cart updates
- **Quick Actions**: Predefined buttons for common queries
- **Voice Input Ready**: Infrastructure for future voice features

## 🏗️ Architecture
Frontend (HTML + TailwindCSS + JavaScript)
         |
         | REST API Calls (AJAX)
         ↓
Backend (Python Flask)
         |
         | SQL Queries
         ↓
Database (SQLite) — Mock Inventory (100+ products)
Modular MVC Structure

RESTful API Endpoints for search, cart, authentication

Session Management to preserve user state

Secure Password Hashing for user data protection

💻 Tech Stack
Layer	Technology
Frontend	HTML5, TailwindCSS, Vanilla JS
Backend	Python Flask
Database	SQLite
Authentication	Flask-Login, Werkzeug Security
Animations	AOS (Animate On Scroll), Custom CSS
Deployment	Replit

🚀 Getting Started
1️⃣ Clone the Repository
bash
Copy
Edit
git clone https://github.com/your-username/shopmate-ai.git
cd shopmate-ai
2️⃣ Setup Virtual Environment
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
3️⃣ Run the Application
bash
Copy
Edit
python app.py
4️⃣ Access the App
Open your browser and navigate to:
http://localhost:5000/

📁 Project Structure
EcommerceChatbot/
├── static/
│   ├── css/
│   └── js/
├── templates/
│   └── *.html
├── database/
│   └── shopmate.db
├── app.py
├── requirements.txt
└── README.md
📝 Documentation
📃 API Endpoints: /login, /register, /search, /cart, /logout

🗂️ Mock Data Generation: Python script provided for auto-generating mock products

📚 Detailed Setup Instructions in README.md

⚙️ Challenges Faced
Challenge	Solution Implemented
Maintaining Chat Context	Used session variables and localStorage for tracking
Real-time Feedback (Typing)	Implemented simulated typing indicators in JS
Responsive UI across devices	TailwindCSS + thorough mobile-first testing
Authentication Security	Used Werkzeug for password hashing

🎯 Future Enhancements
🗣 Voice Input Integration (SpeechRecognition API)

🤖 Advanced NLP with transformers for better product recommendations

🏦 Payment Gateway Integration for end-to-end shopping

📱 PWA Support for installable mobile experience

💬 AI-powered Chat Summaries and Product Comparisons

👨‍💻 Developed with ❤️ by Priyadarshini Sathishkumar

