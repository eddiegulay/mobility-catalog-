"""
Image search utilities for finding stock images.

Uses Unsplash API for free high-quality stock images.
"""

import os
import requests
from typing import List, Tuple
from utils.logger import logger


def search_unsplash_images(query: str, count: int = 3) -> List[str]:
    """
    Search for stock images on Unsplash.
    
    Args:
        query: Search query for images
        count: Number of images to retrieve (max 3)
        
    Returns:
        List of image URLs
    """
    # Unsplash offers free API access with attribution
    # For production, get API key from https://unsplash.com/developers
    
    # Using Unsplash Source API (no auth required for basic usage)
    # Format: https://source.unsplash.com/800x600/?{query}
    
    images = []
    
    # Generate multiple image URLs with different variations
    search_terms = generate_search_terms(query)
    
    for i, term in enumerate(search_terms[:count]):
        # Unsplash source URL with unique seed for variation
        url = f"https://source.unsplash.com/800x600/?{term}&sig={i}"
        images.append(url)
        logger.debug(f"Generated image URL for '{term}': {url}")
    
    return images


def generate_search_terms(measure_name: str) -> List[str]:
    """
    Generate relevant search terms for a mobility measure.
    
    Args:
        measure_name: Name of the mobility measure
        
    Returns:
        List of search terms
    """
    # Clean and prepare base term
    base_term = measure_name.lower().replace(" ", ",")
    
    # Generate variations
    terms = [
        base_term,
        f"{base_term},urban",
        f"{base_term},city",
        f"{base_term},sustainable,transport",
        f"{base_term},mobility"
    ]
    
    return terms


def get_mobility_measure_images(measure_name: str, count: int = 3) -> List[str]:
    """
    Get stock images for a mobility measure.
    
    This is the main function used by agents.
    
    Args:
        measure_name: Name of the mobility measure
        count: Number of images (1-3 recommended)
        
    Returns:
        List of image URLs
    """
    try:
        images = search_unsplash_images(measure_name, min(count, 3))
        logger.info(f"Retrieved {len(images)} images for '{measure_name}'")
        return images
    except Exception as e:
        logger.error(f"Error retrieving images: {e}")
        return []
