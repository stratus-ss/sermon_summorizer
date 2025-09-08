"""
Test data factories using factory-boy for the Sermon Summarizer project.

This module provides factory classes for creating test data objects
that are consistent, realistic, and follow TDD best practices.
Each factory creates valid domain objects that can be used across
different test scenarios.
"""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import factory
from factory import Faker, Sequence


class SermonFactory(factory.Factory):
    """
    Factory for creating Sermon test objects.

    Creates valid sermon data with realistic YouTube URLs,
    titles, and metadata for testing purposes.
    """

    class Meta:
        model = dict  # Will be replaced with actual Sermon model later

    # Basic sermon properties
    id = Sequence(lambda n: f"sermon_{n}")
    url = Sequence(lambda n: f"https://www.youtube.com/watch?v=test{n:04d}")
    title = Faker("sentence", nb_words=6)
    status = "pending"

    # Metadata
    @factory.lazy_attribute
    def metadata(self):
        """Generate sermon metadata."""
        return {
            "uploader": "Test Church",
            "uploader_id": "test_church_123",
            "upload_date": "20240101",
            "duration": 3600,  # 1 hour
            "view_count": 1000,
            "like_count": 50,
            "description": "Test sermon description",
            "tags": ["sermon", "church", "faith", "test", "tdd"],
        }

    # Timestamps
    created_at = factory.LazyAttribute(lambda _: datetime.now())
    updated_at = factory.LazyAttribute(lambda _: datetime.now())

    @factory.lazy_attribute
    def pastor_name(self):
        """Generate realistic pastor names."""
        return "Pastor John Smith"


class AudioFileFactory(factory.Factory):
    """
    Factory for creating AudioFile test objects.

    Creates realistic audio file data with proper formats,
    durations, and file system paths for testing.
    """

    class Meta:
        model = dict  # Will be replaced with actual AudioFile model later

    # File properties
    id = Sequence(lambda n: f"audio_{n}")
    original_filename = factory.LazyAttribute(lambda obj: f"{obj.sermon_id or 'unknown'}.{obj.format}")
    path = factory.LazyAttribute(lambda obj: str(Path("/tmp/test_audio") / f"{obj.id}.{obj.format}"))
    format = factory.Faker("random_element", elements=["mp3", "wav", "m4a", "aac"])

    # Audio properties
    duration = factory.Faker("random_int", min=1800, max=7200)  # 30min to 2hr
    size_bytes = factory.LazyAttribute(lambda obj: int(obj.duration * 128 * 1000 / 8))  # Rough estimate for 128kbps
    sample_rate = factory.Faker("random_element", elements=[16000, 22050, 44100, 48000])
    channels = factory.Faker("random_element", elements=[1, 2])
    bitrate = factory.Faker("random_element", elements=[96, 128, 192, 256, 320])

    # Quality metrics
    quality_score = factory.Faker("pyfloat", min_value=0.7, max_value=1.0)
    noise_level = factory.Faker("pyfloat", min_value=0.0, max_value=0.3)

    # Relationships
    sermon_id = factory.SubFactory(SermonFactory)

    # Processing status
    processed = False
    processed_at = None

    # Timestamps
    created_at = factory.LazyAttribute(lambda _: datetime.now())
    updated_at = factory.LazyAttribute(lambda _: datetime.now())


class TranscriptSegmentFactory(factory.Factory):
    """
    Factory for creating transcript segment test objects.

    Creates realistic transcript segments with timing,
    text content, and confidence scores.
    """

    class Meta:
        model = dict  # Will be replaced with actual TranscriptSegment model later

    id = Sequence(lambda n: n)
    start_time = factory.Faker("pyfloat", min_value=0, max_value=7200)
    end_time = factory.LazyAttribute(
        lambda obj: obj.start_time + factory.Faker("pyfloat", min_value=1, max_value=30).generate()
    )
    text = factory.Faker("sentence", nb_words=15)
    confidence = factory.Faker("pyfloat", min_value=0.8, max_value=1.0)

    # Whisper-specific fields
    tokens = factory.LazyAttribute(
        lambda _: [factory.Faker("random_int", min=1, max=50000).generate() for _ in range(10)]
    )
    temperature = factory.Faker("pyfloat", min_value=0.0, max_value=1.0)
    avg_logprob = factory.Faker("pyfloat", min_value=-1.0, max_value=0.0)
    compression_ratio = factory.Faker("pyfloat", min_value=0.8, max_value=2.5)
    no_speech_prob = factory.Faker("pyfloat", min_value=0.0, max_value=0.5)

    # Speaker identification (future feature)
    speaker_id = None
    speaker_confidence = None


class TranscriptFactory(factory.Factory):
    """
    Factory for creating Transcript test objects.

    Creates complete transcript data with multiple segments,
    language detection, and quality metrics.
    """

    class Meta:
        model = dict  # Will be replaced with actual Transcript model later

    # Basic properties
    id = Sequence(lambda n: f"transcript_{n}")
    language = "en"
    full_text = factory.LazyAttribute(lambda obj: " ".join([segment["text"] for segment in obj.segments]))

    # Quality metrics
    overall_confidence = factory.Faker("pyfloat", min_value=0.85, max_value=0.98)
    word_count = factory.LazyAttribute(lambda obj: len(obj.full_text.split()) if obj.full_text else 0)

    # Segments
    segments = factory.LazyAttribute(
        lambda _: [
            TranscriptSegmentFactory.build() for _ in range(factory.Faker("random_int", min=5, max=20).generate())
        ]
    )

    # Processing metadata
    whisper_model = "whisper-1"
    processing_time = factory.Faker("pyfloat", min_value=30.0, max_value=300.0)

    # Relationships
    audio_file_id = factory.SubFactory(AudioFileFactory)
    sermon_id = factory.SubFactory(SermonFactory)

    # Timestamps
    created_at = factory.LazyAttribute(lambda _: datetime.now())
    updated_at = factory.LazyAttribute(lambda _: datetime.now())


class SummarySectionFactory(factory.Factory):
    """
    Factory for creating summary section test objects.

    Creates structured summary sections with titles,
    content, and scripture references.
    """

    class Meta:
        model = dict  # Will be replaced with actual SummarySection model later

    title = factory.Faker("sentence", nb_words=4)
    content = factory.Faker("text", max_nb_chars=500)
    order = Sequence(lambda n: n)
    section_type = factory.Faker(
        "random_element", elements=["main_point", "scripture", "application", "prayer", "conclusion"]
    )

    # Scripture references (if applicable)
    scripture_references = factory.LazyAttribute(
        lambda obj: (
            [
                f"{book} {chapter}:{verse}"
                for book, chapter, verse in [
                    (
                        "John",
                        factory.Faker("random_int", min=1, max=21).generate(),
                        factory.Faker("random_int", min=1, max=25).generate(),
                    ),
                    (
                        "Romans",
                        factory.Faker("random_int", min=1, max=16).generate(),
                        factory.Faker("random_int", min=1, max=39).generate(),
                    ),
                ]
            ]
            if obj.section_type == "scripture"
            else []
        )
    )


class SummaryFactory(factory.Factory):
    """
    Factory for creating Summary test objects.

    Creates complete sermon summaries with structured sections,
    key points, and formatted markdown content.
    """

    class Meta:
        model = dict  # Will be replaced with actual Summary model later

    # Basic properties
    id = Sequence(lambda n: f"summary_{n}")
    title = factory.LazyAttribute(lambda obj: obj.sermon_title or Faker("sentence", nb_words=6).generate())

    # Main content sections
    sections = factory.LazyAttribute(
        lambda _: [SummaryFactory.build() for _ in range(factory.Faker("random_int", min=3, max=8).generate())]
    )

    # Key elements
    main_points = factory.LazyAttribute(
        lambda _: [
            factory.Faker("sentence", nb_words=8).generate()
            for _ in range(factory.Faker("random_int", min=2, max=5).generate())
        ]
    )

    key_quotes = factory.LazyAttribute(
        lambda _: [
            f'"{factory.Faker("sentence", nb_words=12).generate()}"'
            for _ in range(factory.Faker("random_int", min=1, max=4).generate())
        ]
    )

    scripture_references = factory.LazyAttribute(
        lambda _: [
            f"{book} {chapter}:{verse_start}-{verse_end}"
            for book, chapter, verse_start, verse_end in [
                (
                    "Matthew",
                    factory.Faker("random_int", min=1, max=28).generate(),
                    factory.Faker("random_int", min=1, max=20).generate(),
                    factory.Faker("random_int", min=1, max=25).generate(),
                ),
                (
                    "Ephesians",
                    factory.Faker("random_int", min=1, max=6).generate(),
                    factory.Faker("random_int", min=1, max=15).generate(),
                    factory.Faker("random_int", min=1, max=20).generate(),
                ),
            ]
        ]
    )

    # Markdown output
    markdown_content = factory.LazyAttribute(
        lambda obj: f"""# {obj.title}

## Main Points
{chr(10).join([f"- {point}" for point in obj.main_points])}

## Key Scripture References
{chr(10).join([f"- {ref}" for ref in obj.scripture_references])}

## Summary
{factory.Faker("text", max_nb_chars=800).generate()}

## Key Quotes
{chr(10).join([f"> {quote}" for quote in obj.key_quotes])}
"""
    )

    # Quality metrics
    completeness_score = factory.Faker("pyfloat", min_value=0.7, max_value=1.0)
    accuracy_score = factory.Faker("pyfloat", min_value=0.8, max_value=1.0)

    # AI processing metadata
    ai_model = "gpt-4"
    processing_time = factory.Faker("pyfloat", min_value=10.0, max_value=120.0)
    token_usage = {
        "prompt_tokens": factory.Faker("random_int", min=1000, max=8000),
        "completion_tokens": factory.Faker("random_int", min=500, max=2000),
    }

    # Relationships
    transcript_id = factory.SubFactory(TranscriptFactory)
    sermon_id = factory.SubFactory(SermonFactory)

    # Timestamps
    created_at = factory.LazyAttribute(lambda _: datetime.now())
    updated_at = factory.LazyAttribute(lambda _: datetime.now())


class ConfigFactory(factory.Factory):
    """
    Factory for creating configuration test objects.

    Creates valid configuration data for different
    testing scenarios and edge cases.
    """

    class Meta:
        model = dict

    # YouTube downloader settings
    youtube_downloader = factory.LazyAttribute(
        lambda _: {
            "quality": factory.Faker("random_element", elements=["best", "worst", "720p"]).generate(),
            "format": factory.Faker("random_element", elements=["mp3", "wav", "best"]).generate(),
            "max_filesize": factory.Faker("random_element", elements=["100MB", "500MB", "1GB"]).generate(),
        }
    )

    # Audio processor settings
    audio_processor = factory.LazyAttribute(
        lambda _: {
            "sample_rate": factory.Faker("random_element", elements=[16000, 44100]).generate(),
            "normalize": factory.Faker("boolean").generate(),
            "noise_reduction": factory.Faker("boolean").generate(),
        }
    )

    # Whisper client settings
    whisper_client = factory.LazyAttribute(
        lambda _: {
            "api_url": "https://api.openai.com/v1/audio/transcriptions",
            "model": factory.Faker("random_element", elements=["whisper-1", "whisper-large"]).generate(),
            "timeout": factory.Faker("random_int", min=60, max=600).generate(),
            "language": factory.Faker("random_element", elements=["en", "auto"]).generate(),
        }
    )

    # AI service settings
    ai_service = factory.LazyAttribute(
        lambda _: {
            "provider": factory.Faker("random_element", elements=["openai", "anthropic"]).generate(),
            "model": factory.Faker("random_element", elements=["gpt-4", "gpt-3.5-turbo"]).generate(),
            "temperature": factory.Faker("pyfloat", min_value=0.1, max_value=1.0).generate(),
            "max_tokens": factory.Faker("random_int", min=1000, max=8000).generate(),
        }
    )

    # Output settings
    output = factory.LazyAttribute(
        lambda _: {
            "audio_dir": "output/audio",
            "transcriptions_dir": "output/transcriptions",
            "summaries_dir": "output/sermon_markdown",
        }
    )


# Trait factories for specific testing scenarios
class SermonFactoryWithLongTitle(SermonFactory):
    """Sermon factory with intentionally long title for testing edge cases."""

    title = factory.Faker("text", max_nb_chars=200)


class SermonFactoryWithSpecialCharacters(SermonFactory):
    """Sermon factory with special characters in title for testing sanitization."""

    title = factory.LazyAttribute(
        lambda _: f"Test Sermon: {factory.Faker('sentence').generate()} & Special <Characters> [Brackets]"
    )


class AudioFileFactoryLarge(AudioFileFactory):
    """Audio file factory for testing large files."""

    duration = 10800  # 3 hours
    size_bytes = 500_000_000  # ~500MB


class AudioFileFactoryLowQuality(AudioFileFactory):
    """Audio file factory for testing low quality audio."""

    quality_score = factory.Faker("pyfloat", min_value=0.3, max_value=0.6)
    noise_level = factory.Faker("pyfloat", min_value=0.4, max_value=0.8)
    sample_rate = 16000
    bitrate = 64


class TranscriptFactoryLowConfidence(TranscriptFactory):
    """Transcript factory for testing low confidence transcriptions."""

    overall_confidence = factory.Faker("pyfloat", min_value=0.5, max_value=0.7)
    segments = factory.LazyAttribute(
        lambda _: [
            TranscriptSegmentFactory.build(confidence=factory.Faker("pyfloat", min_value=0.4, max_value=0.7).generate())
            for _ in range(factory.Faker("random_int", min=5, max=15).generate())
        ]
    )


# Batch factories for creating related objects
def create_complete_sermon_pipeline(**overrides) -> Dict[str, Any]:
    """
    Create a complete set of related objects for testing the full pipeline.

    Args:
        **overrides: Override default values for any object

    Returns:
        Dict[str, Any]: Dictionary containing all related objects
    """
    sermon_data = SermonFactory.build(**overrides.get("sermon", {}))
    audio_data = AudioFileFactory.build(sermon_id=sermon_data["id"], **overrides.get("audio", {}))
    transcript_data = TranscriptFactory.build(
        sermon_id=sermon_data["id"], audio_file_id=audio_data["id"], **overrides.get("transcript", {})
    )
    summary_data = SummaryFactory.build(
        sermon_id=sermon_data["id"], transcript_id=transcript_data["id"], **overrides.get("summary", {})
    )

    return {
        "sermon": sermon_data,
        "audio_file": audio_data,
        "transcript": transcript_data,
        "summary": summary_data,
    }


def create_batch_sermons(count: int = 5, **overrides) -> List[Dict[str, Any]]:
    """
    Create multiple sermon objects for batch testing.

    Args:
        count: Number of sermons to create
        **overrides: Override default values

    Returns:
        List[Dict[str, Any]]: List of sermon data dictionaries
    """
    return [SermonFactory.build(**overrides) for _ in range(count)]
