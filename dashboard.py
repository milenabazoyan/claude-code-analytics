import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(page_title="Claude Code Analytics", page_icon="🚀", layout="wide")
st.title("🚀 Claude Code Usage Analytics Platform")
st.markdown("Interactive dashboard exploring developer patterns, tool reliability, and financial ROI.")

# Load Data
@st.cache_data
def load_data():
    events = pd.read_csv("output/events_distribution.csv")
    tool_perf = pd.read_csv("output/tool_performance.csv")
    roi = pd.read_csv("output/practice_roi.csv")
    level_eff = pd.read_csv("output/level_efficiency.csv")
    hourly = pd.read_csv("output/hourly_usage.csv").rename(columns={"0": "count"})
    daily_trend = pd.read_csv("output/daily_cost_trend.csv")
    return events, tool_perf, roi, level_eff, hourly, daily_trend

events, tool_perf, roi, level_eff, hourly, daily_trend = load_data()

# Tabs for Different Stakeholders
tab1, tab2, tab3, tab4 = st.tabs(["📊 Executive Summary", "🛠️ Tool Performance", "👨‍💻 Developer Patterns", "📈 Predictive Trend"])

# TAB 1: Executive Summary (For Leadership) 
with tab1:
    st.header("Platform Overview")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Event Distribution")
        fig_events = px.pie(events, values='count', names='event_name', hole=0.4)
        st.plotly_chart(fig_events, use_container_width=True)
        
    with col2:
        st.subheader("Cost per Successful Tool by Practice")
        fig_roi = px.bar(roi.sort_values('cost_per_success'), 
                         x='practice', y='cost_per_success', 
                         color='cost_per_success',
                         color_continuous_scale='Viridis_r',
                         labels={'cost_per_success': 'Cost per Success ($)', 'practice': 'Engineering Practice'})
        st.plotly_chart(fig_roi, use_container_width=True)

# TAB 2: Tool Performance (For Platform Engineers) 
with tab2:
    st.header("Tool Reliability")
    st.markdown("Success rates of Claude Code tools used by developers. Focus on optimizing lower-performing tools.")
    
    fig_tools = px.bar(tool_perf.sort_values('success_bool'), 
                       x='tool_name', y='success_bool', 
                       color='success_bool',
                       color_continuous_scale='RdYlGn',
                       labels={'success_bool': 'Success Rate', 'tool_name': 'Tool Name'})
    fig_tools.layout.yaxis.tickformat = ',.1%'
    fig_tools.layout.coloraxis.colorbar.tickformat = ',.1%' 
    st.plotly_chart(fig_tools, use_container_width=True)

# TAB 3: Developer Patterns (For Dev Productivity Teams)
with tab3:
    st.header("Usage & Efficiency Patterns")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Efficiency by Seniority Level")
        fig_level = px.bar(level_eff.sort_values('success_per_dollar', ascending=False), 
                           x='level', y='success_per_dollar', 
                           labels={'success_per_dollar': 'Successful Tools per $1', 'level': 'Seniority Level'})
        st.plotly_chart(fig_level, use_container_width=True)
        
    with col_b:
        st.subheader("Daily Usage Heatmap")
        fig_hour = px.line(hourly, x='hour', y='count', markers=True,
                           labels={'count': 'Number of Events', 'hour': 'Hour of Day (UTC)'})
        # X axis to show 0-23 hours
        fig_hour.update_xaxes(dtick=2)
        st.plotly_chart(fig_hour, use_container_width=True)


# TAB 4: Predictive Analytics 
with tab4:
    st.header("📈 Predictive Cost Forecasting")
    st.markdown("Using **Exponential Moving Average (EMA)** to smooth high-variance daily costs and forecast short-term trajectory based on recent momentum.")
    
    fig_trend = go.Figure()
    
    # 1. Add the noisy actual daily costs as Light Blue Bars
    fig_trend.add_trace(go.Bar(
        x=daily_trend['date'], 
        y=daily_trend['cost_usd'],
        name='Actual Daily Cost',
        marker_color='rgba(54, 162, 235, 0.6)' 
    ))
    
    # 2. Add the smoothed EMA and Forecast as a Red Dashed Line
    fig_trend.add_trace(go.Scatter(
        x=daily_trend['date'],
        y=daily_trend['trend'],
        mode='lines',
        name='EMA Trend & Forecast',
        line=dict(color='#ff4b4b', width=3, dash='dash')
    ))
    
    fig_trend.update_layout(
        title="Daily API Cost vs. 14-Day Forecast", 
        xaxis_title="Date", 
        yaxis_title="Cost (USD)",
        hovermode="x unified"
    )
    
    st.plotly_chart(fig_trend, use_container_width=True)