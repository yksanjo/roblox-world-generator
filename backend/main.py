"""
FastAPI backend server for Roblox World Generator
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import os
import uuid
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from core.prompt_processor import PromptProcessor
from core.world_generator import WorldGenerator
from core.model_processor import ModelProcessor
from utils.storage import StorageManager

app = FastAPI(title="Roblox World Generator API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
prompt_processor = PromptProcessor()
world_generator = WorldGenerator()
model_processor = ModelProcessor()
storage = StorageManager()

# In-memory job storage (use Redis in production)
jobs: Dict[str, Dict[str, Any]] = {}


class GenerationRequest(BaseModel):
    prompt: str = Field(..., description="Text description of the world to generate")
    world_size: int = Field(512, ge=128, le=2048, description="World size in studs")
    complexity: str = Field("medium", pattern="^(low|medium|high)$")
    style: Optional[str] = Field(None, description="Art style (e.g., 'medieval', 'modern', 'fantasy')")
    include_terrain: bool = True
    include_structures: bool = True
    include_objects: bool = True


class GenerationResponse(BaseModel):
    job_id: str
    status: str
    message: str


@app.get("/")
async def root():
    return {
        "name": "Roblox World Generator API",
        "version": "1.0.0",
        "status": "running"
    }


@app.post("/api/generate", response_model=GenerationResponse)
async def generate_world(request: GenerationRequest, background_tasks: BackgroundTasks):
    """Generate a Roblox world from a text prompt"""
    job_id = str(uuid.uuid4())
    
    # Initialize job
    jobs[job_id] = {
        "status": "queued",
        "progress": 0,
        "created_at": datetime.now().isoformat(),
        "request": request.dict()
    }
    
    # Start generation in background
    background_tasks.add_task(
        process_generation,
        job_id,
        request
    )
    
    return GenerationResponse(
        job_id=job_id,
        status="queued",
        message="World generation started"
    )


async def process_generation(job_id: str, request: GenerationRequest):
    """Background task to process world generation"""
    try:
        jobs[job_id]["status"] = "processing"
        jobs[job_id]["progress"] = 10
        
        # Step 1: Process prompt
        jobs[job_id]["progress"] = 20
        world_spec = await prompt_processor.process(request.prompt, {
            "style": request.style,
            "complexity": request.complexity
        })
        
        # Step 2: Generate world structure
        jobs[job_id]["progress"] = 40
        world_data = await world_generator.generate(world_spec, {
            "size": request.world_size,
            "include_terrain": request.include_terrain,
            "include_structures": request.include_structures,
            "include_objects": request.include_objects
        })
        
        # Step 3: Process 3D models if needed
        jobs[job_id]["progress"] = 60
        if world_data.get("models"):
            processed_models = await model_processor.process_models(
                world_data["models"]
            )
            world_data["models"] = processed_models
        
        # Step 4: Convert to Roblox format
        jobs[job_id]["progress"] = 80
        roblox_world = await world_generator.to_roblox_format(world_data)
        
        # Step 5: Save world file
        jobs[job_id]["progress"] = 90
        file_path = await storage.save_world(job_id, roblox_world)
        
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["progress"] = 100
        jobs[job_id]["file_path"] = file_path
        jobs[job_id]["completed_at"] = datetime.now().isoformat()
        
    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)
        jobs[job_id]["failed_at"] = datetime.now().isoformat()


@app.get("/api/status/{job_id}")
async def get_status(job_id: str):
    """Get the status of a generation job"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    return {
        "job_id": job_id,
        "status": job["status"],
        "progress": job.get("progress", 0),
        "created_at": job.get("created_at"),
        "completed_at": job.get("completed_at"),
        "failed_at": job.get("failed_at"),
        "error": job.get("error")
    }


@app.get("/api/download/{job_id}")
async def download_world(job_id: str):
    """Download the generated world file"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    if job["status"] != "completed":
        raise HTTPException(
            status_code=400,
            detail=f"Job not completed. Current status: {job['status']}"
        )
    
    file_path = job.get("file_path")
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="World file not found")
    
    return FileResponse(
        file_path,
        media_type="application/json",
        filename=f"world_{job_id}.rbxlx"
    )


@app.get("/api/jobs")
async def list_jobs(limit: int = 10):
    """List recent generation jobs"""
    recent_jobs = sorted(
        jobs.items(),
        key=lambda x: x[1].get("created_at", ""),
        reverse=True
    )[:limit]
    
    return {
        "jobs": [
            {
                "job_id": job_id,
                "status": job["status"],
                "progress": job.get("progress", 0),
                "created_at": job.get("created_at"),
                "prompt": job.get("request", {}).get("prompt", "")[:100]
            }
            for job_id, job in recent_jobs
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

