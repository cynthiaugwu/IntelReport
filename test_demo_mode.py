#!/usr/bin/env python3
"""
Test IntelliReport Professional in Demo Mode
Validates all core functionality without requiring API key.
"""

import sys
import os
from datetime import datetime

# Add the project root to Python path
sys.path.insert(0, os.path.abspath('.'))

def test_analytical_engine():
    """Test the analytical engine components."""
    print("🧠 Testing Analytical Engine...")

    from intellireport.analytical_engine import (
        AnalyticalTrail, StructuredAnalyticTechniques,
        AnalysisMode, Hypothesis, Assumption
    )

    # Test AnalyticalTrail
    trail = AnalyticalTrail()
    trail.log('test_step', {'type': 'source_corroboration', 'confidence': 0.8})

    assert len(trail.steps) == 1
    assert trail.steps[0]['type'] == 'test_step'
    print("✅ AnalyticalTrail logging works")

    # Test SAT engine
    sat = StructuredAnalyticTechniques()

    # Test ACH
    hypotheses, selected = sat.analysis_of_competing_hypotheses(
        "Government implemented new policy",
        "Policy was announced after protests"
    )
    assert len(hypotheses) >= 3
    assert selected is not None
    print("✅ Analysis of Competing Hypotheses works")

    # Test KAC
    assumptions = sat.key_assumptions_check(
        "The government will continue this policy because it was effective. "
        "Officials likely believe this approach will remain successful."
    )
    assert len(assumptions) > 0
    print("✅ Key Assumptions Check works")

    # Test confidence calculation
    confidence_score, confidence_level = sat.calculate_confidence(0.8, 0.6, 0.7, 0.75)
    assert 0 <= confidence_score <= 1
    print(f"✅ Confidence calculation: {confidence_score:.2f} ({confidence_level.value})")

def test_synthesis_engine():
    """Test multi-source synthesis engine."""
    print("\n🔄 Testing Synthesis Engine...")

    from intellireport.synthesis_engine import MultiSourceSynthesis
    from intellireport.analytical_engine import AnalysisMode

    synthesis = MultiSourceSynthesis()

    # Test documents
    test_docs = [
        {
            "title": "Government Report",
            "content": "Government suspended diplomatic relations with neighboring country due to border disputes.",
            "source": "Official Government Statement"
        },
        {
            "title": "News Report",
            "content": "Diplomatic crisis escalated when border incidents increased this week.",
            "source": "International News Agency"
        }
    ]

    # Test synthesis processing
    results = synthesis.process_multiple_documents(test_docs, AnalysisMode.MULTI_SOURCE)

    assert 'executive_summary' in results
    assert 'corroborated_claims' in results
    assert 'contradictions' in results
    assert 'analytical_metadata' in results

    print("✅ Multi-source synthesis works")
    print(f"✅ Executive summary: {results['executive_summary'][:100]}...")

def test_schemas():
    """Test schema validation."""
    print("\n📋 Testing Schemas...")

    from intellireport.schemas import (
        StandardReport, ProfessionalEntities, IntelligenceRecommendations,
        ClassificationLevel, ReliabilityLevel, CredibilityLevel
    )

    # Test entities
    entities = ProfessionalEntities(
        people=["John Smith", "Jane Doe"],
        organizations=["Government Agency", "Intelligence Service"],
        locations=["Capital City", "Border Region"]
    )
    assert len(entities.people) == 2
    print("✅ ProfessionalEntities validation works")

    # Test recommendations
    recommendations = IntelligenceRecommendations(
        immediate_actions=["Monitor situation", "Increase security"],
        risk_mitigation=["Diplomatic engagement", "Border security"]
    )
    assert len(recommendations.immediate_actions) == 2
    print("✅ IntelligenceRecommendations validation works")

    # Test StandardReport
    report = StandardReport(
        bluf="This is a comprehensive intelligence assessment demonstrating the platform's sophisticated analytical capabilities and structured approach to intelligence processing. The assessment incorporates multiple structured analytic techniques including Analysis of Competing Hypotheses, Key Assumptions Check, and source triangulation to provide decision-quality intelligence analysis that meets professional intelligence community standards.",
        key_assessments=[
            "Primary assessment confirmed through multiple sources with high confidence",
            "Analysis techniques applied successfully using structured methodologies",
            "Confidence calculations validated through weighted scoring approach"
        ],
        current_situation="Platform demonstrates full operational capability for professional intelligence analysis",
        entities=entities,
        recommendations=recommendations,
        classification=ClassificationLevel.UNCLASSIFIED,
        source_reliability=ReliabilityLevel.B,
        info_credibility=CredibilityLevel.TWO
    )

    assert report.is_professional_standard
    print("✅ StandardReport meets professional standards")

def test_demo_mode_processing():
    """Test demo mode without API key."""
    print("\n🎭 Testing Demo Mode Processing...")

    # Import the generate_mock_analysis function from app.py
    sys.path.insert(0, os.path.abspath('.'))
    from app import generate_mock_analysis
    from intellireport.analytical_engine import AnalysisMode

    test_docs = [{"content": "Test intelligence document", "source": "Test Source", "title": "Test"}]
    config = {'apply_ach': True, 'identify_assumptions': True}

    results = generate_mock_analysis(test_docs, AnalysisMode.SINGLE_DOCUMENT, config)

    assert results['type'] == 'mock_analysis'
    assert results['demo_mode'] == True
    assert 'report' in results
    assert results['report'].is_professional_standard

    print("✅ Demo mode processing works")
    print(f"✅ Mock report BLUF: {results['report'].bluf[:100]}...")

def test_ui_components():
    """Test UI component functions."""
    print("\n🎨 Testing UI Components...")

    from app import calculate_threat_level
    from intellireport.schemas import StandardReport

    # Create test report
    test_report = StandardReport(
        bluf="Test intelligence assessment for UI validation demonstrating threat level calculation functionality in professional intelligence analysis platform",
        key_assessments=["Test assessment 1", "Test assessment 2", "Test assessment 3"],
        urgency_level="high"
    )

    threat_level = calculate_threat_level(test_report)
    assert threat_level == "🟠 HIGH"
    print("✅ Threat level calculation works")

def main():
    """Run all tests."""
    print("🚀 INTELLIREPORT PROFESSIONAL - DEMO MODE VALIDATION")
    print("=" * 80)
    print(f"🕐 Test started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    try:
        test_analytical_engine()
        test_synthesis_engine()
        test_schemas()
        test_demo_mode_processing()
        test_ui_components()

        print("\n" + "=" * 80)
        print("🎉 ALL TESTS PASSED! IntelliReport Professional is ready for deployment.")
        print("✅ Analytical Engine: OPERATIONAL")
        print("✅ Synthesis Engine: OPERATIONAL")
        print("✅ Schema Validation: OPERATIONAL")
        print("✅ Demo Mode: OPERATIONAL")
        print("✅ UI Components: OPERATIONAL")
        print("\n🔧 To use with live API, set ANTHROPIC_API_KEY environment variable")
        print("🌐 Demo mode provides full analytical capabilities for evaluation")

    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()