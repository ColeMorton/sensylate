"""
Test cases for data extraction script.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch

from scripts.data_extraction import DataExtractor
from scripts.utils.config_loader import ConfigLoader


class TestDataExtractor:
    """Test cases for DataExtractor class."""
    
    @pytest.fixture
    def sample_config(self):
        """Sample configuration for testing."""
        return {
            'metadata': {
                'name': 'Test Data Extraction',
                'version': '1.0.0'
            },
            'input': {
                'database': {
                    'connection_string': 'test://localhost/test',
                    'timeout': 30
                }
            },
            'output': {
                'file_path': 'data/raw/test_data.parquet',
                'format': 'parquet'
            },
            'logging': {
                'level': 'INFO',
                'file': 'outputs/logs/test.log'
            }
        }
    
    def test_extractor_initialization(self, sample_config):
        """Test that DataExtractor initializes correctly."""
        extractor = DataExtractor(sample_config)
        assert extractor.config == sample_config
        assert extractor.logger is not None
    
    @patch('scripts.data_extraction.Path.mkdir')
    def test_extract_data_creates_output_directory(self, mock_mkdir, sample_config):
        """Test that extract_data creates output directory."""
        extractor = DataExtractor(sample_config)
        
        with patch.object(extractor.logger, 'info'):
            result = extractor.extract_data()
        
        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
        assert isinstance(result, Path)


class TestConfigLoader:
    """Test cases for ConfigLoader class."""
    
    def test_config_loader_initialization(self):
        """Test that ConfigLoader initializes correctly."""
        loader = ConfigLoader()
        assert loader.env_pattern is not None
    
    def test_substitute_string_variables(self):
        """Test environment variable substitution."""
        loader = ConfigLoader()
        
        with patch.dict('os.environ', {'TEST_VAR': 'test_value'}):
            result = loader._substitute_string_variables('${TEST_VAR}/path')
            assert result == 'test_value/path'
    
    def test_merge_configs(self):
        """Test configuration merging."""
        loader = ConfigLoader()
        
        base = {
            'section1': {'key1': 'value1'},
            'section2': {'key2': 'value2'}
        }
        
        overlay = {
            'section1': {'key1': 'new_value1'},
            'section3': {'key3': 'value3'}
        }
        
        result = loader._merge_configs(base, overlay)
        
        assert result['section1']['key1'] == 'new_value1'
        assert result['section2']['key2'] == 'value2'
        assert result['section3']['key3'] == 'value3'