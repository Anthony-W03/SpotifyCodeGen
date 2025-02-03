# Spotify Door Decoration Generator

A Python script that generates composite images of Spotify album/playlist art, Spotify codes and with people's names.

## Features
- Processes both Spotify albums and playlists
- Downloads high-resolution album/playlist artwork
- Generates Spotify scannable codes
- Creates composite images with custom text overlay
- Supports custom font selection and positioning
- Handles multiple entries via dictionary input

## Requirements
### Libraries
- `spotipy`: Spotify Web API interaction
- `Pillow`: Image processing and text overlay
- `requests`: HTTP requests for downloading images
- `re`: Regular expression parsing for Spotify URLs

### Additional Requirements
- Spotify Developer account credentials (Client ID and Secret)
- Custom font files (if using non-system fonts)

## Core Functions

### `extract_id(spotify_url)`
Extracts the Spotify ID and determines if the URL is for an album or playlist.

### `get_item_info(spotify_url)`
Retrieves metadata for a Spotify item (album or playlist) including:
- Item name
- Cover artwork URL
- Spotify URI
- Generated Spotify code URL

### `download_image(url)`
Downloads and processes images from URLs using the requests library.

### `create_composite_image(person_name, item_info)`
Creates the final composite image by:
- Setting up a white canvas (1080x1450)
- Placing the album/playlist artwork
- Adding the Spotify code
- Overlaying centered text with the person's name
- Applying custom font styling

## Usage
1. Set up Spotify API credentials
2. Prepare a dictionary of names and Spotify URLs ( Ex: {'Bob':'playlist_url'} )
3. Run the script to generate customized door decorations
4. Find output images in the 'album_assets' directory

## Note
The script requires valid Spotify URLs and proper API credentials to function. Ensure all dependencies are installed and credentials are properly configured before running.