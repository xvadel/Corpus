from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any

app = FastAPI(
    title="Corpus AI Career Communication Platform",
    description="Backend API for Project Analysis, RAG, and Communication Coaching.",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Corpus API"}

@app.post("/api/projects/upload")
async def upload_project(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Receives a markdown file containing the user's project details,
    parses it, and simulates a domain/skill detection process using Gemini (placeholder).
    """
    if not file.filename.endswith('.md'):
        raise HTTPException(status_code=400, detail="Only Markdown (.md) files are supported.")
        
    try:
        content = await file.read()
        markdown_text = content.decode('utf-8')
        
        # TODO: Hook up actual Google Gemini API for extraction.
        # This is a simulated response for Phase 1 MVP testing.
        return {
            "status": "success",
            "filename": file.filename,
            "analysis": {
                "domain": "Artificial Intelligence",
                "subdomains": [
                    "Retrieval-Augmented Generation (RAG)",
                    "Natural Language Processing",
                    "Vector Databases"
                ],
                "extracted_skills": ["Python", "FastAPI", "Prompt Engineering"],
                "content_length": len(markdown_text)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing file: {str(e)}")
