"""
Prompt processing module - converts natural language to world specifications
"""
import os
from typing import Dict, Any, Optional
from openai import OpenAI

class PromptProcessor:
    """Processes natural language prompts into structured world specifications"""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.client = OpenAI(api_key=api_key)
    
    async def process(self, prompt: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process a natural language prompt into a structured world specification
        
        Args:
            prompt: Natural language description of the world
            options: Additional options (style, complexity, etc.)
        
        Returns:
            Dictionary containing structured world specification
        """
        options = options or {}
        
        system_prompt = """You are a world generation expert for Roblox. 
Convert user descriptions into structured world specifications.

Return a JSON object with the following structure:
{
    "terrain": {
        "type": "mountain|valley|plains|island|desert|forest",
        "height_variation": 0.0-1.0,
        "features": ["hills", "rivers", "caves", etc.]
    },
    "structures": [
        {
            "type": "building|castle|house|tower|bridge",
            "position": {"x": 0-1, "y": 0-1, "z": 0-1},
            "size": {"width": 1-100, "height": 1-100, "depth": 1-100},
            "style": "medieval|modern|fantasy|sci-fi"
        }
    ],
    "objects": [
        {
            "type": "tree|rock|furniture|decoration",
            "position": {"x": 0-1, "y": 0-1, "z": 0-1},
            "count": 1-100,
            "spread": 0.0-1.0
        }
    ],
    "atmosphere": {
        "lighting": "bright|dim|dark|sunset",
        "weather": "clear|cloudy|foggy|rainy",
        "color_scheme": ["#hexcolor1", "#hexcolor2"]
    },
    "theme": "description of overall theme"
}"""
        
        user_prompt = f"""Generate a world specification for: "{prompt}"
        
Additional requirements:
- Style: {options.get('style', 'any')}
- Complexity: {options.get('complexity', 'medium')}

Return only valid JSON, no additional text."""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            import json
            world_spec = json.loads(response.choices[0].message.content)
            
            # Validate and normalize the specification
            return self._normalize_spec(world_spec)
            
        except Exception as e:
            # Log error but continue with fallback
            print(f"GPT-4 API error: {e}. Using fallback parser.")
            # Fallback to basic parsing if API fails
            return self._fallback_parse(prompt, options)
    
    def _normalize_spec(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize and validate world specification"""
        # Ensure all required fields exist
        normalized = {
            "terrain": spec.get("terrain", {"type": "plains", "height_variation": 0.3}),
            "structures": spec.get("structures", []),
            "objects": spec.get("objects", []),
            "atmosphere": spec.get("atmosphere", {
                "lighting": "bright",
                "weather": "clear",
                "color_scheme": ["#87CEEB", "#90EE90"]
            }),
            "theme": spec.get("theme", "generic")
        }
        
        return normalized
    
    def _fallback_parse(self, prompt: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback parser for when API is unavailable"""
        prompt_lower = prompt.lower()
        
        # Simple keyword-based parsing
        terrain_type = "plains"
        if any(word in prompt_lower for word in ["mountain", "hill", "peak"]):
            terrain_type = "mountain"
        elif any(word in prompt_lower for word in ["valley", "canyon"]):
            terrain_type = "valley"
        elif any(word in prompt_lower for word in ["island", "beach", "ocean"]):
            terrain_type = "island"
        elif any(word in prompt_lower for word in ["desert", "sand"]):
            terrain_type = "desert"
        elif any(word in prompt_lower for word in ["forest", "tree", "wood"]):
            terrain_type = "forest"
        
        structures = []
        if any(word in prompt_lower for word in ["castle", "fortress"]):
            structures.append({
                "type": "castle",
                "position": {"x": 0.5, "y": 0.0, "z": 0.5},
                "size": {"width": 50, "height": 80, "depth": 50},
                "style": "medieval"
            })
        elif any(word in prompt_lower for word in ["house", "building", "village"]):
            structures.append({
                "type": "house",
                "position": {"x": 0.5, "y": 0.0, "z": 0.5},
                "size": {"width": 20, "height": 30, "depth": 20},
                "style": "medieval"
            })
        
        return {
            "terrain": {
                "type": terrain_type,
                "height_variation": 0.5,
                "features": []
            },
            "structures": structures,
            "objects": [],
            "atmosphere": {
                "lighting": "bright",
                "weather": "clear",
                "color_scheme": ["#87CEEB", "#90EE90"]
            },
            "theme": prompt
        }

