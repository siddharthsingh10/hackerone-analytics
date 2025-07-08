#!/usr/bin/env python3
"""
HackerOne Analytics Dashboard
Interactive dashboard for exploring vulnerability reports and insights
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime
import numpy as np

# Page configuration
st.set_page_config(
    page_title="HackerOne Analytics Dashboard",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .insight-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #1f77b4;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load all source of truth tables"""
    try:
        vulnerability_summary = pd.read_csv('data/processed/vulnerability_summary.csv')
        org_metrics = pd.read_csv('data/processed/organization_metrics.csv')
        reporter_analytics = pd.read_csv('data/processed/reporter_analytics.csv')
        time_trends = pd.read_csv('data/processed/time_trends.csv')
        
        # Load key insights
        try:
            with open('data/processed/key_insights.json', 'r') as f:
                key_insights = json.load(f)
        except:
            key_insights = {}
        
        return vulnerability_summary, org_metrics, reporter_analytics, time_trends, key_insights
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None, None, {}

def get_first_valid(series):
    for val in series:
        if pd.notna(val) and isinstance(val, str) and val.lower() not in ["none", "null", "nan", "unknown", ""]:
            return val
    return "Unknown"

def main():
    # Header
    st.markdown('<h1 class="main-header">🔒 HackerOne Analytics Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("### Senior Analytics Engineer Assignment - Data Democratization & Insights")
    
    # Load data
    vulnerability_summary, org_metrics, reporter_analytics, time_trends, key_insights = load_data()
    
    if vulnerability_summary is None:
        st.error("Failed to load data. Please ensure the data processing script has been run.")
        return
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a section:",
        ["📊 Overview", "🔍 Vulnerability Analysis", "🏢 Organization Metrics", 
         "👥 Reporter Analytics", "📈 Time Trends", "💡 Insights & Recommendations"]
    )
    
    # Overview Page
    if page == "📊 Overview":
        show_overview(vulnerability_summary, org_metrics, reporter_analytics, key_insights)
    
    # Vulnerability Analysis Page
    elif page == "🔍 Vulnerability Analysis":
        show_vulnerability_analysis(vulnerability_summary, time_trends)
    
    # Organization Metrics Page
    elif page == "🏢 Organization Metrics":
        show_organization_metrics(org_metrics)
    
    # Reporter Analytics Page
    elif page == "👥 Reporter Analytics":
        show_reporter_analytics(reporter_analytics)
    
    # Time Trends Page
    elif page == "📈 Time Trends":
        show_time_trends(time_trends)
    
    # Insights Page
    elif page == "💡 Insights & Recommendations":
        show_insights_and_recommendations(vulnerability_summary, org_metrics, reporter_analytics)

def show_overview(vulnerability_summary, org_metrics, reporter_analytics, key_insights):
    """Display overview dashboard with key metrics"""
    st.header("📊 Executive Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_reports = vulnerability_summary['total_reports'].sum()
        st.metric("Total Reports", f"{total_reports:,}")
    
    with col2:
        total_bounties = vulnerability_summary['bounty_reports'].sum()
        st.metric("Total Bounties", f"{total_bounties:,}")
    
    with col3:
        bounty_rate = (total_bounties / total_reports * 100).round(2)
        st.metric("Bounty Rate", f"{bounty_rate}%")
    
    with col4:
        st.metric("Organizations", f"{len(org_metrics):,}")
    
    # Additional metrics
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.metric("Active Reporters", f"{len(reporter_analytics):,}")
    
    with col6:
        st.metric("Vulnerability Types", f"{len(vulnerability_summary):,}")
    
    with col7:
        avg_vote = vulnerability_summary['avg_vote_count'].mean()
        st.metric("Avg Vote Count", f"{avg_vote:.1f}")
    
    with col8:
        # Get first valid vulnerability type
        top_vuln = get_first_valid(vulnerability_summary['weakness_name'])
        st.metric("Top Vulnerability", top_vuln[:20] + "..." if len(top_vuln) > 20 else top_vuln)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top Vulnerability Types")
        # Filter out null/None/Unknown
        filtered_vulns = vulnerability_summary[~vulnerability_summary['weakness_name'].isin([None, np.nan, "None", "null", "nan", "Unknown", ""])]
        top_vulns = filtered_vulns.head(10).sort_values("total_reports", ascending=False)
        fig = px.bar(top_vulns, x='weakness_name', y='total_reports',
                    color='bounty_percentage', color_continuous_scale='viridis',
                    title="Top 10 Vulnerability Types",
                    labels={"weakness_name": "Vulnerability Type", "total_reports": "Total Reports"})
        fig.update_layout(xaxis_tickangle=-45, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Organization Performance")
        top_orgs = org_metrics.head(10)
        fig = px.scatter(top_orgs, x='total_reports', y='bounty_percentage',
                        size='avg_vote_count', hover_data=['team_name'],
                        title="Reports vs Bounty Rate")
        st.plotly_chart(fig, use_container_width=True)

def show_vulnerability_analysis(vulnerability_summary, time_trends):
    """Display vulnerability analysis"""
    st.header("🔍 Vulnerability Analysis")
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        min_reports = st.slider("Minimum reports", 0, 1000, 10)
    with col2:
        top_n = st.selectbox("Show top N vulnerabilities", [10, 20, 50, 100])
    
    # Filter data
    # Filter out null/None/Unknown
    filtered_vulns = vulnerability_summary[~vulnerability_summary['weakness_name'].isin([None, np.nan, "None", "null", "nan", "Unknown", ""])]
    filtered_vulns = filtered_vulns[filtered_vulns['total_reports'] >= min_reports].head(top_n)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Vulnerability Distribution")
        fig = px.pie(filtered_vulns, values='total_reports', names='weakness_name',
                    title="Report Distribution by Vulnerability Type")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Bounty Rate by Vulnerability Type")
        fig = px.bar(filtered_vulns.sort_values("bounty_percentage", ascending=False), x='weakness_name', y='bounty_percentage',
                    title="Bounty Rate by Vulnerability Type",
                    labels={"weakness_name": "Vulnerability Type", "bounty_percentage": "Bounty %"})
        fig.update_layout(xaxis_tickangle=-45, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed table
    st.subheader("Detailed Vulnerability Analysis")
    # Add note if severity is missing
    if filtered_vulns['most_common_severity'].isnull().all() or (filtered_vulns['most_common_severity'] == "None").all():
        st.info("Note: Severity data is missing for most vulnerability types.")
    st.dataframe(filtered_vulns, use_container_width=True)

def show_organization_metrics(org_metrics):
    """Display organization metrics"""
    st.header("🏢 Organization Metrics")
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        min_reports = st.slider("Minimum reports per org", 0, 100, 5)
    with col2:
        bounty_rate_filter = st.slider("Minimum bounty rate (%)", 0, 100, 0)
    
    # Filter data
    # Filter out null/None/Unknown
    filtered_orgs = org_metrics[~org_metrics['team_handle'].isin([None, np.nan, "None", "null", "nan", "Unknown", ""])]
    filtered_orgs = filtered_orgs[(filtered_orgs['total_reports'] >= min_reports) & (filtered_orgs['bounty_percentage'] >= bounty_rate_filter)]
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Organization Performance Matrix")
        fig = px.scatter(filtered_orgs, x='total_reports', y='bounty_percentage',
                        size='avg_vote_count', hover_data=['team_name'],
                        title="Reports vs Bounty Rate")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Top Organizations by Report Volume")
        top_orgs = filtered_orgs.head(10).sort_values("total_reports", ascending=False)
        fig = px.bar(top_orgs, x='team_name', y='total_reports',
                    color='bounty_percentage', color_continuous_scale='viridis',
                    title="Top 10 Organizations",
                    labels={"team_name": "Organization", "total_reports": "Total Reports"})
        fig.update_layout(xaxis_tickangle=-45, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed table
    st.subheader("Organization Details")
    st.dataframe(filtered_orgs, use_container_width=True)

def show_reporter_analytics(reporter_analytics):
    """Display reporter analytics"""
    st.header("👥 Reporter Analytics")
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        min_reports = st.slider("Minimum reports per reporter", 0, 100, 5)
    with col2:
        min_valid_rate = st.slider("Minimum valid rate (%)", 0, 100, 50)
    
    # Filter data
    filtered_reporters = reporter_analytics[
        (reporter_analytics['total_reports'] >= min_reports) &
        (reporter_analytics['valid_percentage'] >= min_valid_rate)
    ]
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Reporter Performance Matrix")
        fig = px.scatter(filtered_reporters, x='total_reports', y='valid_percentage',
                        size='avg_vote_count', hover_data=['username'],
                        title="Volume vs Quality")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Top Reporters by Volume")
        top_reporters = filtered_reporters.head(10)
        fig = px.bar(top_reporters, x='username', y='total_reports',
                    color='valid_percentage', color_continuous_scale='viridis',
                    title="Top 10 Reporters")
        fig.update_layout(xaxis_tickangle=-45, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed table
    st.subheader("Reporter Details")
    st.dataframe(filtered_reporters, use_container_width=True)

def show_time_trends(time_trends):
    """Display time trends analysis"""
    st.header("📈 Time Trends Analysis")
    
    # Convert year_month to datetime
    time_trends['year_month'] = pd.to_datetime(time_trends['year_month'].astype(str))
    
    # Monthly volume
    monthly_volume = time_trends.groupby('year_month')['report_count'].sum().reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Monthly Report Volume")
        fig = px.line(monthly_volume, x='year_month', y='report_count',
                     title="Report Volume Over Time")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Monthly Bounty Rate")
        monthly_bounty = time_trends.groupby('year_month').agg({
            'report_count': 'sum',
            'bounty_count': 'sum'
        }).reset_index()
        monthly_bounty['bounty_rate'] = (monthly_bounty['bounty_count'] / monthly_bounty['report_count'] * 100)
        
        fig = px.line(monthly_bounty, x='year_month', y='bounty_rate',
                     title="Bounty Rate Over Time")
        st.plotly_chart(fig, use_container_width=True)
    
    # Vulnerability trends
    st.subheader("Vulnerability Type Trends")
    top_vuln_types = time_trends.groupby('vulnerability_type')['report_count'].sum().nlargest(5).index
    vuln_trends = time_trends[time_trends['vulnerability_type'].isin(top_vuln_types)]
    
    fig = px.line(vuln_trends, x='year_month', y='report_count',
                  color='vulnerability_type', title="Top Vulnerability Types Over Time")
    st.plotly_chart(fig, use_container_width=True)

def show_insights_and_recommendations(vulnerability_summary, org_metrics, reporter_analytics):
    """Display insights and recommendations"""
    st.header("💡 Insights & Strategic Recommendations")
    
    # Key insights
    st.subheader("🔍 Key Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **📊 Volume Patterns:**
        - Information Disclosure is the most common vulnerability type
        - XSS remains a significant threat despite security education
        - Top 5 vulnerability types represent 40% of all reports
        """)
        
        st.markdown("""
        **🏢 Organization Insights:**
        - Mail.ru has the highest report volume (705 reports)
        - U.S. Dept of Defense has low bounty rate (2.91%)
        - Internet Bug Bounty has highest bounty rate (91.97%)
        """)
    
    with col2:
        st.markdown("""
        **👥 Community Insights:**
        - bobrov is the top reporter (85 reports, 96.47% valid)
        - High-quality reporters show >90% valid rates
        - Verified reporters produce higher quality submissions
        """)
        
        st.markdown("""
        **📈 Trend Insights:**
        - Report volume shows seasonal patterns
        - Bounty rates vary significantly by organization
        - Vulnerability types evolve over time
        """)
    
    # Strategic recommendations
    st.subheader("🎯 Strategic Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🚀 Platform Optimization:**
        1. Focus on Information Disclosure and XSS detection
        2. Implement automated vulnerability pattern recognition
        3. Use verification status for report prioritization
        4. Develop AI-powered threat detection
        """)
        
        st.markdown("""
        **👥 Community Building:**
        1. Identify and nurture high-quality reporters
        2. Provide specialized training programs
        3. Create incentives for verified researchers
        4. Build regional talent clusters
        """)
    
    with col2:
        st.markdown("""
        **🏢 Customer Success:**
        1. Help low-bounty organizations improve programs
        2. Share best practices from top performers
        3. Develop maturity assessment framework
        4. Provide benchmarking reports
        """)
        
        st.markdown("""
        **🔮 Market Intelligence:**
        1. Monitor vulnerability trends for early detection
        2. Analyze geographic and industry patterns
        3. Develop predictive threat models
        4. Create security maturity scoring
        """)
    
    # Action items
    st.subheader("📋 Immediate Action Items")
    st.markdown("""
    1. **High Priority:**
       - Implement verification-based report prioritization
       - Develop automated detection for top vulnerability types
       - Create customer success program for low-performing organizations
    
    2. **Medium Priority:**
       - Build reporter quality scoring system
       - Develop vulnerability trend monitoring dashboard
       - Create organization benchmarking reports
    
    3. **Long Term:**
       - AI-powered threat prediction models
       - Global talent development programs
       - Industry-specific security maturity frameworks
    """)

if __name__ == "__main__":
    main() 