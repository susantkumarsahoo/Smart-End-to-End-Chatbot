from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from smart_chatbot.backend.database import get_db, init_db
from smart_chatbot.backend.models import Conversation, Message
from smart_chatbot.backend.schemas import ChatRequest, ChatResponse, ConversationResponse
from smart_chatbot.backend.chatbot.chain import ChatbotChain
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
        db.refresh(user_message)

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
        db.refresh(assistant_message)

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
    uvicorn.run(app, host="127.0.0.1", port=8000)
