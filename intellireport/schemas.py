"""
Pydantic models for data validation and serialization.
"""

from typing import Optional, Dict, Any, List, Literal
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, model_validator

# Pydantic v2 compatibility
try:
    from pydantic import field_validator
except ImportError:
    # Fallback for different Pydantic installations
    try:
        from pydantic.functional_validators import field_validator
    except ImportError:
        # Use validator for older versions
        from pydantic import validator as field_validator


class ReliabilityLevel(str, Enum):
    """Source reliability levels."""
    A = "A - Completely reliable"
    B = "B - Usually reliable"
    C = "C - Fairly reliable"
    D = "D - Not usually reliable"
    E = "E - Unreliable"
    F = "F - Reliability cannot be judged"


class CredibilityLevel(str, Enum):
    """Information credibility levels."""
    ONE = "1 - Confirmed by other sources"
    TWO = "2 - Probably true"
    THREE = "3 - Possibly true"
    FOUR = "4 - Doubtfully true"
    FIVE = "5 - Improbable"
    SIX = "6 - Truth cannot be judged"


class ClassificationLevel(str, Enum):
    """Security classification levels."""
    UNCLASSIFIED = "UNCLASSIFIED"
    CUI = "CONTROLLED UNCLASSIFIED INFORMATION"
    CONFIDENTIAL = "CONFIDENTIAL"
    SECRET = "SECRET"
    TOP_SECRET = "TOP SECRET"


class ToneType(str, Enum):
    """Report tone types."""
    NGO = "ngo"
    CORPORATE = "corporate"
    PROFESSIONAL = "professional"


class BLUFData(BaseModel):
    """Bottom Line Up Front data model (legacy support)."""
    summary: str = Field(..., description="Main summary of the report")
    key_points: List[str] = Field(default_factory=list, description="Key takeaways")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations")
    urgency_level: Optional[str] = Field(None, description="Urgency level (low, medium, high, critical)")


class ReportMetadata(BaseModel):
    """Report metadata model (legacy support)."""
    title: Optional[str] = None
    author: Optional[str] = None
    date_created: Optional[datetime] = None
    classification: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0)


class EntityRedaction(BaseModel):
    """Entity redaction information."""
    entity_type: str = Field(..., description="Type of entity (person, organization, location, etc.)")
    original_text: str = Field(..., description="Original text that was redacted")
    redacted_text: str = Field(..., description="Replacement text")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in redaction")
    location_start: int = Field(..., ge=0, description="Start position in original text")
    location_end: int = Field(..., ge=0, description="End position in original text")


class ProfessionalEntities(BaseModel):
    """Professional entity extraction following intelligence standards."""
    people: List[str] = Field(default_factory=list, description="Full names only - real people mentioned")
    organizations: List[str] = Field(default_factory=list, description="Actual organization names - not generic phrases")
    locations: List[str] = Field(default_factory=list, description="Cities, countries, regions - specific places")
    dates: List[str] = Field(default_factory=list, description="Specific dates and timeframes")
    equipment_systems: List[str] = Field(default_factory=list, description="Weapons, technology, equipment mentioned")
    critical_figures: Dict[str, str] = Field(default_factory=dict, description="Key statistics with context")


class IntelligenceRecommendations(BaseModel):
    """Structured recommendations following intelligence standards."""
    immediate_actions: List[str] = Field(default_factory=list, description="Urgent actions required within 24-48 hours")
    risk_mitigation: List[str] = Field(default_factory=list, description="Medium-term risk reduction measures")
    collection_priorities: List[str] = Field(default_factory=list, description="Intelligence gathering priorities")
    decision_points: List[str] = Field(default_factory=list, description="Key decisions requiring leadership attention")


class ReportMetadataProfessional(BaseModel):
    """Professional report metadata."""
    title: Optional[str] = Field(None, description="Extracted or generated report title")
    date: Optional[str] = Field(None, description="Report date in YYYY-MM-DD format")
    author: Optional[str] = Field(None, description="If mentioned in source")
    source_type: Optional[str] = Field(None, description="Type of source material")
    urgency_level: Optional[Literal["low", "medium", "high", "critical"]] = Field(None)


class StandardReport(BaseModel):
    """Professional intelligence report following CIA/MI6/Mossad standards."""

    # Core Intelligence Fields - NO truncation limits
    classification: ClassificationLevel = Field(default=ClassificationLevel.UNCLASSIFIED)
    bluf: str = Field(..., min_length=100, description="Complete executive summary - 3-5 sentences minimum")
    key_assessments: List[str] = Field(..., min_items=3, description="5-10 critical findings with specific data")

    # Structured Intelligence Analysis
    current_situation: Optional[str] = Field(None, description="Detailed description of what IS happening now")
    recent_developments: Optional[str] = Field(None, description="What has CHANGED recently - trends and new developments")
    threat_assessment: Optional[str] = Field(None, description="What COULD happen - potential threats and scenarios")
    risk_analysis: Optional[str] = Field(None, description="Likelihood vs impact assessment with specific risk factors")

    # Intelligence Products
    intelligence_gaps: List[str] = Field(default_factory=list, description="Critical information missing")
    recommendations: IntelligenceRecommendations = Field(default_factory=IntelligenceRecommendations)
    entities: ProfessionalEntities = Field(default_factory=ProfessionalEntities)

    # Credibility Assessment
    source_reliability: ReliabilityLevel = Field(default=ReliabilityLevel.C)
    info_credibility: CredibilityLevel = Field(default=CredibilityLevel.THREE)
    confidence_level: Literal["High", "Medium", "Low"] = Field(default="Medium")
    confidence_score: float = Field(default=0.5, ge=0.0, le=1.0)

    # Analyst Information
    analyst_notes: Optional[str] = Field(None, description="Additional observations, assumptions, and analytical caveats")
    report_metadata: ReportMetadataProfessional = Field(default_factory=ReportMetadataProfessional)

    # Legacy fields for backward compatibility - REMOVE size limits
    date: datetime = Field(default_factory=datetime.now, description="Report date")
    title: Optional[str] = Field(None, description="Report title - NO SIZE LIMIT")
    author: Optional[str] = Field(None, description="Report author - NO SIZE LIMIT")
    source: Optional[str] = Field(None, description="Information source - NO SIZE LIMIT")
    location: Optional[str] = Field(None, description="Relevant location - NO SIZE LIMIT")
    tags: List[str] = Field(default_factory=list, description="Topic tags")
    urgency_level: Optional[Literal["low", "medium", "high", "critical"]] = Field(None)

    # Legacy compatibility fields
    key_findings: List[str] = Field(default_factory=list, description="Legacy field - use key_assessments instead")

    @field_validator('bluf')
    def validate_bluf(cls, v):
        # Professional intelligence BLUF must be comprehensive - NO truncation
        if len(v.strip()) < 100:
            raise ValueError('Professional BLUF must be at least 100 characters - should be 3-5 complete sentences')
        return v.strip()

    @field_validator('key_assessments')
    def validate_key_assessments(cls, v):
        if not v or len(v) < 3:
            raise ValueError('Professional intelligence requires at least 3 key assessments')
        return v

    @model_validator(mode='after')
    def validate_professional_standards(self):
        """Ensure professional intelligence standards are met."""
        # Professional BLUF should be substantial
        if len(self.bluf) < 200:
            # This is a warning, not an error - allow shorter BLUF but encourage longer
            pass

        return self

    @property
    def is_professional_standard(self) -> bool:
        """Check if report meets professional intelligence standards."""
        checks = [
            len(self.bluf) >= 200,  # Substantial BLUF
            len(self.key_assessments) >= 3,  # Multiple assessments
            self.confidence_score > 0,  # Confidence assessment
            bool(self.current_situation or self.threat_assessment)  # Analysis sections
        ]
        return sum(checks) >= 3  # At least 3/4 criteria met


class ExtractedEntities(BaseModel):
    """Extracted entities from text."""
    people: List[str] = Field(default_factory=list, description="Person names")
    organizations: List[str] = Field(default_factory=list, description="Organization names")
    locations: List[str] = Field(default_factory=list, description="Geographic locations")
    dates: List[str] = Field(default_factory=list, description="Dates and times")
    other: List[str] = Field(default_factory=list, description="Other named entities")


class MissingFields(BaseModel):
    """Identifies missing required fields."""
    missing_fields: List[str] = Field(default_factory=list, description="Fields that could not be extracted")
    confidence_issues: List[str] = Field(default_factory=list, description="Fields with low confidence")
    suggestions: List[str] = Field(default_factory=list, description="Suggestions for improvement")


class ReportData(BaseModel):
    """Complete report processing data."""
    raw_text: str = Field(..., description="Original input text")
    standard_report: Optional[StandardReport] = None
    extracted_entities: Optional[ExtractedEntities] = None
    missing_fields: Optional[MissingFields] = None
    redacted_text: Optional[str] = None
    redacted_entities: List[EntityRedaction] = Field(default_factory=list)
    processing_timestamp: datetime = Field(default_factory=datetime.now)
    processing_tone: ToneType = Field(default=ToneType.PROFESSIONAL)

    # Legacy support
    bluf: Optional[BLUFData] = None
    metadata: Optional[ReportMetadata] = None


class ProcessingResult(BaseModel):
    """Result of report processing."""
    data: ReportData = Field(..., description="Processed report data")
    formatted_output: Optional[str] = Field(None, description="Formatted output string")
    output_format: str = Field(default="json", description="Format of the output")
    errors: List[str] = Field(default_factory=list, description="Processing errors")
    warnings: List[str] = Field(default_factory=list, description="Processing warnings")
    processing_time_ms: Optional[int] = Field(None, ge=0, description="Processing time in milliseconds")
    tokens_used: Optional[int] = Field(None, ge=0, description="API tokens consumed")

    @property
    def has_errors(self) -> bool:
        """Check if processing had errors."""
        return len(self.errors) > 0

    @property
    def has_warnings(self) -> bool:
        """Check if processing had warnings."""
        return len(self.warnings) > 0

    @property
    def success(self) -> bool:
        """Check if processing was successful."""
        return not self.has_errors


class JSONOutput(BaseModel):
    """Structured JSON output format."""
    report: StandardReport
    metadata: Dict[str, Any] = Field(default_factory=dict)
    processing_info: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
        }


class MarkdownOutput(BaseModel):
    """Structured Markdown output format."""
    title: str = Field(default="Intelligence Report")
    sections: List[Dict[str, str]] = Field(default_factory=list)
    metadata_table: bool = Field(default=True)
    include_classification: bool = Field(default=True)

    def generate_markdown(self, report: StandardReport) -> str:
        """Generate markdown from StandardReport."""
        lines = []

        # Header with classification
        if self.include_classification:
            lines.append(f"**CLASSIFICATION: {report.classification.value}**")
            lines.append("")

        # Title
        title = report.title or self.title
        lines.append(f"# {title}")
        lines.append("")

        # BLUF
        lines.append("## Bottom Line Up Front (BLUF)")
        lines.append(report.bluf)
        lines.append("")

        # Key Findings
        lines.append("## Key Findings")
        for i, finding in enumerate(report.key_findings, 1):
            lines.append(f"{i}. {finding}")
        lines.append("")

        # Recommendations
        if report.recommendations:
            lines.append("## Recommendations")
            for i, rec in enumerate(report.recommendations, 1):
                lines.append(f"{i}. {rec}")
            lines.append("")

        # Metadata table
        if self.metadata_table:
            lines.append("## Report Details")
            lines.append("| Field | Value |")
            lines.append("|-------|-------|")
            lines.append(f"| Date | {report.date.strftime('%Y-%m-%d %H:%M')} |")
            lines.append(f"| Source Reliability | {report.source_reliability.value} |")
            lines.append(f"| Info Credibility | {report.info_credibility.value} |")
            if report.author:
                lines.append(f"| Author | {report.author} |")
            if report.source:
                lines.append(f"| Source | {report.source} |")
            if report.location:
                lines.append(f"| Location | {report.location} |")
            if report.urgency_level:
                lines.append(f"| Urgency | {report.urgency_level.upper()} |")
            lines.append(f"| Confidence | {report.confidence_score:.2f} |")
            lines.append("")

        return "\n".join(lines)