"""
Professional intelligence report processing core rebuilt for CIA/MI6/Mossad standards.
No truncation limits, handles reports up to 50K characters, professional analysis.
"""

import os
import time
import asyncio
from typing import Optional, Dict, Any, List
import logging
from datetime import datetime

from .schemas import (
    ReportData, ProcessingResult, StandardReport, ToneType,
    ExtractedEntities, MissingFields, ProfessionalEntities
)
from .extractors import (
    ProfessionalIntelligenceExtractor, BLUFExtractor, MetadataExtractor,
    EntityExtractor, MissingFieldsAnalyzer
)
from .formatters import OutputFormatter
from .redactor import EntityRedactor, RedactionLevel


logger = logging.getLogger(__name__)


class APIKeyManager:
    """Manages API key configuration and validation."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize with optional API key."""
        self.api_key = api_key or self._get_api_key_from_env()
        if not self.api_key:
            raise ValueError(
                "Anthropic API key is required for professional intelligence analysis. "
                "Set ANTHROPIC_API_KEY environment variable or pass api_key parameter."
            )

    def _get_api_key_from_env(self) -> Optional[str]:
        """Get API key from environment variables."""
        return (
            os.getenv("ANTHROPIC_API_KEY") or
            os.getenv("CLAUDE_API_KEY") or
            os.getenv("API_KEY")
        )

    @property
    def key(self) -> str:
        """Get the API key."""
        return self.api_key


class ProfessionalReportProcessor:
    """
    Professional intelligence report processor for CIA/MI6/Mossad standards.

    Features:
    - NO truncation limits (handles reports up to 50K characters)
    - Professional entity extraction (real entities only)
    - Intelligence community format output
    - Chunking for very long reports
    - Elite-level analysis prompts
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-3-5-sonnet-latest",
        tone: ToneType = ToneType.PROFESSIONAL,
        max_input_length: int = 50000,  # NO truncation
        timeout: int = 120
    ):
        """
        Initialize professional intelligence processor.

        Args:
            api_key: Anthropic API key (required)
            model: Claude model for elite intelligence processing
            tone: Default analysis tone (professional/corporate/ngo)
            max_input_length: Maximum input length - handles up to 50K
            timeout: Processing timeout for complex reports
        """
        self.api_key_manager = APIKeyManager(api_key)
        self.model = model
        self.default_tone = tone
        self.max_input_length = max_input_length
        self.timeout = timeout

        # Initialize professional intelligence extractor
        self.intelligence_extractor = ProfessionalIntelligenceExtractor(
            api_key=self.api_key_manager.key,
            model=model,
            max_tokens=8192,  # Increased for comprehensive analysis
            timeout=timeout
        )

        # Initialize supporting components
        self.formatter = OutputFormatter()
        self.redactor = EntityRedactor(
            api_key=self.api_key_manager.key,
            model=model
        )

        logger.info(f"Professional intelligence processor initialized: {model}, tone: {tone.value}")

    def process(
        self,
        text: str,
        tone: Optional[ToneType] = None,
        output_format: str = "json",
        extract_entities: bool = True,
        analyze_missing_fields: bool = False,  # Optional for professional mode
        redact_pii: bool = False,
        redaction_level: RedactionLevel = RedactionLevel.MEDIUM,
        report_type: Optional[str] = None  # INTSUM, INTREP, THREATWARN, SITREP
    ) -> ProcessingResult:
        """
        Process intelligence report to professional standards.

        Args:
            text: Raw intelligence text (NO length limits)
            tone: Analysis tone (overrides default)
            output_format: Output format (json, markdown, html)
            extract_entities: Extract named entities using professional NER
            analyze_missing_fields: Analyze intelligence gaps
            redact_pii: Redact personally identifiable information
            redaction_level: Level of PII redaction
            report_type: Intelligence product type (INTSUM, INTREP, etc.)

        Returns:
            ProcessingResult with professional intelligence analysis
        """
        start_time = time.time()
        processing_tone = tone or self.default_tone

        logger.info(f"Processing intelligence report: {len(text)} chars, {processing_tone.value} tone")

        # Validate input length
        if len(text) > self.max_input_length:
            logger.warning(f"Report length {len(text)} exceeds {self.max_input_length} - will use chunking")

        # Initialize result containers
        errors = []
        warnings = []
        tokens_used = 0

        try:
            # Professional intelligence analysis - NO truncation
            standard_report, analysis_tokens = self.intelligence_extractor.process_intelligence_report(
                text=text,
                tone=processing_tone,
                report_type=report_type
            )
            tokens_used += analysis_tokens

            # Validate professional standards
            if not standard_report.is_professional_standard:
                warnings.append("Report may not meet full professional intelligence standards")

            # Create report data container
            report_data = ReportData(
                raw_text=text,
                standard_report=standard_report,
                processing_tone=processing_tone
            )

            # Extract entities using professional NER if requested
            if extract_entities:
                try:
                    prof_entities, entity_tokens = self.intelligence_extractor.extract_entities_professional(text)

                    # Convert to legacy format for compatibility
                    legacy_entities = ExtractedEntities(
                        people=prof_entities.people,
                        organizations=prof_entities.organizations,
                        locations=prof_entities.locations,
                        dates=prof_entities.dates,
                        other=prof_entities.equipment_systems
                    )

                    report_data.extracted_entities = legacy_entities
                    tokens_used += entity_tokens

                except Exception as e:
                    error_msg = f"Professional entity extraction failed: {str(e)}"
                    warnings.append(error_msg)
                    logger.warning(error_msg)

            # Redact PII if requested
            if redact_pii:
                try:
                    redacted_text, redacted_entities = self.redactor.redact_pii(
                        text, level=redaction_level
                    )
                    report_data.redacted_text = redacted_text
                    report_data.redacted_entities = redacted_entities

                except Exception as e:
                    error_msg = f"PII redaction failed: {str(e)}"
                    warnings.append(error_msg)
                    logger.warning(error_msg)

            # Format output
            try:
                formatted_output = self.formatter.format(
                    standard_report,
                    format_type=output_format
                )
            except Exception as e:
                error_msg = f"Output formatting failed: {str(e)}"
                warnings.append(error_msg)
                logger.warning(error_msg)
                formatted_output = "Output formatting failed - raw data available"

            # Calculate processing time
            processing_time_ms = int((time.time() - start_time) * 1000)

            # Create professional processing result
            result = ProcessingResult(
                data=report_data,
                formatted_output=formatted_output,
                output_format=output_format,
                errors=errors,
                warnings=warnings,
                processing_time_ms=processing_time_ms,
                tokens_used=tokens_used
            )

            logger.info(f"Professional intelligence processing completed: {processing_time_ms}ms, {tokens_used} tokens")
            return result

        except Exception as e:
            error_msg = f"Professional intelligence processing failed: {str(e)}"
            errors.append(error_msg)
            logger.error(error_msg, exc_info=True)

            # Create error result
            processing_time_ms = int((time.time() - start_time) * 1000)

            return ProcessingResult(
                data=ReportData(
                    raw_text=text,
                    processing_tone=processing_tone
                ),
                formatted_output="Professional processing failed - see errors",
                output_format=output_format,
                errors=errors,
                warnings=warnings,
                processing_time_ms=processing_time_ms,
                tokens_used=tokens_used
            )

    def process_batch(
        self,
        texts: List[str],
        tone: Optional[ToneType] = None,
        **kwargs
    ) -> List[ProcessingResult]:
        """
        Process multiple intelligence reports in batch.

        Args:
            texts: List of intelligence texts to process
            tone: Analysis tone for all reports
            **kwargs: Additional arguments for process()

        Returns:
            List of ProcessingResult objects
        """
        logger.info(f"Professional batch processing: {len(texts)} reports")

        results = []
        for i, text in enumerate(texts):
            logger.info(f"Processing batch report {i+1}/{len(texts)}")
            try:
                result = self.process(text, tone=tone, **kwargs)
                results.append(result)
            except Exception as e:
                logger.error(f"Batch report {i+1} failed: {str(e)}")
                # Create error result for failed report
                error_result = ProcessingResult(
                    data=ReportData(raw_text=text),
                    formatted_output="Batch processing failed",
                    output_format=kwargs.get('output_format', 'json'),
                    errors=[f"Batch processing error: {str(e)}"],
                    warnings=[],
                    processing_time_ms=0,
                    tokens_used=0
                )
                results.append(error_result)

        logger.info(f"Professional batch processing completed: {len(results)} results")
        return results

    def get_available_report_types(self) -> List[str]:
        """Get list of available professional report types."""
        return self.intelligence_extractor.prompt_manager.get_available_templates()

    def get_report_type_description(self, report_type: str) -> str:
        """Get description of specific report type."""
        return self.intelligence_extractor.prompt_manager.get_template_description(report_type)

    def validate_professional_standards(self, report: StandardReport) -> Dict[str, Any]:
        """
        Validate report against professional intelligence standards.

        Args:
            report: StandardReport to validate

        Returns:
            Dictionary with validation results
        """
        checks = {
            "bluf_length": len(report.bluf) >= 200,
            "key_assessments_count": len(report.key_assessments) >= 3,
            "confidence_assessment": report.confidence_score > 0,
            "intelligence_structure": bool(
                report.current_situation or
                report.threat_assessment or
                report.risk_analysis
            ),
            "entity_extraction": bool(report.entities.people or report.entities.organizations),
            "source_reliability": report.source_reliability.value != "F - Reliability cannot be judged",
            "professional_recommendations": bool(report.recommendations.immediate_actions)
        }

        score = sum(checks.values()) / len(checks)

        return {
            "overall_score": score,
            "checks": checks,
            "meets_standards": score >= 0.7,  # 70% threshold for professional standards
            "recommendations": self._get_improvement_recommendations(checks)
        }

    def _get_improvement_recommendations(self, checks: Dict[str, bool]) -> List[str]:
        """Generate recommendations for improving report quality."""
        recommendations = []

        if not checks["bluf_length"]:
            recommendations.append("Expand BLUF to 2-3 complete paragraphs for comprehensive executive summary")

        if not checks["key_assessments_count"]:
            recommendations.append("Include at least 3 specific key assessments with supporting data")

        if not checks["intelligence_structure"]:
            recommendations.append("Add structured intelligence analysis (current situation, threat assessment, risk analysis)")

        if not checks["entity_extraction"]:
            recommendations.append("Ensure proper named entity extraction (people, organizations, locations)")

        if not checks["source_reliability"]:
            recommendations.append("Assess source reliability based on content quality and verification")

        if not checks["professional_recommendations"]:
            recommendations.append("Include specific, actionable recommendations for decision-makers")

        return recommendations


# Legacy compatibility wrapper
class ReportProcessor(ProfessionalReportProcessor):
    """Legacy wrapper for backward compatibility."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-3-5-sonnet-latest",
        tone: ToneType = ToneType.PROFESSIONAL,
        retry_config: Optional[Dict] = None
    ):
        """Initialize with legacy parameters."""
        super().__init__(
            api_key=api_key,
            model=model,
            tone=tone,
            timeout=120
        )

    def process_report(
        self,
        text: str,
        extract_bluf: bool = True,
        extract_metadata: bool = True,
        redact_entities: bool = False,
        output_format: str = "json"
    ) -> ProcessingResult:
        """Legacy method for backward compatibility."""
        return self.process(
            text=text,
            extract_entities=extract_metadata,
            redact_pii=redact_entities,
            output_format=output_format
        )


# Export main processor
__all__ = ['ProfessionalReportProcessor', 'ReportProcessor', 'APIKeyManager']