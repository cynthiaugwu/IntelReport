"""
Enhanced output formatting utilities for multiple formats.
"""

import json
import yaml
import xml.etree.ElementTree as ET
from typing import Dict, Any, Optional, List
from datetime import datetime
from xml.dom import minidom

from .schemas import StandardReport, ReportData, JSONOutput, MarkdownOutput


class OutputFormatter:
    """Enhanced formatter for multiple output formats."""

    def __init__(self):
        """Initialize the formatter."""
        self.markdown_formatter = MarkdownOutput()

    def format(
        self,
        data: StandardReport,
        format_type: str = "json",
        **kwargs
    ) -> str:
        """
        Format StandardReport data into specified format.

        Args:
            data: StandardReport object to format
            format_type: Output format (json, yaml, xml, markdown, html)
            **kwargs: Additional formatting options

        Returns:
            Formatted string output
        """
        format_type = format_type.lower()

        if format_type == "json":
            return self.format_json(data, **kwargs)
        elif format_type == "yaml":
            return self.format_yaml(data, **kwargs)
        elif format_type == "xml":
            return self.format_xml(data, **kwargs)
        elif format_type == "markdown":
            return self.format_markdown(data, **kwargs)
        elif format_type == "html":
            return self.format_html(data, **kwargs)
        else:
            raise ValueError(f"Unsupported format: {format_type}")

    def format_json(
        self,
        data: StandardReport,
        indent: int = 2,
        include_metadata: bool = True,
        exclude_none: bool = True
    ) -> str:
        """
        Format as structured JSON.

        Args:
            data: StandardReport to format
            indent: JSON indentation
            include_metadata: Whether to include processing metadata
            exclude_none: Whether to exclude None values

        Returns:
            JSON formatted string
        """
        # Create structured JSON output
        json_output = JSONOutput(
            report=data,
            metadata={
                "generated_at": datetime.now().isoformat(),
                "format_version": "1.0",
                "library": "intellireport"
            } if include_metadata else {},
            processing_info={
                "classification": data.classification.value,
                "reliability": data.source_reliability.value,
                "credibility": data.info_credibility.value,
                "confidence": data.confidence_score
            } if include_metadata else {}
        )

        # Convert to dict and handle serialization
        output_dict = self._serialize_for_json(json_output.dict(exclude_none=exclude_none))

        return json.dumps(output_dict, indent=indent, ensure_ascii=False, default=str)

    def format_yaml(
        self,
        data: StandardReport,
        include_metadata: bool = True,
        exclude_none: bool = True
    ) -> str:
        """
        Format as YAML.

        Args:
            data: StandardReport to format
            include_metadata: Whether to include processing metadata
            exclude_none: Whether to exclude None values

        Returns:
            YAML formatted string
        """
        # Convert to dict
        output_dict = data.dict(exclude_none=exclude_none)

        # Add metadata if requested
        if include_metadata:
            output_dict["_metadata"] = {
                "generated_at": datetime.now().isoformat(),
                "format_version": "1.0",
                "library": "intellireport"
            }

        # Handle enum serialization for YAML
        output_dict = self._serialize_for_yaml(output_dict)

        return yaml.dump(
            output_dict,
            default_flow_style=False,
            indent=2,
            allow_unicode=True,
            sort_keys=False
        )

    def format_xml(
        self,
        data: StandardReport,
        pretty: bool = True,
        include_metadata: bool = True
    ) -> str:
        """
        Format as XML.

        Args:
            data: StandardReport to format
            pretty: Whether to pretty-print XML
            include_metadata: Whether to include processing metadata

        Returns:
            XML formatted string
        """
        root = ET.Element("IntelliReport")

        if include_metadata:
            metadata = ET.SubElement(root, "metadata")
            ET.SubElement(metadata, "generated_at").text = datetime.now().isoformat()
            ET.SubElement(metadata, "format_version").text = "1.0"
            ET.SubElement(metadata, "library").text = "intellireport"

        # Add report data
        report_elem = ET.SubElement(root, "report")

        # Convert StandardReport to XML
        self._dict_to_xml(data.dict(exclude_none=True), report_elem)

        if pretty:
            # Pretty print XML
            xml_str = ET.tostring(root, encoding='unicode')
            dom = minidom.parseString(xml_str)
            return dom.toprettyxml(indent="  ")
        else:
            return ET.tostring(root, encoding='unicode')

    def format_markdown(
        self,
        data: StandardReport,
        title: Optional[str] = None,
        include_classification: bool = True,
        include_metadata_table: bool = True,
        include_toc: bool = False
    ) -> str:
        """
        Format as Markdown.

        Args:
            data: StandardReport to format
            title: Custom title (uses report title if None)
            include_classification: Whether to show classification header
            include_metadata_table: Whether to include metadata table
            include_toc: Whether to include table of contents

        Returns:
            Markdown formatted string
        """
        lines = []

        # Classification header
        if include_classification:
            classification = data.classification.value
            lines.append(f"**CLASSIFICATION: {classification}**")
            lines.append("")

        # Title
        report_title = title or data.title or "Intelligence Report"
        lines.append(f"# {report_title}")
        lines.append("")

        # Date and basic info
        lines.append(f"**Date:** {data.date.strftime('%Y-%m-%d %H:%M')}")
        if data.author:
            lines.append(f"**Author:** {data.author}")
        if data.source:
            lines.append(f"**Source:** {data.source}")
        lines.append("")

        # Table of Contents
        if include_toc:
            lines.append("## Table of Contents")
            lines.append("1. [Bottom Line Up Front (BLUF)](#bluf)")
            lines.append("2. [Key Findings](#key-findings)")
            if data.recommendations:
                lines.append("3. [Recommendations](#recommendations)")
            if include_metadata_table:
                lines.append("4. [Report Details](#report-details)")
            lines.append("")

        # BLUF Section
        lines.append("## Bottom Line Up Front (BLUF) {#bluf}")
        lines.append("")
        lines.append(data.bluf)
        lines.append("")

        # Urgency indicator
        if data.urgency_level:
            urgency_emoji = {
                "low": "🟢",
                "medium": "🟡",
                "high": "🟠",
                "critical": "🔴"
            }.get(data.urgency_level, "⚪")
            lines.append(f"**Urgency Level:** {urgency_emoji} {data.urgency_level.upper()}")
            lines.append("")

        # Current Situation
        if data.current_situation:
            lines.append("## Current Situation")
            lines.append("")
            lines.append(data.current_situation)
            lines.append("")

        # Key Findings
        lines.append("## Key Findings {#key-findings}")
        lines.append("")
        for i, finding in enumerate(data.key_findings, 1):
            lines.append(f"{i}. {finding}")
        lines.append("")

        # Threat Assessment
        if data.threat_assessment:
            lines.append("## Threat Assessment")
            lines.append("")
            lines.append(data.threat_assessment)
            lines.append("")

        # Risk Analysis
        if data.risk_analysis:
            lines.append("## Risk Analysis")
            lines.append("")
            lines.append(data.risk_analysis)
            lines.append("")

            # Add risk matrix if we can extract risk elements
            lines.append("### Risk Matrix Assessment")
            lines.append("")
            lines.append("| Risk Factor | Likelihood | Impact | Timeframe | Priority |")
            lines.append("|-------------|------------|--------|-----------|----------|")

            # Use AI-generated risk matrix if available
            if hasattr(data, 'risk_matrix') and data.risk_matrix:
                # Parse risk matrix from AI output
                risk_lines = data.risk_matrix.strip().split('\n')
                for line in risk_lines:
                    if '|' in line and line.strip() and not line.startswith('Risk Factor'):
                        lines.append(line)
            else:
                # Extract risk indicators from the analysis text
                risk_indicators = self._extract_risk_indicators(data.risk_analysis)
                if risk_indicators:
                    for risk in risk_indicators:
                        lines.append(f"| {risk['factor']} | {risk['likelihood']} | {risk['impact']} | {risk['timeframe']} | {risk['priority']} |")
                else:
                    lines.append("| Insufficient data for risk assessment | Unknown | Unknown | TBD | Low |")

            lines.append("")

        # Intelligence Gaps
        if data.intelligence_gaps:
            lines.append("## Intelligence Gaps")
            lines.append("")
            lines.append("**Critical Information Missing:**")
            for gap in data.intelligence_gaps:
                lines.append(f"• {gap}")
            lines.append("")

        # Recommendations
        if data.recommendations:
            lines.append("## Recommendations {#recommendations}")
            lines.append("")

            # Check if recommendations is an IntelligenceRecommendations object or a simple list
            if hasattr(data.recommendations, 'immediate_actions'):
                # Professional structured recommendations
                if data.recommendations.immediate_actions:
                    lines.append("### Immediate Actions")
                    for action in data.recommendations.immediate_actions:
                        lines.append(f"• {action}")
                    lines.append("")

                if data.recommendations.risk_mitigation:
                    lines.append("### Risk Mitigation")
                    for mitigation in data.recommendations.risk_mitigation:
                        lines.append(f"• {mitigation}")
                    lines.append("")

                if data.recommendations.collection_priorities:
                    lines.append("### Collection Priorities")
                    for priority in data.recommendations.collection_priorities:
                        lines.append(f"• {priority}")
                    lines.append("")

                if data.recommendations.decision_points:
                    lines.append("### Decision Points")
                    for decision in data.recommendations.decision_points:
                        lines.append(f"• {decision}")
                    lines.append("")
            else:
                # Legacy list format
                for i, rec in enumerate(data.recommendations, 1):
                    lines.append(f"{i}. {rec}")
                lines.append("")

        # Analyst Notes
        if data.analyst_notes:
            lines.append("## Analyst Notes")
            lines.append("")
            lines.append(data.analyst_notes)
            lines.append("")

        # Named Entities
        if data.entities:
            lines.append("## Named Entities")
            lines.append("")

            # Check if entities is a ProfessionalEntities object or legacy format
            if hasattr(data.entities, 'people'):
                # Professional structured entities
                if data.entities.people:
                    lines.append("**People:**")
                    for person in data.entities.people:
                        lines.append(f"• {person}")
                    lines.append("")

                if data.entities.organizations:
                    lines.append("**Organizations:**")
                    for org in data.entities.organizations:
                        lines.append(f"• {org}")
                    lines.append("")

                if data.entities.locations:
                    lines.append("**Locations:**")
                    for location in data.entities.locations:
                        lines.append(f"• {location}")
                    lines.append("")

                if data.entities.dates:
                    lines.append("**Dates:**")
                    for date in data.entities.dates:
                        lines.append(f"• {date}")
                    lines.append("")

                if data.entities.equipment_systems:
                    lines.append("**Equipment/Systems:**")
                    for equipment in data.entities.equipment_systems:
                        lines.append(f"• {equipment}")
                    lines.append("")

                if hasattr(data.entities, 'critical_figures') and data.entities.critical_figures:
                    lines.append("**Critical Figures:**")
                    for key, value in data.entities.critical_figures.items():
                        lines.append(f"• {key}: {value}")
                    lines.append("")
            else:
                # Legacy list format
                lines.append("**Entities Identified:**")
                for entity in data.entities:
                    lines.append(f"- {entity}")
                lines.append("")

        # Tags
        if data.tags:
            lines.append("**Tags:** " + " • ".join([f"`{tag}`" for tag in data.tags]))
            lines.append("")

        # Metadata Table
        if include_metadata_table:
            lines.append("## Report Details {#report-details}")
            lines.append("")
            lines.append("| Field | Value |")
            lines.append("|-------|-------|")
            lines.append(f"| Source Reliability | {data.source_reliability.value} |")
            lines.append(f"| Information Credibility | {data.info_credibility.value} |")
            if data.location:
                lines.append(f"| Location | {data.location} |")
            lines.append(f"| Confidence Score | {data.confidence_score:.2f} |")
            lines.append("")

        # Summary Assessment
        lines.append("## Summary Assessment")
        lines.append("")

        # Generate overall threat level based on confidence score and urgency
        threat_level = self._calculate_threat_level(data)
        confidence_emoji = "🔴" if data.confidence_score >= 0.8 else "🟡" if data.confidence_score >= 0.5 else "⚪"

        lines.append(f"**Overall Threat Level:** {threat_level}")
        lines.append(f"**Assessment Confidence:** {confidence_emoji} {data.confidence_level} ({data.confidence_score:.1%})")
        lines.append("")

        # Key takeaways (first 3 key assessments)
        if data.key_assessments:
            lines.append("**Key Takeaways:**")
            for takeaway in data.key_assessments[:3]:
                lines.append(f"• {takeaway}")
            lines.append("")

        # Next 72 hours watch points
        lines.append("**Watch Points (Next 72 Hours):**")
        watch_points = self._generate_watch_points(data)
        for point in watch_points:
            lines.append(f"• {point}")
        lines.append("")

        # Footer
        lines.append("---")
        lines.append(f"*Report generated on {datetime.now().strftime('%Y-%m-%d at %H:%M')} UTC*")

        return "\n".join(lines)

    def format_html(
        self,
        data: StandardReport,
        title: Optional[str] = None,
        include_css: bool = True,
        css_style: str = "default"
    ) -> str:
        """
        Format as HTML.

        Args:
            data: StandardReport to format
            title: Custom title
            include_css: Whether to include CSS styling
            css_style: CSS style theme (default, minimal, dark)

        Returns:
            HTML formatted string
        """
        # Get CSS if requested
        css = self._get_css_styles(css_style) if include_css else ""

        # Build HTML content
        report_title = title or data.title or "Intelligence Report"

        html_parts = [
            "<!DOCTYPE html>",
            "<html lang='en'>",
            "<head>",
            "  <meta charset='UTF-8'>",
            "  <meta name='viewport' content='width=device-width, initial-scale=1.0'>",
            f"  <title>{report_title}</title>",
        ]

        if include_css:
            html_parts.append(f"  <style>{css}</style>")

        html_parts.extend([
            "</head>",
            "<body>",
            "  <div class='report-container'>",
        ])

        # Classification header
        classification = data.classification.value
        if classification != "UNCLASSIFIED":
            html_parts.append(f"    <div class='classification-header'>{classification}</div>")

        # Title and basic info
        html_parts.extend([
            f"    <h1 class='report-title'>{report_title}</h1>",
            "    <div class='report-meta'>",
            f"      <p><strong>Date:</strong> {data.date.strftime('%Y-%m-%d %H:%M')}</p>",
        ])

        if data.author:
            html_parts.append(f"      <p><strong>Author:</strong> {data.author}</p>")
        if data.source:
            html_parts.append(f"      <p><strong>Source:</strong> {data.source}</p>")

        html_parts.append("    </div>")

        # BLUF Section
        html_parts.extend([
            "    <section class='bluf-section'>",
            "      <h2>Bottom Line Up Front (BLUF)</h2>",
            f"      <p class='bluf-content'>{data.bluf}</p>",
        ])

        # Urgency indicator
        if data.urgency_level:
            urgency_class = f"urgency-{data.urgency_level}"
            html_parts.append(f"      <div class='urgency-indicator {urgency_class}'>")
            html_parts.append(f"        Urgency Level: {data.urgency_level.upper()}")
            html_parts.append("      </div>")

        html_parts.append("    </section>")

        # Key Findings
        html_parts.extend([
            "    <section class='findings-section'>",
            "      <h2>Key Findings</h2>",
            "      <ol class='findings-list'>",
        ])

        for finding in data.key_findings:
            html_parts.append(f"        <li>{finding}</li>")

        html_parts.append("      </ol>")
        html_parts.append("    </section>")

        # Recommendations
        if data.recommendations:
            html_parts.extend([
                "    <section class='recommendations-section'>",
                "      <h2>Recommendations</h2>",
                "      <ol class='recommendations-list'>",
            ])

            for rec in data.recommendations:
                html_parts.append(f"        <li>{rec}</li>")

            html_parts.extend([
                "      </ol>",
                "    </section>",
            ])

        # Entities and Tags
        if data.entities or data.tags:
            html_parts.append("    <section class='additional-info'>")

            if data.entities:
                html_parts.extend([
                    "      <h3>Named Entities</h3>",
                    "      <div class='entities-list'>",
                ])
                for entity in data.entities:
                    html_parts.append(f"        <span class='entity-tag'>{entity}</span>")
                html_parts.append("      </div>")

            if data.tags:
                html_parts.extend([
                    "      <h3>Tags</h3>",
                    "      <div class='tags-list'>",
                ])
                for tag in data.tags:
                    html_parts.append(f"        <span class='tag'>{tag}</span>")
                html_parts.append("      </div>")

            html_parts.append("    </section>")

        # Metadata table
        html_parts.extend([
            "    <section class='metadata-section'>",
            "      <h2>Report Details</h2>",
            "      <table class='metadata-table'>",
            f"        <tr><td>Source Reliability</td><td>{data.source_reliability.value}</td></tr>",
            f"        <tr><td>Information Credibility</td><td>{data.info_credibility.value}</td></tr>",
        ])

        if data.location:
            html_parts.append(f"        <tr><td>Location</td><td>{data.location}</td></tr>")

        html_parts.extend([
            f"        <tr><td>Confidence Score</td><td>{data.confidence_score:.2f}</td></tr>",
            "      </table>",
            "    </section>",
        ])

        # Footer
        html_parts.extend([
            "    <footer class='report-footer'>",
            f"      <p>Report generated on {datetime.now().strftime('%Y-%m-%d at %H:%M')} UTC</p>",
            "    </footer>",
            "  </div>",
            "</body>",
            "</html>",
        ])

        return "\n".join(html_parts)

    def _extract_risk_indicators(self, risk_analysis: str) -> List[Dict[str, str]]:
        """Extract specific risk indicators from risk analysis text for risk matrix."""
        import re

        indicators = []

        # Look for specific threat entities in the text
        text_lower = risk_analysis.lower()

        # Extract specific threats, actors, and systems mentioned
        threat_entities = []

        # Pattern for specific entities (capitalized words that aren't generic)
        entity_patterns = [
            r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b',  # Proper nouns
            r'\b[A-Z]{2,}\b',  # Acronyms
        ]

        for pattern in entity_patterns:
            matches = re.findall(pattern, risk_analysis)
            threat_entities.extend(matches)

        # Filter out generic terms
        generic_terms = {'Security', 'Risk', 'Analysis', 'Assessment', 'Report', 'The', 'This', 'That', 'General', 'Overall', 'Current', 'Recent', 'Major', 'Critical', 'High', 'Medium', 'Low'}
        specific_entities = [entity for entity in threat_entities if entity not in generic_terms and len(entity) > 2]

        # Create specific risk indicators based on actual content
        if specific_entities:
            # Use first few specific entities to create targeted risks
            for i, entity in enumerate(specific_entities[:5]):
                risk_types = ['Attack Risk', 'Vulnerability Risk', 'Escalation Risk', 'Disruption Risk', 'Compromise Risk']
                risk_type = risk_types[i % len(risk_types)]

                indicators.append({
                    'factor': f"{entity} {risk_type}",
                    'likelihood': 'Medium',
                    'impact': 'High',
                    'timeframe': '72 hours',
                    'priority': 'High'
                })

        return indicators[:5]  # Limit to 5 indicators

    def _calculate_threat_level(self, data: StandardReport) -> str:
        """Calculate overall threat level based on report data."""
        score = 0

        # Factor in urgency level
        if data.urgency_level:
            urgency_scores = {'low': 1, 'medium': 2, 'high': 3, 'critical': 4}
            score += urgency_scores.get(data.urgency_level, 2)

        # Factor in confidence score
        if data.confidence_score >= 0.8:
            score += 2
        elif data.confidence_score >= 0.5:
            score += 1

        # Factor in text content indicators
        text_content = (data.bluf + ' ' + ' '.join(data.key_assessments)).lower()
        high_risk_terms = ['critical', 'urgent', 'immediate', 'escalation', 'attack', 'threat', 'violence']
        risk_count = sum(1 for term in high_risk_terms if term in text_content)
        score += min(risk_count, 3)

        # Calculate threat level
        if score >= 7:
            return "🔴 CRITICAL"
        elif score >= 5:
            return "🟠 HIGH"
        elif score >= 3:
            return "🟡 MEDIUM"
        else:
            return "🟢 LOW"

    def _generate_watch_points(self, data: StandardReport) -> List[str]:
        """Generate watch points for next 72 hours based on report content."""
        watch_points = []

        # Extract potential watch points from report content
        if data.threat_assessment:
            if 'escalation' in data.threat_assessment.lower():
                watch_points.append("Monitor for signs of escalation in threat levels")
            if 'attack' in data.threat_assessment.lower():
                watch_points.append("Heightened alert for potential attack indicators")

        if data.current_situation:
            if 'deteriorating' in data.current_situation.lower() or 'worsening' in data.current_situation.lower():
                watch_points.append("Track continued deterioration of current situation")

        # Add immediate action points as watch items
        if hasattr(data.recommendations, 'immediate_actions') and data.recommendations.immediate_actions:
            first_action = data.recommendations.immediate_actions[0]
            watch_points.append(f"Implementation of immediate action: {first_action[:50]}...")

        # Default watch points if none extracted
        if not watch_points:
            watch_points = [
                "Monitor for changes in key threat indicators",
                "Track implementation of recommended immediate actions",
                "Assess effectiveness of risk mitigation measures"
            ]

        return watch_points[:3]  # Limit to 3 watch points

    def _serialize_for_json(self, obj: Any) -> Any:
        """Serialize objects for JSON output."""
        if isinstance(obj, dict):
            return {k: self._serialize_for_json(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._serialize_for_json(item) for item in obj]
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif hasattr(obj, 'value'):  # Enum
            return obj.value
        else:
            return obj

    def _serialize_for_yaml(self, obj: Any) -> Any:
        """Serialize objects for YAML output."""
        if isinstance(obj, dict):
            return {k: self._serialize_for_yaml(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._serialize_for_yaml(item) for item in obj]
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif hasattr(obj, 'value'):  # Enum
            return obj.value
        else:
            return obj

    def _dict_to_xml(self, data: Dict[str, Any], parent: ET.Element) -> None:
        """Recursively convert dictionary to XML elements."""
        for key, value in data.items():
            # Clean key name for XML
            clean_key = key.replace(' ', '_').replace('-', '_')
            element = ET.SubElement(parent, clean_key)

            if isinstance(value, dict):
                self._dict_to_xml(value, element)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        item_element = ET.SubElement(element, "item")
                        self._dict_to_xml(item, item_element)
                    else:
                        item_element = ET.SubElement(element, "item")
                        item_element.text = str(item)
            elif isinstance(value, datetime):
                element.text = value.isoformat()
            elif hasattr(value, 'value'):  # Enum
                element.text = str(value.value)
            elif value is not None:
                element.text = str(value)

    def _get_css_styles(self, style: str = "default") -> str:
        """Get CSS styles for HTML output."""
        if style == "minimal":
            return self._minimal_css()
        elif style == "dark":
            return self._dark_css()
        else:
            return self._default_css()

    def _default_css(self) -> str:
        """Default CSS styles."""
        return """
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; margin: 0; padding: 20px; background-color: #f5f5f5; }
        .report-container { max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .classification-header { background: #d32f2f; color: white; padding: 10px; text-align: center; font-weight: bold; margin: -40px -40px 30px; border-radius: 8px 8px 0 0; }
        .report-title { color: #1976d2; border-bottom: 3px solid #1976d2; padding-bottom: 10px; margin-bottom: 20px; }
        .report-meta { background: #f8f9fa; padding: 15px; border-radius: 4px; margin-bottom: 30px; }
        .bluf-section { background: #e3f2fd; padding: 20px; border-radius: 4px; border-left: 4px solid #1976d2; margin-bottom: 30px; }
        .bluf-content { font-size: 1.1em; font-weight: 500; margin: 0; }
        .urgency-indicator { display: inline-block; padding: 5px 15px; border-radius: 20px; font-weight: bold; margin-top: 10px; }
        .urgency-low { background: #4caf50; color: white; }
        .urgency-medium { background: #ff9800; color: white; }
        .urgency-high { background: #f44336; color: white; }
        .urgency-critical { background: #b71c1c; color: white; animation: pulse 2s infinite; }
        @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.7; } 100% { opacity: 1; } }
        .findings-section, .recommendations-section { margin-bottom: 30px; }
        .findings-list, .recommendations-list { padding-left: 20px; }
        .findings-list li, .recommendations-list li { margin-bottom: 10px; }
        .additional-info { margin-bottom: 30px; }
        .entities-list, .tags-list { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }
        .entity-tag, .tag { background: #e0e0e0; padding: 4px 12px; border-radius: 16px; font-size: 0.9em; }
        .metadata-table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        .metadata-table td { padding: 10px; border: 1px solid #ddd; }
        .metadata-table td:first-child { font-weight: bold; background: #f5f5f5; width: 30%; }
        .report-footer { margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 0.9em; color: #666; text-align: center; }
        h2 { color: #333; border-bottom: 2px solid #e0e0e0; padding-bottom: 5px; }
        h3 { color: #555; }
        """

    def _minimal_css(self) -> str:
        """Minimal CSS styles."""
        return """
        body { font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; max-width: 800px; }
        .classification-header { background: #333; color: white; padding: 10px; text-align: center; }
        .urgency-critical { background: red; color: white; padding: 5px; }
        .urgency-high { background: orange; padding: 5px; }
        .urgency-medium { background: yellow; padding: 5px; }
        .urgency-low { background: green; color: white; padding: 5px; }
        table { border-collapse: collapse; width: 100%; }
        td { border: 1px solid #ddd; padding: 8px; }
        """

    def _dark_css(self) -> str:
        """Dark theme CSS styles."""
        return """
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; margin: 0; padding: 20px; background-color: #1a1a1a; color: #e0e0e0; }
        .report-container { max-width: 800px; margin: 0 auto; background: #2d2d2d; padding: 40px; border-radius: 8px; }
        .classification-header { background: #d32f2f; color: white; padding: 10px; text-align: center; font-weight: bold; margin: -40px -40px 30px; border-radius: 8px 8px 0 0; }
        .report-title { color: #64b5f6; border-bottom: 3px solid #64b5f6; padding-bottom: 10px; margin-bottom: 20px; }
        .report-meta { background: #383838; padding: 15px; border-radius: 4px; margin-bottom: 30px; }
        .bluf-section { background: #1e3a5f; padding: 20px; border-radius: 4px; border-left: 4px solid #64b5f6; margin-bottom: 30px; }
        .bluf-content { font-size: 1.1em; font-weight: 500; margin: 0; }
        .findings-section, .recommendations-section { margin-bottom: 30px; }
        .metadata-table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        .metadata-table td { padding: 10px; border: 1px solid #555; }
        .metadata-table td:first-child { font-weight: bold; background: #383838; }
        h2 { color: #e0e0e0; border-bottom: 2px solid #555; padding-bottom: 5px; }
        """


# Legacy compatibility function
def format_json(data, indent: int = 2) -> str:
    """Legacy JSON formatting function."""
    formatter = OutputFormatter()
    if hasattr(data, 'dict'):
        return formatter.format_json(data, indent=indent)
    else:
        return json.dumps(data, indent=indent, default=str)


def format_markdown(data, title: str = "Report") -> str:
    """Legacy Markdown formatting function."""
    formatter = OutputFormatter()
    if hasattr(data, 'dict'):
        return formatter.format_markdown(data, title=title)
    else:
        # Basic fallback for dict data
        lines = [f"# {title}", "", str(data)]
        return "\n".join(lines)