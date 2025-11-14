# Setup Guide

Complete setup instructions for the Roblox World Generator.

## Prerequisites

- **Python 3.9+** - [Download](https://www.python.org/downloads/)
- **Node.js 16+** - [Download](https://nodejs.org/)
- **Roblox Studio** - [Download](https://www.roblox.com/create)
- **API Keys**:
  - OpenAI API key (required) - [Get one here](https://platform.openai.com/api-keys)
  - 3D Generation API key (optional) - Luma/Meshy/CSM

## Backend Setup

1. **Navigate to backend directory:**
```bash
cd roblox-world-generator/backend
```

2. **Create virtual environment (recommended):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment:**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

5. **Create storage directory:**
```bash
mkdir -p storage/worlds
```

6. **Run the server:**
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## Frontend Setup

1. **Navigate to frontend directory:**
```bash
cd roblox-world-generator/frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Configure API URL (optional):**
Create a `.env` file:
```
REACT_APP_API_URL=http://localhost:8000
```

4. **Start development server:**
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## Roblox Plugin Setup

1. **Open Roblox Studio**

2. **Install the plugin:**
   - Go to **Plugins** → **Manage Plugins**
   - Click **"Install from File"**
   - Navigate to `roblox-world-generator/plugin/src/main.lua`
   - Select the file

3. **Configure API URL:**
   - Open `plugin/src/main.lua`
   - Find the line: `local API_URL = "http://localhost:8000"`
   - Change to your backend URL if different

4. **Use the plugin:**
   - Click the "World Generator" button in the toolbar
   - Enter a world description
   - Click "Generate World"
   - Wait for generation to complete
   - World will be imported automatically

## Testing

### Test Backend API

```bash
# Test root endpoint
curl http://localhost:8000/

# Test generation
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A small village with houses",
    "world_size": 256,
    "complexity": "low"
  }'
```

### Test Frontend

1. Start backend server
2. Start frontend server
3. Open `http://localhost:3000`
4. Enter a prompt and click "Generate World"

## Troubleshooting

### Backend Issues

**Import errors:**
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.9+)

**API key errors:**
- Verify your `.env` file exists and contains `OPENAI_API_KEY`
- Check API key is valid at OpenAI dashboard

**Port already in use:**
- Change port in `main.py`: `uvicorn.run(app, host="0.0.0.0", port=8001)`

### Frontend Issues

**Cannot connect to API:**
- Verify backend is running on port 8000
- Check `REACT_APP_API_URL` in `.env` file
- Check CORS settings in backend

**Build errors:**
- Clear node_modules: `rm -rf node_modules && npm install`
- Check Node.js version: `node --version` (should be 16+)

### Plugin Issues

**Plugin not appearing:**
- Make sure you installed from the correct file path
- Check Roblox Studio console for errors (View → Output)

**Cannot connect to API:**
- Verify backend is running
- Check API_URL in `main.lua`
- Make sure firewall allows connections

## Production Deployment

### Backend

1. **Use a production ASGI server:**
```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

2. **Set up environment variables:**
- Use a proper `.env` file or environment variables
- Never commit API keys to version control

3. **Configure CORS:**
- Update `allow_origins` in `main.py` to your frontend domain

### Frontend

1. **Build for production:**
```bash
npm run build
```

2. **Serve static files:**
- Use nginx, Apache, or a CDN
- Point to the `build` directory

## Next Steps

- Add authentication for API access
- Implement user accounts and saved worlds
- Add more terrain types and structures
- Integrate with 3D generation APIs
- Add real-time collaboration features

