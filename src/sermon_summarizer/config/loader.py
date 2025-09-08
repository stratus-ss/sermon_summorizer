"""Configuration loading and management.

This module handles loading configuration from YAML files and environment
variables, with support for validation and error handling.
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
import yaml

# TODO: These imports will be implemented in Phase 1.2 and 1.3
# from sermon_summarizer.core.exceptions import ConfigurationError
# from sermon_summarizer.config.models import Settings

# Temporary placeholder classes for Phase 1.1 setup
class ConfigurationError(Exception):
    """Temporary configuration error class."""
    def __init__(self, message: str, error_code: str = "", context: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.error_code = error_code
        self.context = context or {}

class Settings:
    """Temporary settings class."""
    def __init__(self, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def dict(self) -> Dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}


# Default configuration file path
DEFAULT_CONFIG_PATH = Path("configs/settings.yaml")


def load_config(config_path: Optional[Path] = None) -> Settings:
    """Load configuration from file and environment variables.

    Args:
        config_path: Path to configuration file. If None, uses DEFAULT_CONFIG_PATH.

    Returns:
        Validated Settings object.

    Raises:
        ConfigurationError: If configuration loading or validation fails.
    """
    if config_path is None:
        config_path = DEFAULT_CONFIG_PATH

    # Load configuration from file
    config_data = _load_yaml_file(config_path)

    # Apply environment variable overrides
    config_data = _apply_env_overrides(config_data)

    # Validate and create Settings object
    try:
        settings = Settings(**config_data)
    except Exception as e:
        raise ConfigurationError(
            f"Configuration validation failed: {e}",
            error_code="CONFIG_VALIDATION_FAILED",
            context={"config_path": str(config_path), "error": str(e)},
        )

    return settings


def _load_yaml_file(config_path: Path) -> Dict[str, Any]:
    """Load configuration from YAML file.

    Args:
        config_path: Path to YAML configuration file.

    Returns:
        Dictionary containing configuration data.

    Raises:
        ConfigurationError: If file loading fails.
    """
    try:
        if not config_path.exists():
            raise ConfigurationError(
                f"Configuration file not found: {config_path}",
                error_code="CONFIG_FILE_NOT_FOUND",
                context={"config_path": str(config_path)},
            )

        with open(config_path, "r", encoding="utf-8") as file:
            config_data = yaml.safe_load(file)

        if config_data is None:
            config_data = {}

        return config_data  # type: ignore[no-any-return]

    except yaml.YAMLError as e:
        raise ConfigurationError(
            f"Invalid YAML syntax in configuration file: {e}",
            error_code="INVALID_YAML_SYNTAX",
            context={"config_path": str(config_path), "yaml_error": str(e)},
        )
    except IOError as e:
        raise ConfigurationError(
            f"Failed to read configuration file: {e}",
            error_code="CONFIG_FILE_READ_ERROR",
            context={"config_path": str(config_path), "io_error": str(e)},
        )


def _apply_env_overrides(config_data: Dict[str, Any]) -> Dict[str, Any]:
    """Apply environment variable overrides to configuration.

    Environment variables should be in the format:
    - SECTION_FIELD_NAME (e.g., WHISPER_BASE_URL, YOUTUBE_OUTPUT_FORMAT)

    Args:
        config_data: Base configuration data from file.

    Returns:
        Configuration data with environment overrides applied.
    """
    # Define mappings from environment variables to config paths
    env_mappings = {
        # Whisper configuration
        "WHISPER_BASE_URL": ("whisper", "base_url"),
        "WHISPER_MODEL": ("whisper", "model"),
        "WHISPER_LANGUAGE": ("whisper", "language"),
        "WHISPER_TIMEOUT": ("whisper", "timeout"),
        # YouTube configuration
        "YOUTUBE_AUDIO_QUALITY": ("youtube", "audio_quality"),
        "YOUTUBE_OUTPUT_FORMAT": ("youtube", "output_format"),
        # AI formatting configuration
        "AI_PROVIDER": ("ai_formatting", "provider"),
        "AI_MODEL": ("ai_formatting", "model"),
        "AI_API_KEY": ("ai_formatting", "api_key"),
        "AI_MAX_TOKENS": ("ai_formatting", "max_tokens"),
        "AI_TEMPERATURE": ("ai_formatting", "temperature"),
        # Output configuration
        "OUTPUT_AUDIO_DIR": ("output", "audio_dir"),
        "OUTPUT_TRANSCRIPT_DIR": ("output", "transcript_dir"),
        "OUTPUT_SUMMARY_DIR": ("output", "summary_dir"),
        "OUTPUT_KEEP_TEMP_FILES": ("output", "keep_temp_files"),
        # Audio processing configuration
        "AUDIO_SILENCE_THRESHOLD": ("audio_processing", "silence_threshold"),
        "AUDIO_MIN_SILENCE_DURATION": ("audio_processing", "min_silence_duration"),
    }

    # Apply environment overrides
    for env_var, (section, field) in env_mappings.items():
        env_value = os.getenv(env_var)
        if env_value is not None:
            # Ensure the section exists in config_data
            if section not in config_data:
                config_data[section] = {}

            # Convert string values to appropriate types
            converted_value = _convert_env_value(env_value, section, field)
            config_data[section][field] = converted_value

    return config_data


def _convert_env_value(value: str, section: str, field: str) -> Any:
    """Convert environment variable string to appropriate type.

    Args:
        value: String value from environment variable.
        section: Configuration section name.
        field: Configuration field name.

    Returns:
        Converted value with appropriate type.
    """
    # Boolean conversions
    if field in ["keep_temp_files"] or value.lower() in ["true", "false"]:
        return value.lower() == "true"

    # Integer conversions
    if field in ["timeout", "max_tokens", "silence_threshold", "min_silence_duration"]:
        try:
            return int(value)
        except ValueError:
            raise ConfigurationError(
                f"Invalid integer value for {section}.{field}: {value}",
                error_code="INVALID_ENV_VALUE_TYPE",
                context={"section": section, "field": field, "value": value},
            )

    # Float conversions
    if field in ["temperature"]:
        try:
            return float(value)
        except ValueError:
            raise ConfigurationError(
                f"Invalid float value for {section}.{field}: {value}",
                error_code="INVALID_ENV_VALUE_TYPE",
                context={"section": section, "field": field, "value": value},
            )

    # String values (default)
    return value


def save_config(settings: Settings, config_path: Path) -> None:
    """Save configuration to YAML file.

    Args:
        settings: Settings object to save.
        config_path: Path where to save the configuration.

    Raises:
        ConfigurationError: If saving fails.
    """
    try:
        # Ensure parent directory exists
        config_path.parent.mkdir(parents=True, exist_ok=True)

        # Convert settings to dictionary
        config_data = settings.dict()

        # Write to YAML file
        with open(config_path, "w", encoding="utf-8") as file:
            yaml.dump(config_data, file, default_flow_style=False, indent=2, allow_unicode=True)

    except IOError as e:
        raise ConfigurationError(
            f"Failed to save configuration file: {e}",
            error_code="CONFIG_FILE_SAVE_ERROR",
            context={"config_path": str(config_path), "io_error": str(e)},
        )
