# Sermon Summarizer Development Plan

## Project Vision

**Goal**: Create a production-ready Python CLI tool that automates the process of converting YouTube sermons into structured markdown summaries through transcription and AI-powered formatting.

**Core Value Proposition**: Streamline sermon content consumption and archival by providing searchable, formatted transcriptions with intelligent summarization.

## Test-Driven Development (TDD) Approach

This project will follow **strict TDD practices** throughout development:

### TDD Cycle
1. **Red**: Write a failing test first
2. **Green**: Write minimal code to make the test pass  
3. **Refactor**: Improve code while keeping tests passing
4. **Repeat**: Continue with next feature

### TDD Benefits for This Project
- **Quality Assurance**: External APIs (YouTube, Whisper, AI services) require robust error handling
- **Documentation**: Tests serve as living documentation of expected behavior
- **Confidence**: Safe refactoring as codebase grows
- **Design**: TDD encourages better API design and loose coupling
- **Debugging**: Isolated failures are easier to diagnose

## Architecture Overview

### Domain-Driven Design Structure
```
src/sermon_summarizer/
├── __init__.py
├── cli.py                    # Entry point
├── models/                   # Domain models
│   ├── __init__.py
│   ├── sermon.py            # Core sermon entity
│   ├── audio.py             # Audio data models
│   ├── transcript.py        # Transcription models
│   └── summary.py           # AI summary models
├── services/                 # Business logic
│   ├── __init__.py
│   ├── youtube_downloader.py
│   ├── audio_processor.py
│   ├── whisper_client.py
│   ├── ai_formatter.py
│   └── sermon_processor.py  # Main orchestrator
├── repositories/            # Data access
│   ├── __init__.py
│   ├── file_repository.py
│   └── cache_repository.py
├── config/                  # Configuration
│   ├── __init__.py
│   ├── loader.py           # Already exists
│   └── settings.py         # Pydantic settings
├── utils/                   # Utilities
│   ├── __init__.py
│   ├── logging.py
│   ├── exceptions.py
│   └── validators.py
└── interfaces/              # Protocols/ABCs
    ├── __init__.py
    ├── downloader.py
    ├── transcriber.py
    └── formatter.py
```

### Test Structure (Mirrors Source)
```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures
├── unit/                    # Fast, isolated tests
│   ├── test_models/
│   ├── test_services/
│   ├── test_repositories/
│   ├── test_config/
│   └── test_utils/
├── integration/             # Service integration tests
│   ├── test_youtube_integration.py
│   ├── test_whisper_integration.py
│   └── test_ai_integration.py
├── e2e/                    # End-to-end tests
│   └── test_full_pipeline.py
├── fixtures/               # Test data
│   ├── audio_samples/
│   ├── mock_responses/
│   └── expected_outputs/
└── factories/              # Test data factories
    └── sermon_factory.py
```

## Phase-by-Phase Development Plan

### Phase 1: Foundation & Core Models (Week 1-2)
**TDD Focus**: Domain model validation and basic configuration

#### 1.1 Project Setup
- [ ] Create virtual environment with all dependencies
- [ ] Configure development tools (black, flake8, mypy, pytest)
- [ ] Set up pre-commit hooks
- [ ] Create base test structure

#### 1.2 Configuration System (TDD)
**Test First**: Configuration loading, validation, defaults
- [ ] Write tests for settings loading from YAML
- [ ] Write tests for environment variable overrides  
- [ ] Write tests for configuration validation
- [ ] Implement configuration classes with Pydantic
- [ ] Add configuration schema validation

#### 1.3 Core Domain Models (TDD)
**Test First**: Model creation, validation, serialization
- [ ] Write tests for `Sermon` model (URL, metadata, status tracking)
- [ ] Write tests for `AudioFile` model (format, duration, path validation)
- [ ] Write tests for `Transcript` model (segments, timestamps, confidence)
- [ ] Write tests for `Summary` model (sections, formatting, metadata)
- [ ] Implement all models with full type annotations

#### 1.4 Exception Hierarchy (TDD)
**Test First**: Custom exceptions with proper inheritance
- [ ] Write tests for exception creation and messaging
- [ ] Write tests for exception chaining and context
- [ ] Implement custom exception classes
- [ ] Add error code system for API errors

### Phase 2: Audio Pipeline (Week 3-4)
**TDD Focus**: YouTube downloading and audio processing

#### 2.1 YouTube Downloader Service (TDD)
**Test First**: URL validation, download process, error handling
- [ ] Write tests for URL validation (various YouTube formats)
- [ ] Write tests for successful downloads (mocked yt-dlp)
- [ ] Write tests for network failures and retries
- [ ] Write tests for unsupported video types
- [ ] Write tests for rate limiting scenarios
- [ ] Implement YouTube downloader with yt-dlp
- [ ] Add progress tracking and cancellation support

#### 2.2 Audio Processing Service (TDD)  
**Test First**: Format conversion, trimming, validation
- [ ] Write tests for audio format detection
- [ ] Write tests for MP3 conversion (mocked pydub)
- [ ] Write tests for silence detection and trimming
- [ ] Write tests for audio file validation
- [ ] Write tests for service pattern recognition (intro/outro detection)
- [ ] Implement audio processor with pydub
- [ ] Add audio quality validation

#### 2.3 File Repository (TDD)
**Test First**: File operations, path management, cleanup
- [ ] Write tests for file creation and validation
- [ ] Write tests for temporary file management
- [ ] Write tests for cleanup on success/failure
- [ ] Write tests for disk space checks
- [ ] Implement file repository with pathlib
- [ ] Add atomic file operations

### Phase 3: Transcription Integration (Week 5-6)
**TDD Focus**: Whisper API integration and transcript processing

#### 3.1 Whisper Client Service (TDD)
**Test First**: API communication, file upload, status polling
- [ ] Write tests for connection validation
- [ ] Write tests for file upload (multipart/form-data)
- [ ] Write tests for job status polling with backoff
- [ ] Write tests for transcription result parsing
- [ ] Write tests for API error scenarios (500s, timeouts)
- [ ] Write tests for authentication if required
- [ ] Implement Whisper WebUI client with requests
- [ ] Add retry logic with exponential backoff

#### 3.2 Transcript Processing (TDD)
**Test First**: Parsing, segmentation, confidence scoring
- [ ] Write tests for transcript parsing (various formats)
- [ ] Write tests for segment creation and timestamps
- [ ] Write tests for confidence score handling
- [ ] Write tests for speaker identification (if supported)
- [ ] Write tests for transcript quality validation
- [ ] Implement transcript processing logic
- [ ] Add text cleaning and normalization

#### 3.3 Service Pattern Recognition (TDD)
**Test First**: Sermon start/end detection, content extraction  
- [ ] Write tests for greeting pattern detection
- [ ] Write tests for sermon start markers
- [ ] Write tests for sermon end markers (prayers, benedictions)
- [ ] Write tests for false positive handling
- [ ] Implement pattern recognition with configurable keywords
- [ ] Add confidence scoring for detected boundaries

### Phase 4: AI Summarization (Week 7-8)
**TDD Focus**: AI service integration and markdown generation

#### 4.1 AI Service Integration (TDD)
**Test First**: Provider abstraction, prompt engineering, response handling
- [ ] Write tests for AI provider abstraction (OpenAI, Anthropic, local)
- [ ] Write tests for prompt template system
- [ ] Write tests for response parsing and validation
- [ ] Write tests for rate limiting and quota management
- [ ] Write tests for fallback provider logic
- [ ] Write tests for cost tracking
- [ ] Implement AI service with configurable providers
- [ ] Add prompt optimization and testing framework

#### 4.2 Markdown Formatting (TDD)
**Test First**: Template system, content structuring, validation
- [ ] Write tests for markdown template processing
- [ ] Write tests for sermon structure detection (title, scripture, points)
- [ ] Write tests for quote extraction and formatting
- [ ] Write tests for scripture reference formatting
- [ ] Write tests for output validation
- [ ] Implement markdown formatter with Jinja2 templates
- [ ] Add customizable output formats

#### 4.3 Quality Validation (TDD)
**Test First**: Output quality checks, content validation
- [ ] Write tests for minimum content length validation
- [ ] Write tests for scripture reference validation
- [ ] Write tests for structural completeness checks
- [ ] Write tests for formatting consistency
- [ ] Implement quality scoring system
- [ ] Add human-readable quality reports

### Phase 5: CLI & Integration (Week 9-10)
**TDD Focus**: User interface and end-to-end workflow

#### 5.1 CLI Interface (TDD)
**Test First**: Command parsing, option validation, user interaction
- [ ] Write tests for command line argument parsing
- [ ] Write tests for configuration file detection
- [ ] Write tests for progress reporting
- [ ] Write tests for error message formatting
- [ ] Write tests for dry-run mode
- [ ] Write tests for batch processing
- [ ] Implement CLI with Click framework
- [ ] Add rich output formatting and progress bars

#### 5.2 Main Orchestrator Service (TDD)
**Test First**: Pipeline coordination, error recovery, state management
- [ ] Write tests for end-to-end pipeline execution
- [ ] Write tests for step failure recovery
- [ ] Write tests for partial completion resume
- [ ] Write tests for resource cleanup
- [ ] Write tests for concurrent processing limits
- [ ] Implement main sermon processor
- [ ] Add pipeline state persistence

#### 5.3 End-to-End Integration Tests
**Test First**: Full workflow validation with mocked services
- [ ] Write test for complete success workflow
- [ ] Write test for network failure scenarios
- [ ] Write test for API rate limiting
- [ ] Write test for disk space issues
- [ ] Write test for malformed inputs
- [ ] Set up integration test environment
- [ ] Add performance benchmarking

### Phase 6: Production Readiness (Week 11-12)
**TDD Focus**: Performance, monitoring, deployment

#### 6.1 Performance & Reliability (TDD)
**Test First**: Resource usage, memory management, concurrent processing
- [ ] Write tests for memory usage limits
- [ ] Write tests for concurrent processing
- [ ] Write tests for large file handling
- [ ] Write tests for long-running job management
- [ ] Add performance profiling and optimization
- [ ] Implement resource monitoring

#### 6.2 Monitoring & Observability (TDD)
**Test First**: Structured logging, metrics, health checks
- [ ] Write tests for structured logging output
- [ ] Write tests for metrics collection
- [ ] Write tests for error correlation IDs
- [ ] Write tests for performance metrics
- [ ] Implement comprehensive logging with correlation
- [ ] Add metrics collection for monitoring

#### 6.3 Documentation & Distribution
- [ ] Write comprehensive user documentation
- [ ] Create API documentation with examples
- [ ] Add troubleshooting guides
- [ ] Create deployment/installation guides
- [ ] Set up automated releases
- [ ] Add Docker containerization

## Testing Strategy

### Test Categories

#### Unit Tests (Fast, Isolated)
- **Target**: 90%+ coverage
- **Focus**: Single class/function behavior
- **Mocking**: External dependencies (APIs, filesystem)
- **Execution**: < 10 seconds total

#### Integration Tests (Service Boundaries)
- **Target**: Critical integration points
- **Focus**: Service-to-service communication
- **Mocking**: External APIs only, internal services real
- **Execution**: < 2 minutes total

#### End-to-End Tests (Full Workflow)
- **Target**: Core user journeys
- **Focus**: Complete pipeline validation
- **Mocking**: External APIs with realistic responses
- **Execution**: < 10 minutes total

### Test Data Strategy
- **Factories**: Use `factory-boy` for model creation
- **Fixtures**: Real audio samples (short, various formats)
- **Mocks**: HTTP responses for external APIs
- **Property Testing**: Use `hypothesis` for edge cases

### Continuous Integration
- **Pre-commit**: Format, lint, type-check
- **PR Pipeline**: Unit → Integration → E2E
- **Coverage**: Fail below 80% overall coverage
- **Quality Gates**: No flake8 violations, mypy clean

## Technology Stack

### Core Dependencies
- **CLI**: Click 8.1+ (rich terminal interface)
- **HTTP**: requests 2.31+ with tenacity for retries  
- **Audio**: pydub 0.25+ for audio processing
- **YouTube**: yt-dlp 2024.1+ (actively maintained)
- **Config**: pydantic-settings 2.1+ for configuration
- **AI**: openai 1.0+ with provider abstraction

### Development Dependencies  
- **Testing**: pytest 7.0+ with pytest-mock, pytest-cov
- **Quality**: black, flake8, mypy for code quality
- **TDD**: pytest-watch for continuous testing
- **Property Testing**: hypothesis for edge case discovery
- **Factories**: factory-boy for test data generation

### Infrastructure
- **Logging**: Structured JSON logs with correlation IDs
- **Monitoring**: Built-in metrics collection
- **Deployment**: Docker containers with health checks
- **CI/CD**: GitHub Actions with comprehensive testing

## Risk Mitigation

### Technical Risks
- **External API Failures**: Comprehensive retry logic + fallbacks
- **Large File Processing**: Streaming, chunking, memory monitoring
- **AI Cost Management**: Token counting, rate limiting, budgets
- **Audio Processing**: Format validation, quality checks

### Quality Risks  
- **Transcription Accuracy**: Quality scoring, human validation hooks
- **AI Hallucination**: Output validation, fact-checking prompts
- **Data Loss**: Atomic operations, backup/recovery procedures

### Operational Risks
- **Rate Limiting**: Exponential backoff, queue management
- **Disk Space**: Space checks, cleanup policies, monitoring
- **Configuration Errors**: Comprehensive validation, safe defaults

## Success Metrics

### Development Quality
- [ ] 80%+ test coverage maintained
- [ ] Zero mypy errors in production code
- [ ] Sub-10s unit test execution time
- [ ] TDD practice: tests written first for all features

### Functional Requirements
- [ ] Successful processing of 95%+ valid YouTube URLs
- [ ] Transcription accuracy verification system
- [ ] AI summary quality scoring system
- [ ] Complete error recovery and retry mechanisms

### Performance Requirements  
- [ ] Process 1-hour sermon in < 15 minutes end-to-end
- [ ] Memory usage < 1GB for typical sermon processing
- [ ] Graceful handling of concurrent processing (3+ streams)

### User Experience
- [ ] Clear progress indication and ETA
- [ ] Comprehensive error messages with resolution steps  
- [ ] Configurable output formats and quality levels
- [ ] Batch processing capabilities

This plan emphasizes **learning TDD through practice** while building a production-quality application. Each phase builds upon previous work, with tests driving design decisions and ensuring quality throughout development.
