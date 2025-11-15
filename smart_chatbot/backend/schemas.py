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
        orm_mode = True

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
        orm_mode = True

