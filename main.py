from fastapi import FastAPI
from api import app as api_router  
import uvicorn
import os
app = FastAPI()

app.include_router(api_router)

if __name__ == "__main__":
    
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
