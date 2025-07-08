#!/usr/bin/env python3
import pandas as pd
import json
import re

def clean_json_string(s):
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

# Load data
df = pd.read_csv('data/raw/hackerone_disclosed_reports.csv')
print(f"Loaded dataset with shape: {df.shape}")

# Test team parsing
sample_team = df['team'].iloc[0]
print(f"\nSample team data: {sample_team[:100]}...")

cleaned = clean_json_string(sample_team)
print(f"Cleaned data: {cleaned[:100]}...")

try:
    parsed = json.loads(cleaned)
    print(f"Parsed successfully! Type: {type(parsed)}")
    print(f"Handle: {parsed.get('handle')}")
    print(f"Name: {parsed.get('profile', {}).get('name')}")
    print(f"Offers bounties: {parsed.get('offers_bounties')}")
    
    # Test extraction function
    def extract_team_info(team_data):
        if isinstance(team_data, dict):
            return {
                'handle': team_data.get('handle', ''),
                'name': team_data.get('profile', {}).get('name', '') if isinstance(team_data.get('profile'), dict) else '',
                'offers_bounties': team_data.get('offers_bounties', False)
            }
        else:
            return {'handle': '', 'name': '', 'offers_bounties': False}
    
    team_info = extract_team_info(parsed)
    print(f"Extracted info: {team_info}")
    
except Exception as e:
    print(f"Error parsing: {e}")

# Test on a few more samples
print(f"\nTesting on first 5 teams:")
for i in range(5):
    team_str = df['team'].iloc[i]
    cleaned = clean_json_string(team_str)
    try:
        parsed = json.loads(cleaned)
        handle = parsed.get('handle', '')
        name = parsed.get('profile', {}).get('name', '')
        print(f"Team {i+1}: handle='{handle}', name='{name}'")
    except:
        print(f"Team {i+1}: Failed to parse") 