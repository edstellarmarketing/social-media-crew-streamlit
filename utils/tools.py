from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from serpapi import GoogleSearch
import os
import json
from typing import Type

class ImageSearchInput(BaseModel):
    """Input for image search tools"""
    query: str = Field(..., description="Search query for finding images")

class GoogleImageSearchTool(BaseTool):
    name: str = "Google Image Search Tool"
    description: str = "Search for images on Google Images. Returns JSON with image results."
    args_schema: Type[BaseModel] = ImageSearchInput
    
    def _run(self, query: str) -> str:
        try:
            params = {
                "engine": "google_images",
                "q": query,
                "api_key": os.getenv("SERPAPI_KEY"),
                "num": 10,
                "safe": "active"
            }
            
            search = GoogleSearch(params)
            results = search.get_dict()
            
            images = []
            if "images_results" in results:
                for img in results["images_results"][:10]:
                    images.append({
                        "title": img.get("title", "")[:100],
                        "source": img.get("source", ""),
                        "link": img.get("original", ""),
                        "thumbnail": img.get("thumbnail", ""),
                        "platform": "Google Images"
                    })
            
            return json.dumps(images, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)})

class PinterestSearchTool(BaseTool):
    name: str = "Pinterest Image Search Tool"
    description: str = "Search for images on Pinterest. Returns JSON with pin results."
    args_schema: Type[BaseModel] = ImageSearchInput
    
    def _run(self, query: str) -> str:
        try:
            params = {
                "engine": "pinterest",
                "q": query,
                "api_key": os.getenv("SERPAPI_KEY")
            }
            
            search = GoogleSearch(params)
            results = search.get_dict()
            
            images = []
            if "pinterest_results" in results:
                for pin in results["pinterest_results"][:10]:
                    images.append({
                        "title": pin.get("title", "")[:100],
                        "source": pin.get("link", ""),
                        "link": pin.get("image", ""),
                        "thumbnail": pin.get("thumbnail", ""),
                        "platform": "Pinterest"
                    })
            
            return json.dumps(images, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)})

class SlideShareSearchTool(BaseTool):
    name: str = "SlideShare Search Tool"
    description: str = "Search for SlideShare presentations. Returns JSON with results."
    args_schema: Type[BaseModel] = ImageSearchInput
    
    def _run(self, query: str) -> str:
        try:
            params = {
                "engine": "google",
                "q": f"site:slideshare.net OR site:scribd.com {query}",
                "api_key": os.getenv("SERPAPI_KEY"),
                "num": 8
            }
            
            search = GoogleSearch(params)
            results = search.get_dict()
            
            presentations = []
            if "organic_results" in results:
                for result in results["organic_results"][:8]:
                    presentations.append({
                        "title": result.get("title", ""),
                        "source": result.get("link", ""),
                        "snippet": result.get("snippet", ""),
                        "platform": "SlideShare/Scribd"
                    })
            
            return json.dumps(presentations, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)})