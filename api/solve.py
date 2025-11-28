import json
import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import sys

# Add parent directory to path to import agent
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import run_agent

load_dotenv()

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET = os.getenv("SECRET", "mor_chabi")

@app.post("/solve")
async def solve(request: Request):
    """Handle solve requests from Vercel"""
    try:
        data = await request.json()
    except Exception:
        return JSONResponse(status_code=400, content={"error": "Invalid JSON"})
    
    url = data.get("url")
    secret = data.get("secret")
    
    if not url or not secret:
        return JSONResponse(status_code=400, content={"error": "Missing url or secret"})
    
    if secret != SECRET:
        return JSONResponse(status_code=403, content={"error": "Invalid secret"})
    
    print(f"Verified starting the task for URL: {url}")
    
    # Run agent synchronously (Vercel doesn't support background tasks well)
    try:
        await run_agent(url)
    except Exception as e:
        print(f"Error running agent: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})
    
    return JSONResponse(status_code=200, content={"status": "ok"})

# Health check
@app.get("/healthz")
async def healthz():
    return JSONResponse(status_code=200, content={"status": "ok"})
