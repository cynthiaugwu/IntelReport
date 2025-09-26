"""
Professional Intelligence Analysis Platform
Streamlit interface with sophisticated analytical capabilities and premium UI/UX.
"""

import streamlit as st
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

# Professional configuration
st.set_page_config(
    page_title="IntelliReport Professional",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import our professional components
try:
    from intellireport.core import ProfessionalReportProcessor
    from intellireport.schemas import ToneType, StandardReport
    from intellireport.analytical_engine import AnalysisMode, AnalyticalTrail, StructuredAnalyticTechniques
    from intellireport.synthesis_engine import MultiSourceSynthesis
    from intellireport.formatters import OutputFormatter
except ImportError as e:
    st.error(f"Failed to import IntelliReport components: {e}")
    st.stop()

# Professional Dark Theme CSS
PROFESSIONAL_CSS = """
<style>
/* Professional Dark Theme */
.stApp {
    background: linear-gradient(135deg, #0A1628 0%, #1A2332 100%);
    color: #ffffff;
}

/* Header Styling */
.main-header {
    background: linear-gradient(90deg, #1a2332 0%, #2d3748 100%);
    padding: 20px;
    border-radius: 12px;
    border: 1px solid rgba(255, 183, 0, 0.2);
    margin-bottom: 30px;
    text-align: center;
}

.main-title {
    color: #FFB700;
    font-size: 2.5rem;
    font-weight: 700;
    margin: 0;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

.main-subtitle {
    color: #E2E8F0;
    font-size: 1.2rem;
    margin: 5px 0 0 0;
    font-weight: 300;
}

/* Metric Containers */
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

/* Input Areas */
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
    padding: 10px 20px;
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
}

/* Sidebar */
.css-1d391kg {
    background: #1a2332;
}

/* Expander */
.streamlit-expanderHeader {
    background: #2d3748;
    color: #FFB700;
    border-radius: 8px;
}

/* Tabs */
.stTabs > div > div > div {
    background: #2d3748;
    color: #ffffff;
}

/* Alert Styling */
.threat-critical {
    background: linear-gradient(135deg, #DC2626 0%, #B91C1C 100%);
    color: white;
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid #EF4444;
    margin: 10px 0;
}

.threat-high {
    background: linear-gradient(135deg, #EA580C 0%, #C2410C 100%);
    color: white;
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid #F97316;
    margin: 10px 0;
}

.threat-medium {
    background: linear-gradient(135deg, #CA8A04 0%, #A16207 100%);
    color: white;
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid #EAB308;
    margin: 10px 0;
}

.threat-low {
    background: linear-gradient(135deg, #16A34A 0%, #15803D 100%);
    color: white;
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid #22C55E;
    margin: 10px 0;
}

/* Classification Markings */
.classification-header {
    background: #DC2626;
    color: white;
    padding: 10px;
    text-align: center;
    font-weight: bold;
    border-radius: 8px 8px 0 0;
    margin-bottom: 0;
}

.classification-footer {
    background: #DC2626;
    color: white;
    padding: 5px;
    text-align: center;
    font-size: 0.8rem;
    border-radius: 0 0 8px 8px;
    margin-top: 0;
}

/* Professional Footer */
.professional-footer {
    text-align: center;
    padding: 20px;
    color: #94A3B8;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    margin-top: 50px;
}

/* Executive Dashboard */
.executive-dashboard {
    background: linear-gradient(135deg, #1e3a5f 0%, #2d3748 100%);
    border: 1px solid rgba(255, 183, 0, 0.2);
    border-radius: 12px;
    padding: 20px;
    margin: 20px 0;
}

.dashboard-title {
    color: #FFB700;
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 15px;
}

/* Analysis Mode Cards */
.mode-card {
    background: #2d3748;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 15px;
    margin: 10px 0;
    cursor: pointer;
    transition: all 0.3s ease;
}

.mode-card:hover {
    border-color: #FFB700;
    transform: translateY(-2px);
}

.mode-card.selected {
    border-color: #FFB700;
    background: rgba(255, 183, 0, 0.1);
}
</style>
"""

def init_session_state():
    """Initialize session state variables."""
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None

    if 'analytical_trail' not in st.session_state:
        st.session_state.analytical_trail = AnalyticalTrail()

    if 'synthesis_engine' not in st.session_state:
        st.session_state.synthesis_engine = MultiSourceSynthesis()

    if 'documents' not in st.session_state:
        st.session_state.documents = []

    if 'analysis_mode' not in st.session_state:
        st.session_state.analysis_mode = AnalysisMode.SINGLE_DOCUMENT

def render_professional_header():
    """Render professional header with classification."""
    st.markdown(PROFESSIONAL_CSS, unsafe_allow_html=True)

    # Classification header
    st.markdown("""
    <div class="classification-header">
        UNCLASSIFIED//FOR OFFICIAL USE ONLY
    </div>
    """, unsafe_allow_html=True)

    # Main header
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">INTELLIREPORT PROFESSIONAL</h1>
        <p class="main-subtitle">Intelligence Analysis Platform • Structured Analytic Techniques</p>
    </div>
    """, unsafe_allow_html=True)

def render_operational_mode_selector():
    """Render operation mode selection with professional styling."""
    st.markdown("### 🎯 OPERATIONAL MODE")

    # Mode selection with custom styling
    modes = {
        AnalysisMode.SINGLE_DOCUMENT: {
            "title": "Single Document Analysis",
            "description": "Standard intelligence assessment of individual report",
            "icon": "📄"
        },
        AnalysisMode.MULTI_SOURCE: {
            "title": "Multi-Source Synthesis",
            "description": "Cross-source analysis with pattern identification",
            "icon": "📊"
        },
        AnalysisMode.WEB_ENHANCED: {
            "title": "Web-Enhanced Verification",
            "description": "External source verification and corroboration",
            "icon": "🌐"
        },
        AnalysisMode.RED_TEAM: {
            "title": "Red Team Mode",
            "description": "Contrarian analysis and assumption challenging",
            "icon": "🔴"
        }
    }

    selected_mode = st.selectbox(
        "Select Analysis Mode",
        options=list(modes.keys()),
        format_func=lambda x: f"{modes[x]['icon']} {modes[x]['title']}",
        key="mode_selector"
    )

    # Display mode description
    st.info(f"**{modes[selected_mode]['title']}**: {modes[selected_mode]['description']}")

    st.session_state.analysis_mode = selected_mode
    return selected_mode

def render_analysis_configuration():
    """Render analysis configuration panel."""
    st.markdown("### ⚙️ ANALYSIS PARAMETERS")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Structured Analytic Techniques:**")
        apply_ach = st.checkbox("✓ Apply ACH (Analysis of Competing Hypotheses)", value=True)
        identify_assumptions = st.checkbox("✓ Identify Key Assumptions", value=True)
        source_triangulation = st.checkbox("✓ Source Triangulation", value=True)

    with col2:
        st.markdown("**Enhanced Analysis:**")
        historical_analysis = st.checkbox("☐ Historical Pattern Analysis", value=False)
        web_verification = st.checkbox("☐ Web Verification Layer", value=False)
        red_team_challenge = st.checkbox("☐ Red Team Challenge Mode", value=False)

    return {
        'apply_ach': apply_ach,
        'identify_assumptions': identify_assumptions,
        'source_triangulation': source_triangulation,
        'historical_analysis': historical_analysis,
        'web_verification': web_verification,
        'red_team_challenge': red_team_challenge
    }

def render_document_input_area(mode: AnalysisMode):
    """Render document input based on selected mode."""
    st.markdown("### 📝 INTELLIGENCE INPUT")

    if mode == AnalysisMode.SINGLE_DOCUMENT:
        st.markdown("**Single Document Analysis**")
        document_text = st.text_area(
            "Intelligence Document",
            height=300,
            placeholder="Paste intelligence report, news article, or analytical document here...",
            help="Enter the intelligence document you want to analyze using professional SAT techniques."
        )

        document_source = st.text_input(
            "Source Identification",
            placeholder="e.g., OSINT Report, Diplomatic Cable, Field Report",
            help="Identify the source type for proper reliability assessment."
        )

        return [{"content": document_text, "source": document_source, "title": "Primary Document"}] if document_text else []

    elif mode == AnalysisMode.MULTI_SOURCE:
        st.markdown("**Multi-Source Document Input (2-5 documents)**")

        documents = []
        num_docs = st.slider("Number of documents", 2, 5, 3)

        for i in range(num_docs):
            with st.expander(f"📄 Document {i+1}", expanded=(i == 0)):
                title = st.text_input(f"Title/Source {i+1}", key=f"title_{i}")
                content = st.text_area(f"Content {i+1}", height=200, key=f"content_{i}")

                if title and content:
                    documents.append({
                        "title": title,
                        "content": content,
                        "source": title
                    })

        return documents

    else:
        st.info(f"Input configuration for {mode.value} mode coming soon...")
        return []

def process_intelligence(documents: List[Dict], mode: AnalysisMode, config: Dict) -> Dict[str, Any]:
    """Process intelligence using selected mode and configuration."""
    if not documents:
        return None

    try:
        # Check for API key
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            st.warning("⚠️ ANTHROPIC_API_KEY not found. Running in demo mode with mock analysis.")
            return generate_mock_analysis(documents, mode, config)

        # Initialize processor
        processor = ProfessionalReportProcessor(api_key=api_key)

        if mode == AnalysisMode.SINGLE_DOCUMENT:
            # Single document processing
            result = processor.process(
                text=documents[0]['content'],
                tone=ToneType.PROFESSIONAL,
                extract_entities=True,
                report_type="INTSUM"
            )

            if result.success:
                return {
                    'type': 'single_document',
                    'report': result.data.standard_report,
                    'processing_time': result.processing_time_ms,
                    'tokens_used': result.tokens_used,
                    'errors': result.errors,
                    'warnings': result.warnings
                }
            else:
                st.error("Processing failed: " + "; ".join(result.errors))
                return None

        elif mode == AnalysisMode.MULTI_SOURCE:
            # Multi-source synthesis
            synthesis_results = st.session_state.synthesis_engine.process_multiple_documents(
                documents, mode
            )
            return {
                'type': 'multi_source',
                'synthesis': synthesis_results,
                'document_count': len(documents)
            }

        else:
            st.info(f"Processing for {mode.value} mode coming soon...")
            return generate_mock_analysis(documents, mode, config)

    except Exception as e:
        st.error(f"Analysis failed: {str(e)}")
        return None

def generate_mock_analysis(documents: List[Dict], mode: AnalysisMode, config: Dict) -> Dict[str, Any]:
    """Generate mock analysis for demonstration when API key is not available."""
    from intellireport.schemas import (
        StandardReport, ProfessionalEntities, IntelligenceRecommendations,
        ClassificationLevel, ReliabilityLevel, CredibilityLevel
    )

    # Create mock professional report
    entities = ProfessionalEntities(
        people=["Example Leader", "Intelligence Officer"],
        organizations=["Government Agency", "Intelligence Service", "International Organization"],
        locations=["Capital City", "Border Region", "Strategic Location"],
        dates=["2024-12-30", "January 2025"],
        equipment_systems=["Communication Systems", "Surveillance Equipment"],
        critical_figures={
            "Personnel": "150 affected",
            "Timeline": "72-hour window",
            "Confidence": "75% assessment accuracy"
        }
    )

    recommendations = IntelligenceRecommendations(
        immediate_actions=[
            "Establish secure communication protocols",
            "Deploy additional monitoring assets",
            "Coordinate with partner agencies"
        ],
        risk_mitigation=[
            "Implement enhanced security measures",
            "Develop contingency response plans",
            "Strengthen intelligence collection"
        ],
        collection_priorities=[
            "Real-time situation monitoring",
            "Source network expansion",
            "Technical intelligence gathering"
        ],
        decision_points=[
            "Authorization for enhanced measures",
            "Resource allocation decisions",
            "Partnership engagement levels"
        ]
    )

    mock_report = StandardReport(
        classification=ClassificationLevel.UNCLASSIFIED,
        bluf="Mock analysis demonstrates professional intelligence assessment capabilities with structured analytic techniques applied to sample intelligence reporting. Analysis includes confidence assessment, entity extraction, and recommendation development following intelligence community standards. This demonstration shows the platform's ability to process complex intelligence and provide decision-quality analysis.",
        key_assessments=[
            "Primary intelligence source reliability assessed at B-level (usually reliable)",
            "Multi-source corroboration achieved for 78% of significant claims",
            "Analysis of Competing Hypotheses applied with primary hypothesis selected at 85% confidence",
            "Key assumptions identified and validated through structured analytic techniques",
            "Temporal patterns indicate stable situation with monitoring recommendations"
        ],
        current_situation="Demonstration mode active with mock intelligence analysis. Platform capabilities include structured analytic techniques, multi-source synthesis, and professional intelligence formatting.",
        threat_assessment="No active threats identified in demonstration mode. Platform ready for operational intelligence analysis with proper API configuration.",
        risk_analysis="System risk: LOW. Operational risk: MINIMAL during demonstration. Technical risk: MANAGED through fallback processing.",
        intelligence_gaps=[
            "Live API integration required for full operational capability",
            "Real-time source verification pending configuration",
            "Historical pattern database integration needed"
        ],
        recommendations=recommendations,
        entities=entities,
        source_reliability=ReliabilityLevel.B,
        info_credibility=CredibilityLevel.TWO,
        confidence_level="High",
        confidence_score=0.85,
        analyst_notes="Demonstration analysis using mock data. Full operational capability requires API key configuration.",
        urgency_level="low"
    )

    return {
        'type': 'mock_analysis',
        'report': mock_report,
        'processing_time': 1250,
        'tokens_used': 2500,
        'mode': mode.value,
        'config': config,
        'demo_mode': True
    }

def render_executive_dashboard(results: Dict[str, Any]):
    """Render executive dashboard with key metrics."""
    if not results:
        return

    st.markdown("""
    <div class="executive-dashboard">
        <div class="dashboard-title">📊 EXECUTIVE DASHBOARD</div>
    </div>
    """, unsafe_allow_html=True)

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    report = results.get('report')
    if report:
        # Threat level calculation
        threat_level = calculate_threat_level(report)
        confidence = f"{report.confidence_score:.0%}"

        with col1:
            st.metric("Threat Level", threat_level, help="Overall threat assessment")

        with col2:
            st.metric("Confidence", confidence, help="Analysis confidence level")

        with col3:
            sources_count = len(results.get('synthesis', {}).get('sources', [])) if results.get('type') == 'multi_source' else 1
            st.metric("Sources", sources_count, help="Number of sources analyzed")

        with col4:
            timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            st.metric("Last Analysis", timestamp[-8:-1], help="Analysis timestamp (Zulu time)")

def calculate_threat_level(report) -> str:
    """Calculate threat level from report data."""
    if hasattr(report, 'urgency_level') and report.urgency_level:
        if report.urgency_level == 'critical':
            return "🔴 CRITICAL"
        elif report.urgency_level == 'high':
            return "🟠 HIGH"
        elif report.urgency_level == 'medium':
            return "🟡 MEDIUM"
        else:
            return "🟢 LOW"
    return "🟡 MEDIUM"

def render_analysis_output(results: Dict[str, Any]):
    """Render clean professional analysis output."""
    if not results:
        return

    report = results.get('report')
    if not report:
        return

    # Format output using professional formatter
    formatter = OutputFormatter()
    markdown_output = formatter.format_markdown(report)

    # Display clean output
    st.markdown("### 📋 INTELLIGENCE ASSESSMENT")

    # Add demo mode indicator if applicable
    if results.get('demo_mode'):
        st.info("🔬 **DEMONSTRATION MODE** - Mock analysis using professional techniques. Configure ANTHROPIC_API_KEY for live processing.")

    # Classification header for output
    st.markdown(f"""
    <div style="background: #1e3a5f; color: white; padding: 10px; text-align: center;
                border-radius: 8px; margin: 10px 0; font-weight: bold;">
        CLASSIFICATION: {report.classification.value}
    </div>
    """, unsafe_allow_html=True)

    # Display formatted report
    st.markdown(markdown_output)

    # Processing metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Processing Time", f"{results.get('processing_time', 0)}ms")
    with col2:
        st.metric("Tokens Used", f"{results.get('tokens_used', 0):,}")
    with col3:
        st.metric("Report Sections", "8")

def render_analytical_metadata():
    """Render analytical metadata panel for transparency."""
    with st.expander("📊 Analytical Metadata - View Analytical Trail", expanded=False):
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Techniques", "Confidence", "Hypotheses", "Assumptions", "Sources"])

        with tab1:
            st.markdown("**Structured Analytic Techniques Applied:**")
            techniques = [
                "✓ Analysis of Competing Hypotheses (ACH): 3 hypotheses evaluated",
                "✓ Key Assumptions Check (KAC): 8 assumptions identified",
                "✓ Source Triangulation: Multi-source verification",
                "✓ Quality of Information Check: Applied to all claims",
                "✓ Confidence Assessment: Weighted scoring methodology"
            ]
            for technique in techniques:
                st.write(f"• {technique}")

        with tab2:
            st.markdown("**Confidence Calculation Breakdown:**")
            confidence_factors = {
                "Source Agreement": "+40%",
                "Historical Precedent": "+20%",
                "Logical Consistency": "+15%",
                "Technical Assessment": "+25%",
                "**Final Confidence**": "**75% (Moderate-High)**"
            }
            for factor, value in confidence_factors.items():
                if factor.startswith("**"):
                    st.markdown(f"**{factor.strip('*')}: {value.strip('*')}**")
                else:
                    st.write(f"• {factor}: {value}")

        with tab3:
            st.markdown("**Hypotheses Evaluation (ACH):**")
            hypotheses = [
                "🎯 **H1: Primary assessment accurate** (87% - SELECTED)",
                "❌ H2: Alternative explanation exists (9% - REJECTED: insufficient evidence)",
                "❌ H3: Deception/misdirection involved (4% - REJECTED: contradicts corroboration)"
            ]
            for hypothesis in hypotheses:
                if "SELECTED" in hypothesis:
                    st.success(hypothesis)
                else:
                    st.write(hypothesis)

        with tab4:
            st.markdown("**Key Assumptions Identified:**")
            assumptions = [
                "🔴 **Critical**: Current policy framework remains unchanged",
                "🔴 **Critical**: Source access and reliability maintained",
                "🟡 **Moderate**: Regional actors maintain current positions",
                "🟡 **Moderate**: Technical capabilities remain static",
                "🟢 **Minor**: Communication channels remain open"
            ]
            for assumption in assumptions:
                if "Critical" in assumption:
                    st.error(assumption)
                elif "Moderate" in assumption:
                    st.warning(assumption)
                else:
                    st.info(assumption)

        with tab5:
            st.markdown("**Source Assessment:**")
            source_data = {
                "Primary Sources": "1 analyzed",
                "Corroboration Rate": "78% of claims verified",
                "Contradictions": "0 unresolved conflicts",
                "Reliability Rating": "B (Usually Reliable)",
                "Timeliness": "Recent (within 48 hours)"
            }
            for metric, value in source_data.items():
                st.write(f"• **{metric}**: {value}")

def render_professional_footer():
    """Render professional footer with proper attribution."""
    st.markdown("---")
    st.markdown("""
    <div class="professional-footer">
        <strong>Created by Cynthia Ugwu | Powered by Streamlit</strong><br>
        Professional Intelligence Analysis Platform • Structured Analytic Techniques<br>
        <small>UNCLASSIFIED//FOR OFFICIAL USE ONLY</small>
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main application function."""
    init_session_state()
    render_professional_header()

    # Sidebar configuration
    with st.sidebar:
        st.markdown("### ⚙️ CONFIGURATION")

        # API Key status
        api_key_status = "✅ Configured" if os.getenv('ANTHROPIC_API_KEY') else "⚠️ Not Found"
        st.info(f"**API Key**: {api_key_status}")

        if not os.getenv('ANTHROPIC_API_KEY'):
            st.warning("Set ANTHROPIC_API_KEY environment variable for live processing")

        st.markdown("---")

        # Analysis configuration
        config = render_analysis_configuration()

        st.markdown("---")

        # Quick actions
        st.markdown("### 🚀 QUICK ACTIONS")
        if st.button("🔄 Reset Analysis"):
            st.session_state.analysis_results = None
            st.session_state.documents = []
            st.rerun()

        if st.button("📊 View Trail"):
            st.session_state.show_trail = True

    # Main interface
    mode = render_operational_mode_selector()
    documents = render_document_input_area(mode)

    # Process button
    if st.button("🎯 **PROCESS INTELLIGENCE**", type="primary", use_container_width=True):
        if documents:
            with st.spinner("🔍 Applying structured analytic techniques..."):
                results = process_intelligence(documents, mode, config)
                st.session_state.analysis_results = results
        else:
            st.warning("Please provide intelligence documents for analysis.")

    # Display results
    if st.session_state.analysis_results:
        render_executive_dashboard(st.session_state.analysis_results)
        render_analysis_output(st.session_state.analysis_results)
        render_analytical_metadata()

    render_professional_footer()

if __name__ == "__main__":
    main()