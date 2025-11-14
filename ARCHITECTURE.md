# Architecture Overview

## System Architecture

```
┌─────────────────┐
│   Frontend      │  React Web UI
│   (React)       │  Port 3000
└────────┬────────┘
         │ HTTP/REST
         │
┌────────▼────────┐
│   Backend API   │  FastAPI Server
│   (Python)      │  Port 8000
└────────┬────────┘
         │
    ┌────┴────┬──────────┬────────────┐
    │         │          │            │
┌───▼───┐ ┌──▼───┐ ┌────▼────┐ ┌────▼────┐
│ OpenAI│ │ 3D   │ │ World   │ │ Storage │
│ GPT-4 │ │ APIs │ │ Gen     │ │ Manager │
└───────┘ └──────┘ └─────────┘ └─────────┘
```

## Component Details

### Frontend (React)
- **Location**: `frontend/`
- **Purpose**: User interface for world generation
- **Features**:
  - Prompt input
  - Parameter controls
  - Progress tracking
  - World download

### Backend API (FastAPI)
- **Location**: `backend/`
- **Purpose**: Core generation logic and API endpoints
- **Components**:
  - `main.py`: API server and routes
  - `core/prompt_processor.py`: Converts text to world specs
  - `core/world_generator.py`: Generates world data
  - `core/model_processor.py`: Processes 3D models
  - `utils/storage.py`: File management

### Roblox Plugin (Lua)
- **Location**: `plugin/`
- **Purpose**: Direct integration with Roblox Studio
- **Features**:
  - World import
  - Real-time generation
  - Direct workspace integration

## Data Flow

1. **User Input** → Frontend receives prompt
2. **API Request** → Frontend sends POST to `/api/generate`
3. **Prompt Processing** → GPT-4 converts text to structured spec
4. **World Generation** → Procedural algorithms create world data
5. **Model Processing** → 3D models converted to Roblox format
6. **Storage** → World saved as JSON/RBXLX file
7. **Response** → Job ID returned to frontend
8. **Status Polling** → Frontend polls `/api/status/{job_id}`
9. **Download** → User downloads completed world

## World Data Structure

```json
{
  "version": "1.0",
  "metadata": {
    "size": 512,
    "theme": "medieval",
    "generated_at": "2024-01-01T00:00:00"
  },
  "workspace": {
    "terrain": {
      "type": "mountain",
      "heightmap": [[...]],
      "resolution": 128
    },
    "parts": [
      {
        "name": "tree",
        "position": {"x": 0, "y": 0, "z": 0},
        "size": {"x": 4, "y": 20, "z": 4}
      }
    ],
    "models": [
      {
        "name": "castle",
        "parts": [...],
        "position": {"x": 0, "y": 0, "z": 0}
      }
    ]
  }
}
```

## API Endpoints

### POST `/api/generate`
Generate a new world from prompt.

**Request:**
```json
{
  "prompt": "A medieval castle",
  "world_size": 512,
  "complexity": "medium",
  "include_terrain": true,
  "include_structures": true,
  "include_objects": true
}
```

**Response:**
```json
{
  "job_id": "uuid",
  "status": "queued",
  "message": "World generation started"
}
```

### GET `/api/status/{job_id}`
Get generation status.

**Response:**
```json
{
  "job_id": "uuid",
  "status": "processing",
  "progress": 45,
  "created_at": "2024-01-01T00:00:00"
}
```

### GET `/api/download/{job_id}`
Download generated world file.

**Response:** Binary file (JSON or RBXLX)

## Technology Stack

- **Backend**: Python 3.9+, FastAPI, OpenAI API
- **Frontend**: React 18, Axios
- **Plugin**: Lua (Roblox Studio API)
- **Storage**: File system (JSON)
- **AI**: GPT-4 for prompt processing

## Future Enhancements

- Redis for job queue management
- Database for user accounts and saved worlds
- Real-time WebSocket updates
- Advanced 3D model generation integration
- Multi-user collaboration
- Cloud storage integration



