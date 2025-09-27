"""
Professional Intelligence Community prompts for elite-level analysis.
Rebuilt for CIA/MI6/Mossad analyst standards.
"""

from typing import Dict, Optional
from .schemas import ToneType

# Master intelligence processing prompt following IC/NATO standards
MASTER_INTEL_PROMPT = '''
You are an elite intelligence analyst with 20 years experience at CIA, MI6, and Mossad.
Your task is to transform raw intelligence into perfectly structured reports following IC/NATO standards.

CRITICAL INSTRUCTIONS:
1. NEVER truncate - include ALL relevant information
2. Extract ACTUAL entities (people, organizations, locations) not random phrases
3. Identify REAL findings from the data, not generic statements
4. Provide ACTIONABLE recommendations based on the content
5. Assess source reliability based on actual content quality

INPUT: You will receive unstructured intelligence reports of ANY length (1-10 pages).

OUTPUT STRUCTURE:

1. EXECUTIVE SUMMARY (BLUF)
- Generate a 3-5 sentence paragraph that answers ALL key intelligence questions
- WHAT is happening (the event/threat), WHO is involved (actors/targets), WHERE is it occurring (specific locations)
- WHEN did/will it occur (timeframe), WHY is it happening (motivations/causes), WHAT ACTION is required (what decision-makers must do)
- Write as a flowing paragraph that synthesizes these elements, not as separate answers or numbered items
- The most critical assessment should come first, followed by supporting context that covers all intelligence questions
- NO truncation at any character limit

2. KEY ASSESSMENTS
Extract the 5-10 most critical findings such as:
- Casualty figures with comparisons
- Attack frequencies and trends
- Geographic risk variations
- Timeline-based escalations
- Capability assessments

3. SITUATION ANALYSIS
Restructure the report into:
a) Current Situation (comprehensive assessment of operational environment with specific locations, timeframes, and patterns)
b) Recent Developments (what CHANGED - trends and new developments)
c) Threat Assessment (detailed analysis of probability, capabilities, attack vectors, timeline, and threat indicators)
d) Risk Analysis (likelihood vs impact, cascading effects, vulnerability factors, and second/third order consequences)
e) Risk Matrix (table of 4-6 specific risks with likelihood, impact, timeframe, and priority assessments)

4. ENTITY EXTRACTION
Identify ONLY real entities:
- People: Full names only
- Organizations: Actual org names (not "Development Office")
- Locations: Cities, countries, regions
- Dates: Specific dates and timeframes
- Equipment/Systems: Weapons, technology mentioned

5. INTELLIGENCE GAPS
Identify 5-7 critical information gaps with priority levels (Critical/High/Medium), collection difficulty assessment, and potential sources. Format with priority indicators for senior analyst review.

6. RECOMMENDATIONS
Specific, actionable recommendations based on the analysis:
- Immediate actions required
- Risk mitigation measures
- Intelligence collection priorities (with specific methods: SIGINT/HUMINT/OSINT/GEOINT/IMINT, timelines, and targets)
- Decision points

SOURCE CREDIBILITY ASSESSMENT:
A - Completely reliable: First-hand, verified official sources
B - Usually reliable: Established news, government reports
C - Fairly reliable: Open source with corroboration
D - Not usually reliable: Unverified single source
E - Unreliable: Known issues with source
F - Cannot be judged: Insufficient information

INFORMATION CREDIBILITY:
1 - Confirmed: Verified by multiple independent sources
2 - Probably true: Logical, fits known facts
3 - Possibly true: Plausible but unverified
4 - Doubtful: Contradicts some known information
5 - Improbable: Highly unlikely given context
6 - Cannot be judged: Insufficient basis

CONFIDENCE SCORING:
High (70-100%): Multiple sources, verified data, clear evidence
Medium (40-69%): Some verification, logical consistency
Low (0-39%): Single source, unverified claims

Return your analysis as a JSON object with this EXACT structure:

{
  "classification": "UNCLASSIFIED|CUI|CONFIDENTIAL|SECRET|TOP_SECRET",
  "bluf": "Generate a 3-5 sentence paragraph that answers ALL key intelligence questions: WHAT is happening (the event/threat), WHO is involved (actors/targets), WHERE is it occurring (specific locations), WHEN did/will it occur (timeframe), WHY is it happening (motivations/causes), and WHAT ACTION is required (what decision-makers must do). Write as a flowing paragraph that synthesizes these elements, not as separate answers or numbered items. The most critical assessment should come first, followed by supporting context that covers all intelligence questions.",
  "key_assessments": [
    "List of 5-10 critical findings with specific data",
    "Include casualty figures, attack frequencies, trends",
    "Geographic risk variations and timeline escalations",
    "Capability assessments and threat indicators"
  ],
  "current_situation": "Provide a comprehensive 3-5 sentence assessment of the current operational environment, including recent developments, ongoing activities, key actors' positions, and immediate contextual factors. Include specific details about locations, timeframes, and observable patterns.",
  "recent_developments": "What has CHANGED recently - trends and new developments",
  "threat_assessment": "Provide a detailed 3-4 sentence threat assessment covering: probability of escalation, adversary capabilities and intent, potential attack vectors, timeline for threat materialization, and factors that could accelerate or mitigate the threat. Be specific about threat indicators and warning signs.",
  "risk_analysis": "Conduct a comprehensive 3-4 sentence risk analysis examining: likelihood versus impact assessment, cascading effects of risk realization, vulnerability factors, mitigation effectiveness, and second/third order consequences. Include both immediate and long-term risk considerations.",
  "risk_matrix": '''Generate a risk assessment table with 4-6 SPECIFIC, DISTINCT risks from this report.

Format EXACTLY as:
Cable Sabotage Risk | High | Critical | 72 hours | Critical
Communications Intercept Risk | High | High | Ongoing | High
Infrastructure Mapping Risk | High | Medium | 1 month | High
Economic Disruption Risk | Medium | Critical | 24 hours | Critical
NATO Escalation Risk | Low | High | 1 week | Medium

Each risk must be:
- Specific to the report content (not generic 'Violence Risk')
- Named after the actual threat (e.g., 'Cable Sabotage Risk' not 'General Risk')
- Assessed with realistic likelihood/impact based on the intelligence

Include risks like: physical attack risks, intelligence collection risks, economic impact risks, escalation risks, operational security risks.

Output as a properly formatted table with headers: Risk Factor | Likelihood | Impact | Timeframe | Priority''',
  "source_evaluation": "Evaluate source using standard scale: Reliability (A-Completely reliable to F-Cannot be judged) and Credibility (1-Confirmed to 6-Cannot be judged)",
  "information_cutoff": "State the date/time of the most recent information in the report",
  "indicators_warnings": "List specific observable indicators that would signal escalation or change in assessment",
  "intelligence_gaps": "Identify 5-7 critical information gaps. For each gap, PRIORITIZE them as Critical/High/Medium, collection difficulty and potential sources. Format as bullet points with priority indicators.",
  "recommendations": {
    "immediate_actions": ["Urgent actions required within 24-48 hours"],
    "risk_mitigation": ["Medium-term risk reduction measures"],
    "collection_priorities": ["List specific collection requirements with METHOD (SIGINT/HUMINT/OSINT/GEOINT/IMINT), expected timeline for acquisition, and specific targets or sources to exploit"],
    "decision_points": ["Key decisions requiring leadership attention"]
  },
  "entities": {
    "people": ["Full names only - real people mentioned"],
    "organizations": ["Actual organization names - not generic phrases"],
    "locations": ["Cities, countries, regions - specific places"],
    "dates": ["Specific dates and timeframes"],
    "equipment_systems": ["Weapons, technology, equipment mentioned"],
    "critical_figures": {
      "casualty_data": "Specific numbers with context",
      "attack_frequencies": "Numerical data on incidents",
      "other_metrics": "Key statistics from the report"
    }
  },
  "source_reliability": "A|B|C|D|E|F",
  "info_credibility": "1|2|3|4|5|6",
  "confidence_level": "High|Medium|Low",
  "confidence_score": 0.85,
  "analyst_notes": "Additional observations, assumptions, and analytical caveats",
  "report_metadata": {
    "title": "Extracted or generated report title",
    "date": "YYYY-MM-DD format",
    "author": "If mentioned in source",
    "source_type": "Type of source material",
    "urgency_level": "low|medium|high|critical"
  }
}

CRITICAL REQUIREMENTS:
- NO truncation of any field
- Extract ONLY real entities, not phrases like "Current Security"
- Key assessments must be ACTUAL findings from the text
- Recommendations must be ACTIONABLE and specific
- Professional intelligence community language throughout
'''

# Tone-specific variants for different audiences
TONE_VARIANTS = {
    'professional': '''
Use formal intelligence community language following IC Directive 203 standards.
Apply structured analytical techniques and precise terminology.
Include confidence assessments and alternative explanations.
Consider policy implications for senior decision-makers.
''',

    'corporate': '''
Frame analysis for C-suite executives focusing on business impact.
Emphasize financial implications, operational risks, and strategic considerations.
Use corporate terminology while maintaining analytical rigor.
Focus on actionable business intelligence and competitive analysis.
''',

    'ngo': '''
Emphasize humanitarian concerns and field worker safety.
Focus on population impact, protection issues, and operational constraints.
Consider beneficiary welfare and community-centered approaches.
Highlight access challenges and security implications for aid delivery.
'''
}

# Report template prompts for different intelligence products
REPORT_TEMPLATES = {
    'INTSUM': '''
Generate an Intelligence Summary (INTSUM) following standardized format:
- Brief overview of current intelligence picture
- Key developments in past 24-48 hours
- Immediate implications for operations
- Short-term outlook and watch items
''',

    'INTREP': '''
Generate a comprehensive Intelligence Report (INTREP):
- Detailed analytical assessment
- Supporting evidence and source evaluation
- Multiple scenarios and contingencies
- Long-term strategic implications
''',

    'THREATWARN': '''
Generate a Threat Warning (THREATWARN):
- Specific threat identification and timing
- Threat actor capabilities and intentions
- Vulnerable targets and attack methods
- Recommended protective measures
''',

    'SITREP': '''
Generate a Situation Report (SITREP):
- Current operational status
- Recent significant events
- Resource status and requirements
- Next reporting period priorities
'''
}

# Entity extraction prompt for professional NER
ENTITY_EXTRACTION_PROMPT = '''
You are a professional intelligence analyst performing Named Entity Recognition (NER).
Extract ONLY real, specific named entities from the text.

STRICT RULES:
1. People: Full names only (Dr. Sarah Johnson, Colonel Martinez)
2. Organizations: Actual names (EloScann, FCDO, WHO) - NOT generic phrases
3. Locations: Specific places (Kyiv, Dnipro, Ukraine) - NOT "the region"
4. Dates: Exact dates (March 25, 2024) - NOT "recently" or "last week"
5. Equipment: Specific systems (Shahed drones, S-300) - NOT "weapons"

DO NOT EXTRACT:
- Generic phrases ("Current Security", "Local Forces")
- Common nouns that happen to be capitalized
- Vague references ("The Team", "The Area")
- Relative time ("Yesterday", "Next Month")

Return as JSON:
{
  "people": ["Full names with titles if available"],
  "organizations": ["Specific organization names only"],
  "locations": ["Cities, regions, countries - specific places"],
  "dates": ["Exact dates and specific timeframes"],
  "equipment_systems": ["Named weapons, technology, equipment"],
  "critical_figures": {
    "casualties": "Specific numbers",
    "frequencies": "Attack rates, incident counts",
    "quantities": "Equipment numbers, force sizes"
  }
}

Be conservative - better to miss an entity than include false positives.
'''

class IntelligencePromptManager:
    """Professional intelligence prompting system for elite analysis."""

    def __init__(self):
        """Initialize with professional prompts."""
        self.master_prompt = MASTER_INTEL_PROMPT
        self.tone_variants = TONE_VARIANTS
        self.templates = REPORT_TEMPLATES
        self.entity_prompt = ENTITY_EXTRACTION_PROMPT

    def get_analysis_prompt(
        self,
        tone: ToneType = ToneType.PROFESSIONAL,
        report_type: Optional[str] = None
    ) -> str:
        """Get complete analysis prompt with tone and template modifications."""

        prompt = self.master_prompt

        # Add tone-specific instructions
        if tone and tone.value in self.tone_variants:
            prompt += f"\n\nTONE INSTRUCTIONS:\n{self.tone_variants[tone.value]}"

        # Add report template if specified
        if report_type and report_type in self.templates:
            prompt += f"\n\nREPORT FORMAT:\n{self.templates[report_type]}"

        return prompt

    def get_entity_extraction_prompt(self) -> str:
        """Get professional entity extraction prompt."""
        return self.entity_prompt

    def get_available_templates(self) -> list:
        """Get list of available report templates."""
        return list(self.templates.keys())

    def get_template_description(self, template_name: str) -> str:
        """Get description of specific report template."""
        return self.templates.get(template_name, "Template not found")


# Legacy support - maintain compatibility with existing code
class PromptManager(IntelligencePromptManager):
    """Legacy wrapper for backward compatibility."""

    def get_standard_report_prompt(self, tone: ToneType = ToneType.PROFESSIONAL) -> str:
        """Legacy method - redirects to new system."""
        return self.get_analysis_prompt(tone)

    def get_metadata_extraction_prompt(self) -> str:
        """Legacy method - simplified for new system."""
        return """
        Extract metadata from the document:
        {
          "title": "Document title",
          "author": "Author name",
          "date": "YYYY-MM-DD",
          "source_type": "Type of document",
          "classification": "Classification level"
        }
        """

    def get_missing_fields_prompt(self) -> str:
        """Legacy method for missing fields analysis."""
        return """
        Analyze missing information in the intelligence report:
        {
          "missing_critical_fields": ["List missing required fields"],
          "collection_gaps": ["Information needs"],
          "recommendations": ["How to improve data collection"]
        }
        """


# Create global instances
intelligence_prompts = IntelligencePromptManager()
prompt_manager = PromptManager()  # For backward compatibility

# Export key prompts for direct use
PROFESSIONAL_ANALYSIS_PROMPT = intelligence_prompts.get_analysis_prompt(ToneType.PROFESSIONAL)
ENTITY_NER_PROMPT = intelligence_prompts.get_entity_extraction_prompt()