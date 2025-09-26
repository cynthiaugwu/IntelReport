"""
Comprehensive example demonstrating IntelliReport library usage.

This script shows how to:
1. Initialize the ReportProcessor with different tones
2. Process various types of reports
3. Handle different output formats
4. Work with entity extraction and redaction
5. Analyze missing fields and improve reports
"""

import os
import json
from pathlib import Path
import sys

# Add the parent directory to the path to import intellireport
sys.path.append(str(Path(__file__).parent.parent))

from intellireport import ReportProcessor
from intellireport.schemas import ToneType
from intellireport.redactor import RedactionLevel


def print_section_header(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f" {title}")
    print("=" * 80)


def print_subsection(title: str):
    """Print a formatted subsection header."""
    print(f"\n--- {title} ---")


def load_sample_report(filename: str) -> str:
    """Load a sample report from the sample_reports directory."""
    sample_path = Path(__file__).parent / "sample_reports" / filename
    try:
        with open(sample_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"Sample report '{filename}' not found. Please check the file path."


def demo_basic_processing():
    """Demonstrate basic report processing with different tones."""
    print_section_header("BASIC REPORT PROCESSING")

    # Load a sample report
    sample_text = load_sample_report("security_assessment.txt")

    if "not found" in sample_text:
        print("⚠️ Sample file not found, using embedded example...")
        sample_text = """
        SECURITY INCIDENT REPORT

        Date: March 26, 2024
        Incident: Unauthorized access attempt detected

        BLUF: Failed login attempts from suspicious IP address indicate potential
        brute force attack against admin accounts. Immediate action required to
        strengthen authentication controls.

        Details:
        - 127 failed login attempts in 15 minutes
        - Source IP: 198.51.100.45 (known malicious)
        - Target accounts: admin, administrator, root
        - No successful breaches detected

        Recommendations:
        1. Implement rate limiting on login attempts
        2. Enable multi-factor authentication
        3. Block suspicious IP ranges
        4. Review and strengthen password policies

        Classification: Confidential
        Reporter: Security Team
        """

    print("📄 Processing sample security report...")

    # Initialize processor with professional tone
    processor = ReportProcessor(tone=ToneType.PROFESSIONAL)

    try:
        # Process the report
        result = processor.process(
            text=sample_text,
            tone=ToneType.PROFESSIONAL,
            output_format="json",
            extract_entities=True,
            analyze_missing_fields=True,
            redact_pii=False
        )

        print(f"✅ Processing completed in {result.processing_time_ms}ms")
        print(f"🎯 Success: {result.success}")
        print(f"📊 Tokens used: {result.tokens_used}")

        if result.data.standard_report:
            report = result.data.standard_report
            print(f"\n📋 BLUF: {report.bluf}")
            print(f"🏷️ Classification: {report.classification}")
            print(f"📈 Confidence: {report.confidence_score:.2%}")

            if report.key_findings:
                print(f"\n🔍 Key Findings ({len(report.key_findings)}):")
                for i, finding in enumerate(report.key_findings[:3], 1):
                    print(f"  {i}. {finding}")

            if report.recommendations:
                print(f"\n💡 Recommendations ({len(report.recommendations)}):")
                for i, rec in enumerate(report.recommendations[:3], 1):
                    print(f"  {i}. {rec}")

        if result.errors:
            print(f"\n❌ Errors: {len(result.errors)}")
            for error in result.errors:
                print(f"  • {error}")

        if result.warnings:
            print(f"\n⚠️ Warnings: {len(result.warnings)}")
            for warning in result.warnings:
                print(f"  • {warning}")

    except Exception as e:
        print(f"❌ Error processing report: {str(e)}")
        print("💡 Make sure your ANTHROPIC_API_KEY environment variable is set")


def demo_tone_comparison():
    """Demonstrate how different tones affect analysis."""
    print_section_header("TONE COMPARISON DEMO")

    # Simple incident report for comparison
    incident_text = """
    Emergency Response Report

    Location: Coastal Village, Delta Region
    Date: March 26, 2024

    A magnitude 6.2 earthquake struck the coastal region at 14:30 local time.
    Preliminary assessment shows 3 villages affected with approximately 1,200 people
    requiring immediate assistance.

    Damage observed:
    - 45 homes partially or completely destroyed
    - Main bridge to regional hospital compromised
    - Water treatment facility offline
    - Communications towers damaged

    Immediate needs:
    - Emergency shelter for 300 families
    - Medical supplies and personnel
    - Clean water for 1,200 people
    - Search and rescue teams

    Access routes are limited due to bridge damage. Helicopter access available
    at primary school landing zone.
    """

    tones = [
        (ToneType.NGO, "🌍 NGO/Humanitarian"),
        (ToneType.CORPORATE, "🏢 Corporate"),
        (ToneType.PROFESSIONAL, "🏛️ Professional/Government")
    ]

    for tone, tone_name in tones:
        print_subsection(f"{tone_name} Analysis")

        try:
            processor = ReportProcessor(tone=tone)
            result = processor.process(
                text=incident_text,
                tone=tone,
                extract_entities=False,  # Skip entities for speed
                analyze_missing_fields=False  # Skip analysis for speed
            )

            if result.data.standard_report:
                report = result.data.standard_report
                print(f"BLUF: {report.bluf}")

                if report.recommendations:
                    print("Top Recommendations:")
                    for i, rec in enumerate(report.recommendations[:2], 1):
                        print(f"  {i}. {rec}")

                print(f"Urgency: {report.urgency_level or 'Not specified'}")
                print(f"Confidence: {report.confidence_score:.2%}")

        except Exception as e:
            print(f"❌ Error with {tone_name}: {str(e)}")


def demo_entity_extraction():
    """Demonstrate entity extraction capabilities."""
    print_section_header("ENTITY EXTRACTION DEMO")

    # Load field observation report for entity extraction
    field_report = load_sample_report("field_observation.txt")

    if "not found" in field_report:
        field_report = """
        Field Report - Border Monitoring

        Observer: Alex Thompson
        Location: Monitoring Post Bravo-3
        Date: March 26, 2024

        Observed unusual convoy activity involving several organizations:
        - UNHCR vehicles heading toward Camp Delta
        - Red Cross medical team at coordinates 34.5234, -118.2437
        - Government forces led by Colonel Martinez
        - Dr. Sarah Chen coordinating with WHO representatives

        Communications intercepted on frequency 156.325 MHz.
        Local contact: Ahmed Hassan (ahmed.hassan@email.com)
        Phone: +1-555-123-4567

        Next meeting scheduled for April 1, 2024 in Geneva, Switzerland.
        """

    print("🔍 Extracting entities from field observation report...")

    try:
        processor = ReportProcessor()
        result = processor.process(
            text=field_report,
            extract_entities=True,
            analyze_missing_fields=False,
            redact_pii=False
        )

        if result.data.extracted_entities:
            entities = result.data.extracted_entities

            print_subsection("Extracted Entities")

            if entities.people:
                print(f"👤 People ({len(entities.people)}):")
                for person in entities.people[:5]:  # Limit to 5
                    print(f"  • {person}")

            if entities.organizations:
                print(f"\n🏢 Organizations ({len(entities.organizations)}):")
                for org in entities.organizations[:5]:
                    print(f"  • {org}")

            if entities.locations:
                print(f"\n📍 Locations ({len(entities.locations)}):")
                for location in entities.locations[:5]:
                    print(f"  • {location}")

            if entities.dates:
                print(f"\n📅 Dates ({len(entities.dates)}):")
                for date in entities.dates[:5]:
                    print(f"  • {date}")

        else:
            print("❌ No entities extracted")

    except Exception as e:
        print(f"❌ Error extracting entities: {str(e)}")


def demo_redaction():
    """Demonstrate PII redaction at different levels."""
    print_section_header("PII REDACTION DEMO")

    # Text with various PII types
    pii_text = """
    Contact Report

    Meeting with field coordinator Dr. Sarah Johnson (sarah.johnson@ngo.org)
    Phone: +1-555-987-6543
    Employee ID: EMP-2024-1234

    Discussed security situation with local police chief Colonel James Smith.
    His contact: james.smith@police.gov, mobile +234-801-234-5678

    Financial details:
    Credit card ending in 4567 was used for emergency supplies.
    Budget account: 123-45-6789

    Location: 123 Main Street, Lagos, Nigeria
    GPS coordinates: 6.5244° N, 3.3792° E

    Next meeting: March 30, 2024 at 14:00
    IP address for video call: 192.168.1.100
    """

    redaction_levels = [
        (RedactionLevel.LOW, "🟢 Low"),
        (RedactionLevel.MEDIUM, "🟡 Medium"),
        (RedactionLevel.HIGH, "🟠 High"),
        (RedactionLevel.MAXIMUM, "🔴 Maximum")
    ]

    for level, level_name in redaction_levels:
        print_subsection(f"{level_name} Redaction Level")

        try:
            processor = ReportProcessor()
            result = processor.process(
                text=pii_text,
                extract_entities=False,
                analyze_missing_fields=False,
                redact_pii=True,
                redaction_level=level
            )

            if result.data.redacted_text:
                print("📝 Redacted text (first 200 chars):")
                print(result.data.redacted_text[:200] + "...")

                if result.data.redacted_entities:
                    print(f"\n🔒 Redacted {len(result.data.redacted_entities)} entities:")
                    # Group by type
                    type_counts = {}
                    for entity in result.data.redacted_entities:
                        type_counts[entity.entity_type] = type_counts.get(entity.entity_type, 0) + 1

                    for entity_type, count in type_counts.items():
                        print(f"  • {entity_type}: {count}")

        except Exception as e:
            print(f"❌ Error with redaction: {str(e)}")


def demo_output_formats():
    """Demonstrate different output formats."""
    print_section_header("OUTPUT FORMATS DEMO")

    # Simple report for formatting demo
    simple_report = """
    Weekly Status Report

    Project: IntelliReport Development
    Date: March 26, 2024

    BLUF: Development on track with 85% of core features complete.
    Demo deployment scheduled for next week with stakeholder review.

    Completed this week:
    - Entity extraction module finalized
    - Redaction system implemented
    - Streamlit demo interface created

    Next week priorities:
    - Documentation completion
    - Performance optimization
    - Security testing

    Risk: Minor delay possible if additional security requirements identified.

    Team: Development team performing well, no resource constraints.
    Classification: Internal Use Only
    """

    try:
        processor = ReportProcessor()
        result = processor.process(
            text=simple_report,
            extract_entities=False,
            analyze_missing_fields=False
        )

        if result.data.standard_report:
            from intellireport.formatters import OutputFormatter
            formatter = OutputFormatter()

            print_subsection("JSON Format")
            json_output = formatter.format_json(result.data.standard_report, indent=2)
            print(json_output[:300] + "...")

            print_subsection("YAML Format")
            yaml_output = formatter.format_yaml(result.data.standard_report)
            print(yaml_output[:300] + "...")

            print_subsection("Markdown Format")
            markdown_output = formatter.format_markdown(
                result.data.standard_report,
                include_classification=True
            )
            print(markdown_output[:400] + "...")

    except Exception as e:
        print(f"❌ Error formatting output: {str(e)}")


def demo_missing_fields_analysis():
    """Demonstrate missing fields analysis."""
    print_section_header("MISSING FIELDS ANALYSIS")

    # Incomplete report for analysis
    incomplete_report = """
    Report

    Something happened yesterday. It was bad. People were affected.
    We should do something about it.

    More details to follow.
    """

    print("🔍 Analyzing incomplete report for missing fields...")

    try:
        processor = ReportProcessor()
        result = processor.process(
            text=incomplete_report,
            analyze_missing_fields=True
        )

        if result.data.missing_fields:
            missing = result.data.missing_fields

            if missing.missing_fields:
                print_subsection("Missing Critical Fields")
                for field in missing.missing_fields:
                    print(f"  ❌ {field}")

            if missing.confidence_issues:
                print_subsection("Low Confidence Fields")
                for issue in missing.confidence_issues:
                    print(f"  ⚠️ {issue}")

            if missing.suggestions:
                print_subsection("Improvement Suggestions")
                for suggestion in missing.suggestions:
                    print(f"  💡 {suggestion}")
        else:
            print("✅ No missing fields analysis available")

    except Exception as e:
        print(f"❌ Error analyzing missing fields: {str(e)}")


def demo_batch_processing():
    """Demonstrate batch processing of multiple reports."""
    print_section_header("BATCH PROCESSING DEMO")

    # Multiple short reports for batch processing
    batch_reports = [
        "Alert: Network intrusion detected at 14:30. Investigating potential data breach.",
        "Status: All systems operational. No incidents reported in past 24 hours.",
        "Incident: Power outage in data center from 09:15-09:45. Backup systems functioned correctly."
    ]

    print(f"📦 Processing batch of {len(batch_reports)} reports...")

    try:
        processor = ReportProcessor()
        results = processor.process_batch(
            texts=batch_reports,
            tone=ToneType.PROFESSIONAL,
            extract_entities=False,
            analyze_missing_fields=False
        )

        print(f"✅ Processed {len(results)} reports")

        for i, result in enumerate(results, 1):
            print(f"\nReport {i}:")
            print(f"  Success: {result.success}")
            if result.data.standard_report:
                print(f"  BLUF: {result.data.standard_report.bluf[:100]}...")
            if result.errors:
                print(f"  Errors: {len(result.errors)}")

    except Exception as e:
        print(f"❌ Error in batch processing: {str(e)}")


def main():
    """Main function demonstrating all IntelliReport features."""
    print_section_header("INTELLIREPORT COMPREHENSIVE DEMO")
    print("🔍 IntelliReport - Intelligence Report Structuring")
    print("📋 Part of the IJEOMA Safety Platform")

    # Check API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("\n⚠️ WARNING: ANTHROPIC_API_KEY environment variable not set!")
        print("   Some features may not work without a valid API key.")
        print("   Set your API key with: export ANTHROPIC_API_KEY='your-key-here'")

    try:
        # Run all demos
        demo_basic_processing()
        demo_tone_comparison()
        demo_entity_extraction()
        demo_redaction()
        demo_output_formats()
        demo_missing_fields_analysis()
        demo_batch_processing()

        print_section_header("DEMO COMPLETED SUCCESSFULLY")
        print("✅ All IntelliReport features demonstrated!")
        print("\n📖 Next Steps:")
        print("   1. Explore the sample reports in examples/sample_reports/")
        print("   2. Try the Streamlit web interface: streamlit run demo/streamlit_app.py")
        print("   3. Read the full documentation in README.md")
        print("   4. Check out the API reference for advanced usage")

        print("\n🌟 Need help?")
        print("   - Documentation: https://github.com/yourusername/intellireport")
        print("   - Issues: https://github.com/yourusername/intellireport/issues")
        print("   - IJEOMA Platform: https://ijeoma.safety")

    except KeyboardInterrupt:
        print("\n👋 Demo interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error in demo: {str(e)}")
        print("🔧 Please check your setup and try again.")


if __name__ == "__main__":
    main()