#!/usr/bin/env python3
"""
Data Processing Script for HackerOne Analytics Assignment
Creates source of truth tables from raw dataset
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime
import os
import warnings
import ast
import re
warnings.filterwarnings('ignore')

def clean_json_string(s):
    """Clean JSON string to make it parseable"""
    if pd.isna(s) or not isinstance(s, str):
        return '{}'
    
    # Replace numpy array calls with empty lists
    s = re.sub(r'array\(\[\], dtype=object\)', '[]', s)
    s = re.sub(r'array\(\[.*?\], dtype=object\)', '[]', s)
    
    # Replace None with null for JSON compatibility
    s = s.replace('None', 'null')
    s = s.replace('True', 'true')
    s = s.replace('False', 'false')
    
    # Convert single quotes to double quotes for JSON compatibility
    s = s.replace("'", '"')
    
    return s

def parse_json_column(series):
    """Parse JSON-like strings in a pandas series"""
    parsed = []
    for item in series:
        if pd.isna(item) or item is None:
            parsed.append({})
        elif isinstance(item, str):
            try:
                # Clean the string first
                cleaned_item = clean_json_string(item)
                # Try to parse as JSON
                parsed.append(json.loads(cleaned_item))
            except:
                try:
                    # Fallback to literal_eval
                    parsed.append(ast.literal_eval(item))
                except:
                    parsed.append({})
        else:
            parsed.append(item)
    return parsed

def main():
    print("=== DATA PROCESSING START ===")
    
    # Load the raw dataset
    df = pd.read_csv('data/raw/hackerone_disclosed_reports.csv')
    print(f"Loaded dataset with shape: {df.shape}")
    
    # Parse JSON columns
    print("\n=== PARSING JSON COLUMNS ===")
    json_columns = ['reporter', 'team', 'weakness', 'structured_scope']
    for col in json_columns:
        if col in df.columns:
            print(f"Parsing {col}...")
            df[f'{col}_parsed'] = parse_json_column(df[col])
    
    print("JSON parsing complete!")
    
    # Extract key fields from parsed JSON
    print("\n=== EXTRACTING FIELDS ===")
    
    # Reporter information
    df['reporter_username'] = df['reporter_parsed'].apply(lambda x: x.get('username', '') if isinstance(x, dict) else '')
    df['reporter_verified'] = df['reporter_parsed'].apply(lambda x: x.get('verified', False) if isinstance(x, dict) else False)
    df['reporter_cleared'] = df['reporter_parsed'].apply(lambda x: x.get('cleared', False) if isinstance(x, dict) else False)
    
    # Team/Organization information - handle single team dictionary
    def extract_team_info(team_data):
        if isinstance(team_data, dict):
            return {
                'handle': team_data.get('handle', ''),
                'name': team_data.get('profile', {}).get('name', '') if isinstance(team_data.get('profile'), dict) else '',
                'offers_bounties': team_data.get('offers_bounties', False)
            }
        elif isinstance(team_data, list) and len(team_data) > 0:
            team = team_data[0]  # Take the first team if it's a list
            return {
                'handle': team.get('handle', ''),
                'name': team.get('profile', {}).get('name', '') if isinstance(team.get('profile'), dict) else '',
                'offers_bounties': team.get('offers_bounties', False)
            }
        else:
            return {'handle': '', 'name': '', 'offers_bounties': False}
    
    team_info = df['team_parsed'].apply(extract_team_info)
    df['team_handle'] = team_info.apply(lambda x: x['handle'])
    df['team_name'] = team_info.apply(lambda x: x['name'])
    df['team_offers_bounties'] = team_info.apply(lambda x: x['offers_bounties'])
    
    # Weakness information
    df['weakness_id'] = df['weakness_parsed'].apply(lambda x: x.get('id', '') if isinstance(x, dict) else '')
    df['weakness_name'] = df['weakness_parsed'].apply(lambda x: x.get('name', '') if isinstance(x, dict) else '')
    
    # Structured scope information
    df['scope_asset_type'] = df['structured_scope_parsed'].apply(lambda x: x.get('asset_type', '') if isinstance(x, dict) else '')
    df['scope_max_severity'] = df['structured_scope_parsed'].apply(lambda x: x.get('max_severity', '') if isinstance(x, dict) else '')
    df['scope_asset_identifier'] = df['structured_scope_parsed'].apply(lambda x: x.get('asset_identifier', '') if isinstance(x, dict) else '')
    
    print("Field extraction complete!")
    
    # Convert date columns
    print("\n=== PROCESSING DATES ===")
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
    df['disclosed_at'] = pd.to_datetime(df['disclosed_at'], errors='coerce')
    
    # Add time-based features
    df['year'] = df['created_at'].dt.year
    df['month'] = df['created_at'].dt.month
    df['year_month'] = df['created_at'].dt.to_period('M')
    
    print("Date processing complete!")
    
    # Create Source of Truth Table 1: Vulnerability Summary
    print("\n=== CREATING VULNERABILITY SUMMARY ===")
    vulnerability_summary = df.groupby('weakness_name').agg({
        'id': 'count',
        'has_bounty?': 'sum',
        'vote_count': 'mean',
        'scope_max_severity': lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else 'unknown'
    }).reset_index()
    
    vulnerability_summary.columns = ['weakness_name', 'total_reports', 'bounty_reports', 'avg_vote_count', 'most_common_severity']
    vulnerability_summary['bounty_percentage'] = (vulnerability_summary['bounty_reports'] / vulnerability_summary['total_reports'] * 100).round(2)
    vulnerability_summary = vulnerability_summary.sort_values('total_reports', ascending=False)
    
    print(f"Created vulnerability summary with {len(vulnerability_summary)} vulnerability types")
    
    # Create Source of Truth Table 2: Organization Metrics
    print("\n=== CREATING ORGANIZATION METRICS ===")
    org_metrics = df.groupby('team_handle').agg({
        'id': 'count',
        'has_bounty?': 'sum',
        'vote_count': 'mean',
        'created_at': ['min', 'max'],
        'team_name': 'first'
    }).reset_index()
    
    org_metrics.columns = ['team_handle', 'total_reports', 'bounty_reports', 'avg_vote_count', 'first_report', 'latest_report', 'team_name']
    org_metrics['bounty_percentage'] = (org_metrics['bounty_reports'] / org_metrics['total_reports'] * 100).round(2)
    org_metrics = org_metrics.sort_values('total_reports', ascending=False)
    
    print(f"Created organization metrics with {len(org_metrics)} organizations")
    
    # Create Source of Truth Table 3: Reporter Analytics
    print("\n=== CREATING REPORTER ANALYTICS ===")
    reporter_analytics = df.groupby('reporter_username').agg({
        'id': 'count',
        'substate': lambda x: (x == 'resolved').sum(),
        'vote_count': 'mean',
        'reporter_verified': 'first',
        'reporter_cleared': 'first',
        'weakness_name': lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else 'unknown'
    }).reset_index()
    
    reporter_analytics.columns = ['username', 'total_reports', 'valid_reports', 'avg_vote_count', 'verified_status', 'cleared_status', 'specialization']
    reporter_analytics['valid_percentage'] = (reporter_analytics['valid_reports'] / reporter_analytics['total_reports'] * 100).round(2)
    reporter_analytics = reporter_analytics.sort_values('total_reports', ascending=False)
    
    print(f"Created reporter analytics with {len(reporter_analytics)} reporters")
    
    # Create Source of Truth Table 4: Time Trends
    print("\n=== CREATING TIME TRENDS ===")
    time_trends = df.groupby(['year_month', 'weakness_name']).agg({
        'id': 'count',
        'has_bounty?': 'sum',
        'team_handle': 'nunique'
    }).reset_index()
    
    time_trends.columns = ['year_month', 'vulnerability_type', 'report_count', 'bounty_count', 'organization_count']
    time_trends['bounty_percentage'] = (time_trends['bounty_count'] / time_trends['report_count'] * 100).round(2)
    time_trends = time_trends.sort_values(['year_month', 'report_count'], ascending=[True, False])
    
    print(f"Created time trends with {len(time_trends)} time-vulnerability combinations")
    
    # Save all source of truth tables
    print("\n=== SAVING TABLES ===")
    PROCESSED_DIR = 'data/processed'
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    
    # Save tables
    vulnerability_summary.to_csv(f'{PROCESSED_DIR}/vulnerability_summary.csv', index=False)
    org_metrics.to_csv(f'{PROCESSED_DIR}/organization_metrics.csv', index=False)
    reporter_analytics.to_csv(f'{PROCESSED_DIR}/reporter_analytics.csv', index=False)
    time_trends.to_csv(f'{PROCESSED_DIR}/time_trends.csv', index=False)
    
    print("All source of truth tables saved to data/processed/")
    
    # Summary statistics
    print("\n=== SOURCE OF TRUTH TABLES SUMMARY ===")
    print(f"1. Vulnerability Summary: {len(vulnerability_summary)} vulnerability types")
    print(f"2. Organization Metrics: {len(org_metrics)} organizations")
    print(f"3. Reporter Analytics: {len(reporter_analytics)} reporters")
    print(f"4. Time Trends: {len(time_trends)} time-vulnerability combinations")
    
    print("\n=== TOP VULNERABILITY TYPES ===")
    print(vulnerability_summary.head(5)[['weakness_name', 'total_reports', 'bounty_percentage']])
    
    print("\n=== TOP ORGANIZATIONS ===")
    print(org_metrics.head(5)[['team_name', 'total_reports', 'bounty_percentage']])
    
    print("\n=== TOP REPORTERS ===")
    print(reporter_analytics.head(5)[['username', 'total_reports', 'valid_percentage']])

if __name__ == "__main__":
    main() 