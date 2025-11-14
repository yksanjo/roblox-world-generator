# Roblox Studio Plugin

This plugin allows you to import AI-generated worlds directly into Roblox Studio.

## Installation

1. Open Roblox Studio
2. Go to **Plugins** → **Manage Plugins**
3. Click **"Install from File"**
4. Navigate to `plugin/src/main.lua` and select it
5. The plugin will appear in your toolbar

## Usage

1. Click the **"World Generator"** button in the toolbar
2. The plugin panel will open on the left side
3. Enter a world description (e.g., "A medieval castle on a mountain")
4. Adjust settings:
   - **World Size**: Size of the world in studs
   - **Complexity**: Low, Medium, or High
5. Click **"Generate World"**
6. Wait for generation to complete
7. The world will be automatically imported into your workspace

## Configuration

Edit `main.lua` and change the `API_URL` variable to point to your backend server:

```lua
local API_URL = "http://localhost:8000"  -- Change to your API URL
```

## Features

- Real-time generation progress
- Automatic world import
- Terrain generation (basic)
- Structure placement
- Object distribution

## Limitations

- Terrain generation is simplified in this version
- Requires backend API to be running
- Some advanced features may require additional setup



