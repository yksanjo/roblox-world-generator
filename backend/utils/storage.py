"""
Storage management for generated worlds
"""
import os
import json
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

class StorageManager:
    """Manages storage of generated world files"""
    
    def __init__(self, storage_path: str = "./storage"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.worlds_path = self.storage_path / "worlds"
        self.worlds_path.mkdir(exist_ok=True)
    
    async def save_world(self, job_id: str, world_data: Dict[str, Any]) -> str:
        """
        Save world data to file
        
        Args:
            job_id: Unique job identifier
            world_data: World data in Roblox format
        
        Returns:
            Path to saved file
        """
        filename = f"world_{job_id}.json"
        file_path = self.worlds_path / filename
        
        # Add metadata
        world_data["metadata"]["job_id"] = job_id
        world_data["metadata"]["saved_at"] = datetime.now().isoformat()
        
        # Save as JSON (in production, convert to .rbxlx format)
        with open(file_path, "w") as f:
            json.dump(world_data, f, indent=2)
        
        return str(file_path)
    
    async def load_world(self, job_id: str) -> Dict[str, Any]:
        """Load world data from file"""
        filename = f"world_{job_id}.json"
        file_path = self.worlds_path / filename
        
        if not file_path.exists():
            raise FileNotFoundError(f"World file not found: {file_path}")
        
        with open(file_path, "r") as f:
            return json.load(f)
    
    async def delete_world(self, job_id: str) -> bool:
        """Delete world file"""
        filename = f"world_{job_id}.json"
        file_path = self.worlds_path / filename
        
        if file_path.exists():
            file_path.unlink()
            return True
        return False



