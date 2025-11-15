from langchain_classic.memory import ConversationBufferMemory
from langchain_classic.schema import HumanMessage, AIMessage
from sqlalchemy.orm import Session
from backend.models import Message

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
        return self.memory.load_memory_variables(inputs)# Custom memory management
