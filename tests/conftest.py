"""
Test configuration and fixtures for the Sermon Summarizer project.

This module contains pytest configuration, common fixtures, and test utilities
used across the entire test suite. It follows TDD best practices by providing
reusable test data, mock objects, and testing infrastructure.
"""

import shutil
import tempfile
from pathlib import Path
from typing import Any, Dict, Generator
from unittest.mock import MagicMock, Mock, patch

import pytest
import yaml

# Test data constants
TEST_YOUTUBE_URL = "https://www.youtube.com/watch?v=test123"
TEST_SERMON_TITLE = "Test Sermon: Walking in Faith"
TEST_AUDIO_DURATION = 3600  # 1 hour
TEST_TRANSCRIPT_TEXT = "This is a test sermon transcript with important spiritual content."


@pytest.fixture(scope="session")
def temp_dir() -> Generator[Path, None, None]:
    """
    Create a temporary directory for test files.

    This fixture provides a clean temporary directory for each test session
    that is automatically cleaned up after tests complete.

    Yields:
        Path: Path object pointing to the temporary directory
    """
    temp_path = Path(tempfile.mkdtemp(prefix="sermon_test_"))
    try:
        yield temp_path
    finally:
        shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def test_config_dir(temp_dir: Path) -> Path:
    """
    Create a test configuration directory with sample config files.

    Args:
        temp_dir: Temporary directory fixture

    Returns:
        Path: Path to the test config directory
    """
    config_dir = temp_dir / "config"
    config_dir.mkdir()

    # Create test settings.yaml
    test_settings = {
        "youtube_downloader": {"quality": "best", "format": "mp3", "max_filesize": "500MB"},
        "audio_processor": {"sample_rate": 16000, "normalize": True},
        "whisper_client": {
            "api_url": "https://api.openai.com/v1/audio/transcriptions",
            "model": "whisper-1",
            "timeout": 300,
        },
        "ai_service": {"provider": "openai", "model": "gpt-4", "temperature": 0.7, "max_tokens": 4000},
        "output": {
            "audio_dir": "output/audio",
            "transcriptions_dir": "output/transcriptions",
            "summaries_dir": "output/sermon_markdown",
        },
    }

    settings_file = config_dir / "settings.yaml"
    with open(settings_file, "w") as f:
        yaml.dump(test_settings, f)

    return config_dir


@pytest.fixture
def test_audio_dir(temp_dir: Path) -> Path:
    """
    Create a test audio directory.

    Args:
        temp_dir: Temporary directory fixture

    Returns:
        Path: Path to the test audio directory
    """
    audio_dir = temp_dir / "audio"
    audio_dir.mkdir()
    return audio_dir


@pytest.fixture
def test_output_dirs(temp_dir: Path) -> Dict[str, Path]:
    """
    Create test output directories.

    Args:
        temp_dir: Temporary directory fixture

    Returns:
        Dict[str, Path]: Dictionary mapping output types to directory paths
    """
    output_dirs = {
        "audio": temp_dir / "output" / "audio",
        "transcriptions": temp_dir / "output" / "transcriptions",
        "summaries": temp_dir / "output" / "sermon_markdown",
    }

    for dir_path in output_dirs.values():
        dir_path.mkdir(parents=True)

    return output_dirs


@pytest.fixture
def sample_audio_file(test_audio_dir: Path) -> Path:
    """
    Create a sample audio file for testing.

    Args:
        test_audio_dir: Test audio directory fixture

    Returns:
        Path: Path to the sample audio file
    """
    audio_file = test_audio_dir / "sample_sermon.mp3"
    # Create a minimal MP3-like file (for testing purposes only)
    with open(audio_file, "wb") as f:
        f.write(b"ID3\x03\x00\x00\x00\x00\x00\x00")  # Minimal MP3 header
    return audio_file


@pytest.fixture
def mock_youtube_response() -> Dict[str, Any]:
    """
    Mock response data from YouTube API/yt-dlp.

    Returns:
        Dict[str, Any]: Mock YouTube video information
    """
    return {
        "id": "test123",
        "title": TEST_SERMON_TITLE,
        "duration": TEST_AUDIO_DURATION,
        "uploader": "Test Church",
        "upload_date": "20240101",
        "description": "A powerful message about faith and spiritual growth.",
        "formats": [{"format_id": "140", "ext": "m4a", "quality": 2, "audio_quality": "medium"}],
    }


@pytest.fixture
def mock_whisper_response() -> Dict[str, Any]:
    """
    Mock response data from Whisper API.

    Returns:
        Dict[str, Any]: Mock transcription response
    """
    return {
        "text": TEST_TRANSCRIPT_TEXT,
        "segments": [
            {
                "id": 0,
                "seek": 0,
                "start": 0.0,
                "end": 10.0,
                "text": "This is a test sermon transcript",
                "tokens": [123, 456, 789],
                "temperature": 0.0,
                "avg_logprob": -0.5,
                "compression_ratio": 1.2,
                "no_speech_prob": 0.1,
            }
        ],
        "language": "en",
    }


@pytest.fixture
def mock_ai_summary_response() -> Dict[str, str]:
    """
    Mock response data from AI summarization service.

    Returns:
        Dict[str, str]: Mock AI summary response
    """
    return {
        "title": TEST_SERMON_TITLE,
        "main_points": "1. Trust in God's plan\n2. Walk by faith, not by sight\n3. Pray without ceasing",
        "scripture_references": "Proverbs 3:5-6, 2 Corinthians 5:7, 1 Thessalonians 5:17",
        "summary": "This sermon encourages believers to maintain unwavering faith in God's guidance.",
        "key_quotes": '"Faith is not about understanding everything, but trusting God with everything."',
    }


@pytest.fixture
def mock_yt_dlp():
    """
    Mock yt-dlp for testing YouTube downloading functionality.

    Returns:
        MagicMock: Mocked yt-dlp instance
    """
    with patch("yt_dlp.YoutubeDL") as mock_ytdl_class:
        mock_ytdl = MagicMock()
        mock_ytdl_class.return_value = mock_ytdl

        # Configure mock behavior
        mock_ytdl.extract_info.return_value = {
            "id": "test123",
            "title": TEST_SERMON_TITLE,
            "duration": TEST_AUDIO_DURATION,
        }

        yield mock_ytdl


@pytest.fixture
def mock_requests():
    """
    Mock requests library for testing HTTP API calls.

    Returns:
        MagicMock: Mocked requests instance
    """
    with patch("requests.Session") as mock_session_class:
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session

        # Configure successful response by default
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success"}
        mock_response.raise_for_status.return_value = None
        mock_session.post.return_value = mock_response
        mock_session.get.return_value = mock_response

        yield mock_session


@pytest.fixture
def mock_openai():
    """
    Mock OpenAI client for testing AI service integration.

    Returns:
        MagicMock: Mocked OpenAI client
    """
    with patch("openai.OpenAI") as mock_openai_class:
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        # Configure mock chat completion
        mock_completion = Mock()
        mock_completion.choices = [Mock()]
        mock_completion.choices[0].message.content = "Mocked AI response"
        mock_client.chat.completions.create.return_value = mock_completion

        yield mock_client


@pytest.fixture
def mock_pydub():
    """
    Mock pydub for testing audio processing functionality.

    Returns:
        MagicMock: Mocked pydub AudioSegment
    """
    with patch("pydub.AudioSegment") as mock_audio_segment:
        mock_audio = MagicMock()
        mock_audio.duration_seconds = TEST_AUDIO_DURATION
        mock_audio.frame_rate = 44100
        mock_audio.channels = 2
        mock_audio_segment.from_file.return_value = mock_audio
        mock_audio_segment.from_mp3.return_value = mock_audio

        yield mock_audio_segment


# Test markers for categorizing tests
pytest_plugins = []


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "unit: mark test as a unit test (fast, isolated)")
    config.addinivalue_line("markers", "integration: mark test as an integration test (slower, external dependencies)")
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "external_api: mark test as requiring external API access")


# Environment setup for tests
@pytest.fixture(autouse=True)
def setup_test_environment(monkeypatch):
    """
    Automatically set up test environment variables for all tests.

    This fixture runs before every test to ensure a clean, consistent
    test environment.
    """
    # Set test environment variables
    monkeypatch.setenv("TESTING", "true")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")

    # Disable external API calls during testing by default
    monkeypatch.setenv("DISABLE_EXTERNAL_APIS", "true")

    # Set test data directories
    monkeypatch.setenv("TEST_DATA_DIR", "/tmp/sermon_test_data")


class TestDataFactory:
    """
    Factory class for creating test data objects.

    This class provides methods to create consistent test data
    across different test modules, supporting the TDD approach
    by providing reliable test fixtures.
    """

    @staticmethod
    def create_sermon_data(**kwargs) -> Dict[str, Any]:
        """
        Create test sermon data.

        Args:
            **kwargs: Override default values

        Returns:
            Dict[str, Any]: Sermon data dictionary
        """
        default_data = {
            "url": TEST_YOUTUBE_URL,
            "title": TEST_SERMON_TITLE,
            "duration": TEST_AUDIO_DURATION,
            "status": "pending",
            "metadata": {
                "uploader": "Test Church",
                "upload_date": "2024-01-01",
                "description": "Test sermon description",
            },
        }
        default_data.update(kwargs)
        return default_data

    @staticmethod
    def create_audio_file_data(**kwargs) -> Dict[str, Any]:
        """
        Create test audio file data.

        Args:
            **kwargs: Override default values

        Returns:
            Dict[str, Any]: Audio file data dictionary
        """
        default_data = {
            "path": "/tmp/test_audio.mp3",
            "format": "mp3",
            "duration": TEST_AUDIO_DURATION,
            "size": 1024 * 1024,  # 1MB
            "sample_rate": 44100,
            "channels": 2,
        }
        default_data.update(kwargs)
        return default_data

    @staticmethod
    def create_transcript_data(**kwargs) -> Dict[str, Any]:
        """
        Create test transcript data.

        Args:
            **kwargs: Override default values

        Returns:
            Dict[str, Any]: Transcript data dictionary
        """
        default_data = {
            "text": TEST_TRANSCRIPT_TEXT,
            "segments": [{"start": 0.0, "end": 10.0, "text": "Test segment", "confidence": 0.95}],
            "language": "en",
            "confidence_score": 0.92,
        }
        default_data.update(kwargs)
        return default_data


@pytest.fixture
def test_data_factory() -> TestDataFactory:
    """
    Provide test data factory for creating consistent test objects.

    Returns:
        TestDataFactory: Factory instance for creating test data
    """
    return TestDataFactory()
