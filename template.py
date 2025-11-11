import os

# Define the folder and file structure
structure = {
    "smart-chatbot": {
        "backend": {
            "__init__.py": "",
            "main.py": "# FastAPI application entry point\n",
            "models.py": "# SQLAlchemy models\n",
            "schemas.py": "# Pydantic schemas\n",
            "database.py": "# Database configuration\n",
            "chatbot": {
                "__init__.py": "",
                "chain.py": "# LangChain conversation chain\n",
                "memory.py": "# Custom memory management\n",
                "prompts.py": "# Prompt templates\n"
            }
        },
        "frontend": {
            "app.py": "# Streamlit UI application\n"
        },
        ".env": "# Add your API keys here\n",
        ".env.example": "OPENAI_API_KEY=your-api-key-here\n",
        "requirements.txt": "# Add your dependencies here\n",
        "README.md": "# Smart Chatbot Project\n",
        ".gitignore": ".env\ndatabase.db\n__pycache__/\n",
        "database.db": None  # Placeholder for SQLite DB
    }
}

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            if content is not None:
                with open(path, "w") as f:
                    f.write(content)
            else:
                open(path, "a").close()  # Create empty file

# Run the script
create_structure(".", structure)
print("✅ Project structure created successfully.")