#!/usr/bin/env python3
import pandas as pd
import json

# Load processed data
vulnerability_summary = pd.read_csv('data/processed/vulnerability_summary.csv')
org_metrics = pd.read_csv('data/processed/organization_metrics.csv')
reporter_analytics = pd.read_csv('data/processed/reporter_analytics.csv')
time_trends = pd.read_csv('data/processed/time_trends.csv')

# Calculate key metrics
total_reports = int(vulnerability_summary['total_reports'].sum())
total_bounties = int(vulnerability_summary['bounty_reports'].sum())
overall_bounty_rate = round((total_bounties / total_reports * 100), 2)

# Get top performers
top_vuln = str(vulnerability_summary.iloc[0]['weakness_name'])
top_org = str(org_metrics.iloc[0]['team_name'])
top_reporter = str(reporter_analytics.iloc[0]['username'])

# Create insights dictionary
insights = {
    'total_reports': total_reports,
    'total_bounties': total_bounties,
    'overall_bounty_rate': overall_bounty_rate,
    'unique_organizations': int(len(org_metrics)),
    'active_reporters': int(len(reporter_analytics)),
    'vulnerability_types': int(len(vulnerability_summary)),
    'top_vulnerability': top_vuln,
    'top_organization': top_org,
    'top_reporter': top_reporter
}

# Save insights
with open('data/processed/key_insights.json', 'w') as f:
    json.dump(insights, f, indent=2)

print("Key insights generated and saved!")
print(f"Total Reports: {total_reports:,}")
print(f"Total Bounties: {total_bounties:,}")
print(f"Bounty Rate: {overall_bounty_rate}%")
print(f"Organizations: {len(org_metrics)}")
print(f"Reporters: {len(reporter_analytics)}")
print(f"Vulnerability Types: {len(vulnerability_summary)}") 