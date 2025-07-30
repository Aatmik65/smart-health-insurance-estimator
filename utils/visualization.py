import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

def create_kpi_cards(base_premium, discount_percentage, final_premium, wellness_score):
    """Create KPI cards for premium breakdown"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Base Premium",
            value=f"${base_premium:,.2f}",
            help="Premium before wellness discount"
        )
    
    with col2:
        st.metric(
            label="Wellness Score",
            value=f"{wellness_score}/100",
            help="Your overall wellness score"
        )
    
    with col3:
        st.metric(
            label="Discount",
            value=f"{discount_percentage}%",
            delta=f"${base_premium * discount_percentage / 100:,.2f} saved",
            help="Discount based on wellness score"
        )
    
    with col4:
        st.metric(
            label="Final Premium",
            value=f"${final_premium:,.2f}",
            delta=f"-${base_premium - final_premium:,.2f}",
            delta_color="inverse",
            help="Premium after wellness discount"
        )

def create_wellness_gauge(wellness_score):
    """Create a Plotly gauge chart for wellness score"""
    
    # Determine color based on score
    if wellness_score >= 80:
        color = "green"
    elif wellness_score >= 60:
        color = "yellow"
    else:
        color = "red"
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = wellness_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Wellness Score"},
        delta = {'reference': 80, 'increasing': {'color': "green"}, 'decreasing': {'color': "red"}},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 60], 'color': "lightgray"},
                {'range': [60, 80], 'color': "yellow"},
                {'range': [80, 100], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        height=400,
        font={'size': 16}
    )
    
    return fig

def create_discount_tier_chart():
    """Create a chart showing discount tiers"""
    
    tiers = {
        'Wellness Score Range': ['90-100', '80-89', '70-79', '60-69', '<60'],
        'Discount Percentage': [20, 15, 10, 5, 0],
        'Tier': ['Excellent', 'Good', 'Fair', 'Poor', 'Needs Improvement']
    }
    
    fig = px.bar(
        x=tiers['Wellness Score Range'],
        y=tiers['Discount Percentage'],
        color=tiers['Discount Percentage'],
        color_continuous_scale='RdYlGn',
        title='Wellness Discount Tiers',
        labels={'x': 'Wellness Score Range', 'y': 'Discount Percentage (%)'}
    )
    
    fig.update_layout(
        xaxis_title="Wellness Score Range",
        yaxis_title="Discount Percentage (%)",
        showlegend=False
    )
    
    return fig

def create_wellness_breakdown_chart(breakdown_scores):
    """Create a radar chart for wellness score breakdown"""
    
    categories = list(breakdown_scores.keys())
    values = list(breakdown_scores.values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Your Scores'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 20]
            )),
        showlegend=True,
        title="Wellness Score Breakdown"
    )
    
    return fig
