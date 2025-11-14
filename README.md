# 🎮 Generative Roblox World Creator

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An AI-powered tool that generates Roblox worlds from text prompts using generative AI and procedural generation. Transform your ideas into playable Roblox worlds in seconds!

## ✨ Features

- 🎨 **Text-to-World Generation**: Describe your world in natural language
- 🏔️ **Procedural Terrain**: Automatically generates terrain based on your description
- 🏗️ **Smart Structure Placement**: AI places buildings, objects, and decorations
- 🎮 **Roblox Studio Integration**: Direct plugin for Roblox Studio
- 🌐 **Web Interface**: User-friendly web UI for world generation
- ⚡ **Real-time Progress**: Track generation progress in real-time
- 🔄 **Fallback System**: Works even if AI API is unavailable

## 📁 Project Structure

```
roblox-world-generator/
├── backend/          # FastAPI server
├── plugin/           # Roblox Studio plugin (Lua)
├── frontend/         # React web interface
├── core/             # Shared generation logic
└── docs/             # Documentation
```

## 🚀 Quick Start

See [QUICKSTART.md](QUICKSTART.md) for a 5-minute setup guide.

### Prerequisites

- Python 3.9+
- Node.js 16+
- Roblox Studio (optional, for plugin)
- OpenAI API key (required for full features)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yksanjo/roblox-world-generator.git
cd roblox-world-generator
```

2. **Backend Setup:**
```bash
cd backend
pip install -r requirements.txt
cp env.example .env
# Edit .env and add your OPENAI_API_KEY
python main.py
```

3. **Frontend Setup (in a new terminal):**
```bash
cd frontend
npm install
npm start
```

4. **Roblox Plugin (optional):**
   - Open Roblox Studio
   - Go to Plugins → Manage Plugins
   - Click "Install from File"
   - Select `plugin/src/main.lua`

## Usage

1. Open the web interface at `http://localhost:3000`
2. Enter a world description (e.g., "A medieval castle on a mountain with a village below")
3. Adjust parameters (size, complexity, style)
4. Click "Generate World"
5. Import the generated world into Roblox Studio via the plugin

## API Endpoints

- `POST /api/generate` - Generate world from prompt
- `GET /api/status/{job_id}` - Check generation status
- `GET /api/download/{job_id}` - Download generated world file

## 📚 Documentation

- [Quick Start Guide](QUICKSTART.md) - Get running in 5 minutes
- [Setup Instructions](SETUP.md) - Detailed setup guide
- [Architecture](ARCHITECTURE.md) - System architecture overview
- [Testing Guide](TESTING.md) - How to test the system

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI, OpenAI API
- **Frontend**: React, Axios
- **Plugin**: Lua (Roblox Studio API)
- **AI**: GPT-4 for prompt processing

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for GPT-4 API
- Roblox for Studio API
- All contributors and users

## ⚠️ Disclaimer

This is an independent project and is not affiliated with Roblox Corporation.

