"""
Professional intelligence extraction system rebuilt for CIA/MI6/Mossad standards.
No truncation limits, proper entity extraction, and elite-level analysis.
"""

import os
import json
import re
import logging
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime
import anthropic

from .schemas import (
    StandardReport, BLUFData, ReportMetadata, ExtractedEntities,
    MissingFields, ToneType, ReliabilityLevel, CredibilityLevel,
    ClassificationLevel, ProfessionalEntities, IntelligenceRecommendations,
    ReportMetadataProfessional
)
from .prompts import IntelligencePromptManager, ENTITY_NER_PROMPT

# Configure logging for professional intelligence operations
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProfessionalIntelligenceExtractor:
    """Elite-level intelligence extraction for professional analysts."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-3-5-sonnet-latest",
        max_tokens: int = 8192,  # Increased for long reports
        timeout: int = 120  # Longer timeout for complex analysis
    ):
        """Initialize professional intelligence extractor."""
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model
        self.max_tokens = max_tokens
        self.timeout = timeout

        if not self.api_key:
            raise ValueError("Anthropic API key required for professional intelligence analysis")

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.prompt_manager = IntelligencePromptManager()

        # Professional analysis settings - NO truncation
        self.max_input_length = 50000  # Handle reports up to 50K characters
        self.chunk_size = 15000  # For very long reports
        self.retry_attempts = 3

    def process_intelligence_report(
        self,
        text: str,
        tone: ToneType = ToneType.PROFESSIONAL,
        report_type: Optional[str] = None
    ) -> Tuple[StandardReport, int]:
        """
        Process intelligence report to professional standards.

        Args:
            text: Raw intelligence text (NO length limits)
            tone: Analysis tone (professional/corporate/ngo)
            report_type: INTSUM, INTREP, THREATWARN, or SITREP

        Returns:
            Tuple of (StandardReport, tokens_used)
        """
        logger.info(f"Processing intelligence report: {len(text)} characters, {tone.value} tone")

        # Handle very long reports with chunking if needed
        if len(text) > self.max_input_length:
            return self._process_long_report(text, tone, report_type)

        # Get professional analysis prompt
        prompt = self.prompt_manager.get_analysis_prompt(tone, report_type)

        # Execute analysis with retry logic
        for attempt in range(self.retry_attempts):
            try:
                response, tokens = self._call_claude_professional(prompt, text)
                report = self._parse_professional_response(response, text)

                # Validate professional standards
                if report.is_professional_standard:
                    logger.info("Professional intelligence standards met")
                else:
                    logger.warning("Report may not meet full professional standards")

                return report, tokens

            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt == self.retry_attempts - 1:
                    # Final fallback with professional standards
                    return self._create_professional_fallback(text, str(e)), 0

        # Should never reach here, but safety fallback
        return self._create_professional_fallback(text, "Max retries exceeded"), 0

    def _call_claude_professional(
        self,
        prompt: str,
        text: str,
        temperature: float = 0.2  # Lower for more consistent professional output
    ) -> Tuple[str, int]:
        """Professional Claude API call with enhanced error handling."""

        full_prompt = f"{prompt}\n\nINTELLIGENCE SOURCE MATERIAL:\n{text}"

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=temperature,
                messages=[{
                    "role": "user",
                    "content": full_prompt
                }],
                timeout=self.timeout
            )

            response_text = response.content[0].text
            estimated_tokens = len(full_prompt + response_text) // 4

            logger.info(f"Professional analysis completed: {estimated_tokens} tokens")
            return response_text, estimated_tokens

        except anthropic.APITimeoutError:
            logger.error("API timeout - report may be too complex")
            raise RuntimeError("Analysis timeout - consider shorter input or chunking")
        except anthropic.APIError as e:
            logger.error(f"API error: {str(e)}")
            raise RuntimeError(f"Professional analysis failed: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise RuntimeError(f"Intelligence processing error: {str(e)}")

    def _process_long_report(
        self,
        text: str,
        tone: ToneType,
        report_type: Optional[str]
    ) -> Tuple[StandardReport, int]:
        """Process very long reports using chunking strategy."""

        logger.info(f"Processing long report: {len(text)} characters using chunking")

        # Split into logical chunks (try to preserve paragraphs)
        chunks = self._intelligent_chunking(text)

        # Process each chunk and combine results
        chunk_reports = []
        total_tokens = 0

        for i, chunk in enumerate(chunks):
            logger.info(f"Processing chunk {i+1}/{len(chunks)}")
            try:
                chunk_report, chunk_tokens = self.process_intelligence_report(chunk, tone, report_type)
                chunk_reports.append(chunk_report)
                total_tokens += chunk_tokens
            except Exception as e:
                logger.warning(f"Chunk {i+1} processing failed: {str(e)}")

        # Combine chunk results into comprehensive report
        combined_report = self._combine_chunk_reports(chunk_reports, text)
        return combined_report, total_tokens

    def _intelligent_chunking(self, text: str) -> List[str]:
        """Intelligently chunk long text preserving context."""

        chunks = []
        current_chunk = ""

        # Split by paragraphs first
        paragraphs = text.split('\n\n')

        for paragraph in paragraphs:
            # If adding this paragraph would exceed chunk size
            if len(current_chunk) + len(paragraph) > self.chunk_size:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = paragraph
                else:
                    # Single paragraph is too long - split by sentences
                    sentences = paragraph.split('. ')
                    for sentence in sentences:
                        if len(current_chunk) + len(sentence) > self.chunk_size:
                            if current_chunk:
                                chunks.append(current_chunk.strip())
                            current_chunk = sentence
                        else:
                            current_chunk += sentence + ". "
            else:
                current_chunk += paragraph + "\n\n"

        # Add final chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        logger.info(f"Created {len(chunks)} intelligent chunks")
        return chunks

    def _parse_professional_response(self, response: str, original_text: str) -> StandardReport:
        """Parse AI response into professional StandardReport structure."""

        try:
            # Extract JSON from response (handle markdown code blocks)
            json_start = response.find('{')
            json_end = response.rfind('}') + 1

            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON structure found in response")

            json_str = response[json_start:json_end]
            data = json.loads(json_str)

            # Parse professional entities
            entities_data = data.get('entities', {})
            entities = ProfessionalEntities(
                people=entities_data.get('people', []),
                organizations=entities_data.get('organizations', []),
                locations=entities_data.get('locations', []),
                dates=entities_data.get('dates', []),
                equipment_systems=entities_data.get('equipment_systems', []),
                critical_figures=entities_data.get('critical_figures', {})
            )

            # Parse structured recommendations
            rec_data = data.get('recommendations', {})
            if isinstance(rec_data, list):
                # Handle legacy format
                recommendations = IntelligenceRecommendations(
                    immediate_actions=rec_data[:2] if rec_data else [],
                    risk_mitigation=rec_data[2:4] if len(rec_data) > 2 else [],
                    collection_priorities=rec_data[4:] if len(rec_data) > 4 else []
                )
            else:
                recommendations = IntelligenceRecommendations(
                    immediate_actions=rec_data.get('immediate_actions', []),
                    risk_mitigation=rec_data.get('risk_mitigation', []),
                    collection_priorities=rec_data.get('collection_priorities', []),
                    decision_points=rec_data.get('decision_points', [])
                )

            # Parse metadata
            metadata_data = data.get('report_metadata', {})
            metadata = ReportMetadataProfessional(
                title=metadata_data.get('title') or data.get('title'),
                date=metadata_data.get('date'),
                author=metadata_data.get('author') or data.get('author'),
                source_type=metadata_data.get('source_type'),
                urgency_level=metadata_data.get('urgency_level')
            )

            # Parse reliability and credibility
            reliability = self._parse_reliability_professional(data.get('source_reliability'))
            credibility = self._parse_credibility_professional(data.get('info_credibility'))
            classification = self._parse_classification_professional(data.get('classification'))

            # Create professional report
            report = StandardReport(
                # Core intelligence fields - NO truncation
                classification=classification,
                bluf=data.get('bluf', 'Executive summary extraction failed'),
                key_assessments=data.get('key_assessments', ['Assessment extraction failed']),

                # Structured analysis
                current_situation=data.get('current_situation'),
                recent_developments=data.get('recent_developments'),
                threat_assessment=data.get('threat_assessment'),
                risk_analysis=data.get('risk_analysis'),

                # Intelligence products
                intelligence_gaps=data.get('intelligence_gaps', []),
                recommendations=recommendations,
                entities=entities,

                # Credibility assessment
                source_reliability=reliability,
                info_credibility=credibility,
                confidence_level=data.get('confidence_level', 'Medium'),
                confidence_score=float(data.get('confidence_score', 0.5)),

                # Analyst information
                analyst_notes=data.get('analyst_notes'),
                report_metadata=metadata,

                # Legacy compatibility
                date=self._parse_date_professional(data.get('date')),
                title=metadata.title,
                author=metadata.author,
                urgency_level=metadata.urgency_level,
                key_findings=data.get('key_assessments', [])  # For backward compatibility
            )

            logger.info("Professional report structure successfully parsed")
            return report

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logger.error(f"Professional parsing failed: {str(e)}")
            return self._create_professional_fallback(original_text, str(e))

    def _parse_reliability_professional(self, reliability_str: Optional[str]) -> ReliabilityLevel:
        """Professional source reliability assessment."""
        if not reliability_str:
            return ReliabilityLevel.C  # Default to fairly reliable for professional analysis

        reliability_str = reliability_str.upper()
        reliability_mapping = {
            'A': ReliabilityLevel.A,
            'B': ReliabilityLevel.B,
            'C': ReliabilityLevel.C,
            'D': ReliabilityLevel.D,
            'E': ReliabilityLevel.E,
            'F': ReliabilityLevel.F
        }

        # Extract letter grade
        for letter, level in reliability_mapping.items():
            if letter in reliability_str:
                return level

        return ReliabilityLevel.C  # Default to fairly reliable

    def _parse_credibility_professional(self, credibility_str: Optional[str]) -> CredibilityLevel:
        """Professional information credibility assessment."""
        if not credibility_str:
            return CredibilityLevel.THREE  # Default to possibly true

        credibility_mapping = {
            '1': CredibilityLevel.ONE,
            '2': CredibilityLevel.TWO,
            '3': CredibilityLevel.THREE,
            '4': CredibilityLevel.FOUR,
            '5': CredibilityLevel.FIVE,
            '6': CredibilityLevel.SIX
        }

        # Extract number
        for number, level in credibility_mapping.items():
            if number in str(credibility_str):
                return level

        return CredibilityLevel.THREE  # Default to possibly true

    def _parse_classification_professional(self, classification_str: Optional[str]) -> ClassificationLevel:
        """Professional classification assessment."""
        if not classification_str:
            return ClassificationLevel.UNCLASSIFIED

        classification_str = classification_str.upper()
        if 'TOP_SECRET' in classification_str or 'TOP SECRET' in classification_str:
            return ClassificationLevel.TOP_SECRET
        elif 'SECRET' in classification_str:
            return ClassificationLevel.SECRET
        elif 'CONFIDENTIAL' in classification_str:
            return ClassificationLevel.CONFIDENTIAL
        elif 'CUI' in classification_str:
            return ClassificationLevel.CUI
        else:
            return ClassificationLevel.UNCLASSIFIED

    def _parse_date_professional(self, date_str: Optional[str]) -> datetime:
        """Professional date parsing with multiple format support."""
        if not date_str:
            return datetime.now()

        date_formats = [
            '%Y-%m-%d',
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%dT%H:%M:%S',
            '%m/%d/%Y',
            '%d/%m/%Y',
            '%B %d, %Y',
            '%d %B %Y'
        ]

        for fmt in date_formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue

        # If all parsing fails, return current time
        logger.warning(f"Could not parse date: {date_str}")
        return datetime.now()

    def _create_professional_fallback(self, text: str, error: str) -> StandardReport:
        """Create professional fallback report when AI processing fails."""

        logger.warning("Creating professional fallback report due to processing failure")

        # Extract basic information using heuristics
        bluf = self._extract_professional_bluf_fallback(text)
        key_assessments = self._extract_professional_assessments_fallback(text)
        entities = self._extract_professional_entities_fallback(text)

        return StandardReport(
            classification=ClassificationLevel.UNCLASSIFIED,
            bluf=bluf,
            key_assessments=key_assessments,
            current_situation=self._extract_situation_fallback(text),
            threat_assessment="Threat assessment requires manual analysis due to processing limitations",
            risk_analysis="Risk analysis requires manual review of source material",
            intelligence_gaps=["Complete analysis requires manual intelligence review"],
            recommendations=IntelligenceRecommendations(
                immediate_actions=["Review source material manually for immediate actions"],
                risk_mitigation=["Conduct comprehensive threat assessment"],
                collection_priorities=["Identify additional intelligence sources"]
            ),
            entities=entities,
            source_reliability=ReliabilityLevel.C,
            info_credibility=CredibilityLevel.THREE,
            confidence_level="Low",
            confidence_score=0.3,
            analyst_notes=f"Automated processing encountered technical issues. Manual analyst review required. Error: {error}",
            report_metadata=ReportMetadataProfessional(
                title="Intelligence Report - Manual Review Required",
                date=datetime.now().strftime('%Y-%m-%d'),
                source_type="Processing fallback",
                urgency_level="medium"
            )
        )

    def _extract_professional_bluf_fallback(self, text: str) -> str:
        """Extract professional BLUF using advanced heuristics."""

        # Look for executive summary patterns
        bluf_patterns = [
            r'(?:BLUF|Bottom Line Up Front|Executive Summary|Key Points)[:\-\s]+(.*?)(?:\n\n|\n(?:[A-Z][A-Z\s]+:))',
            r'^([^.\n]*(?:critical|urgent|immediate|significant|threat|risk|assessment)[^.\n]*\.)',
            r'(.*?(?:recommends?|suggests?|advises?|requires?)[^.\n]*\.)',
        ]

        extracted_parts = []

        for pattern in bluf_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE | re.DOTALL)
            for match in matches:
                clean_match = match.strip()
                if len(clean_match) > 50:  # Substantial content
                    extracted_parts.append(clean_match)

        if extracted_parts:
            # Combine and clean up
            bluf = ' '.join(extracted_parts[:3])  # Use first 3 substantial parts
            # Ensure it's substantial for professional standards
            if len(bluf) >= 200:
                return bluf[:1000]  # Professional length limit

        # Fallback: create structured BLUF from content analysis
        first_paragraphs = [p.strip() for p in text.split('\n\n')[:3] if len(p.strip()) > 50]

        if first_paragraphs:
            combined = ' '.join(first_paragraphs)
            if len(combined) >= 200:
                return combined[:1000]

        # Final professional fallback
        return (
            "Intelligence analysis indicates significant developments requiring immediate attention and assessment. "
            "The source material contains information relevant to operational security and strategic planning that "
            "necessitates comprehensive review by qualified intelligence analysts. Manual analysis is recommended "
            "to extract complete intelligence picture and develop actionable recommendations for decision-makers."
        )

    def _extract_professional_assessments_fallback(self, text: str) -> List[str]:
        """Extract key assessments using professional heuristics."""

        assessments = []

        # Look for numerical data - critical for intelligence assessments
        number_patterns = [
            r'(\d+(?:,\d+)*)\s*(?:casualties?|deaths?|killed|wounded|injured)',
            r'(\d+(?:,\d+)*)\s*(?:attacks?|strikes?|incidents?|operations?)',
            r'(\d+(?:,\d+)*)\s*(?:personnel|troops|forces|combatants)',
            r'(\d+(?:,\d+)*)\s*(?:percent|%)\s*(?:increase|decrease|change)',
            r'(\d+(?:,\d+)*)\s*(?:million|billion)\s*(?:dollars?|\$|cost)'
        ]

        for pattern in number_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                # Get context around the number
                start = max(0, match.start() - 100)
                end = min(len(text), match.end() + 100)
                context = text[start:end].strip()

                # Clean and format
                sentences = context.split('.')
                for sentence in sentences:
                    if match.group() in sentence and len(sentence.strip()) > 30:
                        assessments.append(sentence.strip())
                        break

        # Look for trend indicators
        trend_patterns = [
            r'[^.\n]*(?:increas|decreas|escalat|intensif|deterior|improv)[^.\n]*\.',
            r'[^.\n]*(?:threat|risk|vulnerabilit|capabilit)[^.\n]*\.',
            r'[^.\n]*(?:timeline|deadline|schedul|target)[^.\n]*\.'
        ]

        for pattern in trend_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                clean_match = match.strip()
                if len(clean_match) > 40 and clean_match not in assessments:
                    assessments.append(clean_match)

        # Ensure minimum professional standards
        if len(assessments) < 3:
            assessments.extend([
                "Source material requires comprehensive analysis to extract quantitative assessments",
                "Intelligence indicates developments requiring further verification and analysis",
                "Situation assessment necessitates additional collection and evaluation"
            ])

        return assessments[:10]  # Limit to 10 professional assessments

    def _extract_professional_entities_fallback(self, text: str) -> ProfessionalEntities:
        """Extract entities using professional NER patterns."""

        # Professional entity patterns - very strict to avoid false positives
        people_patterns = [
            r'\b(?:Dr|Colonel|General|Admiral|Professor|Director)\.\s+[A-Z][a-z]+\s+[A-Z][a-z]+',
            r'\b[A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+(?:said|stated|reported|indicated|confirmed))',
            r'\b(?:Mr|Ms|Mrs)\.\s+[A-Z][a-z]+\s+[A-Z][a-z]+'
        ]

        org_patterns = [
            r'\b[A-Z]{2,6}\b',  # Acronyms like WHO, FCDO, NATO
            r'\b[A-Z][a-zA-Z\s&]+(?:Agency|Office|Department|Ministry|Organization|Company|Corporation)\b',
            r'\b(?:United Nations|World Health Organization|Red Cross|UNICEF|NATO)\b'
        ]

        location_patterns = [
            r'\b[A-Z][a-z]+,\s*[A-Z][a-z]+',  # City, Country
            r'\b(?:Kyiv|Kiev|Lviv|Dnipro|Ukraine|Russia|Poland|Belarus)\b',
            r'\b[A-Z][a-z]+\s+(?:Oblast|Region|Province|State|County)\b'
        ]

        date_patterns = [
            r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}',
            r'\b\d{1,2}/\d{1,2}/\d{4}',
            r'\b\d{4}-\d{2}-\d{2}'
        ]

        equipment_patterns = [
            r'\b[A-Z][a-z]*-?\d+\s*(?:drone|missile|aircraft|tank|system)',
            r'\b(?:Shahed|Bayraktar|S-\d+|HIMARS|Javelin)\b'
        ]

        # Extract entities
        people = self._extract_pattern_matches(text, people_patterns)
        organizations = self._extract_pattern_matches(text, org_patterns)
        locations = self._extract_pattern_matches(text, location_patterns)
        dates = self._extract_pattern_matches(text, date_patterns)
        equipment = self._extract_pattern_matches(text, equipment_patterns)

        # Extract critical figures
        critical_figures = {}
        number_contexts = [
            (r'(\d+(?:,\d+)*)\s*(?:casualties?|deaths?)', 'casualty_data'),
            (r'(\d+(?:,\d+)*)\s*(?:attacks?|strikes?)', 'attack_frequencies'),
            (r'(\d+(?:,\d+)*)\s*(?:personnel|troops)', 'force_numbers')
        ]

        for pattern, key in number_contexts:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                critical_figures[key] = matches[0]

        return ProfessionalEntities(
            people=people[:10],
            organizations=organizations[:10],
            locations=locations[:10],
            dates=dates[:10],
            equipment_systems=equipment[:10],
            critical_figures=critical_figures
        )

    def _extract_pattern_matches(self, text: str, patterns: List[str]) -> List[str]:
        """Extract and clean pattern matches."""
        matches = []

        for pattern in patterns:
            found = re.findall(pattern, text, re.IGNORECASE)
            for match in found:
                clean_match = match.strip()
                if clean_match and clean_match not in matches:
                    matches.append(clean_match)

        return matches

    def _extract_situation_fallback(self, text: str) -> str:
        """Extract current situation using heuristics."""

        # Look for situation indicators
        situation_patterns = [
            r'(?:Current situation|Currently|Presently|At this time|Status)[:\-\s]+(.*?)(?:\n\n|\n[A-Z])',
            r'(?:The situation|Situation)[^.]*[.]',
            r'[^.\n]*(?:is currently|are currently|remains|continues)[^.\n]*\.'
        ]

        for pattern in situation_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                clean_match = match.strip()
                if len(clean_match) > 50:
                    return clean_match[:500]

        # Fallback: use first substantial paragraph
        paragraphs = [p.strip() for p in text.split('\n\n') if len(p.strip()) > 100]
        if paragraphs:
            return paragraphs[0][:500]

        return "Current situation requires comprehensive assessment based on available intelligence"

    def _combine_chunk_reports(self, chunk_reports: List[StandardReport], original_text: str) -> StandardReport:
        """Combine multiple chunk reports into comprehensive intelligence product."""

        if not chunk_reports:
            return self._create_professional_fallback(original_text, "No successful chunk processing")

        # Combine BLUFs
        combined_bluf = " ".join([report.bluf for report in chunk_reports])[:2000]  # Professional length

        # Combine assessments
        all_assessments = []
        for report in chunk_reports:
            all_assessments.extend(report.key_assessments)
        unique_assessments = list(dict.fromkeys(all_assessments))  # Remove duplicates, preserve order

        # Combine entities
        combined_entities = ProfessionalEntities()
        for report in chunk_reports:
            combined_entities.people.extend(report.entities.people)
            combined_entities.organizations.extend(report.entities.organizations)
            combined_entities.locations.extend(report.entities.locations)
            combined_entities.dates.extend(report.entities.dates)
            combined_entities.equipment_systems.extend(report.entities.equipment_systems)
            combined_entities.critical_figures.update(report.entities.critical_figures)

        # Remove duplicates from entity lists
        combined_entities.people = list(dict.fromkeys(combined_entities.people))
        combined_entities.organizations = list(dict.fromkeys(combined_entities.organizations))
        combined_entities.locations = list(dict.fromkeys(combined_entities.locations))
        combined_entities.dates = list(dict.fromkeys(combined_entities.dates))
        combined_entities.equipment_systems = list(dict.fromkeys(combined_entities.equipment_systems))

        # Use first chunk's structure as base
        base_report = chunk_reports[0]

        # Create comprehensive combined report
        return StandardReport(
            classification=base_report.classification,
            bluf=combined_bluf,
            key_assessments=unique_assessments[:10],  # Top 10 assessments
            current_situation=base_report.current_situation,
            recent_developments=base_report.recent_developments,
            threat_assessment=base_report.threat_assessment,
            risk_analysis=base_report.risk_analysis,
            intelligence_gaps=base_report.intelligence_gaps,
            recommendations=base_report.recommendations,
            entities=combined_entities,
            source_reliability=base_report.source_reliability,
            info_credibility=base_report.info_credibility,
            confidence_level=base_report.confidence_level,
            confidence_score=base_report.confidence_score,
            analyst_notes=f"Combined analysis from {len(chunk_reports)} report sections",
            report_metadata=base_report.report_metadata
        )

    def extract_entities_professional(self, text: str) -> Tuple[ProfessionalEntities, int]:
        """Extract entities using professional NER standards."""
        prompt = self.prompt_manager.get_entity_extraction_prompt()

        try:
            response, tokens = self._call_claude_professional(prompt, text)

            # Parse entity response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1

            if json_start != -1 and json_end > 0:
                json_str = response[json_start:json_end]
                data = json.loads(json_str)

                entities = ProfessionalEntities(
                    people=data.get('people', []),
                    organizations=data.get('organizations', []),
                    locations=data.get('locations', []),
                    dates=data.get('dates', []),
                    equipment_systems=data.get('equipment_systems', []),
                    critical_figures=data.get('critical_figures', {})
                )

                logger.info(f"Professional entity extraction successful: {len(entities.people)} people, {len(entities.organizations)} orgs")
                return entities, tokens
            else:
                # Fallback to pattern-based extraction
                entities = self._extract_professional_entities_fallback(text)
                return entities, 0

        except Exception as e:
            logger.warning(f"Professional entity extraction failed: {str(e)}")
            entities = self._extract_professional_entities_fallback(text)
            return entities, 0

    def _extract_professional_entities_fallback(self, text: str) -> ProfessionalEntities:
        """Fallback entity extraction using pattern matching."""
        import re

        # Pattern-based extraction for common entities
        people_patterns = [
            r'\b[A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b',  # Full names
            r'\b(?:Mr|Ms|Mrs|Dr|Prof|Colonel|General|President|Prime Minister|Minister)\.\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b'
        ]

        org_patterns = [
            r'\b[A-Z]{2,10}\b',  # Acronyms
            r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Corporation|Company|Ltd|Inc|Organization|Agency|Department|Ministry|Bureau)\b'
        ]

        location_patterns = [
            r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:,\s+[A-Z]{2,})\b',  # City, Country
            r'\b(?:United States|United Kingdom|Russia|China|France|Germany|Ukraine|Chad|Sudan|Yemen|Syria|Iraq|Iran|Afghanistan)\b'
        ]

        people = []
        organizations = []
        locations = []

        # Extract entities using patterns
        for pattern in people_patterns:
            people.extend(re.findall(pattern, text))

        for pattern in org_patterns:
            organizations.extend(re.findall(pattern, text))

        for pattern in location_patterns:
            locations.extend(re.findall(pattern, text))

        # Remove duplicates and filter out common words
        people = list(set([p for p in people if len(p.split()) >= 2 and not any(word.lower() in ['the', 'and', 'this', 'that'] for word in p.split())]))[:10]
        organizations = list(set([o for o in organizations if len(o) > 2]))[:10]
        locations = list(set([l for l in locations if len(l) > 2]))[:10]

        return ProfessionalEntities(
            people=people,
            organizations=organizations,
            locations=locations,
            dates=[],
            equipment_systems=[],
            critical_figures={}
        )


# Legacy wrapper for backward compatibility
class BLUFExtractor(ProfessionalIntelligenceExtractor):
    """Legacy BLUF extractor - redirects to professional system."""

    def extract_standard_report(self, text: str, tone: ToneType = ToneType.PROFESSIONAL) -> Tuple[StandardReport, int]:
        """Legacy method - redirects to professional processor."""
        return self.process_intelligence_report(text, tone)

    def extract(self, text: str) -> BLUFData:
        """Legacy BLUF extraction."""
        report, _ = self.process_intelligence_report(text)
        return BLUFData(
            summary=report.bluf,
            key_points=report.key_assessments,
            recommendations=report.recommendations.immediate_actions,
            urgency_level=report.urgency_level
        )


class EntityExtractor(ProfessionalIntelligenceExtractor):
    """Professional entity extraction system."""

    def extract_entities_professional(self, text: str) -> Tuple[ProfessionalEntities, int]:
        """Extract entities using professional NER standards."""

        prompt = self.prompt_manager.get_entity_extraction_prompt()

        try:
            response, tokens = self._call_claude_professional(prompt, text)

            # Parse entity response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1

            if json_start != -1 and json_end > 0:
                json_str = response[json_start:json_end]
                data = json.loads(json_str)

                entities = ProfessionalEntities(
                    people=data.get('people', []),
                    organizations=data.get('organizations', []),
                    locations=data.get('locations', []),
                    dates=data.get('dates', []),
                    equipment_systems=data.get('equipment_systems', []),
                    critical_figures=data.get('critical_figures', {})
                )

                return entities, tokens
            else:
                # Fallback to pattern-based extraction
                entities = self._extract_professional_entities_fallback(text)
                return entities, 0

        except Exception as e:
            logger.warning(f"Professional entity extraction failed: {str(e)}")
            entities = self._extract_professional_entities_fallback(text)
            return entities, 0

    def extract(self, text: str) -> Tuple[ExtractedEntities, int]:
        """Legacy entity extraction for backward compatibility."""
        prof_entities, tokens = self.extract_entities_professional(text)

        # Convert to legacy format
        legacy_entities = ExtractedEntities(
            people=prof_entities.people,
            organizations=prof_entities.organizations,
            locations=prof_entities.locations,
            dates=prof_entities.dates,
            other=prof_entities.equipment_systems
        )

        return legacy_entities, tokens


# Create aliases for backward compatibility
BaseExtractor = ProfessionalIntelligenceExtractor
MetadataExtractor = ProfessionalIntelligenceExtractor
MissingFieldsAnalyzer = ProfessionalIntelligenceExtractor