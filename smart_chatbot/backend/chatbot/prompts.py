from langchain_classic.prompts import (
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

SIMPLE_PROMPT = ChatPromptTemplate.from_template(
    """You are a helpful AI assistant. Respond to the following:
    
    {input}
    
    Response:"""
)

