"""
Test cases for IntelliReport core functionality.
"""

import unittest
from unittest.mock import Mock, patch
import sys
from pathlib import Path

# Add the parent directory to the path to import intellireport
sys.path.append(str(Path(__file__).parent.parent))

from intellireport.core import ReportProcessor
from intellireport.schemas import BLUFData, ReportMetadata, ReportData


class TestReportProcessor(unittest.TestCase):
    """Test cases for ReportProcessor class."""

    def setUp(self):
        """Set up test fixtures."""
        self.sample_text = """
        MEMORANDUM FOR RECORD

        TO: Department Head
        FROM: John Smith
        DATE: March 15, 2024
        SUBJECT: Test Report

        BLUF: This is a test report for demonstration purposes.
        The main finding is that the system is working correctly.

        Recommendations:
        1. Continue testing
        2. Add more features

        Contact: john.smith@company.com
        """

    @patch('intellireport.extractors.anthropic.Anthropic')
    def test_init(self, mock_anthropic):
        """Test ReportProcessor initialization."""
        processor = ReportProcessor(api_key="test_key", model="test_model")

        self.assertEqual(processor.api_key, "test_key")
        self.assertEqual(processor.model, "test_model")
        self.assertIsNotNone(processor.bluf_extractor)
        self.assertIsNotNone(processor.metadata_extractor)
        self.assertIsNotNone(processor.formatter)
        self.assertIsNotNone(processor.redactor)

    @patch('intellireport.extractors.anthropic.Anthropic')
    def test_process_report_basic(self, mock_anthropic):
        """Test basic report processing."""
        # Mock the API responses
        mock_client = Mock()
        mock_anthropic.return_value = mock_client

        # Mock BLUF response
        mock_bluf_response = Mock()
        mock_bluf_response.content = [Mock()]
        mock_bluf_response.content[0].text = """{
            "summary": "Test summary",
            "key_points": ["Point 1", "Point 2"],
            "recommendations": ["Rec 1", "Rec 2"],
            "urgency_level": "medium"
        }"""

        # Mock metadata response
        mock_metadata_response = Mock()
        mock_metadata_response.content = [Mock()]
        mock_metadata_response.content[0].text = """{
            "title": "Test Report",
            "author": "John Smith",
            "date_created": "2024-03-15",
            "classification": "Unclassified",
            "tags": ["test", "demo"],
            "confidence_score": 0.95
        }"""

        mock_client.messages.create.side_effect = [
            mock_bluf_response,
            mock_metadata_response
        ]

        processor = ReportProcessor(api_key="test_key")
        result = processor.process_report(
            self.sample_text,
            extract_bluf=True,
            extract_metadata=True,
            redact_entities=False
        )

        self.assertIsNotNone(result)
        self.assertIsNotNone(result.data)
        self.assertIsInstance(result.data, ReportData)
        self.assertEqual(result.data.raw_text, self.sample_text)

    @patch('intellireport.extractors.anthropic.Anthropic')
    def test_bluf_extraction(self, mock_anthropic):
        """Test BLUF extraction functionality."""
        mock_client = Mock()
        mock_anthropic.return_value = mock_client

        mock_response = Mock()
        mock_response.content = [Mock()]
        mock_response.content[0].text = """{
            "summary": "Critical security vulnerabilities found",
            "key_points": ["SQL injection", "Weak passwords"],
            "recommendations": ["Patch immediately", "Enforce strong passwords"],
            "urgency_level": "critical"
        }"""

        mock_client.messages.create.return_value = mock_response

        processor = ReportProcessor(api_key="test_key")
        result = processor.process_report(
            self.sample_text,
            extract_bluf=True,
            extract_metadata=False,
            redact_entities=False
        )

        self.assertIsNotNone(result.data.bluf)
        self.assertEqual(result.data.bluf.summary, "Critical security vulnerabilities found")
        self.assertEqual(len(result.data.bluf.key_points), 2)
        self.assertEqual(len(result.data.bluf.recommendations), 2)
        self.assertEqual(result.data.bluf.urgency_level, "critical")

    @patch('intellireport.extractors.anthropic.Anthropic')
    def test_metadata_extraction(self, mock_anthropic):
        """Test metadata extraction functionality."""
        mock_client = Mock()
        mock_anthropic.return_value = mock_client

        mock_response = Mock()
        mock_response.content = [Mock()]
        mock_response.content[0].text = """{
            "title": "Security Assessment Report",
            "author": "Jane Doe",
            "date_created": null,
            "classification": "Confidential",
            "tags": ["security", "assessment"],
            "confidence_score": 0.85
        }"""

        mock_client.messages.create.return_value = mock_response

        processor = ReportProcessor(api_key="test_key")
        result = processor.process_report(
            self.sample_text,
            extract_bluf=False,
            extract_metadata=True,
            redact_entities=False
        )

        self.assertIsNotNone(result.data.metadata)
        self.assertEqual(result.data.metadata.title, "Security Assessment Report")
        self.assertEqual(result.data.metadata.author, "Jane Doe")
        self.assertEqual(result.data.metadata.classification, "Confidential")
        self.assertEqual(len(result.data.metadata.tags), 2)
        self.assertEqual(result.data.metadata.confidence_score, 0.85)

    def test_output_formatting(self):
        """Test different output formats."""
        from intellireport.formatters import OutputFormatter
        from intellireport.schemas import ReportData, BLUFData, ReportMetadata

        formatter = OutputFormatter()

        # Create test data
        bluf = BLUFData(
            summary="Test summary",
            key_points=["Point 1"],
            recommendations=["Rec 1"],
            urgency_level="medium"
        )

        metadata = ReportMetadata(
            title="Test Report",
            author="Test Author",
            tags=["test"]
        )

        report_data = ReportData(
            raw_text="Test text",
            bluf=bluf,
            metadata=metadata
        )

        # Test JSON format
        json_output = formatter.format(report_data, "json")
        self.assertIn("Test summary", json_output)
        self.assertIn("Test Report", json_output)

        # Test YAML format
        yaml_output = formatter.format(report_data, "yaml")
        self.assertIn("summary: Test summary", yaml_output)

        # Test Markdown format
        markdown_output = formatter.format(report_data, "markdown")
        self.assertIn("# Report Analysis", markdown_output)
        self.assertIn("Test summary", markdown_output)

    def test_invalid_api_key(self):
        """Test handling of invalid API key."""
        with self.assertRaises(ValueError):
            ReportProcessor(api_key=None)

    @patch('intellireport.extractors.anthropic.Anthropic')
    def test_api_error_handling(self, mock_anthropic):
        """Test handling of API errors."""
        mock_client = Mock()
        mock_anthropic.return_value = mock_client
        mock_client.messages.create.side_effect = Exception("API Error")

        processor = ReportProcessor(api_key="test_key")

        with self.assertRaises(RuntimeError):
            processor.process_report(
                self.sample_text,
                extract_bluf=True,
                extract_metadata=False,
                redact_entities=False
            )

    def test_empty_text_handling(self):
        """Test handling of empty text input."""
        with patch('intellireport.extractors.anthropic.Anthropic'):
            processor = ReportProcessor(api_key="test_key")
            result = processor.process_report(
                "",
                extract_bluf=False,
                extract_metadata=False,
                redact_entities=False
            )

            self.assertEqual(result.data.raw_text, "")
            self.assertIsNone(result.data.bluf)
            self.assertIsNone(result.data.metadata)


class TestSchemas(unittest.TestCase):
    """Test cases for Pydantic schemas."""

    def test_bluf_data_validation(self):
        """Test BLUFData model validation."""
        bluf = BLUFData(
            summary="Test summary",
            key_points=["Point 1", "Point 2"],
            recommendations=["Rec 1"],
            urgency_level="high"
        )

        self.assertEqual(bluf.summary, "Test summary")
        self.assertEqual(len(bluf.key_points), 2)
        self.assertEqual(len(bluf.recommendations), 1)
        self.assertEqual(bluf.urgency_level, "high")

    def test_report_metadata_validation(self):
        """Test ReportMetadata model validation."""
        metadata = ReportMetadata(
            title="Test Report",
            author="Test Author",
            classification="Unclassified",
            tags=["test", "demo"],
            confidence_score=0.95
        )

        self.assertEqual(metadata.title, "Test Report")
        self.assertEqual(metadata.author, "Test Author")
        self.assertEqual(metadata.classification, "Unclassified")
        self.assertEqual(len(metadata.tags), 2)
        self.assertEqual(metadata.confidence_score, 0.95)

    def test_report_data_validation(self):
        """Test ReportData model validation."""
        report_data = ReportData(raw_text="Test text")

        self.assertEqual(report_data.raw_text, "Test text")
        self.assertIsNone(report_data.bluf)
        self.assertIsNone(report_data.metadata)
        self.assertIsNotNone(report_data.processing_timestamp)


if __name__ == '__main__':
    unittest.main()