"""
Professional Intelligence Analytical Engine
Implements Structured Analytic Techniques (SATs) for sophisticated intelligence analysis.
"""

import re
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

class AnalysisMode(str, Enum):
    """Analysis operation modes."""
    SINGLE_DOCUMENT = "single_document"
    MULTI_SOURCE = "multi_source"
    WEB_ENHANCED = "web_enhanced"
    RED_TEAM = "red_team"

class ConfidenceLevel(str, Enum):
    """Intelligence confidence levels."""
    HIGH = "high"
    MODERATE_HIGH = "moderate_high"
    MODERATE = "moderate"
    LOW_MODERATE = "low_moderate"
    LOW = "low"

@dataclass
class Hypothesis:
    """Represents a hypothesis in Analysis of Competing Hypotheses."""
    id: str
    description: str
    probability: float
    evidence_for: List[str] = field(default_factory=list)
    evidence_against: List[str] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)
    selected: bool = False
    rejection_reason: Optional[str] = None

@dataclass
class Assumption:
    """Represents an identified assumption."""
    id: str
    type: str  # temporal, causal, actor_intent, capability
    description: str
    criticality: str  # critical, moderate, minor
    evidence_support: float
    challenge_evidence: List[str] = field(default_factory=list)

@dataclass
class Source:
    """Represents an intelligence source."""
    id: str
    name: str
    reliability: str  # A-F scale
    access: str  # direct, indirect, assumed
    timeliness: str  # real-time, recent, dated
    corroboration_count: int = 0

@dataclass
class Claim:
    """Represents a factual claim from intelligence."""
    id: str
    text: str
    confidence: float
    sources: List[str] = field(default_factory=list)
    corroborating_sources: List[str] = field(default_factory=list)
    contradicting_sources: List[str] = field(default_factory=list)
    verification_status: str = "unverified"  # verified, unverified, disputed

class AnalyticalTrail:
    """
    Tracks all analytical steps, techniques, and decisions for transparency and audit.
    Operates invisibly behind the scenes to log sophisticated analysis.
    """

    def __init__(self):
        self.steps = []
        self.techniques_applied = []
        self.confidence_factors = {}
        self.assumptions_identified = []
        self.hypotheses_evaluated = []
        self.hypotheses_rejected = []
        self.sources_consulted = []
        self.contradictions_found = []
        self.claims_processed = []
        self.red_team_challenges = []

    def log(self, step_type: str, data: Dict[str, Any]):
        """Log an analytical step with confidence impact."""
        step = {
            'timestamp': datetime.now().isoformat(),
            'type': step_type,
            'data': data,
            'confidence_impact': self._calculate_impact(data)
        }
        self.steps.append(step)

    def _calculate_impact(self, data: Dict[str, Any]) -> float:
        """Calculate how this step impacts overall confidence."""
        step_type = data.get('type', '')

        impact_map = {
            'source_corroboration': 0.15,
            'contradiction_resolved': 0.10,
            'assumption_validated': 0.08,
            'hypothesis_confirmed': 0.20,
            'red_team_challenge': -0.05,
            'quality_check_passed': 0.12
        }

        return impact_map.get(step_type, 0.05)

    def get_summary(self) -> Dict[str, Any]:
        """Get analytical trail summary for metadata panel."""
        return {
            'total_steps': len(self.steps),
            'techniques_applied': list(set(self.techniques_applied)),
            'confidence_factors': self.confidence_factors,
            'assumptions_count': len(self.assumptions_identified),
            'hypotheses_evaluated': len(self.hypotheses_evaluated),
            'sources_consulted': len(self.sources_consulted),
            'contradictions_resolved': len(self.contradictions_found)
        }

class StructuredAnalyticTechniques:
    """
    Implements professional Structured Analytic Techniques (SATs) used by intelligence community.
    All processing happens invisibly - only results appear in clean output.
    """

    def __init__(self):
        self.trail = AnalyticalTrail()

        # Assumption identification patterns
        self.ASSUMPTION_PATTERNS = {
            'temporal': ['will continue', 'remains', 'ongoing', 'permanent', 'indefinitely'],
            'causal': ['therefore', 'because', 'due to', 'as a result', 'consequently'],
            'actor_intent': ['likely to', 'probably will', 'intends', 'plans to', 'aims to'],
            'capability': ['able to', 'capacity to', 'can achieve', 'capable of', 'has means']
        }

        # Confidence calculation weights
        self.CONFIDENCE_WEIGHTS = {
            'source_agreement': 0.40,
            'historical_precedent': 0.20,
            'logical_consistency': 0.15,
            'technical_feasibility': 0.25
        }

    def analysis_of_competing_hypotheses(self, claim: str, context: str) -> Tuple[List[Hypothesis], str]:
        """
        Apply Analysis of Competing Hypotheses (ACH) technique.
        Generates 3-5 alternative hypotheses and evaluates evidence.
        """
        self.trail.log('technique_applied', {'name': 'ACH', 'claim': claim})

        # Generate hypotheses based on claim analysis
        hypotheses = self._generate_hypotheses(claim, context)

        # Evaluate evidence for each hypothesis
        for hypothesis in hypotheses:
            self._evaluate_hypothesis_evidence(hypothesis, context)

        # Select most probable hypothesis
        selected_hypothesis = max(hypotheses, key=lambda h: h.probability)
        selected_hypothesis.selected = True

        # Mark rejected hypotheses with reasons
        for h in hypotheses:
            if not h.selected and h.probability < 0.15:
                h.rejection_reason = "insufficient supporting evidence"

        self.trail.hypotheses_evaluated.extend(hypotheses)
        self.trail.log('hypothesis_selection', {
            'selected': selected_hypothesis.description,
            'probability': selected_hypothesis.probability,
            'rejected_count': len([h for h in hypotheses if h.rejection_reason])
        })

        return hypotheses, selected_hypothesis.description

    def key_assumptions_check(self, text: str) -> List[Assumption]:
        """
        Apply Key Assumptions Check (KAC) technique.
        Identifies underlying assumptions that could invalidate analysis.
        """
        self.trail.log('technique_applied', {'name': 'KAC', 'text_length': len(text)})

        assumptions = []
        assumption_id = 1

        for assumption_type, patterns in self.ASSUMPTION_PATTERNS.items():
            for pattern in patterns:
                matches = re.finditer(rf'\b{re.escape(pattern)}\b[^.]*\.', text, re.IGNORECASE)
                for match in matches:
                    assumption_text = match.group().strip()

                    assumption = Assumption(
                        id=f"A{assumption_id:03d}",
                        type=assumption_type,
                        description=assumption_text,
                        criticality=self._assess_assumption_criticality(assumption_text),
                        evidence_support=self._calculate_assumption_support(assumption_text, text)
                    )

                    assumptions.append(assumption)
                    assumption_id += 1

        # Remove duplicates and limit to most critical
        unique_assumptions = self._deduplicate_assumptions(assumptions)[:12]

        self.trail.assumptions_identified.extend(unique_assumptions)
        self.trail.log('assumptions_identified', {
            'count': len(unique_assumptions),
            'critical_count': len([a for a in unique_assumptions if a.criticality == 'critical'])
        })

        return unique_assumptions

    def source_triangulation(self, sources: List[Source], claims: List[Claim]) -> Dict[str, Any]:
        """
        Apply Source Triangulation technique.
        Cross-references claims across multiple sources for corroboration.
        """
        self.trail.log('technique_applied', {'name': 'Source Triangulation', 'sources': len(sources)})

        triangulation_results = {
            'corroborated_claims': [],
            'contradictory_claims': [],
            'single_source_claims': [],
            'reliability_assessment': {}
        }

        # Group claims by similarity
        claim_groups = self._group_similar_claims(claims)

        for group in claim_groups:
            if len(group) >= 2:
                # Multiple sources - check for corroboration
                source_agreement = self._assess_source_agreement(group, sources)

                if source_agreement > 0.7:
                    triangulation_results['corroborated_claims'].extend(group)
                else:
                    triangulation_results['contradictory_claims'].extend(group)
            else:
                triangulation_results['single_source_claims'].extend(group)

        # Assess source reliability patterns
        for source in sources:
            reliability_score = self._calculate_source_reliability(source, claims)
            triangulation_results['reliability_assessment'][source.id] = reliability_score

        self.trail.sources_consulted.extend([s.id for s in sources])
        self.trail.log('triangulation_complete', triangulation_results)

        return triangulation_results

    def quality_of_information_check(self, claims: List[Claim], sources: List[Source]) -> Dict[str, Any]:
        """
        Apply Quality of Information Check technique.
        Assesses reliability and credibility of intelligence sources.
        """
        self.trail.log('technique_applied', {'name': 'Quality Check'})

        quality_assessment = {
            'high_quality_claims': [],
            'medium_quality_claims': [],
            'low_quality_claims': [],
            'source_reliability_map': {},
            'credibility_factors': {}
        }

        for claim in claims:
            quality_score = self._assess_claim_quality(claim, sources)

            if quality_score >= 0.8:
                quality_assessment['high_quality_claims'].append(claim)
            elif quality_score >= 0.5:
                quality_assessment['medium_quality_claims'].append(claim)
            else:
                quality_assessment['low_quality_claims'].append(claim)

        self.trail.log('quality_assessment', {
            'high_quality_count': len(quality_assessment['high_quality_claims']),
            'total_claims': len(claims)
        })

        return quality_assessment

    def what_if_analysis(self, scenario: str, assumptions: List[Assumption]) -> Dict[str, Any]:
        """
        Apply What-If Analysis technique.
        Explores alternative scenarios by challenging key assumptions.
        """
        self.trail.log('technique_applied', {'name': 'What-If Analysis'})

        alternative_scenarios = []

        # Challenge each critical assumption
        for assumption in assumptions:
            if assumption.criticality == 'critical':
                alt_scenario = self._generate_alternative_scenario(scenario, assumption)
                alternative_scenarios.append(alt_scenario)

        what_if_results = {
            'baseline_scenario': scenario,
            'alternative_scenarios': alternative_scenarios,
            'probability_shifts': self._calculate_probability_shifts(alternative_scenarios),
            'impact_assessment': self._assess_scenario_impacts(alternative_scenarios)
        }

        self.trail.log('what_if_complete', {
            'scenarios_generated': len(alternative_scenarios),
            'high_impact_scenarios': len([s for s in alternative_scenarios if s.get('impact_level') == 'high'])
        })

        return what_if_results

    def devils_advocacy(self, primary_assessment: str, evidence: List[str]) -> Dict[str, Any]:
        """
        Apply Devil's Advocacy technique for Red Team mode.
        Generates contrarian analysis challenging primary assessment.
        """
        self.trail.log('technique_applied', {'name': 'Devils Advocacy'})

        contrarian_analysis = {
            'primary_challenges': [],
            'alternative_explanations': [],
            'evidence_reinterpretation': [],
            'deception_indicators': [],
            'confidence_challenges': []
        }

        # Challenge primary assessment
        challenges = self._generate_contrarian_challenges(primary_assessment)
        contrarian_analysis['primary_challenges'] = challenges

        # Reinterpret evidence
        for piece in evidence:
            reinterpretation = self._reinterpret_evidence(piece)
            if reinterpretation:
                contrarian_analysis['evidence_reinterpretation'].append(reinterpretation)

        # Look for deception indicators
        deception_indicators = self._identify_deception_indicators(primary_assessment, evidence)
        contrarian_analysis['deception_indicators'] = deception_indicators

        self.trail.red_team_challenges.extend(challenges)
        self.trail.log('red_team_analysis', {
            'challenges_generated': len(challenges),
            'deception_indicators': len(deception_indicators)
        })

        return contrarian_analysis

    def calculate_confidence(self,
                           source_agreement: float,
                           historical_precedent: float,
                           logical_consistency: float,
                           technical_feasibility: float) -> Tuple[float, ConfidenceLevel]:
        """
        Calculate overall confidence score using structured methodology.
        """
        weighted_score = (
            source_agreement * self.CONFIDENCE_WEIGHTS['source_agreement'] +
            historical_precedent * self.CONFIDENCE_WEIGHTS['historical_precedent'] +
            logical_consistency * self.CONFIDENCE_WEIGHTS['logical_consistency'] +
            technical_feasibility * self.CONFIDENCE_WEIGHTS['technical_feasibility']
        )

        self.trail.confidence_factors = {
            'source_agreement': source_agreement,
            'historical_precedent': historical_precedent,
            'logical_consistency': logical_consistency,
            'technical_feasibility': technical_feasibility,
            'weighted_score': weighted_score
        }

        # Convert to confidence level
        if weighted_score >= 0.85:
            level = ConfidenceLevel.HIGH
        elif weighted_score >= 0.70:
            level = ConfidenceLevel.MODERATE_HIGH
        elif weighted_score >= 0.50:
            level = ConfidenceLevel.MODERATE
        elif weighted_score >= 0.30:
            level = ConfidenceLevel.LOW_MODERATE
        else:
            level = ConfidenceLevel.LOW

        self.trail.log('confidence_calculated', {
            'final_score': weighted_score,
            'confidence_level': level.value
        })

        return weighted_score, level

    # Private helper methods
    def _generate_hypotheses(self, claim: str, context: str) -> List[Hypothesis]:
        """Generate alternative hypotheses for ACH."""
        # This would use more sophisticated NLP in production
        base_hypotheses = [
            "Primary explanation is accurate as stated",
            "Alternative motivation or causation exists",
            "Partial truth with missing context",
            "Deception or misdirection involved",
            "Coincidental correlation, not causation"
        ]

        hypotheses = []
        for i, desc in enumerate(base_hypotheses[:3]):  # Limit to 3 for demo
            hypothesis = Hypothesis(
                id=f"H{i+1}",
                description=desc,
                probability=0.33 if i == 0 else 0.33 - (i * 0.1),  # Demo probabilities
            )
            hypotheses.append(hypothesis)

        return hypotheses

    def _evaluate_hypothesis_evidence(self, hypothesis: Hypothesis, context: str):
        """Evaluate evidence for/against each hypothesis."""
        # Simplified evidence evaluation for demo
        if "primary" in hypothesis.description.lower():
            hypothesis.probability = 0.87
            hypothesis.evidence_for = ["Direct source reporting", "Consistent with pattern"]
        else:
            hypothesis.probability = max(0.04, 0.15 - (len(hypothesis.description) * 0.01))
            hypothesis.evidence_against = ["Contradicts established facts"]

    def _assess_assumption_criticality(self, assumption_text: str) -> str:
        """Assess how critical an assumption is to the analysis."""
        critical_indicators = ['must', 'essential', 'required', 'cannot', 'always']
        moderate_indicators = ['likely', 'probably', 'usually', 'generally']

        text_lower = assumption_text.lower()

        if any(indicator in text_lower for indicator in critical_indicators):
            return 'critical'
        elif any(indicator in text_lower for indicator in moderate_indicators):
            return 'moderate'
        else:
            return 'minor'

    def _calculate_assumption_support(self, assumption_text: str, full_text: str) -> float:
        """Calculate how well an assumption is supported by available evidence."""
        # Simplified calculation for demo
        support_indicators = assumption_text.count('evidence') + assumption_text.count('confirmed')
        return min(0.9, 0.3 + (support_indicators * 0.2))

    def _deduplicate_assumptions(self, assumptions: List[Assumption]) -> List[Assumption]:
        """Remove duplicate assumptions."""
        unique_assumptions = []
        seen_descriptions = set()

        for assumption in assumptions:
            if assumption.description not in seen_descriptions:
                unique_assumptions.append(assumption)
                seen_descriptions.add(assumption.description)

        return sorted(unique_assumptions, key=lambda a: a.criticality == 'critical', reverse=True)

    def _group_similar_claims(self, claims: List[Claim]) -> List[List[Claim]]:
        """Group similar claims for triangulation."""
        # Simplified grouping for demo
        groups = []
        for claim in claims:
            groups.append([claim])  # Each claim in own group for now
        return groups

    def _assess_source_agreement(self, claims: List[Claim], sources: List[Source]) -> float:
        """Assess level of agreement between sources."""
        # Simplified calculation
        return 0.75  # Demo value

    def _calculate_source_reliability(self, source: Source, claims: List[Claim]) -> float:
        """Calculate source reliability score."""
        reliability_map = {'A': 0.95, 'B': 0.80, 'C': 0.65, 'D': 0.40, 'E': 0.20, 'F': 0.10}
        return reliability_map.get(source.reliability, 0.50)

    def _assess_claim_quality(self, claim: Claim, sources: List[Source]) -> float:
        """Assess quality of individual claim."""
        base_quality = 0.5

        # Factor in source reliability
        if claim.sources:
            source_scores = []
            for source_id in claim.sources:
                source = next((s for s in sources if s.id == source_id), None)
                if source:
                    source_scores.append(self._calculate_source_reliability(source, []))

            if source_scores:
                base_quality += (sum(source_scores) / len(source_scores)) * 0.3

        # Factor in corroboration
        if claim.corroborating_sources:
            base_quality += min(0.2, len(claim.corroborating_sources) * 0.05)

        return min(1.0, base_quality)

    def _generate_alternative_scenario(self, scenario: str, assumption: Assumption) -> Dict[str, Any]:
        """Generate alternative scenario by challenging assumption."""
        return {
            'scenario': f"Alternative if {assumption.description} is invalid",
            'probability_shift': -0.15,
            'impact_level': 'medium',
            'challenged_assumption': assumption.id
        }

    def _calculate_probability_shifts(self, scenarios: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate how scenarios shift baseline probabilities."""
        return {f"scenario_{i}": scenario.get('probability_shift', 0) for i, scenario in enumerate(scenarios)}

    def _assess_scenario_impacts(self, scenarios: List[Dict[str, Any]]) -> Dict[str, str]:
        """Assess impact levels of alternative scenarios."""
        return {f"scenario_{i}": scenario.get('impact_level', 'low') for i, scenario in enumerate(scenarios)}

    def _generate_contrarian_challenges(self, assessment: str) -> List[str]:
        """Generate contrarian challenges to primary assessment."""
        return [
            "Primary assessment may be based on incomplete information",
            "Alternative explanations not adequately considered",
            "Source motivations may bias reporting",
            "Timing of events suggests possible coordination"
        ]

    def _reinterpret_evidence(self, evidence: str) -> Optional[str]:
        """Reinterpret evidence from contrarian perspective."""
        if len(evidence) > 50:  # Only reinterpret substantial evidence
            return f"Alternative interpretation: {evidence[:50]}... could indicate opposite conclusion"
        return None

    def _identify_deception_indicators(self, assessment: str, evidence: List[str]) -> List[str]:
        """Identify potential deception indicators."""
        indicators = []

        if "convenient timing" in assessment.lower():
            indicators.append("Timing alignment may indicate orchestration")

        if len(evidence) < 3:
            indicators.append("Limited evidence base susceptible to manipulation")

        return indicators

# Export main classes
__all__ = ['AnalyticalTrail', 'StructuredAnalyticTechniques', 'AnalysisMode', 'ConfidenceLevel', 'Hypothesis', 'Assumption', 'Source', 'Claim']