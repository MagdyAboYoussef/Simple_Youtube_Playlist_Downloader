# YouTube Playlist Downloader

A simple desktop application to download YouTube playlists in MP3 or MP4 format.
<img width="802" height="797" alt="image" src="https://github.com/user-attachments/assets/65a239f6-befd-4b2c-90c5-c48fbe71633c" />

## About

This is a simple script to download YouTube playlists. I was searching for online sites or simple scripts to download music but didn't find any that worked well, so I created this tool. I use it from time to time and thought it would be helpful to share. An executable is provided if you prefer not to run the Python code directly.

## Features

- Download entire YouTube playlists
- MP3 audio extraction
- MP4 video downloads with custom quality selection ( 1080p, 720p, 480p, 360p)
- Clean interface
- Stop/pause downloads at any time
- Choose custom output folder
- Real-time download status

## How to Run Python Code

### Prerequisites

- Python 3.8 or higher

### Installation

1. Install yt-dlp:
   ```bash
   pip install yt-dlp
   ```

2. Run the application:
   ```bash
   python youtube_downloader.py
   ```

The application window will open and you can start downloading.

### Note

When running from source, `yt-dlp` and `ffmpeg` must be installed on your system:
- **yt-dlp**: `pip install yt-dlp`
- **ffmpeg**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH

## How to Run the EXE File

If you are lazy and don't want to setup python or dependancies you can run the executable which includes the dependencies loaded in it

1. Download `YouTube_Downloader.exe` from the [Releases](https://github.com/MagdyAboYoussef/Youtube-Playlist-Downloade/releases/latest) page
2. Double-click the executable to run
3. No installation required - everything is bundled

### Windows SmartScreen Warning

When you first run the application, Windows SmartScreen might show a warning because the executable is not code-signed. This is normal for free, open-source applications.
