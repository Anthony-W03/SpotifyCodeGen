import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import requests
from urllib.parse import quote
import os
import re
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from album_urls import albums, playlists
from Spotify_Creds import Spotify_ID, Spotify_Secret

# Initialize Spotify client
client_credentials_manager = SpotifyClientCredentials(
    client_id=Spotify_ID, 
    client_secret=Spotify_Secret
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def extract_id(spotify_url):
    # Extract album ID from various Spotify URL formats
    patterns = [
        r'album/([a-zA-Z0-9]{22})',  # Album pattern
        r'playlist/([a-zA-Z0-9]{22})',  # Playlist pattern
        r'spotify:album:([a-zA-Z0-9]{22})',  # Album URI
        r'spotify:playlist:([a-zA-Z0-9]{22})'  # Playlist URI
    ]
    
    for pattern in patterns:
        match = re.search(pattern, spotify_url)
        if match:
            return match.group(1), 'playlist' if 'playlist' in pattern else 'album'
    return None, None

def get_item_info(spotify_url):
    item_id, item_type = extract_id(spotify_url)
    if not item_id:
        print(f"Could not extract album ID from URL: {spotify_url}")
        return None
    
    try:
        if item_type == 'album':
            item = sp.album(item_id)
            item_info = {
                'name': item['name'],
                'image_url': item['images'][0]['url'],
                'spotify_uri': item['uri'],
                'spotify_code_url': generate_spotify_code(item['uri'])
            }
        else:  # playlist
            item = sp.playlist(item_id)
            item_info = {
                'name': item['name'],
                'image_url': item['images'][0]['url'],
                'spotify_uri': item['uri'],
                'spotify_code_url': generate_spotify_code(item['uri'])
            }
        
        return item_info
    except Exception as e:
        print(f"Error getting album info: {e}")
        return None

def generate_spotify_code(spotify_uri):
    # Generate Spotify code URL
    # Format options: 'svg' or 'png'
    # Background/code colors should be hex values without '#'
    format_type = 'png'
    background_color = '000000'  # Black background
    code_color = 'white'  # White code
    size = 300  # Size in pixels
    
    code_url = f'https://scannables.scdn.co/uri/plain/{format_type}/{background_color}/{code_color}/{size}/{spotify_uri}'
    
    return code_url

def download_image(url):
    response = requests.get(url)
    #print(response.status_code)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    return None

def create_composite_image(person_name, album_info):
    # Create a white background
    WIDTH = 1080
    HEIGHT = 1460
    composite = Image.new('RGB', (WIDTH, HEIGHT), 'white')
    draw = ImageDraw.Draw(composite)
    
    try:
        # Download and resize album artwork

        album_art = download_image(album_info['image_url'])
        album_art = album_art.resize((1080,1080))
        
        # Download and resize Spotify code
        spotify_code = download_image(album_info['spotify_code_url'])
        spotify_code = spotify_code.resize((1080, 300))
        
        # Place album art on the left
        composite.paste(album_art, (0, 90))
        
        # Place Spotify code in the middle
        composite.paste(spotify_code, (0, 1170))
        
        # Try to use a nice font, fall back to default if not available
        try:
            font = ImageFont.truetype("C:/Users/Anthony/Appdata/Local/Microsoft/Windows/Fonts/Fredoka-VariableFont_wdth,wght.ttf", 72)
        except Exception as e:
            print(f"font failed: {e}")
            font = ImageFont.load_default(70)
        
        # Add person's name at the top right
        name_bbox = draw.textbbox((0,0), person_name, font=font)
        name_width = name_bbox[2] - name_bbox[0]
        name_x = (WIDTH - name_width) // 2
        draw.text((name_x, -2), person_name, fill='black',stroke_width=3, font=font)
        
        return composite
    
    except Exception as e:
        print(f"Error creating composite image: {e}")
        return None

def process_albums(albums_dict):
    # Create output directory if it doesn't exist
    if not os.path.exists('album_assets'):
        os.makedirs('album_assets')
    
    albums_info = {}
    
    for person, url in albums_dict.items():
        print(f"Processing album for: {person}")
        album_info = get_item_info(url)
        
        if album_info:
            # Create composite image
            composite = create_composite_image(person, album_info)
            
            if composite:
                # Save the composite image
                safe_name = re.sub(r'[<>:"/\\|?*]', '', person)
                composite.save(f"album_assets/{safe_name}_composite.png")
                
                # Store the information
                albums_info[person] = album_info
                print(f"✓ Created composite image for: {person}")
        else:
            print(f"✗ Could not process URL for: {person}")
    
    # Save all album information to a JSON file
    with open('album_assets/albums_info.json', 'w') as f:
        json.dump(albums_info, f, indent=2)

if __name__ == "__main__":
    process_albums(albums)
    process_albums(playlists)
