import os
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')

# Initialize the LLM
llm = GoogleGenerativeAI(model='gemini-pro', temperature=0.7)

# Create a prompt template
prompt = ChatPromptTemplate.from_messages([
    ('system', 'You are an excellent content writer so write on a topic given by the user'),
    ('user', '{user_query}')
])

# Pydantic model for request body (POST)
class UserQuery(BaseModel):
    user_query: str

# Initialize router
app = APIRouter()

# Helper function to generate content
def generate_content_from_query(user_query: str) -> str:
    try:
        # Format the prompt and invoke the LLM
        formatted_prompt = prompt.format_prompt(user_query=user_query)
        response = llm.invoke(formatted_prompt.to_string())
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating content: {str(e)}")

# GET method to handle query parameters
@app.get("/user_prompt")
async def generate_content_get(user_query: str = Query(..., description="The query string provided by the user")):
    """
    Generate content based on a query string sent as a query parameter.
    """
    response = generate_content_from_query(user_query)
    return {"status": "success", "response": response}

# POST method to handle JSON body
@app.post("/prompt_response")
async def generate_content_post(data: UserQuery):
    """
    Generate content based on a query string sent in the request body.
    """
    response = generate_content_from_query(data.user_query)
    return {"status": "success", "response": response}
