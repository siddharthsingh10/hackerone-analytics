# HackerOne Analytics - Metrics Dictionary

## Overview

This document provides detailed explanations of all metrics used in the HackerOne Analytics dashboard, including calculation logic, business significance, and interpretation guidelines.

## Core Metrics

### 1. Bounty Rate (bounty_percentage)

**Definition:** Percentage of reports that received monetary bounties

**Calculation:** `(bounty_reports / total_reports) * 100`

**Business Significance:**
- **Quality Indicator**: Higher rates suggest better report quality
- **Organization Performance**: Reflects how well organizations engage with researchers
- **Market Health**: Indicates overall platform effectiveness
- **Reporter Success**: Shows individual researcher effectiveness

**Interpretation:**
- **High (70%+)**: Excellent report quality or generous organization
- **Medium (30-70%)**: Standard performance range
- **Low (<30%)**: May indicate quality issues or strict criteria

**Example:** Mail.ru has 60.43% bounty rate (426 bounties out of 705 reports)

### 2. Average Vote Count (avg_vote_count)

**Definition:** Average number of community votes per report

**Calculation:** `AVG(vote_count) by grouping dimension`

**Business Significance:**
- **Community Engagement**: Higher votes indicate more interesting/valuable reports
- **Report Quality**: Correlates with report comprehensiveness and impact
- **Platform Activity**: Shows community participation levels
- **Vulnerability Interest**: Indicates which issues resonate with researchers

**Interpretation:**
- **High (50+ votes)**: Highly engaging or impactful vulnerabilities
- **Medium (10-50 votes)**: Standard community interest
- **Low (<10 votes)**: May indicate less critical or common issues

**Example:** Memory Corruption reports average 5.04 votes (technical, less accessible)

### 3. Total Reports

**Definition:** Count of all vulnerability reports in the dataset

**Calculation:** `COUNT(*) by grouping dimension`

**Business Significance:**
- **Volume Metrics**: Platform activity and engagement levels
- **Market Size**: Overall bug bounty ecosystem health
- **Organization Activity**: Individual organization engagement
- **Reporter Activity**: Individual researcher participation

**Interpretation:**
- **High Volume**: Active platform or organization
- **Low Volume**: May indicate new programs or declining activity

### 4. Bounty Reports

**Definition:** Count of reports that received monetary compensation

**Calculation:** `COUNT(*) WHERE bounty_amount > 0`

**Business Significance:**
- **Success Metrics**: Actual monetary value generated
- **Quality Filter**: Only reports meeting payout criteria
- **Economic Impact**: Direct financial value to researchers
- **Program Effectiveness**: Shows successful vulnerability discovery

## Vulnerability-Specific Metrics

### 5. Most Common Severity

**Definition:** Most frequently occurring severity level for a vulnerability type

**Calculation:** `MODE(severity) by weakness_name`

**Business Significance:**
- **Risk Assessment**: Understanding typical impact levels
- **Resource Planning**: Helps prioritize response efforts
- **Trend Analysis**: Shows if vulnerabilities are becoming more/less severe
- **Training Focus**: Guides security education priorities

**Severity Levels:**
- **Critical**: Immediate action required
- **High**: Significant security impact
- **Medium**: Moderate security concern
- **Low**: Minor security issue
- **None**: Informational only

### 6. Vulnerability Type Distribution

**Definition:** Breakdown of reports by vulnerability category

**Calculation:** `COUNT(*) GROUP BY weakness_name`

**Business Significance:**
- **Attack Vector Focus**: Shows most common attack methods
- **Defense Priorities**: Guides security investment decisions
- **Training Needs**: Identifies skills gaps in security teams
- **Tool Development**: Guides security tool priorities

## Organization Metrics

### 7. Organization Bounty Rate

**Definition:** Organization-specific percentage of reports receiving bounties

**Calculation:** `(bounty_reports / total_reports) * 100 BY team_handle`

**Business Significance:**
- **Program Effectiveness**: How well organizations run bug bounty programs
- **Quality Standards**: Reflects organization's security maturity
- **Competitive Benchmarking**: Compare against industry peers
- **Resource Allocation**: Guides program investment decisions

**Benchmarking:**
- **Top Performers**: 90%+ (Internet Bug Bounty: 91.97%)
- **Average**: 30-70% (Most organizations)
- **Low Performers**: <30% (U.S. Dept of Defense: 2.91%)

### 8. Organization Engagement Period

**Definition:** Time span from first to latest report

**Calculation:** `MAX(reported_at) - MIN(reported_at) BY team_handle`

**Business Significance:**
- **Program Longevity**: Shows sustained commitment to security
- **Maturity Assessment**: Longer programs typically more mature
- **Success Patterns**: Correlates with program effectiveness
- **Resource Planning**: Helps forecast long-term needs

### 9. Organization Volume Metrics

**Definition:** Total reports and bounties per organization

**Calculation:** `COUNT(*) BY team_handle`

**Business Significance:**
- **Program Scale**: Shows organization's bug bounty investment
- **Market Position**: Indicates relative program size
- **Resource Requirements**: Guides staffing and tool needs
- **Success Correlation**: Volume often correlates with program maturity

## Reporter Metrics

### 10. Reporter Validity Rate

**Definition:** Percentage of reporter's reports that are valid

**Calculation:** `(valid_reports / total_reports) * 100 BY reporter_username`

**Business Significance:**
- **Quality Assessment**: Individual reporter effectiveness
- **Talent Identification**: Helps identify top researchers
- **Training Needs**: Shows areas for reporter improvement
- **Program Success**: Correlates with overall program quality

**Quality Tiers:**
- **Elite (95%+)**: Top-tier researchers
- **Good (80-95%)**: Reliable contributors
- **Average (60-80%)**: Standard performance
- **Needs Improvement (<60%)**: May need training/support

### 11. Reporter Specialization

**Definition:** Primary vulnerability focus area for each reporter

**Calculation:** `MODE(weakness_name) BY reporter_username`

**Business Significance:**
- **Expertise Mapping**: Identifies specialist researchers
- **Resource Allocation**: Guides program focus areas
- **Training Planning**: Shows skill development opportunities
- **Community Building**: Helps connect researchers with similar interests

### 12. Reporter Engagement Period

**Definition:** Time span of reporter's activity

**Calculation:** `MAX(reported_at) - MIN(reported_at) BY reporter_username`

**Business Significance:**
- **Community Retention**: Shows long-term engagement
- **Experience Level**: Correlates with report quality
- **Program Loyalty**: Indicates program satisfaction
- **Success Patterns**: Longer engagement often means better results

## Time-Based Metrics

### 13. Monthly Report Volume

**Definition:** Number of reports submitted per month

**Calculation:** `COUNT(*) BY DATE_TRUNC('month', reported_at)`

**Business Significance:**
- **Trend Analysis**: Shows platform growth/decline
- **Seasonal Patterns**: Identifies cyclical behavior
- **Growth Planning**: Guides resource allocation
- **Success Measurement**: Tracks program expansion

### 14. Monthly Bounty Rate

**Definition:** Percentage of reports receiving bounties per month

**Calculation:** `(bounty_count / report_count) * 100 BY month`

**Business Significance:**
- **Quality Trends**: Shows if report quality is improving
- **Program Evolution**: Reflects changing standards
- **Market Dynamics**: Indicates competitive landscape changes
- **Success Metrics**: Tracks program effectiveness over time

### 15. Vulnerability Evolution

**Definition:** Changes in vulnerability type popularity over time

**Calculation:** `COUNT(*) BY year_month, weakness_name`

**Business Significance:**
- **Threat Landscape**: Shows evolving attack vectors
- **Defense Priorities**: Guides security investment
- **Training Focus**: Identifies emerging skill needs
- **Tool Development**: Guides security tool priorities

## Composite Metrics

### 16. Organization Performance Score

**Definition:** Combined metric of volume, quality, and engagement

**Calculation:** `(bounty_rate * 0.4) + (log(total_reports) * 0.3) + (engagement_period_days * 0.3)`

**Business Significance:**
- **Benchmarking**: Comprehensive organization comparison
- **Resource Allocation**: Guides program investment decisions
- **Success Measurement**: Holistic program evaluation
- **Competitive Analysis**: Market position assessment

### 17. Reporter Quality Index

**Definition:** Combined metric of validity, bounty success, and engagement

**Calculation:** `(validity_rate * 0.4) + (bounty_percentage * 0.4) + (avg_vote_count / 100 * 0.2)`

**Business Significance:**
- **Talent Identification**: Find top researchers
- **Program Success**: Correlates with overall quality
- **Resource Allocation**: Guide program focus
- **Community Building**: Identify key contributors

## Data Quality Metrics

### 18. Null Value Rates

**Definition:** Percentage of missing data in key fields

**Calculation:** `COUNT(*) WHERE field IS NULL / COUNT(*) * 100`

**Business Significance:**
- **Data Reliability**: Indicates data quality issues
- **Processing Needs**: Shows required data cleaning
- **Reporting Accuracy**: Affects metric reliability
- **System Improvements**: Identifies platform enhancement needs

**Key Findings:**
- **weakness_name**: 11.8% null (1,190 reports)
- **team_name**: 12.9% null (423 organizations)
- **severity**: Significant missing data
- **verification_status**: Some incomplete data

### 19. Data Consistency Checks

**Definition:** Validation of calculated metrics

**Calculation:** Various cross-checks and sanity tests

**Business Significance:**
- **Data Integrity**: Ensures reliable reporting
- **System Health**: Identifies processing issues
- **Trust Building**: Maintains stakeholder confidence
- **Quality Assurance**: Validates metric accuracy

## Interpretation Guidelines

### High-Value Insights

1. **Information Disclosure Dominance**: 1,010 reports (47.72% bounty rate)
   - *Implication*: Focus security training on information handling
   - *Action*: Implement better data classification and access controls

2. **Memory Corruption High Bounty Rate**: 85.66% bounty rate
   - *Implication*: Critical vulnerabilities receive higher rewards
   - *Action*: Prioritize memory safety in development practices

3. **Organization Maturity Correlation**: Longer programs have higher bounty rates
   - *Implication*: Program maturity improves outcomes
   - *Action*: Invest in program development and process improvement

### Strategic Recommendations

1. **Focus on Top Vulnerability Types**: Information Disclosure, XSS, Authentication
2. **Nurture High-Quality Reporters**: Those with >96% validity rates
3. **Help Low-Performing Organizations**: Those with <30% bounty rates
4. **Develop Predictive Models**: Based on time trends and patterns

## Technical Notes

### Calculation Precision
- All percentages calculated to 2 decimal places
- Averages computed using arithmetic mean
- Null values excluded from calculations where appropriate

### Performance Considerations
- Aggregations pre-calculated for dashboard performance
- Caching implemented for real-time filtering
- Indexed queries for large dataset efficiency

### Data Freshness
- Data processed from HuggingFace dataset
- Timestamp-based filtering for recent analysis
- Version control for historical comparisons 