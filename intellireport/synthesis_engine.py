"""
Multi-Source Intelligence Synthesis Engine
Processes multiple documents simultaneously with sophisticated analytical techniques.
"""

import re
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass

from .analytical_engine import (
    AnalyticalTrail, StructuredAnalyticTechniques, AnalysisMode,
    Claim, Source, Hypothesis, Assumption
)

@dataclass
class TemporalPattern:
    """Represents temporal patterns across multiple sources."""
    pattern_type: str  # escalation, de-escalation, cyclical, sporadic
    timeframe: str
    confidence: float
    supporting_events: List[str]

@dataclass
class EntityRelationship:
    """Represents relationships between entities across documents."""
    entity1: str
    entity2: str
    relationship_type: str  # allied, adversarial, neutral, hierarchical
    confidence: float
    source_documents: List[str]

@dataclass
class Contradiction:
    """Represents contradictions found between sources."""
    claim1: str
    claim2: str
    source1: str
    source2: str
    contradiction_type: str  # factual, temporal, causal
    resolution_approach: str
    resolved: bool = False

class MultiSourceSynthesis:
    """
    Sophisticated engine for synthesizing intelligence from multiple sources.
    Identifies patterns, contradictions, and relationships across documents.
    """

    def __init__(self):
        self.sat_engine = StructuredAnalyticTechniques()
        self.trail = AnalyticalTrail()

        # Patterns for identifying claims
        self.CLAIM_PATTERNS = {
            'factual': [
                r'(\d+)\s+(people|casualties|deaths|injured)',
                r'(suspended|banned|restricted|imposed|announced)',
                r'(attacked|destroyed|captured|seized|occupied)',
                r'(signed|agreed|negotiated|declared|announced)'
            ],
            'temporal': [
                r'(yesterday|today|tomorrow|this week|last month)',
                r'(on\s+\w+\s+\d{1,2}|in\s+\w+\s+\d{4})',
                r'(before|after|during|since|until)'
            ],
            'causal': [
                r'(because|due to|as a result|therefore|consequently)',
                r'(led to|caused|triggered|resulted in|prompted)'
            ]
        }

    def process_multiple_documents(self,
                                 documents: List[Dict[str, str]],
                                 mode: AnalysisMode = AnalysisMode.MULTI_SOURCE) -> Dict[str, Any]:
        """
        Process up to 5 documents simultaneously with full synthesis analysis.

        Args:
            documents: List of documents with 'title', 'content', 'source' keys
            mode: Analysis mode (multi_source, web_enhanced, red_team)

        Returns:
            Comprehensive synthesis results with analytical trail
        """
        if len(documents) > 5:
            documents = documents[:5]  # Limit to 5 documents

        self.trail.log('synthesis_started', {
            'document_count': len(documents),
            'mode': mode.value,
            'total_length': sum(len(doc['content']) for doc in documents)
        })

        # Extract claims from all documents
        all_claims = []
        all_sources = []

        for i, doc in enumerate(documents):
            source = Source(
                id=f"SRC{i+1:03d}",
                name=doc.get('source', f"Document {i+1}"),
                reliability=self._assess_document_reliability(doc),
                access="indirect",  # Assumed for text documents
                timeliness=self._assess_document_timeliness(doc)
            )
            all_sources.append(source)

            claims = self._extract_claims_from_document(doc, source.id)
            all_claims.extend(claims)

        # Apply structured analytic techniques
        synthesis_results = {
            'executive_summary': '',
            'corroborated_claims': [],
            'contradictions': [],
            'temporal_patterns': [],
            'entity_relationships': [],
            'confidence_assessment': {},
            'recommendations': [],
            'analytical_metadata': {}
        }

        # Source triangulation
        triangulation = self.sat_engine.source_triangulation(all_sources, all_claims)
        synthesis_results['corroborated_claims'] = triangulation['corroborated_claims']

        # Identify contradictions
        contradictions = self._identify_contradictions(all_claims, all_sources)
        synthesis_results['contradictions'] = contradictions

        # Temporal pattern analysis
        temporal_patterns = self._analyze_temporal_patterns(all_claims, documents)
        synthesis_results['temporal_patterns'] = temporal_patterns

        # Entity relationship mapping
        entity_relationships = self._map_entity_relationships(documents)
        synthesis_results['entity_relationships'] = entity_relationships

        # Overall confidence assessment
        confidence_scores = self._calculate_synthesis_confidence(
            all_sources, all_claims, contradictions, temporal_patterns
        )
        synthesis_results['confidence_assessment'] = confidence_scores

        # Generate synthesis recommendations
        recommendations = self._generate_synthesis_recommendations(synthesis_results)
        synthesis_results['recommendations'] = recommendations

        # Apply mode-specific analysis
        if mode == AnalysisMode.RED_TEAM:
            red_team_analysis = self._apply_red_team_mode(synthesis_results)
            synthesis_results['red_team_analysis'] = red_team_analysis

        # Generate executive summary
        executive_summary = self._generate_executive_summary(synthesis_results, documents)
        synthesis_results['executive_summary'] = executive_summary

        # Compile analytical metadata
        synthesis_results['analytical_metadata'] = self._compile_analytical_metadata()

        self.trail.log('synthesis_completed', {
            'corroborated_claims': len(synthesis_results['corroborated_claims']),
            'contradictions_found': len(contradictions),
            'patterns_identified': len(temporal_patterns),
            'relationships_mapped': len(entity_relationships)
        })

        return synthesis_results

    def process_claim(self, claim_text: str, context: str = "") -> Dict[str, Any]:
        """
        Enhanced claim processing with sophisticated analysis.
        Applies ACH, assumption checking, and confidence calculation.
        """
        self.trail.log('claim_processing_started', {'claim': claim_text[:100]})

        # Apply Analysis of Competing Hypotheses
        hypotheses, selected_hypothesis = self.sat_engine.analysis_of_competing_hypotheses(
            claim_text, context
        )

        # Extract and check assumptions
        assumptions = self.sat_engine.key_assumptions_check(claim_text + " " + context)

        # Calculate confidence using multiple factors
        source_agreement = self._assess_source_agreement_for_claim(claim_text)
        historical_precedent = self._assess_historical_precedent(claim_text)
        logical_consistency = self._assess_logical_consistency(claim_text, context)
        technical_feasibility = self._assess_technical_feasibility(claim_text)

        confidence_score, confidence_level = self.sat_engine.calculate_confidence(
            source_agreement, historical_precedent, logical_consistency, technical_feasibility
        )

        # Format output for clean display
        processed_claim = {
            'original_claim': claim_text,
            'assessed_claim': f"{claim_text} ({confidence_level.value} confidence)",
            'confidence_score': confidence_score,
            'confidence_level': confidence_level.value,
            'selected_hypothesis': selected_hypothesis,
            'critical_assumptions': [a for a in assumptions if a.criticality == 'critical'],
            'analytical_notes': self._generate_analytical_notes(hypotheses, assumptions)
        }

        self.trail.log('claim_processed', {
            'confidence_level': confidence_level.value,
            'hypotheses_evaluated': len(hypotheses),
            'assumptions_identified': len(assumptions)
        })

        return processed_claim

    def _extract_claims_from_document(self, document: Dict[str, str], source_id: str) -> List[Claim]:
        """Extract factual claims from document text."""
        claims = []
        content = document['content']
        claim_id = 1

        # Extract different types of claims
        for claim_type, patterns in self.CLAIM_PATTERNS.items():
            for pattern in patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    # Extract sentence containing the match
                    start = max(0, content.rfind('.', 0, match.start()) + 1)
                    end = content.find('.', match.end())
                    if end == -1:
                        end = len(content)

                    claim_text = content[start:end].strip()

                    if len(claim_text) > 10:  # Filter out very short matches
                        claim = Claim(
                            id=f"C{claim_id:03d}",
                            text=claim_text,
                            confidence=0.5,  # Default, will be updated
                            sources=[source_id]
                        )
                        claims.append(claim)
                        claim_id += 1

        return claims[:20]  # Limit to most significant claims

    def _assess_document_reliability(self, document: Dict[str, str]) -> str:
        """Assess document reliability based on content and metadata."""
        content = document['content'].lower()
        source_name = document.get('source', '').lower()

        # Simple heuristic-based assessment
        if any(indicator in source_name for indicator in ['government', 'official', 'ministry']):
            return 'B'  # Usually reliable
        elif any(indicator in content for indicator in ['confirmed', 'verified', 'official']):
            return 'C'  # Fairly reliable
        elif any(indicator in content for indicator in ['rumor', 'unconfirmed', 'alleged']):
            return 'D'  # Not usually reliable
        else:
            return 'C'  # Default to fairly reliable

    def _assess_document_timeliness(self, document: Dict[str, str]) -> str:
        """Assess how current the document information is."""
        content = document['content'].lower()

        if any(indicator in content for indicator in ['today', 'this morning', 'breaking']):
            return 'real-time'
        elif any(indicator in content for indicator in ['yesterday', 'this week', 'recent']):
            return 'recent'
        else:
            return 'dated'

    def _identify_contradictions(self, claims: List[Claim], sources: List[Source]) -> List[Contradiction]:
        """Identify contradictions between claims from different sources."""
        contradictions = []

        # Compare claims for contradictions (simplified logic)
        for i, claim1 in enumerate(claims):
            for claim2 in claims[i+1:]:
                if claim1.sources != claim2.sources:  # Different sources
                    contradiction_type = self._assess_contradiction_type(claim1.text, claim2.text)

                    if contradiction_type:
                        contradiction = Contradiction(
                            claim1=claim1.text,
                            claim2=claim2.text,
                            source1=claim1.sources[0] if claim1.sources else "unknown",
                            source2=claim2.sources[0] if claim2.sources else "unknown",
                            contradiction_type=contradiction_type,
                            resolution_approach=self._suggest_resolution_approach(contradiction_type)
                        )
                        contradictions.append(contradiction)

        self.trail.contradictions_found.extend(contradictions)
        return contradictions[:5]  # Limit to most significant

    def _assess_contradiction_type(self, claim1: str, claim2: str) -> Optional[str]:
        """Assess if two claims contradict and determine type."""
        # Simplified contradiction detection
        claim1_lower = claim1.lower()
        claim2_lower = claim2.lower()

        # Factual contradictions
        if ('suspended' in claim1_lower and 'resumed' in claim2_lower) or \
           ('increased' in claim1_lower and 'decreased' in claim2_lower):
            return 'factual'

        # Temporal contradictions
        if ('before' in claim1_lower and 'after' in claim2_lower) or \
           ('yesterday' in claim1_lower and 'tomorrow' in claim2_lower):
            return 'temporal'

        return None

    def _suggest_resolution_approach(self, contradiction_type: str) -> str:
        """Suggest approach for resolving contradiction."""
        approaches = {
            'factual': 'Seek additional corroborating sources',
            'temporal': 'Verify timeline with primary sources',
            'causal': 'Apply structured analytic techniques'
        }
        return approaches.get(contradiction_type, 'Further investigation required')

    def _analyze_temporal_patterns(self, claims: List[Claim], documents: List[Dict]) -> List[TemporalPattern]:
        """Analyze temporal patterns across claims and documents."""
        patterns = []

        # Look for escalation patterns
        escalation_indicators = ['increased', 'escalated', 'intensified', 'expanded']
        escalation_count = sum(1 for claim in claims
                             if any(indicator in claim.text.lower() for indicator in escalation_indicators))

        if escalation_count >= 2:
            pattern = TemporalPattern(
                pattern_type='escalation',
                timeframe='72 hours',
                confidence=0.7,
                supporting_events=[claim.text for claim in claims
                                 if any(indicator in claim.text.lower() for indicator in escalation_indicators)][:3]
            )
            patterns.append(pattern)

        return patterns

    def _map_entity_relationships(self, documents: List[Dict]) -> List[EntityRelationship]:
        """Map relationships between entities across documents."""
        relationships = []

        # Extract entities and their relationships (simplified)
        all_text = " ".join(doc['content'] for doc in documents)

        # Look for relationship indicators
        adversarial_patterns = ['against', 'opposed', 'conflict', 'fighting']
        allied_patterns = ['with', 'together', 'allied', 'cooperation']

        # This would be more sophisticated in production with NER
        entities = ['Chad', 'Sudan', 'France', 'AU', 'UN']  # Example entities

        for i, entity1 in enumerate(entities):
            for entity2 in entities[i+1:]:
                if entity1 in all_text and entity2 in all_text:
                    # Simple relationship detection
                    context = self._extract_entity_context(all_text, entity1, entity2)

                    if any(pattern in context.lower() for pattern in adversarial_patterns):
                        relationship_type = 'adversarial'
                        confidence = 0.6
                    elif any(pattern in context.lower() for pattern in allied_patterns):
                        relationship_type = 'allied'
                        confidence = 0.6
                    else:
                        relationship_type = 'neutral'
                        confidence = 0.4

                    relationship = EntityRelationship(
                        entity1=entity1,
                        entity2=entity2,
                        relationship_type=relationship_type,
                        confidence=confidence,
                        source_documents=[doc.get('title', f'Doc{i}') for i, doc in enumerate(documents)]
                    )
                    relationships.append(relationship)

        return relationships[:5]  # Limit to most significant

    def _extract_entity_context(self, text: str, entity1: str, entity2: str) -> str:
        """Extract context around two entities."""
        # Find sentences containing both entities
        sentences = text.split('.')
        for sentence in sentences:
            if entity1 in sentence and entity2 in sentence:
                return sentence.strip()
        return ""

    def _calculate_synthesis_confidence(self,
                                      sources: List[Source],
                                      claims: List[Claim],
                                      contradictions: List[Contradiction],
                                      patterns: List[TemporalPattern]) -> Dict[str, Any]:
        """Calculate overall confidence in synthesis."""
        base_confidence = 0.5

        # Factor in source quality
        avg_source_reliability = self._average_source_reliability(sources)
        base_confidence += avg_source_reliability * 0.3

        # Factor in corroboration
        corroborated_claims = len([c for c in claims if len(c.corroborating_sources) > 0])
        if claims:
            corroboration_rate = corroborated_claims / len(claims)
            base_confidence += corroboration_rate * 0.2

        # Reduce for contradictions
        contradiction_penalty = min(0.2, len(contradictions) * 0.05)
        base_confidence -= contradiction_penalty

        # Factor in pattern strength
        pattern_boost = min(0.1, len(patterns) * 0.03)
        base_confidence += pattern_boost

        final_confidence = min(1.0, max(0.0, base_confidence))

        return {
            'overall_confidence': final_confidence,
            'source_reliability_avg': avg_source_reliability,
            'corroboration_rate': corroboration_rate if claims else 0,
            'contradiction_count': len(contradictions),
            'pattern_strength': len(patterns)
        }

    def _average_source_reliability(self, sources: List[Source]) -> float:
        """Calculate average source reliability."""
        reliability_map = {'A': 1.0, 'B': 0.8, 'C': 0.6, 'D': 0.4, 'E': 0.2, 'F': 0.1}
        if not sources:
            return 0.5

        total_reliability = sum(reliability_map.get(source.reliability, 0.5) for source in sources)
        return total_reliability / len(sources)

    def _generate_synthesis_recommendations(self, synthesis_results: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on synthesis analysis."""
        recommendations = []

        # Based on contradictions
        if synthesis_results['contradictions']:
            recommendations.append("Resolve source contradictions through additional collection")

        # Based on confidence
        confidence = synthesis_results['confidence_assessment'].get('overall_confidence', 0.5)
        if confidence < 0.6:
            recommendations.append("Seek additional sources to improve assessment confidence")

        # Based on patterns
        if synthesis_results['temporal_patterns']:
            recommendations.append("Monitor escalation indicators for next 72 hours")

        return recommendations

    def _apply_red_team_mode(self, synthesis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Apply red team analysis to challenge synthesis results."""
        executive_summary = synthesis_results.get('executive_summary', '')

        red_team_analysis = self.sat_engine.devils_advocacy(
            executive_summary,
            [claim.text for claim in synthesis_results.get('corroborated_claims', [])]
        )

        return red_team_analysis

    def _generate_executive_summary(self, synthesis_results: Dict[str, Any], documents: List[Dict]) -> str:
        """Generate clean executive summary from synthesis."""
        # This would be more sophisticated in production
        doc_count = len(documents)
        corroborated_count = len(synthesis_results.get('corroborated_claims', []))
        contradiction_count = len(synthesis_results.get('contradictions', []))

        summary = f"Analysis of {doc_count} intelligence sources reveals {corroborated_count} corroborated claims "

        if contradiction_count > 0:
            summary += f"with {contradiction_count} contradictions requiring resolution. "
        else:
            summary += "with consistent reporting across sources. "

        if synthesis_results.get('temporal_patterns'):
            summary += "Temporal analysis indicates escalation pattern requiring immediate attention."
        else:
            summary += "Situation appears stable with no clear escalation indicators."

        return summary

    def _compile_analytical_metadata(self) -> Dict[str, Any]:
        """Compile complete analytical metadata for transparency."""
        return {
            'trail_summary': self.trail.get_summary(),
            'techniques_applied': list(set(self.trail.techniques_applied)),
            'confidence_factors': self.trail.confidence_factors,
            'processing_steps': len(self.trail.steps),
            'last_updated': datetime.now().isoformat()
        }

    # Helper methods for claim processing
    def _assess_source_agreement_for_claim(self, claim: str) -> float:
        """Assess source agreement for specific claim."""
        # Simplified - would use actual source comparison in production
        return 0.75

    def _assess_historical_precedent(self, claim: str) -> float:
        """Assess historical precedent for claim."""
        # Simplified - would check historical databases in production
        return 0.65

    def _assess_logical_consistency(self, claim: str, context: str) -> float:
        """Assess logical consistency of claim with context."""
        # Simplified logical consistency check
        return 0.80

    def _assess_technical_feasibility(self, claim: str) -> float:
        """Assess technical feasibility of claim."""
        # Simplified feasibility assessment
        return 0.70

    def _generate_analytical_notes(self, hypotheses: List[Hypothesis], assumptions: List[Assumption]) -> str:
        """Generate analytical notes for metadata."""
        selected_hyp = next((h for h in hypotheses if h.selected), hypotheses[0] if hypotheses else None)
        critical_assumptions = [a for a in assumptions if a.criticality == 'critical']

        notes = f"Primary hypothesis: {selected_hyp.description if selected_hyp else 'None identified'}. "
        if critical_assumptions:
            notes += f"Critical assumptions: {len(critical_assumptions)} identified requiring validation."
        else:
            notes += "No critical assumptions identified."

        return notes

# Export main class
__all__ = ['MultiSourceSynthesis', 'TemporalPattern', 'EntityRelationship', 'Contradiction']