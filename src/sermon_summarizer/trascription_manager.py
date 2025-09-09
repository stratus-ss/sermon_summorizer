"""Transcription manager for the Sermon Summarizer project.
This module will either send the audio file to the local Whisper WebUI server or to so other transcription service.
"""

import requests
import time
import json
from datetime import datetime

class ExternalTranscriptionManager:
    """Transcription manager for the Sermon Summarizer project."""
    
    def __init__(self, audio_file: str, base_url: str):
        """Initialize the transcription manager."""
        self.audio_file = audio_file
        self.base_url = base_url
        
    def transcribe_audio(self):
        """Transcribe the audio file."""
        with open(self.audio_file, "rb") as f:
            response = requests.post(self.base_url, files={"file": f})
        return response.json()
    
    def retrieve_transcription(self, job_id: str):
        """Retrieve the transcription from the transcription service."""
        response = requests.get(f"{self.base_url}/jobs/{job_id}")
        return response.json()

class WhisperTranscriptionManager:
    
    def __init__(self, audio_file: str, base_url: str):
        self.API_URL = base_url
        self.SOURCE_DIR = './audio/processed'
        self.OUTPUT_DIR = './output/transcripts'
        self.COMPLETED_DIR = './audio/completed'
        self.POLL_INTERVAL = 5
        self.mp3_path = audio_file

        self.API_SETTINGS = {
            'model_size': 'small',
            'lang': 'en',
            'is_translate': False,
            'compute_type': 'float16',
            'beam_size': 5,
            'best_of': 5,
            'batch_size': 8,
            'vad_filter': True,
            'no_speech_threshold': 0.5,
            'log_prob_threshold': -1.0,
            'temperature': 0,
            'word_timestamps': True,
            'condition_on_previous_text': True,
        }

    def upload_and_get_task_id(self, mp3_path):
        with open(mp3_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f'{self.API_URL}/transcription/', files=files, data=self.API_SETTINGS)
            response.raise_for_status()
            response_data = response.json()
            print(f" Upload response: {response_data.get('message', 'Task queued')}")
            task_id = response_data.get('identifier')
            if not task_id:
                raise ValueError(f"No identifier found in response: {response_data}")
            return task_id

    def poll_for_result(self, task_id):
        """Poll for transcription result using the correct /task/ endpoint"""
        last_progress = -1
        start_time = datetime.now()
        print(f" Start time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        while True:
            try:
                response = requests.get(f'{self.API_URL}/task/{task_id}')
                response.raise_for_status()
                data = response.json()

                status = data.get('status')
                progress = data.get('progress', 0)

                elapsed = datetime.now() - start_time
                elapsed_str = str(elapsed).split('.')[0]
                if progress != last_progress:
                    print(f" Status: {status}, Progress: {progress:.1%}, Elapsed: {elapsed_str}")
                    last_progress = progress

                if status == 'completed':
                    end_time = datetime.now()
                    total_elapsed = end_time - start_time
                    total_elapsed_str = str(total_elapsed).split('.')[0]
                    print(f" End time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
                    print(f" Total time: {total_elapsed_str}")
                    print(f" Transcription completed!")
                    return data

                elif status in ['failed', 'error']:
                    end_time = datetime.now()
                    total_elapsed = end_time - start_time
                    total_elapsed_str = str(total_elapsed).split('.')[0]
                    print(f" End time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
                    print(f" Total time: {total_elapsed_str}")
                    error_msg = data.get('error') or 'Unknown error'
                    raise RuntimeError(f'Task {task_id} failed: {error_msg}')

                elif status in ['queued', 'pending', 'in_progress', 'processing']:
                    pass
                else:
                    print(f" Unknown status: {status}, Elapsed: {elapsed_str}")

            except requests.exceptions.RequestException as e:
                elapsed = datetime.now() - start_time
                elapsed_str = str(elapsed).split('.')[0]
                print(f" Polling error: {e}, Elapsed: {elapsed_str}")

            time.sleep(self.POLL_INTERVAL)

    def seconds_to_srt_time(self, seconds):
        """Convert seconds to SRT time format HH:MM:SS,mmm"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        milliseconds = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"

    def save_transcription_as_srt(self, result_data, output_path):
        """Extract transcription and save as SRT file"""
        result = result_data.get('result', [])
        if isinstance(result, list) and result:
            segments = result
        else:
            print(f" Warning: Unexpected result format, saving JSON instead.")
            with open(output_path.replace('.srt', '_raw.json'), 'w', encoding='utf-8') as f:
                json.dump(result_data, f, indent=2)
            return False
        with open(output_path, 'w', encoding='utf-8') as f:
            for i, segment in enumerate(segments, 1):
                start_time = segment.get('start', 0)
                end_time = segment.get('end', 0)
                text = segment.get('text', '').strip()
                if not text:
                    continue
                f.write(f"{i}\n")
                f.write(f"{self.seconds_to_srt_time(start_time)} --> {self.seconds_to_srt_time(end_time)}\n")
                f.write(f"{text}\n\n")
        return True