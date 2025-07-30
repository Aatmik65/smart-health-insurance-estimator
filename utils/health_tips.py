def get_health_tips():
    """
    Return categorized health tips for improving wellness scores
    """
    
    tips = {
        'exercise': [
            "💪 Aim for at least 150 minutes of moderate-intensity aerobic activity per week",
            "🏃‍♀️ Include strength training exercises at least 2 days per week",
            "🚶‍♂️ Take regular walking breaks throughout your workday",
            "🏊‍♀️ Try low-impact activities like swimming or cycling if you have joint issues",
            "🧘‍♀️ Include flexibility and balance exercises in your routine"
        ],
        
        'nutrition': [
            "🥗 Fill half your plate with fruits and vegetables at each meal",
            "🌾 Choose whole grains over refined grains whenever possible",
            "🐟 Include lean proteins like fish, poultry, beans, and nuts",
            "💧 Stay hydrated by drinking plenty of water throughout the day",
            "🧂 Limit processed foods high in sodium, sugar, and unhealthy fats"
        ],
        
        'sleep': [
            "😴 Maintain a consistent sleep schedule, even on weekends",
            "📱 Avoid screens at least 1 hour before bedtime",
            "🌡️ Keep your bedroom cool, dark, and quiet for optimal sleep",
            "☕ Limit caffeine intake, especially in the afternoon and evening",
            "🛏️ Create a relaxing bedtime routine to signal your body it's time to sleep"
        ],
        
        'stress': [
            "🧘‍♀️ Practice mindfulness meditation for just 10 minutes daily",
            "🌬️ Use deep breathing exercises when feeling stressed",
            "📝 Keep a gratitude journal to focus on positive aspects of life",
            "👥 Maintain strong social connections with family and friends",
            "⏰ Practice time management to reduce daily stress triggers"
        ]
    }
    
    return tips

def get_personalized_tips(wellness_score, breakdown_scores):
    """
    Get personalized tips based on user's wellness score and breakdown
    """
    all_tips = get_health_tips()
    personalized = {}
    
    # Identify areas that need improvement (scores below 15)
    low_scoring_areas = {k: v for k, v in breakdown_scores.items() if v < 15}
    
    if "BMI Score" in low_scoring_areas:
        personalized["BMI Improvement"] = [
            "🎯 Consult with a healthcare provider about a healthy weight management plan",
            "📊 Track your food intake and physical activity",
            "🥗 Focus on portion control and nutrient-dense foods"
        ]
    
    if "Exercise Score" in low_scoring_areas:
        personalized["Exercise Improvement"] = all_tips['exercise'][:3]
    
    if "Diet Score" in low_scoring_areas:
        personalized["Nutrition Improvement"] = all_tips['nutrition'][:3]
    
    if "Sleep Score" in low_scoring_areas:
        personalized["Sleep Improvement"] = all_tips['sleep'][:3]
    
    if "Stress Score" in low_scoring_areas:
        personalized["Stress Management"] = all_tips['stress'][:3]
    
    if "Smoking Score" in low_scoring_areas:
        personalized["Smoking Cessation"] = [
            "🚭 Speak with your doctor about smoking cessation programs",
            "📞 Call a quitline for support and resources",
            "💊 Consider nicotine replacement therapy or medications",
            "👥 Join a support group for people quitting smoking"
        ]
    
    return personalized

def get_wellness_facts():
    """
    Return interesting facts about wellness and health insurance
    """
    
    facts = [
        "🎯 People with higher wellness scores can save up to 20% on their insurance premiums",
        "💪 Regular exercise can reduce healthcare costs by up to 25% annually",
        "🚭 Quitting smoking can lead to immediate health benefits and premium reductions",
        "😴 Poor sleep quality is linked to increased healthcare utilization and costs",
        "🧘‍♀️ Stress management programs can reduce medical expenses by 28%",
        "🥗 A healthy diet can prevent up to 80% of premature heart disease and stroke",
        "📊 Maintaining a healthy BMI reduces the risk of chronic diseases significantly",
        "🏃‍♀️ Just 30 minutes of daily activity can improve overall health markers"
    ]
    
    return facts
