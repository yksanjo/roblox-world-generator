# Quick Start Guide

Get up and running in 5 minutes!

## 1. Backend Setup (2 minutes)

```bash
cd roblox-world-generator/backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp env.example .env
# Edit .env and add your OPENAI_API_KEY
python main.py
```

Backend should now be running at `http://localhost:8000`

## 2. Frontend Setup (2 minutes)

In a new terminal:

```bash
cd roblox-world-generator/frontend
npm install
npm start
```

Frontend should now be running at `http://localhost:3000`

## 3. Test It!

1. Open `http://localhost:3000` in your browser
2. Enter a prompt like: "A medieval castle on a mountain"
3. Click "Generate World"
4. Wait for generation (30-60 seconds)
5. Download the world file

## 4. Roblox Plugin (Optional)

1. Open Roblox Studio
2. Plugins → Manage Plugins → Install from File
3. Select `plugin/src/main.lua`
4. Click the "World Generator" button in toolbar
5. Generate worlds directly in Studio!

## That's it! 🎉

You now have a working AI-powered Roblox world generator!

For detailed setup, see [SETUP.md](SETUP.md)



