from langchain_openai import ChatOpenAI
from langchain_classic.chains import ConversationChain
from langchain_classic.memory import ConversationBufferMemory
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
            return "I apologize, but I encountered an error processing your request."# LangChain conversation chain
