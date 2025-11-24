"""
AI-powered screenshot analysis using Google Gemini Vision
"""
import base64
import json
from pathlib import Path
from typing import Dict, Optional
import os


class AIAnalyzer:
    """Analyze screenshots using Google Gemini Vision API"""
    
    def __init__(self, api_key: Optional[str] = None, logger=None):
        """Initialize AI analyzer
        
        Args:
            api_key: Google Gemini API key
            logger: Optional logger instance
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.logger = logger
        self.model = None
        
        if self.api_key:
            self._initialize_gemini()
    
    def _initialize_gemini(self):
        """Initialize Gemini model"""
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            
            if self.logger:
                self.logger.info("Gemini AI initialized successfully")
        except ImportError:
            if self.logger:
                self.logger.error("google-generativeai package not installed")
            raise Exception("Please install: pip install google-generativeai")
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to initialize Gemini: {e}")
            raise
    
    def is_configured(self) -> bool:
        """Check if AI is properly configured"""
        return self.model is not None
    
    def analyze_screenshot(self, image_path: Path) -> Dict[str, str]:
        """Analyze screenshot and extract documentation fields
        
        Args:
            image_path: Path to screenshot image
            
        Returns:
            Dict with title, details, location_type, location_url
        """
        if not self.is_configured():
            raise Exception("AI not configured. Please set API key.")
        
        try:
            # Read image
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            # Create prompt
            prompt = self._create_analysis_prompt()
            
            # Import PIL for image
            from PIL import Image
            import io
            pil_image = Image.open(io.BytesIO(image_data))
            
            # Send to Gemini
            if self.logger:
                self.logger.info(f"Analyzing screenshot: {image_path.name}")
            
            response = self.model.generate_content([prompt, pil_image])
            
            # Parse response
            result = self._parse_response(response.text)
            
            if self.logger:
                self.logger.info(f"AI analysis complete: {result.get('title', 'No title')}")
            
            return result
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"AI analysis failed: {e}", exc_info=True)
            raise Exception(f"AI analysis failed: {str(e)}")
    
    def _create_analysis_prompt(self) -> str:
        """Create prompt for Gemini"""
        return """Analyze this screenshot and extract documentation information.

Provide a JSON response with these fields:
- title: A concise, descriptive title (max 60 characters) that captures what this screenshot shows
- details: A 2-3 sentence description of what's visible, what's being demonstrated, and any notable elements
- location_type: One of: "web", "app", "desktop", "mobile", "other"
- location_url: The URL (if web), file path (if desktop), or app name (if application)

Rules:
- Be concise and clear
- Focus on what's being documented or demonstrated
- Extract any visible URLs, paths, or application names
- If you can't determine something, use appropriate defaults

Example response:
{
  "title": "Login Page - Email Validation Error",
  "details": "Screenshot shows a login form with an email validation error. The error message 'Invalid email format' appears below the email field in red text. Submit button is disabled.",
  "location_type": "web",
  "location_url": "https://app.example.com/login"
}

Respond ONLY with valid JSON, no additional text."""
    
    def _parse_response(self, response_text: str) -> Dict[str, str]:
        """Parse Gemini response into structured data"""
        try:
            # Remove markdown code blocks if present
            text = response_text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()
            
            # Parse JSON
            data = json.loads(text)
            
            # Validate and set defaults
            result = {
                "title": data.get("title", "Untitled Screenshot")[:60],
                "details": data.get("details", ""),
                "location_type": data.get("location_type", "other").lower(),
                "location_url": data.get("location_url", "")
            }
            
            # Validate location_type
            valid_types = ["web", "app", "desktop", "mobile", "other"]
            if result["location_type"] not in valid_types:
                result["location_type"] = "other"
            
            return result
            
        except json.JSONDecodeError as e:
            if self.logger:
                self.logger.error(f"Failed to parse JSON response: {e}")
                self.logger.debug(f"Response text: {response_text}")
            
            # Fallback: try to extract some basic info
            return {
                "title": "Screenshot (AI parsing failed)",
                "details": response_text[:200] if response_text else "",
                "location_type": "other",
                "location_url": ""
            }
    
    def test_connection(self) -> bool:
        """Test API connection
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            if not self.is_configured():
                return False
            
            # Simple test prompt
            response = self.model.generate_content("Reply with just 'OK'")
            return "OK" in response.text.upper()
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"API test failed: {e}")
            return False


def get_api_key_from_file() -> Optional[str]:
    """Load API key from config file if it exists
    
    Returns:
        API key or None
    """
    try:
        config_file = Path.home() / ".docshot" / "gemini_key.txt"
        if config_file.exists():
            return config_file.read_text().strip()
    except:
        pass
    return None


def save_api_key_to_file(api_key: str) -> bool:
    """Save API key to config file
    
    Args:
        api_key: API key to save
        
    Returns:
        True if successful
    """
    try:
        config_dir = Path.home() / ".docshot"
        config_dir.mkdir(exist_ok=True)
        config_file = config_dir / "gemini_key.txt"
        config_file.write_text(api_key)
        return True
    except Exception as e:
        return False
