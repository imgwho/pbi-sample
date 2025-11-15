import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page config
st.set_page_config(page_title="Fitcheck Marketing Dashboard", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 5px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        text-align: center;
    }
    .metric-value {
        font-size: 48px;
        font-weight: bold;
        margin: 10px 0;
    }
    .metric-label {
        font-size: 16px;
        color: #666;
    }
    h1 {
        font-size: 36px !important;
        font-weight: bold !important;
        margin-bottom: 30px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('Fitcheck OVERVIEW.csv', encoding='utf-8-sig')
    df['Post Date'] = pd.to_datetime(df['Post Date'])
    df['Post Date Month'] = df['Post Date'].dt.to_period('M').dt.to_timestamp()
    return df

df = load_data()

# Title
st.markdown("# FITCHECK MARKETING")

# Filters row
col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])

with col1:
    # Date range filter
    min_date = df['Post Date'].min().date()
    max_date = df['Post Date'].max().date()
    date_range = st.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        key='date_range'
    )

with col2:
    platforms = ['All'] + sorted(df['Platform'].unique().tolist())
    selected_platform = st.selectbox("Platform", platforms, key='platform')

with col3:
    themes = ['All'] + sorted(df['Content Theme'].unique().tolist())
    selected_theme = st.selectbox("Content Theme", themes, key='theme')

with col4:
    audiences = ['All'] + sorted(df['Target Audience'].unique().tolist())
    selected_audience = st.selectbox("Target Audience", audiences, key='audience')

# Apply filters
filtered_df = df.copy()

if len(date_range) == 2:
    filtered_df = filtered_df[
        (filtered_df['Post Date'].dt.date >= date_range[0]) &
        (filtered_df['Post Date'].dt.date <= date_range[1])
    ]

if selected_platform != 'All':
    filtered_df = filtered_df[filtered_df['Platform'] == selected_platform]

if selected_theme != 'All':
    filtered_df = filtered_df[filtered_df['Content Theme'] == selected_theme]

if selected_audience != 'All':
    filtered_df = filtered_df[filtered_df['Target Audience'] == selected_audience]

# Calculate KPIs
total_revenue = filtered_df['Conversion Value Usd'].sum()
total_spend = filtered_df['Spend Usd'].sum()
total_conversions = int(filtered_df['Conversions'].sum())
roi = ((total_revenue - total_spend) / total_spend * 100) if total_spend > 0 else 0
avg_cost_per_conv = total_spend / total_conversions if total_conversions > 0 else 0

# Display note about metrics
st.markdown("Performance = Overall Success (ROI, Revenue, Conversions) | Efficiency = Cost Effectiveness (CPC, CPM, Spend)")
st.markdown("")

# KPI Cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{roi:,.2f}%</div>
            <div class="metric-label">Overall ROI</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${total_revenue/1000000:.1f}M</div>
            <div class="metric-label">Total Revenue</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_conversions:,}</div>
            <div class="metric-label">Total Conversions</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${avg_cost_per_conv:.2f}</div>
            <div class="metric-label">Avg Cost/Conv</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Charts layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### Platform Performance: ROI Comparison")

    # Calculate ROI by platform
    platform_metrics = filtered_df.groupby('Platform').agg({
        'Conversion Value Usd': 'sum',
        'Spend Usd': 'sum'
    }).reset_index()

    platform_metrics['ROI'] = ((platform_metrics['Conversion Value Usd'] - platform_metrics['Spend Usd']) /
                                platform_metrics['Spend Usd'] * 100)
    platform_metrics = platform_metrics.sort_values('ROI', ascending=True)

    # Create horizontal bar chart
    fig1 = go.Figure()

    # Define colors for each platform (matching Power BI)
    colors = {
        'LinkedIn': '#6B8E9E',  # Blue-gray
        'Instagram': '#B89BB4',  # Mauve/Purple
        'Facebook': '#6B8E9E',  # Blue-gray
        'X': '#6B8E9E',  # Blue-gray
        'TikTok': '#7DBAA6'  # Teal/Green
    }

    bar_colors = [colors.get(platform, '#gray') for platform in platform_metrics['Platform']]

    fig1.add_trace(go.Bar(
        y=platform_metrics['Platform'],
        x=platform_metrics['ROI'],
        orientation='h',
        marker=dict(color=bar_colors),
        text=[f"{val:.3f}%" for val in platform_metrics['ROI']],
        textposition='outside',
        showlegend=False
    ))

    # Add reference line
    fig1.add_vline(x=roi, line_dash="dash", line_color="orange",
                   annotation_text=f"Index: {roi:.3f}%",
                   annotation_position="top")

    fig1.update_layout(
        height=850,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis_title="",
        yaxis_title="",
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("### Monthly Conversion Trends")

    # Aggregate by month
    monthly_trends = filtered_df.groupby('Post Date Month')['Conversions'].sum().reset_index()
    monthly_trends['Post Date Month'] = monthly_trends['Post Date Month'].dt.strftime('%Y年%m月')

    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(
        x=monthly_trends['Post Date Month'],
        y=monthly_trends['Conversions'],
        mode='lines',
        line=dict(color='#7F7F7F', width=2),
        showlegend=False
    ))

    fig2.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis_title="Post Date 月",
        yaxis_title="Conversions",
        plot_bgcolor='white',
        paper_bgcolor='white',
        yaxis=dict(
            tickformat=',',
            range=[0, monthly_trends['Conversions'].max() * 1.2]
        )
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Platform Efficiency Bubble (moved here, below the line chart)
    st.markdown("### Platform Efficiency Bubble")

    # Calculate platform metrics for bubble chart
    bubble_data = filtered_df.groupby('Platform').agg({
        'Conversions': 'sum',
        'Conversion Value Usd': 'sum',
        'Spend Usd': 'sum',
        'Impressions': 'sum'
    }).reset_index()

    bubble_data['ROI'] = ((bubble_data['Conversion Value Usd'] - bubble_data['Spend Usd']) /
                           bubble_data['Spend Usd'] * 100)

    # Create bubble chart
    fig3 = go.Figure()

    colors_bubble = {
        'LinkedIn': '#6B8E9E',  # Blue-gray
        'Instagram': '#E199D3',  # Pink/Purple
        'Facebook': '#6B8E9E',  # Blue-gray
        'X': '#6B8E9E',  # Blue-gray
        'TikTok': '#6B8E9E'  # Blue-gray (X marker in original)
    }

    # Calculate bubble size scaling
    min_impressions = bubble_data['Impressions'].min()
    max_impressions = bubble_data['Impressions'].max()

    for platform in bubble_data['Platform'].unique():
        platform_data = bubble_data[bubble_data['Platform'] == platform]

        # Normalize bubble size to 20-80 range
        normalized_size = 20 + (platform_data['Impressions'].values[0] - min_impressions) / (max_impressions - min_impressions) * 60

        fig3.add_trace(go.Scatter(
            x=platform_data['Conversions'],
            y=platform_data['ROI'],
            mode='markers+text',
            name=platform,
            text=platform,
            textposition='middle center',
            textfont=dict(size=10, color='white'),
            marker=dict(
                size=normalized_size,
                color=colors_bubble.get(platform, 'gray'),
                opacity=0.7,
                line=dict(width=2, color='white')
            ),
            showlegend=True
        ))

    # Calculate appropriate axis ranges
    x_range = [0, bubble_data['Conversions'].max() * 1.2]
    y_min = bubble_data['ROI'].min()
    y_max = bubble_data['ROI'].max()
    y_padding = (y_max - y_min) * 0.2
    y_range = [y_min - y_padding, y_max + y_padding]

    fig3.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis_title="Number of Conversions",
        yaxis_title="ROI (%)",
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            tickformat=',',
            range=x_range,
            gridcolor='#f0f0f0'
        ),
        yaxis=dict(
            tickformat=',',
            range=y_range,
            gridcolor='#f0f0f0'
        ),
        legend=dict(
            orientation="v",
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99,
            bgcolor='rgba(255,255,255,0.8)'
        )
    )

    st.plotly_chart(fig3, use_container_width=True)
