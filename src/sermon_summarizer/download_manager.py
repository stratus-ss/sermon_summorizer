"""Download manager for the Sermon Summarizer project.

This module handles the downloading of sermons from YouTube.
"""

import yt_dlp

class DownloadManager:
    """Download manager for the Sermon Summarizer project."""
    
    def __init__(self, playlist_url: str):
        """Initialize the download manager."""
        self.ydl_opts = {
            'format': 'bestaudio/best',
            "extractaudio": True,
            "audioformat": "mp3",
            # The output should have the Sermon Series Name and the Sermon Title
            "outtmpl": "output/audio/raw/%(series_name)s/%(title)s.%(ext)s",
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        self.playlist_url = playlist_url
        
    def download_sermons(self):
        """Download a sermon from YouTube."""
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download([self.playlist_url])
            
            
            
            