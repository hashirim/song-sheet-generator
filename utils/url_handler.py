from typing import Dict, Optional

def get_song_url(urls: Dict[str, str]) -> Optional[str]:
    """Get the preferred URL for a song based on priority"""
    url_priority = ['bandcamp', 'soundcloud', 'youtu', 'youtube']
    
    # Check priority list
    for key in url_priority:
        if key in urls:
            return urls[key]
    
    # If none found in priority, return first alphabetically
    if urls:
        return urls[sorted(urls.keys())[0]]
    
    return None

