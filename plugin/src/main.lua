-- Roblox World Generator Plugin
-- This plugin allows importing AI-generated worlds into Roblox Studio

local HttpService = game:GetService("HttpService")
local Selection = game:GetService("Selection")
local StudioService = game:GetService("StudioService")

local plugin = plugin
local toolbar = plugin:CreateToolbar("World Generator")
local button = toolbar:CreateButton("Generate World", "Generate a world from AI prompt", "rbxasset://textures/DevConsole/DevConsole.png")

local widget = plugin:CreateDockWidgetPluginGui(
    "WorldGeneratorWidget",
    DockWidgetPluginGuiInfo.new(
        Enum.InitialDockState.Left,
        false,
        false,
        300,
        400,
        200,
        200
    )
)
widget.Title = "World Generator"

-- API Configuration
local API_URL = "http://localhost:8000"  -- Change to your API URL

-- UI Elements
local screenGui = Instance.new("ScreenGui")
screenGui.Name = "WorldGeneratorUI"
screenGui.Parent = widget

local mainFrame = Instance.new("Frame")
mainFrame.Name = "MainFrame"
mainFrame.Size = UDim2.new(1, 0, 1, 0)
mainFrame.BackgroundColor3 = Color3.fromRGB(30, 30, 30)
mainFrame.BorderSizePixel = 0
mainFrame.Parent = screenGui

local scrollFrame = Instance.new("ScrollingFrame")
scrollFrame.Name = "ScrollFrame"
scrollFrame.Size = UDim2.new(1, -20, 1, -20)
scrollFrame.Position = UDim2.new(0, 10, 0, 10)
scrollFrame.BackgroundTransparency = 1
scrollFrame.ScrollBarThickness = 6
scrollFrame.Parent = mainFrame

local uiListLayout = Instance.new("UIListLayout")
uiListLayout.Padding = UDim.new(0, 10)
uiListLayout.Parent = scrollFrame

-- Title
local title = Instance.new("TextLabel")
title.Name = "Title"
title.Size = UDim2.new(1, 0, 0, 40)
title.BackgroundTransparency = 1
title.Text = "AI World Generator"
title.TextColor3 = Color3.fromRGB(255, 255, 255)
title.TextSize = 24
title.Font = Enum.Font.SourceSansBold
title.TextXAlignment = Enum.TextXAlignment.Left
title.Parent = scrollFrame

-- Prompt Input
local promptLabel = Instance.new("TextLabel")
promptLabel.Name = "PromptLabel"
promptLabel.Size = UDim2.new(1, 0, 0, 20)
promptLabel.BackgroundTransparency = 1
promptLabel.Text = "Describe your world:"
promptLabel.TextColor3 = Color3.fromRGB(200, 200, 200)
promptLabel.TextSize = 14
promptLabel.TextXAlignment = Enum.TextXAlignment.Left
promptLabel.Parent = scrollFrame

local promptBox = Instance.new("TextBox")
promptBox.Name = "PromptBox"
promptBox.Size = UDim2.new(1, 0, 0, 100)
promptBox.BackgroundColor3 = Color3.fromRGB(40, 40, 40)
promptBox.BorderColor3 = Color3.fromRGB(60, 60, 60)
promptBox.Text = "A medieval castle on a mountain with a village below"
promptBox.TextColor3 = Color3.fromRGB(255, 255, 255)
promptBox.TextSize = 14
promptBox.TextWrapped = true
promptBox.Font = Enum.Font.SourceSans
promptBox.PlaceholderText = "Enter world description..."
promptBox.Parent = scrollFrame

-- World Size
local sizeLabel = Instance.new("TextLabel")
sizeLabel.Name = "SizeLabel"
sizeLabel.Size = UDim2.new(1, 0, 0, 20)
sizeLabel.BackgroundTransparency = 1
sizeLabel.Text = "World Size:"
sizeLabel.TextColor3 = Color3.fromRGB(200, 200, 200)
sizeLabel.TextSize = 14
sizeLabel.TextXAlignment = Enum.TextXAlignment.Left
sizeLabel.Parent = scrollFrame

local sizeSlider = Instance.new("TextButton")
sizeSlider.Name = "SizeSlider"
sizeSlider.Size = UDim2.new(1, 0, 0, 30)
sizeSlider.BackgroundColor3 = Color3.fromRGB(50, 50, 50)
sizeSlider.BorderColor3 = Color3.fromRGB(70, 70, 70)
sizeSlider.Text = "512 studs"
sizeSlider.TextColor3 = Color3.fromRGB(255, 255, 255)
sizeSlider.TextSize = 14
sizeSlider.Parent = scrollFrame

local currentSize = 512

-- Complexity
local complexityLabel = Instance.new("TextLabel")
complexityLabel.Name = "ComplexityLabel"
complexityLabel.Size = UDim2.new(1, 0, 0, 20)
complexityLabel.BackgroundTransparency = 1
complexityLabel.Text = "Complexity:"
complexityLabel.TextColor3 = Color3.fromRGB(200, 200, 200)
complexityLabel.TextSize = 14
complexityLabel.TextXAlignment = Enum.TextXAlignment.Left
complexityLabel.Parent = scrollFrame

local complexityFrame = Instance.new("Frame")
complexityFrame.Name = "ComplexityFrame"
complexityFrame.Size = UDim2.new(1, 0, 0, 30)
complexityFrame.BackgroundTransparency = 1
complexityFrame.Parent = scrollFrame

local complexityLayout = Instance.new("UIListLayout")
complexityLayout.FillDirection = Enum.FillDirection.Horizontal
complexityLayout.Padding = UDim.new(0, 5)
complexityLayout.Parent = complexityFrame

local complexities = {"Low", "Medium", "High"}
local selectedComplexity = "medium"

for i, comp in ipairs(complexities) do
    local button = Instance.new("TextButton")
    button.Name = comp
    button.Size = UDim2.new(0.33, -4, 1, 0)
    button.BackgroundColor3 = Color3.fromRGB(50, 50, 50)
    button.BorderColor3 = Color3.fromRGB(70, 70, 70)
    button.Text = comp
    button.TextColor3 = Color3.fromRGB(255, 255, 255)
    button.TextSize = 12
    button.Parent = complexityFrame
    
    if comp == "Medium" then
        button.BackgroundColor3 = Color3.fromRGB(0, 162, 255)
    end
    
    button.MouseButton1Click:Connect(function()
        selectedComplexity = string.lower(comp)
        for _, btn in ipairs(complexityFrame:GetChildren()) do
            if btn:IsA("TextButton") then
                btn.BackgroundColor3 = Color3.fromRGB(50, 50, 50)
            end
        end
        button.BackgroundColor3 = Color3.fromRGB(0, 162, 255)
    end)
end

-- Generate Button
local generateButton = Instance.new("TextButton")
generateButton.Name = "GenerateButton"
generateButton.Size = UDim2.new(1, 0, 0, 40)
generateButton.BackgroundColor3 = Color3.fromRGB(0, 162, 255)
generateButton.BorderSizePixel = 0
generateButton.Text = "Generate World"
generateButton.TextColor3 = Color3.fromRGB(255, 255, 255)
generateButton.TextSize = 16
generateButton.Font = Enum.Font.SourceSansBold
generateButton.Parent = scrollFrame

-- Status Label
local statusLabel = Instance.new("TextLabel")
statusLabel.Name = "StatusLabel"
statusLabel.Size = UDim2.new(1, 0, 0, 30)
statusLabel.BackgroundTransparency = 1
statusLabel.Text = ""
statusLabel.TextColor3 = Color3.fromRGB(200, 200, 200)
statusLabel.TextSize = 12
statusLabel.TextWrapped = true
statusLabel.Parent = scrollFrame

-- Progress Bar
local progressFrame = Instance.new("Frame")
progressFrame.Name = "ProgressFrame"
progressFrame.Size = UDim2.new(1, 0, 0, 20)
progressFrame.BackgroundColor3 = Color3.fromRGB(40, 40, 40)
progressFrame.BorderSizePixel = 0
progressFrame.Visible = false
progressFrame.Parent = scrollFrame

local progressBar = Instance.new("Frame")
progressBar.Name = "ProgressBar"
progressBar.Size = UDim2.new(0, 0, 1, 0)
progressBar.BackgroundColor3 = Color3.fromRGB(0, 162, 255)
progressBar.BorderSizePixel = 0
progressBar.Parent = progressFrame

-- Functions
local function updateStatus(text, color)
    statusLabel.Text = text
    statusLabel.TextColor3 = color or Color3.fromRGB(200, 200, 200)
end

local function updateProgress(percent)
    progressFrame.Visible = true
    progressBar.Size = UDim2.new(percent / 100, 0, 1, 0)
end

local function createPartFromData(partData, parent)
    local part = Instance.new("Part")
    part.Name = partData.name or "Part"
    part.Size = Vector3.new(
        partData.size.x or 4,
        partData.size.y or 4,
        partData.size.z or 4
    )
    part.Position = Vector3.new(
        partData.position.x or 0,
        partData.position.y or 0,
        partData.position.z or 0
    )
    
    if partData.rotation then
        part.Orientation = Vector3.new(
            partData.rotation.x or 0,
            partData.rotation.y or 0,
            partData.rotation.z or 0
        )
    end
    
    if partData.material then
        part.Material = Enum.Material[partData.material] or Enum.Material.Plastic
    end
    
    if partData.color then
        part.Color = Color3.fromRGB(
            partData.color[1] or 200,
            partData.color[2] or 200,
            partData.color[3] or 200
        )
    end
    
    part.Anchored = true
    part.Parent = parent
    
    return part
end

local function createModelFromData(modelData, parent)
    local model = Instance.new("Model")
    model.Name = modelData.name or "Model"
    model.PrimaryPart = nil
    
    for _, partData in ipairs(modelData.parts or {}) do
        local part = createPartFromData(partData, model)
        if not model.PrimaryPart then
            model.PrimaryPart = part
        end
    end
    
    if modelData.position then
        local cf = CFrame.new(
            modelData.position.x or 0,
            modelData.position.y or 0,
            modelData.position.z or 0
        )
        if model.PrimaryPart then
            model:SetPrimaryPartCFrame(cf)
        end
    end
    
    model.Parent = parent
    return model
end

local function generateTerrain(terrainData, workspace)
    -- Placeholder terrain generation
    -- In production, this would use Roblox Terrain API
    updateStatus("Terrain generation not fully implemented in this version", Color3.fromRGB(255, 200, 0))
end

local function importWorld(worldData)
    local workspace = game:GetService("Workspace")
    
    -- Create world folder
    local worldFolder = Instance.new("Folder")
    worldFolder.Name = "GeneratedWorld_" .. os.time()
    worldFolder.Parent = workspace
    
    -- Generate terrain
    if worldData.workspace.terrain then
        generateTerrain(worldData.workspace.terrain, workspace)
    end
    
    -- Create parts
    for _, partData in ipairs(worldData.workspace.parts or {}) do
        createPartFromData(partData, worldFolder)
    end
    
    -- Create models
    for _, modelData in ipairs(worldData.workspace.models or {}) do
        createModelFromData(modelData, worldFolder)
    end
    
    Selection:Set({worldFolder})
    updateStatus("World imported successfully!", Color3.fromRGB(0, 255, 0))
end

local function checkStatus(jobId)
    local success, response = pcall(function()
        return HttpService:GetAsync(API_URL .. "/api/status/" .. jobId)
    end)
    
    if not success then
        updateStatus("Error checking status: " .. tostring(response), Color3.fromRGB(255, 0, 0))
        return false
    end
    
    local statusData = HttpService:JSONDecode(response)
    
    if statusData.status == "completed" then
        updateProgress(100)
        -- Download world
        local downloadSuccess, worldResponse = pcall(function()
            return HttpService:GetAsync(API_URL .. "/api/download/" .. jobId)
        end)
        
        if downloadSuccess then
            local worldData = HttpService:JSONDecode(worldResponse)
            importWorld(worldData)
            progressFrame.Visible = false
            return true
        else
            updateStatus("Error downloading world: " .. tostring(worldResponse), Color3.fromRGB(255, 0, 0))
            return false
        end
    elseif statusData.status == "failed" then
        updateStatus("Generation failed: " .. (statusData.error or "Unknown error"), Color3.fromRGB(255, 0, 0))
        progressFrame.Visible = false
        return false
    else
        updateProgress(statusData.progress or 0)
        updateStatus("Generating... " .. (statusData.progress or 0) .. "%", Color3.fromRGB(0, 162, 255))
        return true
    end
end

local function startGeneration()
    local prompt = promptBox.Text
    if prompt == "" then
        updateStatus("Please enter a world description", Color3.fromRGB(255, 200, 0))
        return
    end
    
    updateStatus("Starting generation...", Color3.fromRGB(0, 162, 255))
    progressFrame.Visible = true
    updateProgress(0)
    generateButton.Enabled = false
    
    local requestData = {
        prompt = prompt,
        world_size = currentSize,
        complexity = selectedComplexity,
        include_terrain = true,
        include_structures = true,
        include_objects = true
    }
    
    local success, response = pcall(function()
        return HttpService:PostAsync(
            API_URL .. "/api/generate",
            HttpService:JSONEncode(requestData),
            Enum.HttpContentType.ApplicationJson
        )
    end)
    
    if not success then
        updateStatus("Error: " .. tostring(response), Color3.fromRGB(255, 0, 0))
        progressFrame.Visible = false
        generateButton.Enabled = true
        return
    end
    
    local responseData = HttpService:JSONDecode(response)
    local jobId = responseData.job_id
    
    -- Poll for status
    local connection
    connection = game:GetService("RunService").Heartbeat:Connect(function()
        if not checkStatus(jobId) then
            connection:Disconnect()
            generateButton.Enabled = true
        end
    end)
end

-- Event Handlers
generateButton.MouseButton1Click:Connect(startGeneration)

button.Click:Connect(function()
    widget.Enabled = not widget.Enabled
end)

-- Update scroll frame size
uiListLayout:GetPropertyChangedSignal("AbsoluteContentSize"):Connect(function()
    scrollFrame.CanvasSize = UDim2.new(0, 0, 0, uiListLayout.AbsoluteContentSize.Y + 20)
end)

