"""
World generation engine - creates world data from specifications
"""
import numpy as np
from typing import Dict, Any, List, Tuple
import random
import math
from datetime import datetime

class WorldGenerator:
    """Generates world data from structured specifications"""
    
    def __init__(self):
        self.terrain_generators = {
            "mountain": self._generate_mountain_terrain,
            "valley": self._generate_valley_terrain,
            "plains": self._generate_plains_terrain,
            "island": self._generate_island_terrain,
            "desert": self._generate_desert_terrain,
            "forest": self._generate_forest_terrain
        }
    
    async def generate(self, spec: Dict[str, Any], options: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate world data from specification
        
        Args:
            spec: World specification from prompt processor
            options: Generation options (size, includes, etc.)
        
        Returns:
            Dictionary containing complete world data
        """
        world_size = options.get("size", 512)
        
        world_data = {
            "size": world_size,
            "terrain": None,
            "structures": [],
            "objects": [],
            "atmosphere": spec.get("atmosphere", {}),
            "theme": spec.get("theme", "generic")
        }
        
        # Generate terrain
        if options.get("include_terrain", True):
            terrain_type = spec.get("terrain", {}).get("type", "plains")
            generator = self.terrain_generators.get(terrain_type, self._generate_plains_terrain)
            world_data["terrain"] = generator(
                world_size,
                spec.get("terrain", {})
            )
        
        # Generate structures
        if options.get("include_structures", True):
            for struct_spec in spec.get("structures", []):
                structure = self._generate_structure(struct_spec, world_size)
                if structure:
                    world_data["structures"].append(structure)
        
        # Generate objects
        if options.get("include_objects", True):
            for obj_spec in spec.get("objects", []):
                objects = self._generate_objects(obj_spec, world_size)
                world_data["objects"].extend(objects)
        
        return world_data
    
    def _generate_mountain_terrain(self, size: int, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate mountain terrain"""
        height_variation = config.get("height_variation", 0.5)
        resolution = min(size // 4, 128)
        
        # Create heightmap using Perlin-like noise
        heights = np.zeros((resolution, resolution))
        center_x, center_y = resolution // 2, resolution // 2
        
        for i in range(resolution):
            for j in range(resolution):
                # Distance from center
                dist = math.sqrt((i - center_x)**2 + (j - center_y)**2)
                max_dist = math.sqrt(center_x**2 + center_y**2)
                
                # Base height (higher in center)
                base_height = max(0, 1 - (dist / max_dist) * 1.5)
                
                # Add noise
                noise = random.uniform(-0.2, 0.2)
                
                # Combine
                height = (base_height + noise) * height_variation * 100
                heights[i][j] = max(0, height)
        
        return {
            "type": "mountain",
            "heightmap": heights.tolist(),
            "resolution": resolution,
            "max_height": float(np.max(heights))
        }
    
    def _generate_valley_terrain(self, size: int, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate valley terrain"""
        resolution = min(size // 4, 128)
        heights = np.zeros((resolution, resolution))
        
        for i in range(resolution):
            for j in range(resolution):
                # Valley shape (lower in center, higher on edges)
                center_dist = abs(i - resolution // 2) / (resolution // 2)
                height = center_dist * 30 + random.uniform(-5, 5)
                heights[i][j] = max(0, height)
        
        return {
            "type": "valley",
            "heightmap": heights.tolist(),
            "resolution": resolution,
            "max_height": float(np.max(heights))
        }
    
    def _generate_plains_terrain(self, size: int, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate flat plains terrain"""
        resolution = min(size // 4, 128)
        heights = np.zeros((resolution, resolution))
        
        # Slight random variation
        for i in range(resolution):
            for j in range(resolution):
                heights[i][j] = random.uniform(0, 5)
        
        return {
            "type": "plains",
            "heightmap": heights.tolist(),
            "resolution": resolution,
            "max_height": 5.0
        }
    
    def _generate_island_terrain(self, size: int, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate island terrain"""
        resolution = min(size // 4, 128)
        heights = np.zeros((resolution, resolution))
        center_x, center_y = resolution // 2, resolution // 2
        
        for i in range(resolution):
            for j in range(resolution):
                dist = math.sqrt((i - center_x)**2 + (j - center_y)**2)
                max_dist = resolution // 2
                
                # Island shape (circular, higher in center)
                if dist < max_dist:
                    height = (1 - dist / max_dist) * 40 + random.uniform(-2, 2)
                    heights[i][j] = max(0, height)
                else:
                    heights[i][j] = -10  # Water level
        
        return {
            "type": "island",
            "heightmap": heights.tolist(),
            "resolution": resolution,
            "max_height": float(np.max(heights))
        }
    
    def _generate_desert_terrain(self, size: int, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate desert terrain with dunes"""
        resolution = min(size // 4, 128)
        heights = np.zeros((resolution, resolution))
        
        for i in range(resolution):
            for j in range(resolution):
                # Dune pattern
                dune_height = math.sin(i * 0.1) * math.cos(j * 0.1) * 15
                heights[i][j] = 10 + dune_height + random.uniform(-2, 2)
        
        return {
            "type": "desert",
            "heightmap": heights.tolist(),
            "resolution": resolution,
            "max_height": float(np.max(heights))
        }
    
    def _generate_forest_terrain(self, size: int, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate forest terrain"""
        resolution = min(size // 4, 128)
        heights = np.zeros((resolution, resolution))
        
        for i in range(resolution):
            for j in range(resolution):
                heights[i][j] = random.uniform(5, 15)
        
        return {
            "type": "forest",
            "heightmap": heights.tolist(),
            "resolution": resolution,
            "max_height": 15.0
        }
    
    def _generate_structure(self, spec: Dict[str, Any], world_size: int) -> Dict[str, Any]:
        """Generate a structure from specification"""
        struct_type = spec.get("type", "building")
        position = spec.get("position", {"x": 0.5, "y": 0.0, "z": 0.5})
        size = spec.get("size", {"width": 20, "height": 30, "depth": 20})
        style = spec.get("style", "generic")
        
        # Convert relative positions to absolute
        x = int(position["x"] * world_size - world_size // 2)
        z = int(position["z"] * world_size - world_size // 2)
        y = int(position.get("y", 0) * 50)
        
        return {
            "type": struct_type,
            "position": {"x": x, "y": y, "z": z},
            "size": size,
            "style": style,
            "parts": self._generate_structure_parts(struct_type, size, style)
        }
    
    def _generate_structure_parts(self, struct_type: str, size: Dict[str, int], style: str) -> List[Dict[str, Any]]:
        """Generate individual parts for a structure"""
        parts = []
        
        if struct_type == "castle":
            # Main tower
            parts.append({
                "shape": "cylinder",
                "size": {"x": size["width"], "y": size["height"], "z": size["width"]},
                "position": {"x": 0, "y": size["height"] // 2, "z": 0},
                "material": "Brick",
                "color": [200, 200, 200]
            })
            # Walls
            wall_height = size["height"] // 3
            parts.append({
                "shape": "block",
                "size": {"x": size["width"] * 2, "y": wall_height, "z": 10},
                "position": {"x": 0, "y": wall_height // 2, "z": size["depth"] // 2},
                "material": "Brick",
                "color": [180, 180, 180]
            })
        elif struct_type in ["house", "building"]:
            # Main building
            parts.append({
                "shape": "block",
                "size": size,
                "position": {"x": 0, "y": size["height"] // 2, "z": 0},
                "material": "Wood",
                "color": [139, 90, 43]
            })
            # Roof
            parts.append({
                "shape": "wedge",
                "size": {"x": size["width"] + 2, "y": size["height"] // 3, "z": size["depth"] + 2},
                "position": {"x": 0, "y": size["height"] + size["height"] // 6, "z": 0},
                "material": "Wood",
                "color": [139, 69, 19]
            })
        else:
            # Generic building
            parts.append({
                "shape": "block",
                "size": size,
                "position": {"x": 0, "y": size["height"] // 2, "z": 0},
                "material": "Plastic",
                "color": [200, 200, 200]
            })
        
        return parts
    
    def _generate_objects(self, spec: Dict[str, Any], world_size: int) -> List[Dict[str, Any]]:
        """Generate multiple objects from specification"""
        obj_type = spec.get("type", "tree")
        position = spec.get("position", {"x": 0.5, "y": 0.0, "z": 0.5})
        count = spec.get("count", 10)
        spread = spec.get("spread", 0.2)
        
        objects = []
        center_x = int(position["x"] * world_size - world_size // 2)
        center_z = int(position["z"] * world_size - world_size // 2)
        
        for _ in range(count):
            # Random position within spread
            offset_x = random.uniform(-spread, spread) * world_size
            offset_z = random.uniform(-spread, spread) * world_size
            
            obj = {
                "type": obj_type,
                "position": {
                    "x": int(center_x + offset_x),
                    "y": 0,
                    "z": int(center_z + offset_z)
                },
                "size": self._get_object_size(obj_type),
                "rotation": random.uniform(0, 360)
            }
            objects.append(obj)
        
        return objects
    
    def _get_object_size(self, obj_type: str) -> Dict[str, int]:
        """Get default size for object type"""
        sizes = {
            "tree": {"x": 4, "y": 20, "z": 4},
            "rock": {"x": 3, "y": 3, "z": 3},
            "furniture": {"x": 4, "y": 4, "z": 4},
            "decoration": {"x": 2, "y": 2, "z": 2}
        }
        return sizes.get(obj_type, {"x": 2, "y": 2, "z": 2})
    
    async def to_roblox_format(self, world_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert world data to Roblox-compatible format"""
        roblox_world = {
            "version": "1.0",
            "metadata": {
                "size": world_data["size"],
                "theme": world_data.get("theme", "generic"),
                "generated_at": str(datetime.now())
            },
            "workspace": {
                "terrain": None,
                "parts": [],
                "models": []
            }
        }
        
        # Convert terrain
        if world_data.get("terrain"):
            roblox_world["workspace"]["terrain"] = self._convert_terrain(
                world_data["terrain"],
                world_data["size"]
            )
        
        # Convert structures
        for structure in world_data.get("structures", []):
            model = {
                "name": structure["type"],
                "parts": structure.get("parts", []),
                "position": structure["position"]
            }
            roblox_world["workspace"]["models"].append(model)
        
        # Convert objects
        for obj in world_data.get("objects", []):
            part = {
                "name": obj["type"],
                "shape": "block",
                "size": obj["size"],
                "position": obj["position"],
                "rotation": {"x": 0, "y": obj.get("rotation", 0), "z": 0},
                "material": self._get_material_for_object(obj["type"]),
                "color": self._get_color_for_object(obj["type"])
            }
            roblox_world["workspace"]["parts"].append(part)
        
        return roblox_world
    
    def _convert_terrain(self, terrain: Dict[str, Any], world_size: int) -> Dict[str, Any]:
        """Convert terrain data to Roblox format"""
        heightmap = terrain.get("heightmap", [])
        resolution = terrain.get("resolution", 64)
        
        # Scale heightmap to world size
        scale = world_size / resolution
        
        return {
            "type": terrain.get("type", "plains"),
            "heightmap": heightmap,
            "resolution": resolution,
            "scale": scale,
            "max_height": terrain.get("max_height", 50)
        }
    
    def _get_material_for_object(self, obj_type: str) -> str:
        """Get Roblox material for object type"""
        materials = {
            "tree": "Wood",
            "rock": "Rock",
            "furniture": "Wood",
            "decoration": "Plastic"
        }
        return materials.get(obj_type, "Plastic")
    
    def _get_color_for_object(self, obj_type: str) -> List[int]:
        """Get color for object type"""
        colors = {
            "tree": [34, 139, 34],  # Forest green
            "rock": [128, 128, 128],  # Gray
            "furniture": [139, 90, 43],  # Brown
            "decoration": [255, 215, 0]  # Gold
        }
        return colors.get(obj_type, [200, 200, 200])

