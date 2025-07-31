import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import bcrypt

# Import custom modules
from ml_model import InsurancePremiumPredictor
from wellness_calculator import WellnessCalculator
from utils.visualization import create_kpi_cards, create_wellness_gauge
from utils.health_tips import get_health_tips
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="Healsure",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'ml_model' not in st.session_state:
    st.session_state.ml_model = InsurancePremiumPredictor()
    st.session_state.ml_model.train_model()

if 'wellness_calc' not in st.session_state:
    st.session_state.wellness_calc = WellnessCalculator()

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'premium_history' not in st.session_state:
    st.session_state.premium_history = []

def check_password():
    def password_entered():
        if (st.session_state["username"] == "user" and 
            st.session_state["password"] == "pass"):
            st.session_state["authenticated"] = True
            del st.session_state["password"]
        else:
            st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        st.text_input("Username", key="username")
        st.text_input("Password", type="password", key="password")
        st.button("Login", on_click=password_entered)
        return False
    else:
        return True

def main():
    col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    logo = Image.open("healsurelogo.png")
    st.image(logo, width=180)
    st.title("Welcome to Healsure")
    st.markdown("### Secure your health. Reward your habits.")
    st.markdown("**Created by Aatmik**")

    if check_password():
        with st.sidebar:
            st.success(f'Welcome *User*')
            if st.button("Logout"):
                st.session_state["authenticated"] = False
                st.rerun()
        show_dashboard()
    else:
        st.warning('Please enter your username and password')
        st.info('Demo credentials: username = **user**, password = **pass**')

def show_dashboard():
    tab1, tab2, tab3, tab4 = st.tabs(["Premium Estimator", "Wellness Dashboard", "Health Tips", "Analytics"])
    with tab1:
        show_premium_estimator()
    with tab2:
        show_wellness_dashboard()
    with tab3:
        show_health_tips()
    with tab4:
        show_analytics()

def show_premium_estimator():
    st.header(" Insurance Premium Estimation")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Personal Information")
        age = st.slider("Age", 18, 80, 35)
        sex = st.selectbox("Gender", ["male", "female"])
        bmi = st.number_input("BMI", 15.0, 50.0, 25.0, 0.1)
        children = st.selectbox("Number of Children", [0, 1, 2, 3, 4, 5])
        smoker = st.selectbox("Smoking Status", ["no", "yes"])
        region = st.selectbox("Region", ["southwest", "southeast", "northwest", "northeast"])

    with col2:
        st.subheader("Wellness Metrics")
        exercise_freq = st.slider("Exercise Frequency (days/week)", 0, 7, 3)
        diet_quality = st.selectbox("Diet Quality", ["Poor", "Fair", "Good", "Excellent"])
        sleep_hours = st.slider("Sleep Hours per Night", 4, 12, 8)
        stress_level = st.slider("Stress Level (1-10)", 1, 10, 5)

        wellness_score = st.session_state.wellness_calc.calculate_wellness_score(
            bmi, exercise_freq, diet_quality, smoker, sleep_hours, stress_level
        )
        discount_percentage = st.session_state.wellness_calc.get_discount_percentage(wellness_score)

    if st.button("Calculate Premium", type="primary"):
        base_premium = st.session_state.ml_model.predict_premium(
            age, sex, bmi, children, smoker, region
        )
        discount_amount = base_premium * (discount_percentage / 100)
        final_premium = base_premium - discount_amount

        st.success("Premium Calculation Complete!")

        create_kpi_cards(base_premium, discount_percentage, final_premium, wellness_score)

        fig_gauge = create_wellness_gauge(wellness_score)
        st.plotly_chart(fig_gauge, use_container_width=True, key="premium_estimator_gauge")

        st.session_state.premium_history.append({
            'date': datetime.now(),
            'base_premium': base_premium,
            'wellness_score': wellness_score,
            'discount_percentage': discount_percentage,
            'final_premium': final_premium,
            'age': age,
            'bmi': bmi,
            'exercise_freq': exercise_freq,
            'diet_quality': diet_quality,
            'sleep_hours': sleep_hours,
            'stress_level': stress_level
        })

def show_wellness_dashboard():
    st.header(" Wellness Score Dashboard")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Health Metrics Input")
        bmi = st.number_input("Current BMI", 15.0, 50.0, 25.0, 0.1, key="wellness_bmi")
        exercise_freq = st.slider("Exercise Frequency (days/week)", 0, 7, 3, key="wellness_exercise")
        diet_quality = st.selectbox("Diet Quality", ["Poor", "Fair", "Good", "Excellent"], key="wellness_diet")
        smoker = st.selectbox("Smoking Status", ["no", "yes"], key="wellness_smoker")
        sleep_hours = st.slider("Sleep Hours per Night", 4, 12, 8, key="wellness_sleep")
        stress_level = st.slider("Stress Level (1-10)", 1, 10, 5, key="wellness_stress")

    with col2:
        wellness_score = st.session_state.wellness_calc.calculate_wellness_score(
            bmi, exercise_freq, diet_quality, smoker, sleep_hours, stress_level
        )
        fig_gauge = create_wellness_gauge(wellness_score)
        st.plotly_chart(fig_gauge, use_container_width=True, key="wellness_dashboard_gauge")

        discount_percentage = st.session_state.wellness_calc.get_discount_percentage(wellness_score)
        st.metric("Potential Discount", f"{discount_percentage}%")

        st.subheader("Wellness Score Breakdown")
        breakdown = st.session_state.wellness_calc.get_score_breakdown(
            bmi, exercise_freq, diet_quality, smoker, sleep_hours, stress_level
        )

        for category, score in breakdown.items():
            st.metric(category, f"{score}/20")

def show_health_tips():
    st.header(" Personalized Health Tips")

    tips = get_health_tips()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🏃‍♂️ Exercise & Fitness")
        for tip in tips['exercise']:
            st.info(tip)
    with col2:
        st.subheader("🥗 Nutrition & Diet")
        for tip in tips['nutrition']:
            st.info(tip)

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("😴 Sleep & Recovery")
        for tip in tips['sleep']:
            st.info(tip)
    with col4:
        st.subheader("🧘‍♀️ Stress Management")
        for tip in tips['stress']:
            st.info(tip)

def show_analytics():
    st.header("Premium & Wellness Analytics")

    col_demo, col_clear = st.columns([1, 1])
    with col_demo:
        if st.button("🎯 Generate Sample Data (Demo)"):
            generate_sample_data()
    with col_clear:
        if st.button("🗑️ Clear All Data"):
            st.session_state.premium_history = []
            st.rerun()

    if st.session_state.premium_history:
        df = pd.DataFrame(st.session_state.premium_history)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')

        col1, col2 = st.columns(2)

        with col1:
            fig_premium = px.line(df, x='date', y=['base_premium', 'final_premium'], 
                                  title="Premium Trend Over Time",
                                  labels={'value': 'Premium (₹)', 'date': 'Date'})
            fig_premium.update_layout(
                xaxis_title="Date",
                yaxis_title="Premium (₹)",
                legend_title="Premium Type"
            )
            st.plotly_chart(fig_premium, use_container_width=True, key="analytics_premium_trend")

        with col2:
            fig_wellness = px.line(df, x='date', y='wellness_score', 
                                   title="Wellness Score Trend",
                                   labels={'wellness_score': 'Wellness Score', 'date': 'Date'})
            fig_wellness.update_layout(
                xaxis_title="Date",
                yaxis_title="Wellness Score",
                yaxis=dict(range=[0, 100])
            )
            st.plotly_chart(fig_wellness, use_container_width=True, key="analytics_wellness_trend")

        col3, col4 = st.columns(2)
        with col3:
            if 'bmi' in df.columns:
                fig_bmi = px.line(df, x='date', y='bmi', 
                                  title="BMI Trend Over Time",
                                  labels={'bmi': 'BMI', 'date': 'Date'})
                fig_bmi.update_layout(xaxis_title="Date", yaxis_title="BMI")
                st.plotly_chart(fig_bmi, use_container_width=True, key="analytics_bmi_trend")
        with col4:
            fig_discount = px.line(df, x='date', y='discount_percentage', 
                                   title="Discount Percentage Trend",
                                   labels={'discount_percentage': 'Discount %', 'date': 'Date'})
            fig_discount.update_layout(
                xaxis_title="Date",
                yaxis_title="Discount Percentage (%)",
                yaxis=dict(range=[0, 25])
            )
            st.plotly_chart(fig_discount, use_container_width=True, key="analytics_discount_trend")

        st.subheader("📊 Summary Statistics")
        col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
        with col_stats1:
            st.metric("Average Base Premium", f"₹{df['base_premium'].mean():.2f}")
        with col_stats2:
            st.metric("Average Wellness Score", f"{df['wellness_score'].mean():.1f}")
        with col_stats3:
            st.metric("Average Discount", f"{df['discount_percentage'].mean():.1f}%")
        with col_stats4:
            st.metric("Total Savings", f"₹{(df['base_premium'] - df['final_premium']).sum():.2f}")

        st.subheader("📋 Calculation History")
        display_df = df[['date', 'base_premium', 'wellness_score', 'discount_percentage', 'final_premium']].copy()
        display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d %H:%M')
        display_df['base_premium'] = display_df['base_premium'].round(2)
        display_df['final_premium'] = display_df['final_premium'].round(2)
        display_df['wellness_score'] = display_df['wellness_score'].round(1)

        st.dataframe(
            display_df,
            column_config={
                "date": "Date",
                "base_premium": st.column_config.NumberColumn("Base Premium (₹)", format="₹%.2f"),
                "wellness_score": "Wellness Score",
                "discount_percentage": st.column_config.NumberColumn("Discount (%)", format="%.1f%%"),
                "final_premium": st.column_config.NumberColumn("Final Premium (₹)", format="₹%.2f"),
            },
            use_container_width=True
        )
    else:
        st.info("💡 No premium calculations available yet. Use the Premium Estimator to generate data, or click 'Generate Sample Data' to see how analytics work!")

def generate_sample_data():
    import random
    from datetime import timedelta

    st.session_state.premium_history = []
    base_date = datetime.now() - timedelta(days=7)

    for i in range(8):
        date = base_date + timedelta(days=i)
        base_wellness = 50 + (i * 5) + random.uniform(-5, 5)
        wellness_score = min(95, max(30, base_wellness))
        age = 35 + random.randint(-10, 15)
        bmi = 25 + random.uniform(-3, 5)
        exercise_freq = max(1, min(7, int(wellness_score / 15)))
        diet_quality = ["Poor", "Fair", "Good", "Excellent"][min(3, int(wellness_score / 25))]
        sleep_hours = 6 + random.randint(0, 3)
        stress_level = max(1, min(10, int(10 - wellness_score / 10)))

        base_premium = st.session_state.ml_model.predict_premium(
            age, "male", bmi, 1, "no", "northeast"
        )

        discount_percentage = st.session_state.wellness_calc.get_discount_percentage(wellness_score)
        final_premium = base_premium * (1 - discount_percentage / 100)

        st.session_state.premium_history.append({
            'date': date,
            'base_premium': base_premium,
            'wellness_score': wellness_score,
            'discount_percentage': discount_percentage,
            'final_premium': final_premium,
            'age': age,
            'bmi': bmi,
            'exercise_freq': exercise_freq,
            'diet_quality': diet_quality,
            'sleep_hours': sleep_hours,
            'stress_level': stress_level
        })

    st.success("Sample data generated! Check out the analytics below.")

if __name__ == "__main__":
    main()
