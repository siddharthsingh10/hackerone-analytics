# HackerOne Analytics - Source of Truth Tables Schema

## Overview

This document describes the structure and schema of the four source of truth tables created for the HackerOne Analytics Engineer assignment. These tables serve as the foundation for data democratization and enable self-service analytics across the organization.

## Table 1: vulnerability_summary.csv

**Purpose:** Aggregated vulnerability type analysis and performance metrics

**Schema:**
| Column | Type | Description | Calculation Logic |
|--------|------|-------------|-------------------|
| `weakness_name` | String | Vulnerability type/category | Grouped from raw report data |
| `total_reports` | Integer | Total number of reports for this vulnerability type | COUNT(*) by weakness_name |
| `bounty_reports` | Integer | Number of reports that received bounties | COUNT(*) where bounty_amount > 0 |
| `avg_vote_count` | Float | Average community votes per report | AVG(vote_count) by weakness_name |
| `most_common_severity` | String | Most frequently occurring severity level | MODE(severity) by weakness_name |
| `bounty_percentage` | Float | Percentage of reports that received bounties | (bounty_reports / total_reports) * 100 |

**Key Insights:**
- **Information Disclosure** dominates with 1,010 reports (47.72% bounty rate)
- **Cross-site Scripting (XSS)** variants are highly prevalent
- **Memory Corruption** has highest bounty rate at 85.66%
- Average vote count varies significantly by vulnerability type

**Dashboard Mapping:**
- Overview page: Top vulnerability types chart
- Vulnerability Analysis: Interactive filtering and exploration
- Insights: Strategic recommendations based on patterns

## Table 2: organization_metrics.csv

**Purpose:** Organization-level performance and engagement metrics

**Schema:**
| Column | Type | Description | Calculation Logic |
|--------|------|-------------|-------------------|
| `team_handle` | String | Organization's HackerOne handle | Unique identifier from raw data |
| `total_reports` | Integer | Total reports submitted to this organization | COUNT(*) by team_handle |
| `bounty_reports` | Integer | Reports that received bounties | COUNT(*) where bounty_amount > 0 |
| `avg_vote_count` | Float | Average community engagement | AVG(vote_count) by team_handle |
| `first_report` | DateTime | Date of first report received | MIN(reported_at) by team_handle |
| `latest_report` | DateTime | Date of most recent report | MAX(reported_at) by team_handle |
| `team_name` | String | Organization's display name | From raw data |
| `bounty_percentage` | Float | Organization's bounty rate | (bounty_reports / total_reports) * 100 |

**Key Insights:**
- **Mail.ru** leads with 705 total reports (60.43% bounty rate)
- **Internet Bug Bounty** has highest bounty rate at 91.97%
- **U.S. Dept of Defense** has lowest bounty rate at 2.91%
- Organizations show significant variation in engagement patterns

**Dashboard Mapping:**
- Organization Metrics page: Performance benchmarking
- Overview: Key organizational statistics
- Time Trends: Temporal analysis of organization activity

## Table 3: reporter_analytics.csv

**Purpose:** Individual reporter performance and quality metrics

**Schema:**
| Column | Type | Description | Calculation Logic |
|--------|------|-------------|-------------------|
| `reporter_username` | String | Reporter's HackerOne username | Unique identifier |
| `total_reports` | Integer | Total reports submitted by this reporter | COUNT(*) by reporter_username |
| `bounty_reports` | Integer | Reports that received bounties | COUNT(*) where bounty_amount > 0 |
| `avg_vote_count` | Float | Average community engagement | AVG(vote_count) by reporter_username |
| `validity_rate` | Float | Percentage of valid reports | (valid_reports / total_reports) * 100 |
| `verification_status` | String | Reporter's verification status | From raw data |
| `specialization` | String | Primary vulnerability focus area | MODE(weakness_name) by reporter |
| `first_report_date` | DateTime | Date of first report | MIN(reported_at) by reporter_username |
| `latest_report_date` | DateTime | Date of most recent report | MAX(reported_at) by reporter_username |
| `bounty_percentage` | Float | Reporter's bounty success rate | (bounty_reports / total_reports) * 100 |

**Key Insights:**
- Top reporters achieve >96% validity rates
- Verification status correlates with report quality
- Specialization patterns show reporter expertise areas
- Community engagement varies significantly by reporter

**Dashboard Mapping:**
- Reporter Analytics page: Individual performance analysis
- Community insights and quality metrics
- Talent identification and community building

## Table 4: time_trends.csv

**Purpose:** Temporal analysis of vulnerability patterns and trends

**Schema:**
| Column | Type | Description | Calculation Logic |
|--------|------|-------------|-------------------|
| `year_month` | String | Year-month combination (YYYY-MM) | DATE_TRUNC('month', reported_at) |
| `weakness_name` | String | Vulnerability type | From raw data |
| `report_count` | Integer | Number of reports in this month | COUNT(*) by year_month, weakness_name |
| `bounty_count` | Integer | Number of bounties awarded | COUNT(*) where bounty_amount > 0 |
| `avg_vote_count` | Float | Average community engagement | AVG(vote_count) by year_month, weakness_name |
| `bounty_rate` | Float | Monthly bounty rate | (bounty_count / report_count) * 100 |
| `organization_count` | Integer | Number of organizations affected | COUNT(DISTINCT team_handle) |

**Key Insights:**
- Seasonal patterns in vulnerability reporting
- Evolution of vulnerability types over time
- Organization participation trends
- Community engagement fluctuations

**Dashboard Mapping:**
- Time Trends page: Temporal analysis and forecasting
- Trend identification and pattern recognition
- Strategic planning based on historical data

## Data Quality Assessment

### Null Value Analysis
- **weakness_name**: 1,190 reports (11.8%) have null/empty vulnerability types
- **team_name**: 423 organizations (12.9%) have missing display names
- **severity**: Significant portion of reports lack severity classification
- **verification_status**: Some reporters have incomplete verification data

### Data Cleaning Applied
1. **Null Handling**: Replaced null values with appropriate defaults
2. **String Normalization**: Standardized vulnerability type names
3. **Date Parsing**: Converted timestamp strings to proper datetime objects
4. **Duplicate Removal**: Eliminated duplicate entries based on unique identifiers

### Validation Checks
- **Referential Integrity**: Ensured all foreign keys have valid references
- **Data Range Validation**: Verified date ranges and numeric value bounds
- **Consistency Checks**: Validated calculated percentages sum correctly
- **Outlier Detection**: Identified and handled extreme values appropriately

## Dashboard Integration

### Data Flow Architecture
```
Raw JSON Data → Data Processing Pipeline → Source of Truth Tables → Streamlit Dashboard
```

### Real-time Updates
- Dashboard loads data from CSV files on each session
- Caching implemented for performance optimization
- Interactive filtering preserves data integrity

### Performance Optimization
- **Caching**: Streamlit cache_data decorator for efficient loading
- **Indexing**: Optimized queries for large datasets
- **Aggregation**: Pre-calculated metrics reduce computation time

## Business Impact

### Data Democratization Achieved
- **Self-service Analytics**: Teams can explore data independently
- **Standardized Metrics**: Consistent reporting across organization
- **Real-time Insights**: Interactive exploration capabilities
- **Scalable Architecture**: Ready for production deployment

### Strategic Value
- **Market Intelligence**: Vulnerability trend analysis
- **Performance Benchmarking**: Organization comparison framework
- **Quality Metrics**: Reporter performance evaluation
- **Predictive Insights**: Future threat forecasting capabilities

## Technical Specifications

### File Formats
- **Input**: JSON files from HuggingFace dataset
- **Output**: CSV files for maximum compatibility
- **Processing**: Python pandas for data manipulation

### Scalability Considerations
- **Modular Design**: Easy to extend with new data sources
- **Performance**: Optimized for datasets up to 100K records
- **Maintenance**: Clear documentation and version control

### Security & Privacy
- **Data Anonymization**: Sensitive information removed
- **Access Control**: Dashboard-level security implementation
- **Audit Trail**: Complete data processing documentation 