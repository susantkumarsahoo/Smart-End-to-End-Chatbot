# Smart-End-to-End-Chatbot
A Smart End-to-End (E2E) Chatbot is an AI-powered conversational agent designed to handle user interactions from the initial greeting to the final resolution without human intervention



# 🚀 Smart End-to-End Chatbot System

A production-ready, modular chatbot system built with modern AI and web technologies. This project demonstrates best practices in building scalable AI applications with conversation persistence and intelligent memory management.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.1+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Code Examples](#code-examples)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- 🧠 **Intelligent Conversations** - Powered by OpenAI GPT models via LangChain
- 💾 **Persistent Storage** - SQLite database for conversation history
- 🔄 **Session Management** - Track individual user sessions and context
- 📝 **Memory Management** - ConversationBufferMemory for context awareness
- 🎨 **Beautiful UI** - Interactive Streamlit interface
- 📡 **RESTful API** - FastAPI backend with automatic documentation
- 🔒 **Secure** - Environment-based API key management
- 🗃️ **Database Integration** - SQLAlchemy ORM with relational models
- 📊 **Conversation Export** - Export chat history as JSON
- 🧩 **Modular Design** - Easy to extend and maintain

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **LangChain** - Framework for developing LLM applications
- **OpenAI** - GPT models for natural language processing
- **SQLAlchemy** - SQL toolkit and ORM
- **SQLite** - Lightweight database engine
- **Pydantic** - Data validation using Python type annotations

### Frontend
- **Streamlit** - Fast way to build data apps
- **Requests** - HTTP library for API communication

### DevOps & Security
- **python-dotenv** - Environment variable management
- **Uvicorn** - ASGI server for FastAPI
- **Logging** - Built-in Python logging for debugging

## 📁 Project Structure

```
smart-chatbot/
│
├── backend/                        # Backend application
│   ├── __init__.py
│   ├── main.py                     # FastAPI application entry point
│   ├── models.py                   # SQLAlchemy database models
│   ├── schemas.py                  # Pydantic schemas for validation
│   ├── database.py                 # Database configuration & connection
│   │
│   └── chatbot/                    # Chatbot logic module
│       ├── __init__.py
│       ├── chain.py                # LangChain conversation chain
│       ├── memory.py               # Custom memory management
│       └── prompts.py              # Prompt templates
│
├── frontend/                       # Frontend application
│   └── app.py                      # Streamlit UI application
│
├── .env                            # Environment variables (DO NOT COMMIT)
├── .env.example                    # Example environment file
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── database.db                     # SQLite database (auto-generated)
└── .gitignore                      # Git ignore rules
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/smart-chatbot.git
   cd smart-chatbot
   ```

2. **Create a virtual environment**
   ```bash
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Verify installation**
   ```bash
   python -c "import fastapi, langchain, streamlit; print('All packages installed successfully!')"
   ```

## ⚙️ Configuration

### 1. Create Environment File

Create a `.env` file in the root directory:

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here

# Database Configuration
DATABASE_URL=sqlite:///./database.db

# API Configuration
DEBUG=True
HOST=0.0.0.0
PORT=8000

# Optional: LangChain Configuration
LANGCHAIN_TRACING_V2=false
LANGCHAIN_API_KEY=your-langchain-api-key-here
```

### 2. Environment Variables Explained

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | ✅ Yes | None |
| `DATABASE_URL` | Database connection string | No | `sqlite:///./database.db` |
| `DEBUG` | Enable debug mode | No | `True` |
| `HOST` | API server host | No | `0.0.0.0` |
| `PORT` | API server port | No | `8000` |

### 3. Create .env.example (for version control)

```env
OPENAI_API_KEY=your-api-key-here
DATABASE_URL=sqlite:///./database.db
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

## 🏃 Running the Application

### Method 1: Run Backend and Frontend Separately

#### Start the Backend (FastAPI)

```bash
# From project root
python -m backend.main

# Or using uvicorn directly
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at:
- API: `http://localhost:8000`
- Interactive API Docs: `http://localhost:8000/docs`
- Alternative API Docs: `http://localhost:8000/redoc`

#### Start the Frontend (Streamlit)

Open a new terminal and run:

```bash
# Make sure you're in the project root and venv is activated
streamlit run frontend/app.py
```

The frontend will open automatically in your browser at `http://localhost:8501`

### Method 2: Use Process Manager (Optional)

Create a `run.sh` script:

```bash
#!/bin/bash
# Start backend
python -m backend.main &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start frontend
streamlit run frontend/app.py &
FRONTEND_PID=$!

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
```

Make it executable and run:
```bash
chmod +x run.sh
./run.sh
```

## 📡 API Documentation

### Endpoints

#### 1. Chat Endpoint
```http
POST /chat
Content-Type: application/json

{
  "message": "Hello, how are you?",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "response": "I'm doing well, thank you for asking! How can I assist you today?",
  "session_id": "generated-or-provided-session-id"
}
```

#### 2. Get All Conversations
```http
GET /conversations
```

**Response:**
```json
[
  {
    "id": 1,
    "session_id": "session_123",
    "created_at": "2025-01-01T10:00:00",
    "messages": [...]
  }
]
```

#### 3. Get Specific Conversation
```http
GET /conversations/{session_id}
```

**Response:**
```json
{
  "id": 1,
  "session_id": "session_123",
  "created_at": "2025-01-01T10:00:00",
  "messages": [
    {
      "id": 1,
      "role": "user",
      "content": "Hello!",
      "timestamp": "2025-01-01T10:00:00"
    },
    {
      "id": 2,
      "role": "assistant",
      "content": "Hi! How can I help you?",
      "timestamp": "2025-01-01T10:00:01"
    }
  ]
}
```

#### 4. Delete Conversation
```http
DELETE /conversations/{session_id}
```

**Response:**
```json
{
  "message": "Conversation deleted successfully"
}
```

### Testing the API

#### Using cURL

```bash
# Send a chat message
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the capital of France?"}'

# Get all conversations
curl "http://localhost:8000/conversations"

# Get specific conversation
curl "http://localhost:8000/conversations/session_123"

# Delete conversation
curl -X DELETE "http://localhost:8000/conversations/session_123"
```

#### Using Python

```python
import requests

# Send a chat message
response = requests.post(
    "http://localhost:8000/chat",
    json={"message": "Tell me a joke"}
)
print(response.json())

# Get all conversations
conversations = requests.get("http://localhost:8000/conversations")
print(conversations.json())
```

## 💻 Code Examples

### Example 1: Custom Prompt Template

Edit `backend/chatbot/prompts.py`:

```python
from langchain.prompts import ChatPromptTemplate

# Create a custom prompt for a specific use case
CUSTOM_PROMPT = ChatPromptTemplate.from_template("""
You are a helpful coding assistant specializing in Python.

User Question: {input}

Provide a clear, concise answer with code examples when appropriate.
Always follow Python best practices and PEP 8 style guide.

Response:
""")
```

### Example 2: Add New Database Model

Edit `backend/models.py`:

```python
class UserFeedback(Base):
    __tablename__ = "user_feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("messages.id"))
    rating = Column(Integer)  # 1-5 stars
    comment = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    message = relationship("Message")
```

### Example 3: Custom Memory Management

```python
from langchain.memory import ConversationSummaryMemory
from backend.chatbot.chain import ChatbotChain

class CustomChatbotChain(ChatbotChain):
    def __init__(self, session_id: str, db):
        super().__init__(session_id, db)
        
        # Replace with summary memory for longer conversations
        self.memory = ConversationSummaryMemory(
            llm=self.llm,
            return_messages=True
        )
```

## 🔧 Troubleshooting

### Common Issues

#### 1. OpenAI API Key Error
```
Error: OpenAI API key not found
```
**Solution:** Ensure your `.env` file contains a valid `OPENAI_API_KEY`

#### 2. Module Not Found Error
```
ModuleNotFoundError: No module named 'backend'
```
**Solution:** Run commands from project root and ensure `__init__.py` files exist

#### 3. Database Lock Error
```
sqlite3.OperationalError: database is locked
```
**Solution:** Close any other connections to the database or delete `database.db` and restart

#### 4. Port Already in Use
```
OSError: [Errno 48] Address already in use
```
**Solution:** 
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
uvicorn backend.main:app --port 8001
```

#### 5. Streamlit Connection Error
```
Error: Failed to connect to backend
```
**Solution:** Ensure backend is running before starting frontend

### Debug Mode

Enable detailed logging:

```python
# In backend/main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Verify Installation

```bash
# Check Python version
python --version

# Check installed packages
pip list | grep -E "fastapi|langchain|streamlit|sqlalchemy"

# Test database connection
python -c "from backend.database import engine; print('Database connection OK')"
```

## 🧪 Testing

### Manual Testing

1. **Test Backend API**
   ```bash
   # Health check
   curl http://localhost:8000/
   
   # Test chat endpoint
   curl -X POST http://localhost:8000/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "test"}'
   ```

2. **Test Frontend**
   - Open `http://localhost:8501`
   - Send a message
   - Check if response appears
   - Verify session persistence

### Automated Testing (Future Enhancement)

```python
# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_chat_endpoint():
    response = client.post(
        "/chat",
        json={"message": "Hello"}
    )
    assert response.status_code == 200
    assert "response" in response.json()
```

## 📊 Database Schema

### Conversations Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| session_id | STRING | Unique session identifier |
| created_at | DATETIME | Creation timestamp |
| updated_at | DATETIME | Last update timestamp |

### Messages Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| conversation_id | INTEGER | Foreign key to conversations |
| role | STRING | 'user' or 'assistant' |
| content | TEXT | Message content |
| timestamp | DATETIME | Message timestamp |

### Viewing the Database

```bash
# Install sqlite3 (if not already installed)
# macOS: brew install sqlite
# Ubuntu: sudo apt-get install sqlite3

# Open database
sqlite3 database.db

# View tables
.tables

# View conversations
SELECT * FROM conversations;

# View messages
SELECT * FROM messages;

# Exit
.quit
```

## 🚀 Deployment

### Docker Deployment (Recommended)

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - ./database.db:/app/database.db
  
  frontend:
    build: .
    command: streamlit run frontend/app.py
    ports:
      - "8501:8501"
    depends_on:
      - backend
```

Run with:
```bash
docker-compose up
```

### Cloud Deployment Options

- **Heroku**: Use Procfile
- **AWS**: Deploy on EC2 or ECS
- **Google Cloud**: Use Cloud Run
- **Railway**: One-click deployment
- **Render**: Automatic deployment from GitHub

## 📈 Performance Optimization

### Tips for Production

1. **Use PostgreSQL instead of SQLite**
   ```python
   DATABASE_URL = "postgresql://user:password@localhost/dbname"
   ```

2. **Add caching**
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=100)
   def get_cached_response(message):
       # Cache frequent responses
       pass
   ```

3. **Rate limiting**
   ```python
   from slowapi import Limiter
   
   limiter = Limiter(key_func=get_remote_address)
   app.state.limiter = limiter
   ```

4. **Async database operations**
   ```python
   from sqlalchemy.ext.asyncio import create_async_engine
   ```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Add docstrings to functions
- Write descriptive commit messages

## 📄 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/smart-chatbot/issues)
- **Documentation**: [Wiki](https://github.com/yourusername/smart-chatbot/wiki)
- **Email**: your.email@example.com

## 🎉 Acknowledgments

- **LangChain** - For the amazing LLM framework
- **FastAPI** - For the modern web framework
- **Streamlit** - For making beautiful UIs simple
- **OpenAI** - For powerful language models

## 🗺️ Roadmap

- [ ] Add user authentication
- [ ] Implement Redis for caching
- [ ] Add voice input/output
- [ ] Create mobile app
- [ ] Add multi-language support
- [ ] Implement RAG (Retrieval Augmented Generation)
- [ ] Add analytics dashboard
- [ ] Create admin panel

---

**Built with ❤️ using Python, LangChain, FastAPI, and Streamlit**

⭐ Star this repo if you find it helpful!



