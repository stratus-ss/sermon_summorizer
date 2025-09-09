"""Audio splitter for the Sermon Summarizer project.

This module handles the splitting of audio files. Isolating the sermon portion of the audio file.
"""

import pydub

class AudioSplitter:
    """Audio splitter for the Sermon Summarizer project."""
    
    def __init__(self, audio_file: str):
        """Initialize the audio splitter."""
        self.audio_file = audio_file
        # Phrases that the pastor says at the beginning of the sermon
        self.phrases = [
            "whether you're here live",
            "whether you are watching us online",
            "wherever you are we are glad that you are joining us"
        ]
        
    def split_audio(self):
        """Isolate the sermon portion of the audio file."""
        audio = pydub.AudioSegment.from_mp3(self.audio_file)
        for phrase in self.phrases:
            audio = audio.split(phrase)
        audio.export("output/audio/processed/%(series_name)s/%(title)s.mp3", format="mp3")