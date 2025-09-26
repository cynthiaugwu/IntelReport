"""
Enhanced entity redaction functionality with configurable levels.
"""

import re
import json
import os
from typing import List, Dict, Any, Tuple, Optional, Set
from enum import Enum
import anthropic

from .schemas import EntityRedaction


class RedactionLevel(str, Enum):
    """Configurable redaction levels."""
    NONE = "none"           # No redaction
    LOW = "low"             # Only critical PII (SSN, credit cards)
    MEDIUM = "medium"       # Standard PII (names, emails, phones)
    HIGH = "high"           # Aggressive redaction (locations, organizations)
    MAXIMUM = "maximum"     # Everything potentially sensitive


class PIIType(str, Enum):
    """Types of PII that can be redacted."""
    PERSON_NAME = "person_name"
    EMAIL = "email"
    PHONE = "phone"
    SSN = "ssn"
    CREDIT_CARD = "credit_card"
    ADDRESS = "address"
    ORGANIZATION = "organization"
    LOCATION = "location"
    DATE = "date"
    ID_NUMBER = "id_number"
    FINANCIAL = "financial"
    MEDICAL = "medical"
    IP_ADDRESS = "ip_address"
    URL = "url"


class EntityRedactor:
    """Enhanced entity redactor with configurable PII levels."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-3-5-sonnet-latest",
        use_ai: bool = True
    ):
        """Initialize the entity redactor."""
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model
        self.use_ai = use_ai

        if self.use_ai and not self.api_key:
            raise ValueError("Anthropic API key is required for AI-powered redaction")

        if self.use_ai:
            self.client = anthropic.Anthropic(api_key=self.api_key)

        # Define redaction patterns for each PII type
        self.redaction_patterns = self._initialize_patterns()

        # Define what gets redacted at each level
        self.level_mappings = {
            RedactionLevel.NONE: set(),
            RedactionLevel.LOW: {
                PIIType.SSN, PIIType.CREDIT_CARD, PIIType.ID_NUMBER
            },
            RedactionLevel.MEDIUM: {
                PIIType.SSN, PIIType.CREDIT_CARD, PIIType.ID_NUMBER,
                PIIType.PERSON_NAME, PIIType.EMAIL, PIIType.PHONE
            },
            RedactionLevel.HIGH: {
                PIIType.SSN, PIIType.CREDIT_CARD, PIIType.ID_NUMBER,
                PIIType.PERSON_NAME, PIIType.EMAIL, PIIType.PHONE,
                PIIType.ADDRESS, PIIType.ORGANIZATION, PIIType.LOCATION
            },
            RedactionLevel.MAXIMUM: set(PIIType)
        }

    def _initialize_patterns(self) -> Dict[PIIType, List[Dict[str, Any]]]:
        """Initialize regex patterns for different PII types."""
        return {
            PIIType.EMAIL: [
                {
                    'pattern': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                    'confidence': 0.95,
                    'replacement': '[REDACTED-EMAIL]'
                }
            ],
            PIIType.PHONE: [
                {
                    'pattern': r'\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b',
                    'confidence': 0.90,
                    'replacement': '[REDACTED-PHONE]'
                },
                {
                    'pattern': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
                    'confidence': 0.85,
                    'replacement': '[REDACTED-PHONE]'
                }
            ],
            PIIType.SSN: [
                {
                    'pattern': r'\b\d{3}-\d{2}-\d{4}\b',
                    'confidence': 0.98,
                    'replacement': '[REDACTED-SSN]'
                },
                {
                    'pattern': r'\b\d{3}\s\d{2}\s\d{4}\b',
                    'confidence': 0.95,
                    'replacement': '[REDACTED-SSN]'
                }
            ],
            PIIType.CREDIT_CARD: [
                {
                    'pattern': r'\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|3[0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b',
                    'confidence': 0.95,
                    'replacement': '[REDACTED-CREDIT-CARD]'
                }
            ],
            PIIType.ADDRESS: [
                {
                    'pattern': r'\d+\s+[A-Za-z0-9\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr|Court|Ct|Place|Pl)',
                    'confidence': 0.80,
                    'replacement': '[REDACTED-ADDRESS]'
                }
            ],
            PIIType.PERSON_NAME: [
                {
                    'pattern': r'\b(?:Mr|Ms|Mrs|Dr|Prof|Gen|Col|Maj|Capt|Lt)\.?\s+[A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+(?:Jr|Sr|II|III|IV))?\b',
                    'confidence': 0.85,
                    'replacement': '[REDACTED-NAME]'
                }
            ],
            PIIType.IP_ADDRESS: [
                {
                    'pattern': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
                    'confidence': 0.90,
                    'replacement': '[REDACTED-IP]'
                }
            ],
            PIIType.URL: [
                {
                    'pattern': r'https?://[^\s]+',
                    'confidence': 0.95,
                    'replacement': '[REDACTED-URL]'
                }
            ],
            PIIType.DATE: [
                {
                    'pattern': r'\b(?:0?[1-9]|1[0-2])[/-](?:0?[1-9]|[12][0-9]|3[01])[/-](?:19|20)\d{2}\b',
                    'confidence': 0.85,
                    'replacement': '[REDACTED-DATE]'
                }
            ],
            PIIType.ID_NUMBER: [
                {
                    'pattern': r'\b(?:ID|Employee|EMP|Badge)[-\s]*[:\#]?[-\s]*[A-Z0-9]{6,15}\b',
                    'confidence': 0.80,
                    'replacement': '[REDACTED-ID]'
                }
            ]
        }

    def redact_pii(
        self,
        text: str,
        level: RedactionLevel = RedactionLevel.MEDIUM,
        custom_patterns: Optional[Dict[str, str]] = None
    ) -> Tuple[str, List[EntityRedaction]]:
        """
        Redact PII from text based on specified level.

        Args:
            text: Input text to redact
            level: Redaction level to apply
            custom_patterns: Additional custom patterns to apply

        Returns:
            Tuple of (redacted_text, list_of_redacted_entities)
        """
        if level == RedactionLevel.NONE:
            return text, []

        redacted_text = text
        redacted_entities = []

        # Get PII types to redact for this level
        pii_types_to_redact = self.level_mappings[level]

        # Apply pattern-based redaction
        for pii_type in pii_types_to_redact:
            if pii_type in self.redaction_patterns:
                redacted_text, entities = self._apply_patterns(
                    redacted_text, pii_type, self.redaction_patterns[pii_type]
                )
                redacted_entities.extend(entities)

        # Apply custom patterns if provided
        if custom_patterns:
            redacted_text, custom_entities = self._apply_custom_patterns(
                redacted_text, custom_patterns
            )
            redacted_entities.extend(custom_entities)

        # Use AI for additional entity detection if enabled and level is HIGH or MAXIMUM
        if self.use_ai and level in [RedactionLevel.HIGH, RedactionLevel.MAXIMUM]:
            try:
                redacted_text, ai_entities = self._apply_ai_redaction(
                    redacted_text, level
                )
                redacted_entities.extend(ai_entities)
            except Exception as e:
                # AI redaction is optional - continue with pattern-based results
                pass

        return redacted_text, redacted_entities

    def _apply_patterns(
        self,
        text: str,
        pii_type: PIIType,
        patterns: List[Dict[str, Any]]
    ) -> Tuple[str, List[EntityRedaction]]:
        """Apply regex patterns for a specific PII type."""
        redacted_text = text
        entities = []

        for pattern_config in patterns:
            pattern = pattern_config['pattern']
            confidence = pattern_config['confidence']
            replacement = pattern_config['replacement']

            matches = list(re.finditer(pattern, redacted_text, re.IGNORECASE))

            for match in reversed(matches):  # Reverse to maintain positions
                original_text = match.group()
                start_pos = match.start()
                end_pos = match.end()

                entity = EntityRedaction(
                    entity_type=pii_type.value,
                    original_text=original_text,
                    redacted_text=replacement,
                    confidence=confidence,
                    location_start=start_pos,
                    location_end=end_pos
                )

                entities.append(entity)

                # Replace in text
                redacted_text = (
                    redacted_text[:start_pos] +
                    replacement +
                    redacted_text[end_pos:]
                )

        return redacted_text, entities

    def _apply_custom_patterns(
        self,
        text: str,
        custom_patterns: Dict[str, str]
    ) -> Tuple[str, List[EntityRedaction]]:
        """Apply user-provided custom redaction patterns."""
        redacted_text = text
        entities = []

        for pattern_name, pattern in custom_patterns.items():
            matches = list(re.finditer(pattern, redacted_text, re.IGNORECASE))

            for match in reversed(matches):
                original_text = match.group()
                start_pos = match.start()
                end_pos = match.end()
                replacement = f"[REDACTED-{pattern_name.upper()}]"

                entity = EntityRedaction(
                    entity_type=f"custom_{pattern_name}",
                    original_text=original_text,
                    redacted_text=replacement,
                    confidence=0.75,  # Lower confidence for custom patterns
                    location_start=start_pos,
                    location_end=end_pos
                )

                entities.append(entity)

                # Replace in text
                redacted_text = (
                    redacted_text[:start_pos] +
                    replacement +
                    redacted_text[end_pos:]
                )

        return redacted_text, entities

    def _apply_ai_redaction(
        self,
        text: str,
        level: RedactionLevel
    ) -> Tuple[str, List[EntityRedaction]]:
        """Use AI to identify and redact additional entities."""
        if not self.use_ai:
            return text, []

        prompt = self._get_ai_redaction_prompt(level)

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                messages=[{
                    "role": "user",
                    "content": f"{prompt}\n\nText to analyze:\n{text}"
                }]
            )

            response_text = response.content[0].text
            ai_entities_data = json.loads(response_text)

            redacted_text = text
            entities = []

            # Process AI-identified entities
            for entity_data in ai_entities_data.get("entities", []):
                if entity_data.get("confidence", 0) >= 0.7:
                    original = entity_data["original_text"]
                    replacement = entity_data["redacted_text"]

                    # Find and replace in text
                    if original in redacted_text:
                        start_pos = redacted_text.find(original)
                        end_pos = start_pos + len(original)

                        entity = EntityRedaction(
                            entity_type=entity_data["entity_type"],
                            original_text=original,
                            redacted_text=replacement,
                            confidence=entity_data["confidence"],
                            location_start=start_pos,
                            location_end=end_pos
                        )

                        entities.append(entity)
                        redacted_text = redacted_text.replace(original, replacement, 1)

            return redacted_text, entities

        except Exception:
            return text, []

    def _get_ai_redaction_prompt(self, level: RedactionLevel) -> str:
        """Get AI prompt for entity redaction based on level."""
        base_prompt = """
        Identify sensitive entities in the following text that should be redacted for privacy/security.
        Return your response as a JSON object with the following structure:

        {
            "entities": [
                {
                    "entity_type": "person|organization|location|financial|medical|other",
                    "original_text": "actual text found",
                    "redacted_text": "[REDACTED-TYPE]",
                    "confidence": 0.95
                }
            ]
        }
        """

        if level == RedactionLevel.HIGH:
            return base_prompt + """
            Focus on:
            1. Person names (full names, first/last names)
            2. Organization names (companies, agencies, departments)
            3. Specific locations (addresses, coordinates, facility names)
            4. Financial information (account numbers, amounts)
            5. Medical information (conditions, treatments)

            Only include entities with confidence > 0.8.
            """
        elif level == RedactionLevel.MAXIMUM:
            return base_prompt + """
            Be very aggressive in identifying potentially sensitive information:
            1. Any person names or references
            2. All organization names
            3. All location references (cities, states, countries)
            4. Dates that could be identifying
            5. Any numbers that could be IDs, accounts, or codes
            6. Technical details (IP addresses, server names, etc.)
            7. Any other potentially identifying information

            Only include entities with confidence > 0.7.
            """
        else:
            return base_prompt + "Focus on high-confidence, clearly sensitive entities only."

    def get_redaction_summary(
        self,
        original_text: str,
        redacted_text: str,
        entities: List[EntityRedaction]
    ) -> Dict[str, Any]:
        """
        Get a summary of redactions performed.

        Args:
            original_text: Original text
            redacted_text: Redacted text
            entities: List of redacted entities

        Returns:
            Dictionary with redaction summary
        """
        # Count by entity type
        type_counts = {}
        for entity in entities:
            entity_type = entity.entity_type
            type_counts[entity_type] = type_counts.get(entity_type, 0) + 1

        # Calculate redaction percentage
        original_len = len(original_text)
        redacted_len = len(redacted_text)
        chars_changed = sum(len(e.original_text) - len(e.redacted_text) for e in entities)

        return {
            "total_redactions": len(entities),
            "redaction_by_type": type_counts,
            "original_length": original_len,
            "redacted_length": redacted_len,
            "characters_redacted": abs(chars_changed),
            "redaction_percentage": (len(entities) / max(original_len, 1)) * 100,
            "high_confidence_redactions": len([e for e in entities if e.confidence >= 0.9]),
            "medium_confidence_redactions": len([e for e in entities if 0.7 <= e.confidence < 0.9]),
            "low_confidence_redactions": len([e for e in entities if e.confidence < 0.7])
        }

    def add_custom_pattern(
        self,
        pii_type: str,
        pattern: str,
        replacement: str,
        confidence: float = 0.8
    ) -> None:
        """
        Add a custom redaction pattern.

        Args:
            pii_type: Type of PII this pattern identifies
            pattern: Regex pattern
            replacement: Text to replace matches with
            confidence: Confidence level for this pattern
        """
        if pii_type not in self.redaction_patterns:
            self.redaction_patterns[pii_type] = []

        self.redaction_patterns[pii_type].append({
            'pattern': pattern,
            'confidence': confidence,
            'replacement': replacement
        })

    def configure_level(
        self,
        level: RedactionLevel,
        pii_types: Set[PIIType]
    ) -> None:
        """
        Configure what PII types are redacted at a specific level.

        Args:
            level: Redaction level to configure
            pii_types: Set of PII types to redact at this level
        """
        self.level_mappings[level] = pii_types

    def test_patterns(self, test_text: str) -> Dict[PIIType, List[str]]:
        """
        Test redaction patterns against sample text.

        Args:
            test_text: Text to test patterns against

        Returns:
            Dictionary mapping PII types to found matches
        """
        results = {}

        for pii_type, patterns in self.redaction_patterns.items():
            matches = []
            for pattern_config in patterns:
                pattern = pattern_config['pattern']
                found_matches = re.findall(pattern, test_text, re.IGNORECASE)
                matches.extend(found_matches)

            if matches:
                results[pii_type] = matches

        return results


# Legacy compatibility functions
def redact(text: str, use_ai: bool = True) -> str:
    """Legacy redaction function."""
    redactor = EntityRedactor(use_ai=use_ai)
    redacted_text, _ = redactor.redact_pii(text, RedactionLevel.MEDIUM)
    return redacted_text


def redact_entities(text: str, entities: List[str]) -> str:
    """Legacy entity redaction function."""
    redactor = EntityRedactor(use_ai=False)

    # Convert entities to custom patterns
    custom_patterns = {}
    for i, entity in enumerate(entities):
        # Escape special regex characters
        escaped_entity = re.escape(entity)
        custom_patterns[f"entity_{i}"] = escaped_entity

    redacted_text, _ = redactor.redact_pii(
        text,
        RedactionLevel.NONE,
        custom_patterns=custom_patterns
    )

    return redacted_text