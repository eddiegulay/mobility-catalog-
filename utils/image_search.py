"""
Image search utilities using Pexels API.

Pexels provides free high-quality stock photos and videos.
API Documentation: https://www.pexels.com/api/documentation/
"""

import requests
from typing import List, Dict, Any
from config.settings import settings
from utils.logger import logger


class PexelsImageSearch:
    """Pexels API client for searching stock images."""
    
    BASE_URL = "https://api.pexels.com/v1"
    
    def __init__(self, api_key: str = None):
        """
        Initialize Pexels API client.
        
        Args:
            api_key: Pexels API key (from settings if not provided)
        """
        self.api_key = api_key or settings.PEXELS_API_KEY
        if not self.api_key:
            logger.warning("PEXELS_API_KEY not set, image search will be disabled")
        
        self.headers = {
            "Authorization": self.api_key
        }
    
    def search_photos(
        self, 
        query: str, 
        per_page: int = 3,
        orientation: str = "landscape"
    ) -> List[Dict[str, Any]]:
        """
        Search for photos on Pexels.
        
        Args:
            query: Search query
            per_page: Number of results (max 80, we use 3)
            orientation: Image orientation (landscape/portrait/square)
            
        Returns:
            List of photo dictionaries with URLs and metadata
        """
        if not self.api_key:
            logger.error("Cannot search images: PEXELS_API_KEY not configured")
            return []
        
        endpoint = f"{self.BASE_URL}/search"
        params = {
            "query": query,
            "per_page": min(per_page, 3),  # Max 3 images
            "orientation": orientation
        }
        
        try:
            response = requests.get(
                endpoint,
                headers=self.headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                photos = data.get("photos", [])
                
                logger.info(f"Found {len(photos)} images for query: '{query}'")
                return photos
            else:
                logger.error(
                    f"Pexels API error: {response.status_code} - {response.text}"
                )
                return []
                
        except Exception as e:
            logger.error(f"Error searching Pexels: {e}")
            return []
    
    def get_image_urls(
        self, 
        query: str, 
        count: int = 3,
        size: str = "large"
    ) -> List[str]:
        """
        Get image URLs for a search query.
        
        Args:
            query: Search query
            count: Number of images (max 3)
            size: Image size (original/large/large2x/medium/small)
            
        Returns:
            List of image URLs
        """
        photos = self.search_photos(query, per_page=count)
        
        if not photos:
            logger.warning(f"No images found for: '{query}'")
            return []
        
        # Extract URLs based on requested size
        urls = []
        for photo in photos:
            src = photo.get("src", {})
            
            # Priority: large -> large2x -> original -> medium
            url = (
                src.get(size) or 
                src.get("large") or 
                src.get("large2x") or 
                src.get("original") or
                src.get("medium")
            )
            
            if url:
                urls.append(url)
        
        return urls


# Global instance
_pexels_client = None


def get_pexels_client() -> PexelsImageSearch:
    """Get or create global Pexels client instance."""
    global _pexels_client
    if _pexels_client is None:
        _pexels_client = PexelsImageSearch()
    return _pexels_client


def search_mobility_images(measure_name: str, count: int = 3) -> List[str]:
    """
    Search for mobility measure images using Pexels.
    
    This is the main function used by agents.
    
    Args:
        measure_name: Name of the mobility measure
        count: Number of images (1-3)
        
    Returns:
        List of image URLs
    """
    client = get_pexels_client()
    
    # Clean and prepare search query
    # For Pexels, simpler queries work better
    query = measure_name.lower()
    
    # Try main query first
    urls = client.get_image_urls(query, count=count, size="large")
    
    # If not enough results, try with "urban mobility" addition
    if len(urls) < count:
        logger.info(f"Only found {len(urls)} images, trying broader query")
        query_alt = f"{query} urban mobility"
        urls_alt = client.get_image_urls(query_alt, count=count-len(urls), size="large")
        urls.extend(urls_alt)
    
    # Ensure we have at least some images
    if not urls:
        logger.warning(f"No images found for '{measure_name}', trying generic 'sustainable transport'")
        urls = client.get_image_urls("sustainable transport", count=count, size="large")
    
    return urls[:count]  # Return max requested count


# Alias for backward compatibility
get_mobility_measure_images = search_mobility_images
