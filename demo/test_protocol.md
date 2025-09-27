# IntelliReport Test Protocol

## FUNCTIONAL TESTS

### Analysis Modes
- [ ] **Single Document Mode** - processes clean report
  - Upload single document
  - Verify standard analysis pipeline
  - Check all output sections populated

- [ ] **Multi-Source Synthesis** - identifies patterns across 2+ docs
  - Upload 2+ documents
  - Verify cross-document pattern identification
  - Check synthesis results in analytical trail
  - Confirm document count display

- [ ] **Web-Enhanced** - adds verification tags
  - Select web-enhanced mode
  - Verify web search terms extracted
  - Check verification status in report
  - Confirm web search indicators in analytical trail

- [ ] **Red Team Mode** - provides contrarian analysis
  - Select red team mode
  - Verify contrarian perspectives generated
  - Check devil's advocacy in techniques tab
  - Confirm alternative hypotheses presented

### Tone Variations
- [ ] **Professional Tone** - formal intelligence community language
  - Test geopolitical risk assessment focus
  - Verify IC terminology usage
  - Check structured analytical techniques

- [ ] **Corporate Tone** - business-focused, risk-oriented
  - Test business continuity focus
  - Verify asset protection emphasis
  - Check executive protection considerations

- [ ] **Humanitarian Tone** - field safety emphasis
  - Test mission continuity focus
  - Verify volunteer safety considerations
  - Check operational security analysis

### Redaction System
- [ ] **Redaction Toggle ON** - removes PII when enabled
  - Enable redaction
  - Upload document with names, emails, phone numbers
  - Verify sensitive data removed from formatted report
  - Check redaction summary in analytical trail

- [ ] **Redaction Toggle OFF** - keeps all information intact
  - Disable redaction
  - Upload same document
  - Verify all information preserved

## QUALITY TESTS

### Report Structure
- [ ] **BLUF answers all W's + action required**
  - WHAT is happening (event/threat)
  - WHO is involved (actors/targets)
  - WHERE is it occurring (specific locations)
  - WHEN did/will it occur (timeframe)
  - WHY is it happening (motivations/causes)
  - WHAT ACTION is required (decision-maker response)

- [ ] **Key Findings** - shows actual content, not numbers/arrays
  - Verify proper text display
  - Check no JSON brackets or Python arrays
  - Confirm prose format

- [ ] **Recommendations** - properly formatted sections
  - Verify immediate actions as bullet points
  - Check risk mitigation as bullet points
  - Confirm collection priorities as bullet points
  - Verify decision points as bullet points

### Intelligence Standards
- [ ] **Confidence levels match IC standards (ICD 203)**
  - Low Confidence: 0-30%
  - Moderate Confidence: 31-70%
  - High Confidence: 71-100%
  - Verify calculation display format

- [ ] **Risk Matrix shows 4-6 specific risks**
  - Verify specific risk names (not generic)
  - Check columns: Risk Factor | Likelihood | Impact | Timeframe | Priority
  - Confirm no "Violence Risk" or "General Security Risk"

- [ ] **Intelligence gaps are prioritized**
  - Verify 5-7 gaps identified
  - Check Critical/High/Medium prioritization
  - Confirm collection difficulty assessment

- [ ] **Collection priorities include methods**
  - Verify SIGINT/HUMINT/OSINT/GEOINT/IMINT specification
  - Check expected timeline inclusion
  - Confirm specific targets/sources identified

- [ ] **Source reliability uses proper scale**
  - Reliability: A (Completely reliable) to F (Cannot be judged)
  - Credibility: 1 (Confirmed) to 6 (Cannot be judged)
  - Verify IC standards compliance

### Analytical Metadata
- [ ] **Techniques Tab** - shows only standard SATs
  - ACH (Analysis of Competing Hypotheses)
  - Key Assumptions Check
  - Quality of Information Check
  - What-If Analysis
  - Devil's Advocacy (Red Team only)

- [ ] **Hypotheses Tab** - document-specific content
  - No generic responses like "diplomatic response"
  - References actual entities and events
  - Uses real document content

- [ ] **Assumptions Tab** - extracted with contrarian format
  - Format: "Assumption: [text] | Alternative: [contrarian view] | Impact: [HIGH/MEDIUM/LOW]"
  - Based on actual document content
  - Provides contrarian viewpoints

- [ ] **Sources Tab** - proper intelligence metadata
  - Documents processed count
  - Content volume (word/character count)
  - Source reliability rating (A-F scale)
  - Processing issues identified

## EDGE CASES

### Document Size Handling
- [ ] **Handles reports <500 words**
  - Upload short document
  - Verify all sections populated
  - Check quality warnings if applicable

- [ ] **Handles reports >10,000 words**
  - Upload large document
  - Verify processing completion
  - Check no truncation occurs
  - Confirm performance acceptable

### Content Complexity
- [ ] **Processes non-English names correctly**
  - Upload document with foreign names/places
  - Verify proper entity extraction
  - Check name preservation in redacted mode

- [ ] **Manages conflicting information properly**
  - Upload documents with contradictory claims
  - Verify contradiction identification
  - Check analytical handling in multi-source mode

### Technical Robustness
- [ ] **API Error Handling**
  - Test with invalid API keys
  - Verify graceful error messages
  - Check system recovery

- [ ] **File Format Support**
  - Test .txt files
  - Test .pdf files (if supported)
  - Test .docx files (if supported)
  - Verify encoding handling

### User Interface
- [ ] **Navigation Functionality**
  - Verify all tabs accessible
  - Check expander sections work
  - Confirm download/copy buttons function

- [ ] **Error Messages**
  - Clear error descriptions
  - Actionable user guidance
  - No system crashes

## PERFORMANCE BENCHMARKS

### Processing Times
- [ ] **Single Document (1,000 words)** - Target: <30 seconds
- [ ] **Multi-Source (3 documents)** - Target: <60 seconds
- [ ] **Web-Enhanced Mode** - Target: <90 seconds
- [ ] **Red Team Analysis** - Target: <45 seconds

### Output Quality
- [ ] **Recommendations Display** - No Python arrays visible
- [ ] **JSON Bracket Removal** - Clean text in all sections
- [ ] **Entity List Hiding** - Backend only, not in formatted report
- [ ] **Prose Formatting** - Flowing text, not bullet points

## REGRESSION TESTS

### After Code Changes
- [ ] **Core functionality preserved** - All modes work
- [ ] **Output format consistent** - No formatting regressions
- [ ] **Performance maintained** - No significant slowdowns
- [ ] **Error handling intact** - Graceful failure modes

---

## TEST COMPLETION CHECKLIST

**Functional Tests:** ___/11 passed
**Quality Tests:** ___/12 passed
**Edge Cases:** ___/8 passed
**Performance:** ___/4 benchmarks met

**Overall System Status:** ⬜ PASS ⬜ FAIL ⬜ NEEDS REVIEW

**Tested By:** ________________
**Date:** ________________
**Version:** ________________