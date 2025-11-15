# Smart Chatbot Project

#   python -m smart_chatbot.backend.main
#   streamlit run smart_chatbot/frontend/app.py

# 🚀 Smart End-to-End Chatbot System

A production-ready, modular chatbot system built with LangChain, FastAPI, and Streamlit. This project includes persistent conversation storage, intelligent memory management, and a beautiful user interface.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.1+-orange.svg)

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Application](#-running-the-application)
- [Complete Code Files](#-complete-code-files)
- [API Documentation](#-api-documentation)
- [Troubleshooting](#-troubleshooting)

---

## ✨ Features

- 🧠 **Intelligent Conversations** - OpenAI GPT models via LangChain
- 💾 **Persistent Storage** - SQLite database for conversation history
- 🔄 **Session Management** - Track individual user sessions
- 📝 **Memory Management** - ConversationBufferMemory for context
- 🎨 **Beautiful UI** - Interactive Streamlit interface
- 📡 **RESTful API** - FastAPI with automatic documentation
- 🔒 **Secure** - Environment-based API key management
- 🧩 **Modular Design** - Easy to extend and maintain

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern web framework for APIs
- **LangChain** - LLM application framework
- **OpenAI** - GPT models
- **SQLAlchemy** - SQL toolkit and ORM
- **SQLite** - Database engine
- **Pydantic** - Data validation

### Frontend
- **Streamlit** - Interactive web UI
- **Requests** - HTTP library

---

## 📁 Project Structure

```
smart-chatbot/
│
├── backend/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── models.py               # Database models
│   ├── schemas.py              # Pydantic schemas
│   ├── database.py             # Database config
│   │
│   └── chatbot/
│       ├── __init__.py
│       ├── chain.py            # LangChain logic
│       ├── memory.py           # Memory management
│       └── prompts.py          # Prompt templates
│
├── frontend/
│   └── app.py                  # Streamlit UI
│
├── .env                        # Environment variables
├── requirements.txt            # Dependencies
├── README.md                   # This file
└── database.db                 # SQLite DB (auto-generated)
```

---

## 🚀 Installation

### Step 1: Clone or Create Project Directory

```bash
mkdir smart-chatbot
cd smart-chatbot
```

### Step 2: Create Virtual Environment

```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

Create `requirements.txt`:

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
langchain==0.1.0
langchain-openai==0.0.2
streamlit==1.28.0
sqlalchemy==2.0.23
python-dotenv==1.0.0
pydantic==2.5.0
requests==2.31.0
python-multipart==0.0.6
```

Install:
```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

### Create `.env` File

```env
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=sqlite:///./database.db
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

**Important:** Replace `your_openai_api_key_here` with your actual OpenAI API key from https://platform.openai.com/api-keys

---

## 🏃 Running the Application

### Terminal 1: Start Backend (FastAPI)

```bash
python -m backend.main
```

Backend will run at: **http://localhost:8000**
API Docs at: **http://localhost:8000/docs**

### Terminal 2: Start Frontend (Streamlit)

```bash
streamlit run frontend/app.py
```

Frontend will open at: **http://localhost:8501**

---

## 📄 Complete Code Files

### 1. `backend/__init__.py`
```python
# Empty file - makes backend a package
```

### 2. `backend/database.py`
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency for database sessions"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
```

### 3. `backend/models.py`
```python
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    role = Column(String)  # "user" or "assistant"
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    conversation = relationship("Conversation", back_populates="messages")
```

### 4. `backend/schemas.py`
```python
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class MessageCreate(BaseModel):
    content: str

class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    timestamp: datetime
    
    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str

class ConversationResponse(BaseModel):
    id: int
    session_id: str
    created_at: datetime
    messages: List[MessageResponse]
    
    class Config:
        from_attributes = True
```

### 5. `backend/chatbot/__init__.py`
```python
# Empty file - makes chatbot a package
```

### 6. `backend/chatbot/prompts.py`
```python
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

SYSTEM_TEMPLATE = """You are a helpful, intelligent AI assistant. 
Your goal is to provide accurate, helpful, and engaging responses to user queries.

Key guidelines:
- Be concise but thorough
- Use examples when helpful
- Ask clarifying questions if needed
- Maintain context from previous messages
- Be friendly and professional

Current conversation context is provided below."""

def get_chat_prompt():
    return ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(SYSTEM_TEMPLATE),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{input}")
    ])
```

### 7. `backend/chatbot/memory.py`
```python
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage
from sqlalchemy.orm import Session

class DatabaseConversationMemory:
    """Custom memory that syncs with database"""
    
    def __init__(self, session_id: str, db: Session):
        self.session_id = session_id
        self.db = db
        self.memory = ConversationBufferMemory(
            return_messages=True,
            memory_key="chat_history"
        )
        self._load_from_db()
    
    def _load_from_db(self):
        """Load conversation history from database"""
        from backend.models import Conversation
        
        conversation = self.db.query(Conversation).filter(
            Conversation.session_id == self.session_id
        ).first()
        
        if conversation:
            for msg in conversation.messages:
                if msg.role == "user":
                    self.memory.chat_memory.add_message(HumanMessage(content=msg.content))
                else:
                    self.memory.chat_memory.add_message(AIMessage(content=msg.content))
    
    def save_context(self, inputs: dict, outputs: dict):
        """Save conversation context"""
        self.memory.save_context(inputs, outputs)
    
    def load_memory_variables(self, inputs: dict):
        """Load memory variables"""
        return self.memory.load_memory_variables(inputs)
```

### 8. `backend/chatbot/chain.py`
```python
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from backend.chatbot.prompts import get_chat_prompt
from backend.chatbot.memory import DatabaseConversationMemory
import os
from dotenv import load_dotenv

load_dotenv()

class ChatbotChain:
    def __init__(self, session_id: str, db):
        self.session_id = session_id
        self.db = db
        
        # Initialize OpenAI LLM
        self.llm = ChatOpenAI(
            temperature=0.7,
            model_name="gpt-3.5-turbo",
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Initialize memory
        self.memory = DatabaseConversationMemory(session_id, db)
        
        # Create conversation chain
        self.chain = ConversationChain(
            llm=self.llm,
            memory=self.memory.memory,
            prompt=get_chat_prompt(),
            verbose=True
        )
    
    def get_response(self, user_input: str) -> str:
        """Get response from the chatbot"""
        try:
            response = self.chain.predict(input=user_input)
            return response
        except Exception as e:
            print(f"Error in chain: {e}")
            return "I apologize, but I encountered an error processing your request."
```

### 9. `backend/main.py`
```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from backend.database import get_db, init_db
from backend.models import Conversation, Message
from backend.schemas import ChatRequest, ChatResponse, ConversationResponse
from backend.chatbot.chain import ChatbotChain
import uuid
from typing import List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Smart Chatbot API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()
    logger.info("Database initialized successfully")

@app.get("/")
async def root():
    return {"message": "Smart Chatbot API is running"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """Main chat endpoint"""
    try:
        # Generate or use existing session ID
        session_id = request.session_id or str(uuid.uuid4())
        
        # Get or create conversation
        conversation = db.query(Conversation).filter(
            Conversation.session_id == session_id
        ).first()
        
        if not conversation:
            conversation = Conversation(session_id=session_id)
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
        
        # Save user message
        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=request.message
        )
        db.add(user_message)
        db.commit()
        
        # Get chatbot response
        chatbot = ChatbotChain(session_id, db)
        bot_response = chatbot.get_response(request.message)
        
        # Save assistant message
        assistant_message = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=bot_response
        )
        db.add(assistant_message)
        db.commit()
        
        return ChatResponse(response=bot_response, session_id=session_id)
    
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/conversations", response_model=List[ConversationResponse])
async def get_conversations(db: Session = Depends(get_db)):
    """Get all conversations"""
    conversations = db.query(Conversation).all()
    return conversations

@app.get("/conversations/{session_id}", response_model=ConversationResponse)
async def get_conversation(session_id: str, db: Session = Depends(get_db)):
    """Get a specific conversation"""
    conversation = db.query(Conversation).filter(
        Conversation.session_id == session_id
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return conversation

@app.delete("/conversations/{session_id}")
async def delete_conversation(session_id: str, db: Session = Depends(get_db)):
    """Delete a conversation"""
    conversation = db.query(Conversation).filter(
        Conversation.session_id == session_id
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    db.delete(conversation)
    db.commit()
    
    return {"message": "Conversation deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 10. `frontend/app.py`
```python
import streamlit as st
import requests
from datetime import datetime

# Configuration
API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Smart AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .user-message {
        background-color: #007bff;
        color: white;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
    }
    .bot-message {
        background-color: #f1f3f4;
        color: black;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'session_id' not in st.session_state:
    st.session_state.session_id = None
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.title("🤖 Smart Chatbot")
    st.markdown("---")
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.session_id = None
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📊 Stats")
    st.metric("Messages", len(st.session_state.messages))
    
    if st.session_state.session_id:
        st.text(f"Session: {st.session_state.session_id[:8]}...")

# Main chat interface
st.title("💬 Smart AI Chatbot")
st.caption("Powered by LangChain, FastAPI & OpenAI")

# Display chat messages
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{API_URL}/chat",
                    json={
                        "message": prompt,
                        "session_id": st.session_state.session_id
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    bot_response = data["response"]
                    st.session_state.session_id = data["session_id"]
                    
                    st.markdown(bot_response)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": bot_response
                    })
                else:
                    st.error("Failed to get response from the server")
            
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Make sure the backend server is running on http://localhost:8000")
```

---

## 📡 API Documentation

### Endpoints

#### 1. POST `/chat` - Send a message
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you?"}'
```

#### 2. GET `/conversations` - Get all conversations
```bash
curl "http://localhost:8000/conversations"
```

#### 3. GET `/conversations/{session_id}` - Get specific conversation
```bash
curl "http://localhost:8000/conversations/your-session-id"
```

#### 4. DELETE `/conversations/{session_id}` - Delete conversation
```bash
curl -X DELETE "http://localhost:8000/conversations/your-session-id"
```

---

## 🔧 Troubleshooting

### Issue: "Module Not Found"
**Solution:** Make sure you're running commands from the project root and all `__init__.py` files exist

### Issue: "OpenAI API Key Error"
**Solution:** Check your `.env` file has the correct `OPENAI_API_KEY`

### Issue: "Connection Refused"
**Solution:** Make sure backend is running before starting frontend

### Issue: "Port Already in Use"
**Solution:** 
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

---

## 📞 Support

If you encounter any issues:
1. Check that all files are created correctly
2. Verify your `.env` file has the OpenAI API key
3. Ensure both backend and frontend are running
4. Check the terminal for error messages

---

## 🎉 Success!

Once everything is running:
- ✅ Backend API: http://localhost:8000
- ✅ API Documentation: http://localhost:8000/docs
- ✅ Frontend UI: http://localhost:8501

**Your chatbot is now ready to use!** 🚀

---

**Built with ❤️ using Python, LangChain, FastAPI, and Streamlit**