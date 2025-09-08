## Project Overview

**Name:** Sermon Summarizer  
**Purpose:** Automated pipeline to download, process, transcribe, and format church sermons from YouTube into structured markdown versions of the transcription.

## Technical Specification

### Core Functionality
1. **YouTube Audio Extraction** - Download audio-only from YouTube URLs
2. **Audio Preprocessing** - Trim audio to isolate sermon portion
3. **Transcription Integration** - Upload to local Whisper WebUI server
4. **Download Transcription** - Monitor and download transcription
5. **AI Summarization** - Generate structured markdown with sections and formatting
6. **Configuration Management** - Handle service patterns and user preferences

### Technology Stack
- **Language:** Python 3.9+
- **Key Dependencies:**
  - Library for YouTube downloading
  - `pydub` - Audio processing
  - `requests` - HTTP client for Whisper API
  -  AI summarization (or local LLM integration), Perplexity or Ollama
  - `click` or `argparse` - CLI interface
  - `pydantic` - Data validation and settings
  - `pathlib` - File system operations

## File Structure

```
sermon-summarizer/
├── tests/
│   ├── __init__.py
│   ├── test_youtube_downloader.py
│   ├── test_audio_processor.py
│   ├── test_whisper_client.py
│   └── test_ai_formatter.py
├── config/
│   ├── settings.yaml
│   └── service_patterns.yaml
├── output/
│   ├── audio/
│   ├── transcripts/
│   └── summaries/
├── docs/
│   ├── README.md
│   ├── USAGE.md
│   └── API.md
├── pyproject.toml
├── requirements.txt
├── .env.example
├── .gitignore
└── Makefile
```


### settings.yaml
```yaml
# Service Configuration
youtube:
  audio_quality: "bestaudio/best"
  output_format: "mp3"
  
audio_processing:
  silence_threshold: -40  # dB
  min_silence_duration: 2000  # ms
  
whisper:
  base_url: "http://localhost:7860"
  model: "large-v3"
  language: "en"
  
ai_formatting:
  provider: "perplexity"  # or "local", "anthropic"
  model: "gpt-4"
  max_tokens: 4000
  temperature: 0.3

# Output Configuration
output:
  audio_dir: "output/audio"
  transcript_dir: "output/transcripts"
  summary_dir: "output/summaries"
  keep_temp_files: false

# Service Pattern Recognition
service_patterns:
  greeting_keywords: ["good morning", "welcome", "glad to see"]
  sermon_start_keywords: ["let's turn to", "our text today", "scripture reading"]
  sermon_end_keywords: ["let's pray", "closing prayer", "benediction"]
```

## Implementation Strategy

### Phase 1: Core Infrastructure
1. Set up project structure and dependencies
2. Implement configuration management
3. Create base models and exceptions
4. Set up logging and CLI framework

### Phase 2: Audio Pipeline
1. YouTube downloader service
2. Audio processing and trimming logic
3. Service pattern recognition
4. Integration tests for audio pipeline

### Phase 3: Transcription Integration
1. Whisper WebUI client
2. File upload and status polling
3. Transcript parsing and segmentation
4. Error handling for API failures

### Phase 4: AI Summarization
1. AI service integration (configurable providers)
2. Prompt engineering for sermon summarization
3. Markdown formatting and templating
4. Quality validation of output

### Phase 5: Polish & Documentation
1. Comprehensive testing
2. Performance optimization
3. User documentation
4. Error recovery mechanisms
