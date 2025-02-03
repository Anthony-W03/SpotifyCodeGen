# Development Notes - Spotify Door Decoration Generator

This document contains the chat history and development process of creating the door decoration generator. It tracks the evolution of features and problem-solving steps taken during development.

## Initial Setup and Base Functionality
- Started with need to automate retrieval of Spotify album images and codes
- Implemented basic Spotify API integration using spotipy
- Created initial script to handle album URLs and download artwork

## Key Development Steps

### Album Artwork and Spotify Code Integration
- Set up functions to extract album IDs from Spotify URLs
- Implemented image downloading and processing
- Added Spotify code generation functionality

### Image Composition
- Created composite image layout (1080x1450)
- Added album artwork (1080x1080)
- Integrated Spotify code (1080x300)
- Implemented text overlay for names

### Text and Font Handling
- Added name text centered at top of image
- Resolved font loading issues with Fredoka One
- Fixed text centering calculations
- Implemented proper font path handling for Windows

### Playlist Support
- Extended functionality to handle both album and playlist URLs
- Modified URL parsing to detect content type
- Updated API calls to handle both content types

### Final Optimizations
- Created .gitignore for clean repository
- Added comprehensive README
- Documented development process

## Issues Addressed
1. Fixed "NoneType object has no attribute resize" error
2. Resolved text centering issues
3. Addressed font loading and path issues
4. Handled both album and playlist URL formats
