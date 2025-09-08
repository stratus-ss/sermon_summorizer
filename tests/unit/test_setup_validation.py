"""
Test module to validate project setup and development environment.

This test validates that all development tools and infrastructure 
are properly configured for TDD development.
"""

import sys
from pathlib import Path

import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))


class TestDevelopmentEnvironmentSetup:
    """Test class to validate development environment setup."""

    def test_python_version(self):
        """Test that Python version meets requirements."""
        assert sys.version_info >= (3, 11), "Python 3.11+ is required"

    def test_project_structure_exists(self):
        """Test that required project directories exist."""
        project_root = Path(__file__).parent.parent.parent
        
        required_dirs = [
            "src/sermon_summarizer",
            "src/sermon_summarizer/config",
            "tests/unit",
            "tests/integration",
            "tests/config",
            "tests/models",
            "tests/services",
            "configs",
            "output",
        ]
        
        for dir_path in required_dirs:
            full_path = project_root / dir_path
            assert full_path.exists(), f"Required directory missing: {dir_path}"

    def test_configuration_files_exist(self):
        """Test that required configuration files exist."""
        project_root = Path(__file__).parent.parent.parent
        
        required_files = [
            "pyproject.toml",
            "Makefile", 
            "configs/settings.yaml",
            ".pre-commit-config.yaml",
        ]
        
        for file_path in required_files:
            full_path = project_root / file_path
            assert full_path.exists(), f"Required configuration file missing: {file_path}"

    def test_virtual_environment_active(self):
        """Test that virtual environment is active and has required packages."""
        # Check if we're in a virtual environment
        assert hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
        
        # Test imports of key packages
        try:
            import yaml  # noqa: F401
            import click  # noqa: F401
            import pytest  # noqa: F401
            import factory  # noqa: F401
        except ImportError as e:
            pytest.fail(f"Required package not available: {e}")

    def test_loader_module_imports(self):
        """Test that config loader module can be imported."""
        try:
            from sermon_summarizer.config import loader  # noqa: F401
        except ImportError as e:
            pytest.fail(f"Failed to import config.loader: {e}")

    def test_test_fixtures_available(self):
        """Test that test fixtures and factories are available."""
        try:
            from tests.conftest import TestDataFactory  # noqa: F401
            from tests.factories import SermonFactory  # noqa: F401
        except ImportError as e:
            pytest.fail(f"Failed to import test utilities: {e}")

    def test_yaml_configuration_loads(self):
        """Test that YAML configuration file loads properly."""
        project_root = Path(__file__).parent.parent.parent
        config_file = project_root / "configs/settings.yaml"
        
        assert config_file.exists(), "settings.yaml not found"
        
        try:
            import yaml
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
            assert isinstance(config, dict), "Configuration should be a dictionary"
            assert len(config) > 0, "Configuration should not be empty"
        except yaml.YAMLError as e:
            pytest.fail(f"Invalid YAML in settings.yaml: {e}")

    @pytest.mark.parametrize("tool", ["black", "flake8", "mypy", "pytest"])
    def test_development_tools_available(self, tool):
        """Test that development tools are available in the virtual environment."""
        try:
            if tool == "black":
                import black  # noqa: F401
            elif tool == "flake8":
                import flake8  # noqa: F401
            elif tool == "mypy":
                import mypy  # noqa: F401
            elif tool == "pytest":
                import pytest  # noqa: F401
        except ImportError:
            pytest.fail(f"Development tool '{tool}' is not available")


class TestProjectInfrastructure:
    """Test class to validate project infrastructure and TDD setup."""

    def test_makefile_targets_exist(self):
        """Test that Makefile has required targets."""
        project_root = Path(__file__).parent.parent.parent
        makefile = project_root / "Makefile"
        
        assert makefile.exists(), "Makefile not found"
        
        makefile_content = makefile.read_text()
        required_targets = [
            "format", "lint", "typecheck", "test", 
            "test-coverage", "clean", "install-dev", "venv"
        ]
        
        for target in required_targets:
            assert f"{target}:" in makefile_content, f"Makefile target '{target}' missing"

    def test_pyproject_toml_configuration(self):
        """Test that pyproject.toml has proper configuration."""
        project_root = Path(__file__).parent.parent.parent
        pyproject_file = project_root / "pyproject.toml"
        
        assert pyproject_file.exists(), "pyproject.toml not found"
        
        content = pyproject_file.read_text()
        
        # Check for required sections
        required_sections = [
            "[project]", "[tool.pytest.ini_options]", 
            "[tool.black]", "[tool.mypy]", "[tool.coverage.run]"
        ]
        
        for section in required_sections:
            assert section in content, f"pyproject.toml section '{section}' missing"

    def test_pre_commit_configuration(self):
        """Test that pre-commit is properly configured."""
        project_root = Path(__file__).parent.parent.parent
        pre_commit_config = project_root / ".pre-commit-config.yaml"
        
        assert pre_commit_config.exists(), ".pre-commit-config.yaml not found"
        
        try:
            import yaml
            with open(pre_commit_config, 'r') as f:
                config = yaml.safe_load(f)
            
            assert 'repos' in config, "pre-commit config should have 'repos' section"
            assert len(config['repos']) > 0, "pre-commit should have at least one repo"
            
            # Check for key tools
            repo_urls = [repo['repo'] for repo in config['repos']]
            expected_tools = ['black', 'flake8', 'mypy']
            
            for tool in expected_tools:
                found = any(tool in url for url in repo_urls)
                assert found, f"pre-commit should include {tool}"
                
        except yaml.YAMLError as e:
            pytest.fail(f"Invalid YAML in .pre-commit-config.yaml: {e}")

    def test_git_hooks_installed(self):
        """Test that git hooks are properly installed."""
        project_root = Path(__file__).parent.parent.parent
        
        # Check for pre-commit hook
        pre_commit_hook = project_root / ".git/hooks/pre-commit"
        assert pre_commit_hook.exists(), "pre-commit git hook not installed"
        
        # Check for pre-push hook  
        pre_push_hook = project_root / ".git/hooks/pre-push"
        assert pre_push_hook.exists(), "pre-push git hook not installed"


class TestTDDInfrastructure:
    """Test class to validate TDD infrastructure setup."""

    def test_test_directory_structure(self):
        """Test that test directory structure supports TDD."""
        project_root = Path(__file__).parent.parent.parent
        tests_dir = project_root / "tests"
        
        required_test_dirs = [
            "unit", "integration", "config", "models", 
            "services", "utils"
        ]
        
        for test_dir in required_test_dirs:
            full_path = tests_dir / test_dir
            assert full_path.exists(), f"Test directory missing: tests/{test_dir}"
            
            # Each test directory should have an __init__.py
            init_file = full_path / "__init__.py"
            assert init_file.exists(), f"Missing __init__.py in tests/{test_dir}"

    def test_conftest_fixtures_available(self):
        """Test that conftest.py provides necessary fixtures."""
        from tests.conftest import (
            temp_dir, test_config_dir, test_audio_dir, test_output_dirs,
            sample_audio_file, mock_youtube_response, mock_whisper_response,
            TestDataFactory
        )
        
        # Test that fixtures are callable/available
        assert callable(TestDataFactory), "TestDataFactory should be callable"
        
        # Test creating test data
        factory = TestDataFactory()
        sermon_data = factory.create_sermon_data()
        assert isinstance(sermon_data, dict)
        assert 'url' in sermon_data
        assert 'title' in sermon_data

    def test_factories_create_valid_data(self):
        """Test that factories create valid test data."""
        # For Phase 1.1, just test basic factory import
        from tests.factories import SermonFactory  # noqa: F401
        
        # Basic test - detailed factory testing will be done in Phase 1.3
        # when we implement the actual models
        assert True, "Factory imports working - detailed testing in Phase 1.3"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
