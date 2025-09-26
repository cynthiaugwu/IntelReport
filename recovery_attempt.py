"""
Polished Streamlit demo app for IntelliReport - Intelligence Report Structuring
Part of the IJEOMA Safety Platform
"""

import streamlit as st
import os
import json
import base64
from pathlib import Path
import sys
import time
from typing import Dict, Any, Optional

# Add the parent directory to the path to import intellireport
sys.path.append(str(Path(__file__).parent.parent))

try:
    from intellireport import ReportProcessor
    from intellireport.schemas import ToneType
    from intellireport.redactor import RedactionLevel
    from intellireport.analytical_engine import AnalyticalTrail, StructuredAnalyticTechniques
    from intellireport.synthesis_engine import MultiSourceSynthesis
except ImportError as e:
    st.error(f"Failed to import IntelliReport: {e}")
    st.stop()


# Page configuration
st.set_page_config(
    page_title="IntelliReport - Intelligence Report Structuring",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Dark Theme CSS
st.markdown("""
<style>
    /* Professional Dark Theme */
    .stApp {
        background: linear-gradient(135deg, #0A1628 0%, #1A2332 100%);
        color: #ffffff;
    }

    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #0A1628 0%, #1A2332 100%);
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 15px 15px;
        color: white;
        border: 1px solid rgba(255, 183, 0, 0.2);
    }

    .main-header h1 {
        color: #FFB700 !important;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        font-weight: 700;
    }

    .main-header p {
        color: #E2E8F0 !important;
        font-size: 1.2rem;
        margin: 0;
        font-weight: 300;
    }

    /* Input areas */
    .stTextArea > div > div > textarea {
        background: #2d3748;
        color: #ffffff;
        border: 1px solid rgba(255, 183, 0, 0.3);
        border-radius: 8px;
    }

    .stTextInput > div > div > input {
        background: #2d3748;
        color: #ffffff;
        border: 1px solid rgba(255, 183, 0, 0.3);
        border-radius: 8px;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(45deg, #FFB700 0%, #FFA000 100%);
        color: #1a1a1a;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background: linear-gradient(45deg, #FFA000 0%, #FF8F00 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 183, 0, 0.3);
    }

    /* Selectbox */
    .stSelectbox > div > div {
        background: #2d3748;
        border: 1px solid rgba(255, 183, 0, 0.3);
        border-radius: 8px;
        color: #ffffff;
    }

    /* Sidebar */
    .css-1d391kg {
        background: #1a2332;
    }

    /* Metric containers */
    [data-testid='metric-container'] {
        background: linear-gradient(135deg, #1a2332 0%, #2d3748 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        color: #ffffff;
    }

    [data-testid='metric-container'] > div {
        color: #ffffff !important;
    }

    [data-testid='metric-container'] [data-testid='metric-value'] {
        color: #FFB700 !important;
        font-weight: 700;
    }

    .sidebar .sidebar-content {
        background: #f8f9fa;
    }

    .stAlert > div {
        border-radius: 10px;
    }

    .success-box {
        padding: 1rem;
        background: linear-gradient(135deg, #00c851 0%, #007e33 100%);
        color: white;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
    }

    .error-box {
        padding: 1rem;
        background: linear-gradient(135deg, #ff4444 0%, #cc0000 100%);
        color: white;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
    }

    .warning-box {
        padding: 1rem;
        background: linear-gradient(135deg, #ffbb33 0%, #ff8800 100%);
        color: white;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
    }

    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #1e3c72;
        margin: 0.5rem 0;
    }

    .stDownloadButton > button {
        width: 100%;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        margin: 0.25rem 0;
    }

    .copy-button {
        background: #28a745;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.25rem 0.5rem;
        cursor: pointer;
        font-size: 0.8rem;
        margin-left: 0.5rem;
    }

    .example-card {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.2s;
    }

    .example-card:hover {
        background: #e9ecef;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)


def get_example_reports() -> Dict[str, Dict[str, str]]:
    """Get example reports for the demo."""
    return {
        "🔒 Cybersecurity Incident": {
            "title": "Critical Security Breach Report",
            "content": """INCIDENT REPORT - CRITICAL

Incident ID: INC-2024-0156
Date/Time: March 22, 2024, 09:30 UTC
Reporter: Sarah Chen, Senior Security Analyst
Classification: CONFIDENTIAL

EXECUTIVE SUMMARY:
Critical security breach detected in the customer portal system at 09:15 UTC.
Unauthorized access to customer database containing approximately 15,000 records.
Immediate containment measures implemented. No confirmed data exfiltration at this time.

TIMELINE:
09:15 - Automated security alert triggered
09:20 - SOC analyst began investigation
09:25 - Confirmed unauthorized access, escalated to CISO
09:30 - System isolated, incident response team activated
10:00 - External forensics team notified
10:30 - Customer notification prepared

AFFECTED SYSTEMS:
- Customer portal (portal.company.com)
- Customer database server (DB-PROD-01)
- Payment processing gateway (limited exposure)

IMPACT ASSESSMENT:
- 15,000 customer records potentially accessed
- Financial data: Credit card numbers (encrypted)
- Personal data: Names, addresses, phone numbers
- No social security numbers in accessed dataset

IMMEDIATE ACTIONS TAKEN:
1. Isolated affected systems from network
2. Preserved forensic evidence
3. Reset all administrative credentials
4. Implemented additional monitoring
5. Blocked suspicious IP addresses: 203.45.67.89, 198.51.100.12

RECOMMENDATIONS:
1. Complete forensic analysis within 48 hours
2. Notify affected customers within 72 hours
3. File breach notification with regulatory authorities
4. Implement multi-factor authentication for all admin accounts
5. Conduct security assessment of all customer-facing systems

CONTACT:
Incident Commander: Sarah Chen (sarah.chen@company.com)
CISO: Michael Rodriguez (michael.rodriguez@company.com)
Legal Counsel: Jennifer Wong (jennifer.wong@lawfirm.com)

CLASSIFICATION: CONFIDENTIAL - HANDLE ACCORDING TO DATA BREACH PROTOCOLS"""
        },

        "🏥 Humanitarian Crisis": {
            "title": "Emergency Needs Assessment - Disaster Response",
            "content": """HUMANITARIAN NEEDS ASSESSMENT

Location: Coastal Region, Province X
Date: March 22, 2024
Assessment Team: Emergency Response Unit Alpha
Report by: Dr. Maria Santos, Field Coordinator

SITUATION OVERVIEW:
Category 4 hurricane made landfall 72 hours ago causing widespread destruction
across coastal communities. Estimated 45,000 people directly affected with
immediate humanitarian needs. Access partially restored to affected areas.

AFFECTED POPULATION:
- Total affected: 45,000 people
- Displaced persons: 12,000 (in 15 temporary shelters)
- Children under 18: 13,500 (30% of affected population)
- Elderly (65+): 4,500 (10% of affected population)
- Persons with disabilities: 2,250 (5% of affected population)

CRITICAL NEEDS ASSESSMENT:
1. SHELTER: 3,000 families require emergency shelter
2. WATER: 60% of water systems damaged, 27,000 people without clean water
3. FOOD: Emergency food supplies needed for 45,000 people for minimum 14 days
4. MEDICAL: 2 hospitals damaged, 5 health centers non-functional
5. PROTECTION: 1,200 unaccompanied minors identified

INFRASTRUCTURE DAMAGE:
- Main coastal road: 70% impassable
- Bridges: 3 of 7 major bridges damaged/destroyed
- Schools: 12 of 18 schools damaged
- Health facilities: 7 of 10 facilities damaged
- Water treatment plants: 2 of 3 non-functional

IMMEDIATE PRIORITIES:
1. Emergency shelter for 3,000 families (within 48 hours)
2. Water purification systems for 27,000 people (within 24 hours)
3. Medical supplies and temporary clinics (within 12 hours)
4. Food distribution network establishment (within 36 hours)
5. Family reunification services for unaccompanied minors

OPERATIONAL CONSTRAINTS:
- Limited helicopter landing zones (only 2 suitable sites)
- Fuel shortage affecting generator operations
- Communication networks 40% functional
- Security concerns in coastal zones due to debris

RESOURCE REQUIREMENTS:
- Emergency shelters: 3,000 family tents, 15,000 blankets
- Water: 10 water purification units, 50,000 liters bottled water daily
- Food: 675,000 ready-to-eat meals for 2 weeks
- Medical: 3 mobile medical units, surgical supplies
- Personnel: 50 additional humanitarian workers

COORDINATION:
Government disaster agency established joint operations center.
UN agencies coordinating response. NGO partners: Red Cross, Doctors Without Borders,
World Vision. Military providing logistics support.

NEXT STEPS:
1. Deploy additional assessment teams to remote villages
2. Establish supply chain from regional hub
3. Set up family tracing and reunification services
4. Begin early recovery planning for infrastructure

Contact: Dr. Maria Santos (+123-456-7890)
Coordination Hub: Emergency Operations Center, Regional Capital"""
        },

        "💼 Market Intelligence": {
            "title": "Competitive Market Analysis - Tech Sector",
            "content": """CONFIDENTIAL MARKET INTELLIGENCE REPORT

Subject: Competitive Analysis - AI Software Market Entry
Date: March 22, 2024
Analyst: Jennifer Park, Senior Market Analyst
Distribution: Executive Leadership Team

EXECUTIVE SUMMARY:
Analysis indicates strong market opportunity for AI-powered document processing
solutions with projected 35% CAGR through 2027. Key competitor weaknesses identified
in enterprise integration and pricing flexibility. Recommended market entry
within Q3 2024 to capture first-mover advantage in mid-market segment.

MARKET OVERVIEW:
- Total Addressable Market: $2.4B (2024), projected $6.1B (2027)
- Serviceable Available Market: $850M focusing on enterprise segment
- Current market leaders: TechCorp (22%), DataSoft (18%), AIVendor (15%)
- Market growth drivers: Digital transformation, regulatory compliance, cost reduction

KEY FINDINGS:
1. COMPETITIVE LANDSCAPE:
   - Market fragmented with no dominant player >25% share
   - Legacy vendors struggling with cloud-native solutions
   - New entrants gaining traction in specific verticals

2. CUSTOMER INSIGHTS:
   - 73% of enterprises plan AI document processing investment in next 18 months
   - Primary pain points: Integration complexity (68%), accuracy concerns (54%)
   - Budget allocation: $50K-$500K for mid-market, $1M+ for enterprise

3. TECHNOLOGY TRENDS:
   - Multi-modal AI processing becoming standard
   - On-premise deployment still required for 45% of enterprise customers
   - API-first architecture increasingly important

COMPETITIVE ANALYSIS:
TechCorp: Market leader, strong brand, weak in mid-market pricing
DataSoft: Good enterprise relationships, outdated technology stack
AIVendor: Innovative features, poor customer support, limited integrations
StartupAI: Strong technical team, limited enterprise sales capability

MARKET OPPORTUNITY:
- Underserved mid-market segment (100-1000 employees)
- Geographic expansion opportunity in EMEA region
- Vertical specialization in financial services and healthcare
- Partnership opportunities with systems integrators

COMPETITIVE ADVANTAGES:
1. Superior accuracy through advanced AI models
2. Flexible deployment options (cloud, on-premise, hybrid)
3. Competitive pricing for mid-market segment
4. Strong integration ecosystem

RISKS AND CHALLENGES:
- Intense competition from well-funded startups
- Potential regulatory changes affecting AI software
- Customer concerns about data privacy and security
- Technical talent shortage for scaling development

FINANCIAL PROJECTIONS:
Year 1: $2.5M revenue (1% market share)
Year 2: $8.2M revenue (2.5% market share)
Year 3: $18.5M revenue (4.1% market share)
Break-even: Month 18
Required investment: $15M over 3 years

RECOMMENDATIONS:
1. Enter market with mid-market focus Q3 2024
2. Develop partnerships with 3 major systems integrators
3. Establish European sales office by Q1 2025
4. Invest in healthcare and financial services vertical solutions
5. Build customer success team to ensure retention >90%

NEXT STEPS:
1. Conduct customer interviews with 20 target prospects
2. Develop pricing strategy and packaging options
3. Create go-to-market plan with sales and marketing
4. Evaluate potential acquisition targets
5. Secure Series B funding to support market entry

Contact: Jennifer Park (jennifer.park@company.com)
Classification: CONFIDENTIAL - BUSINESS STRATEGY"""
        },

        "🏛️ Government Intelligence": {
            "title": "Intelligence Assessment - Regional Security",
            "content": """INTELLIGENCE ASSESSMENT

Classification: SECRET//NOFORN
Subject: Regional Security Assessment - Eastern Border Region
Date: 22 March 2024
Originator: Regional Intelligence Center
Dissemination: Senior Policy Officials

BOTTOM LINE UP FRONT:
Increased military activity observed along eastern border indicates possible
preparations for expanded regional operations. Assessment confidence: MODERATE.
Recommend enhanced monitoring and diplomatic engagement to prevent escalation.

SITUATION ASSESSMENT:
Intelligence reporting indicates significant increase in military preparations
along the eastern border region over the past 30 days. Activity patterns
suggest potential for expanded operations rather than routine exercises.

KEY DEVELOPMENTS:
1. MILITARY BUILDUP:
   - 15,000 additional personnel deployed to border region
   - 3 armored divisions repositioned within 50km of border
   - Establishment of 2 new forward operating bases
   - Increased logistics activity supporting sustained operations

2. COMMUNICATIONS INTERCEPTS:
   - 40% increase in encrypted military communications
   - References to "Operation Sentinel" in intercepted traffic
   - Coordination meetings involving senior military leadership
   - Discussion of "contingency timeline" in signals intelligence

3. DIPLOMATIC INDICATORS:
   - Reduction in bilateral diplomatic engagements
   - Formal complaints filed regarding border incidents
   - Ambassador recalled for "consultations"
   - Suspension of joint border patrol agreements

INTELLIGENCE GAPS:
- Specific operational timeline remains unclear
- Objective scope and geographic extent unknown
- Political decision-making process not well understood
- International coordination efforts require further assessment

ANALYTICAL ASSESSMENT:
We assess with MODERATE confidence that observed military preparations
indicate planning for potential expanded operations. This assessment is
based on the scale and nature of military deployments, communications
patterns, and diplomatic developments.

Alternative explanation: Enhanced defensive posture in response to
perceived security threats. This possibility cannot be ruled out
given regional tensions and historical threat perceptions.

IMPLICATIONS:
- Potential for regional instability and humanitarian crisis
- Risk of broader international involvement
- Economic disruption to trade routes and energy supplies
- Refugee movements affecting neighboring countries

COLLECTION REQUIREMENTS:
1. Political leadership intentions and decision timeline
2. Military operational plans and capability assessments
3. International diplomatic coordination efforts
4. Economic preparations for sustained operations

RECOMMENDATIONS:
1. Increase diplomatic engagement through back-channel communications
2. Coordinate intelligence sharing with regional allies
3. Enhance monitoring of military and political indicators
4. Prepare contingency plans for multiple scenarios
5. Brief senior policymakers on assessment and implications

CONFIDENCE ASSESSMENTS:
- Military buildup: HIGH confidence
- Operational intent: MODERATE confidence
- Timeline assessment: LOW confidence
- International dimensions: MODERATE confidence

SOURCES:
Multiple intelligence disciplines contributed to this assessment including
signals intelligence, human intelligence, and imagery analysis. Source
reliability and information credibility vary by reporting stream.

NEXT UPDATE: 29 March 2024 (weekly assessment cycle)

Classification: SECRET//NOFORN
Prepared by: Regional Intelligence Center
Distribution: As directed by intelligence oversight"""
        }
    }


def copy_to_clipboard_button(text: str, key: str, label: str = "📋 Copy"):
    """Create a copy to clipboard button."""
    if st.button(label, key=f"copy_{key}", help="Copy to clipboard"):
        st.write(f"```\n{text}\n```")
        st.success("Content ready to copy! Select the text above and use Ctrl+C (Cmd+C on Mac)")


def create_download_button(content: str, filename: str, mime_type: str, label: str):
    """Create a download button for content."""
    return st.download_button(
        label=label,
        data=content,
        file_name=filename,
        mime=mime_type,
        use_container_width=True
    )


def display_metrics(result):
    """Display processing metrics in an attractive format."""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>⏱️ Processing Time</h4>
            <h2>{:.1f}s</h2>
        </div>
        """.format((result.processing_time_ms or 0) / 1000), unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4>🎯 Confidence</h4>
            <h2>{:.1%}</h2>
        </div>
        """.format(result.data.standard_report.confidence_score if result.data.standard_report else 0), unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
            <h4>📊 Tokens Used</h4>
            <h2>{:,}</h2>
        </div>
        """.format(result.tokens_used or 0), unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="metric-card">
            <h4>✅ Success</h4>
            <h2>{}</h2>
        </div>
        """.format("Yes" if result.success else "No"), unsafe_allow_html=True)


def main():
    """Main Streamlit application."""

    # Header
    st.markdown("""
    <div class="main-header">
        <h1><strong>IntelliReport</strong></h1>
        <p>Structured Intelligence Report • Part of the Ijeoma Safety App</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar Configuration
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")

        # API Key Input
        api_key = st.text_input(
            "🔑 Anthropic API Key",
            type="password",
            help="Enter your Anthropic API key or set ANTHROPIC_API_KEY environment variable",
            value=os.getenv("ANTHROPIC_API_KEY", "")
        )

        st.markdown("---")

        # Tone Selection
        st.markdown("### 🎭 Analysis Tone")
        tone_options = {
            "🏛️ Professional/Government": ToneType.PROFESSIONAL,
            "🏢 Corporate/Business": ToneType.CORPORATE,
            "🌍 NGO/Humanitarian": ToneType.NGO
        }

        selected_tone = st.selectbox(
            "Select analysis perspective:",
            options=list(tone_options.keys()),
            index=0,
            help="Choose the analytical perspective for report processing"
        )
        tone = tone_options[selected_tone]

        st.markdown("---")

        # Redaction Settings
        st.markdown("### 🔒 Privacy & Redaction")
        enable_redaction = st.toggle(
            "Enable PII Redaction",
            value=False,
            help="Automatically redact personally identifiable information"
        )

        if enable_redaction:
            redaction_levels = {
                "🟢 Low (SSN, Credit Cards only)": RedactionLevel.LOW,
                "🟡 Medium (+ Names, Emails, Phones)": RedactionLevel.MEDIUM,
                "🟠 High (+ Addresses, Organizations)": RedactionLevel.HIGH,
                "🔴 Maximum (All sensitive data)": RedactionLevel.MAXIMUM
            }

            selected_level = st.selectbox(
                "Redaction Level:",
                options=list(redaction_levels.keys()),
                index=1
            )
            redaction_level = redaction_levels[selected_level]
        else:
            redaction_level = RedactionLevel.NONE

        st.markdown("---")

        # Example Reports
        st.markdown("### 📄 Example Reports")
        st.markdown("*Click to load an example:*")

        examples = get_example_reports()

        for emoji_title, example in examples.items():
            if st.button(
                emoji_title,
                help=f"Load: {example['title']}",
                use_container_width=True,
                key=f"example_{emoji_title}"
            ):
                st.session_state.example_text = example['content']
                st.rerun()

    # Main Content Area
    st.markdown("### 📝 Report Input")

    # Text area for report input
    report_text = st.text_area(
        "Enter your report text:",
        height=400,
        placeholder="Paste your report text here or load an example from the sidebar...",
        value=st.session_state.get('example_text', ''),
        help="Enter the report text you want to analyze and structure"
    )

    # Clear example text after it's been loaded
    if 'example_text' in st.session_state:
        del st.session_state.example_text

    # Process Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        process_button = st.button(
            "🚀 Process Report",
            type="primary",
            use_container_width=True,
            disabled=not report_text.strip()
        )

    # Processing and Results
    if process_button:
        if not report_text.strip():
            st.error("❌ Please enter some report text to analyze.")
            return

        if not api_key and not os.getenv("ANTHROPIC_API_KEY"):
            st.error("❌ Please provide an Anthropic API key in the sidebar or set the ANTHROPIC_API_KEY environment variable.")
            return

        # Processing with spinner
        with st.spinner("🔄 Processing report with AI... This may take a few moments."):
            try:
                # Initialize processor
                processor = ReportProcessor(
                    api_key=api_key if api_key else None,
                    tone=tone
                )

                # Process the report
                start_time = time.time()
                result = processor.process(
                    text=report_text,
                    tone=tone,
                    output_format="json",
                    extract_entities=True,
                    analyze_missing_fields=True,
                    redact_pii=enable_redaction,
                    redaction_level=redaction_level
                )
                processing_time = time.time() - start_time

                # Success message
                if result.success:
                    st.markdown("""
                    <div class="success-box">
                        ✅ Report processed successfully!
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="warning-box">
                        ⚠️ Report processed with some issues. Check the details below.
                    </div>
                    """, unsafe_allow_html=True)

                # Display metrics
                st.markdown("### 📊 Processing Metrics")
                display_metrics(result)

                # Show errors and warnings if any
                if result.errors:
                    st.markdown("### ❌ Errors")
                    for error in result.errors:
                        st.error(error)

                if result.warnings:
                    st.markdown("### ⚠️ Warnings")
                    for warning in result.warnings:
                        st.warning(warning)

                # Results in tabs
                st.markdown("### 📋 Results")

                tab1, tab2, tab3 = st.tabs(["📊 Structured JSON", "📝 Formatted Report", "🔍 Analysis & Gaps"])

                with tab1:
                    st.markdown("#### Structured Data Output")

                    if result.data.standard_report:
                        # Format the JSON nicely
                        json_output = json.dumps(
                            result.data.standard_report.dict(exclude_none=True),
                            indent=2,
                            default=str
                        )

                        st.code(json_output, language="json")

                        # Download and copy buttons
                        col1, col2 = st.columns(2)
                        with col1:
                            create_download_button(
                                json_output,
                                "intellireport_structured.json",
                                "application/json",
                                "💾 Download JSON"
                            )
                        with col2:
                            copy_to_clipboard_button(json_output, "json", "📋 Copy JSON")
                    else:
                        st.error("❌ Failed to extract structured report data.")

                with tab2:
                    st.markdown("#### Formatted Report")

                    if result.data.standard_report:
                        # Generate markdown format
                        from intellireport.formatters import OutputFormatter
                        formatter = OutputFormatter()
                        markdown_output = formatter.format_markdown(
                            result.data.standard_report,
                            include_classification=True,
                            include_metadata_table=True
                        )

                        # Display markdown
                        st.markdown(markdown_output)

                        # Download and copy buttons
                        col1, col2 = st.columns(2)
                        with col1:
                            create_download_button(
                                markdown_output,
                                "intellireport_formatted.md",
                                "text/markdown",
                                "💾 Download Markdown"
                            )
                        with col2:
                            copy_to_clipboard_button(markdown_output, "markdown", "📋 Copy Markdown")
                    else:
                        st.error("❌ Failed to generate formatted report.")

                with tab3:
                    st.markdown("#### Analysis Quality & Missing Fields")

                    # Entity extraction results
                    if result.data.extracted_entities:
                        st.markdown("##### 🏷️ Extracted Entities")
                        entities = result.data.extracted_entities

                        col1, col2 = st.columns(2)
                        with col1:
                            if entities.people:
                                st.markdown("**👤 People:**")
                                for person in entities.people:
                                    st.write(f"• {person}")

                            if entities.organizations:
                                st.markdown("**🏢 Organizations:**")
                                for org in entities.organizations:
                                    st.write(f"• {org}")

                        with col2:
                            if entities.locations:
                                st.markdown("**📍 Locations:**")
                                for location in entities.locations:
                                    st.write(f"• {location}")

                            if entities.dates:
                                st.markdown("**📅 Dates:**")
                                for date in entities.dates[:5]:  # Limit to 5
                                    st.write(f"• {date}")

                    # Missing fields analysis
                    if result.data.missing_fields:
                        st.markdown("##### 🔍 Missing Fields Analysis")
                        missing = result.data.missing_fields

                        if missing.missing_fields:
                            st.markdown("**❌ Missing Critical Fields:**")
                            for field in missing.missing_fields:
                                st.write(f"• {field}")

                        if missing.confidence_issues:
                            st.markdown("**⚠️ Low Confidence Fields:**")
                            for issue in missing.confidence_issues:
                                st.write(f"• {issue}")

                        if missing.suggestions:
                            st.markdown("**💡 Improvement Suggestions:**")
                            for suggestion in missing.suggestions:
                                st.write(f"• {suggestion}")

                    # Redaction summary if redaction was enabled
                    if enable_redaction and result.data.redacted_entities:
                        st.markdown("##### 🔒 Redaction Summary")
                        redacted_count = len(result.data.redacted_entities)
                        st.info(f"🔒 Redacted {redacted_count} sensitive entities")

                        # Group by entity type
                        type_counts = {}
                        for entity in result.data.redacted_entities:
                            entity_type = entity.entity_type
                            type_counts[entity_type] = type_counts.get(entity_type, 0) + 1

                        for entity_type, count in type_counts.items():
                            st.write(f"• {entity_type}: {count} items")

            except Exception as e:
                st.markdown(f"""
                <div class="error-box">
                    ❌ Error processing report: {str(e)}
                </div>
                """, unsafe_allow_html=True)

                st.markdown("### 🔧 Troubleshooting Tips")
                st.info("""
                **Common issues and solutions:**

                1. **API Key Issues**: Make sure your Anthropic API key is valid and has sufficient credits
                2. **Text Length**: Very long texts may timeout - try shorter excerpts
                3. **Network Issues**: Check your internet connection
                4. **Rate Limits**: If you get rate limit errors, wait a few minutes and try again

                **Need help?** Check the [IntelliReport documentation](https://github.com/yourusername/intellireport) for more information.
                """)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9em; padding: 2rem 0;">
        <p>
            🔍 <strong>IntelliReport</strong> - Part of the IJEOMA Safety Platform<br>
            Built with ❤️ using <a href="https://streamlit.io" target="_blank">Streamlit</a>
            and <a href="https://www.anthropic.com" target="_blank">Anthropic Claude</a>
        </p>
        <p style="font-size: 0.8em; margin-top: 1rem;">
            <em>For support and documentation, visit our GitHub repository</em>
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()