import numpy as np

class WellnessCalculator:
    def __init__(self):
        # Define scoring weights for different health factors
        self.weights = {
            'bmi': 0.25,
            'exercise': 0.25,
            'diet': 0.20,
            'smoking': 0.15,
            'sleep': 0.10,
            'stress': 0.05
        }
        
        # Define discount tiers
        self.discount_tiers = [
            (90, 100, 20),  # 90-100: 20%
            (80, 89, 15),   # 80-89: 15%
            (70, 79, 10),   # 70-79: 10%
            (60, 69, 5),    # 60-69: 5%
            (0, 59, 0)      # <60: 0%
        ]
    
    def calculate_bmi_score(self, bmi):
        """Calculate BMI score (0-20)"""
        if 18.5 <= bmi <= 24.9:
            return 20  # Optimal BMI
        elif 25.0 <= bmi <= 29.9:
            return 15  # Overweight
        elif 30.0 <= bmi <= 34.9:
            return 10  # Obese Class I
        elif 35.0 <= bmi <= 39.9:
            return 5   # Obese Class II
        else:
            return 0   # Underweight or Severely Obese
    
    def calculate_exercise_score(self, exercise_freq):
        """Calculate exercise score (0-20)"""
        if exercise_freq >= 5:
            return 20
        elif exercise_freq >= 4:
            return 16
        elif exercise_freq >= 3:
            return 12
        elif exercise_freq >= 2:
            return 8
        elif exercise_freq >= 1:
            return 4
        else:
            return 0
    
    def calculate_diet_score(self, diet_quality):
        """Calculate diet score (0-20)"""
        diet_scores = {
            "Excellent": 20,
            "Good": 15,
            "Fair": 10,
            "Poor": 0
        }
        return diet_scores.get(diet_quality, 0)
    
    def calculate_smoking_score(self, smoker):
        """Calculate smoking score (0-20)"""
        return 0 if smoker == "yes" else 20
    
    def calculate_sleep_score(self, sleep_hours):
        """Calculate sleep score (0-20)"""
        if 7 <= sleep_hours <= 9:
            return 20  # Optimal sleep
        elif 6 <= sleep_hours < 7 or 9 < sleep_hours <= 10:
            return 15  # Slightly off optimal
        elif 5 <= sleep_hours < 6 or 10 < sleep_hours <= 11:
            return 10  # Suboptimal
        else:
            return 5   # Poor sleep
    
    def calculate_stress_score(self, stress_level):
        """Calculate stress score (0-20)"""
        # Lower stress is better, so invert the scale
        if stress_level <= 3:
            return 20
        elif stress_level <= 5:
            return 15
        elif stress_level <= 7:
            return 10
        elif stress_level <= 8:
            return 5
        else:
            return 0
    
    def calculate_wellness_score(self, bmi, exercise_freq, diet_quality, smoker, sleep_hours, stress_level):
        """Calculate overall wellness score (0-100)"""
        bmi_score = self.calculate_bmi_score(bmi)
        exercise_score = self.calculate_exercise_score(exercise_freq)
        diet_score = self.calculate_diet_score(diet_quality)
        smoking_score = self.calculate_smoking_score(smoker)
        sleep_score = self.calculate_sleep_score(sleep_hours)
        stress_score = self.calculate_stress_score(stress_level)
        
        # Weighted average
        total_score = (
            bmi_score * self.weights['bmi'] +
            exercise_score * self.weights['exercise'] +
            diet_score * self.weights['diet'] +
            smoking_score * self.weights['smoking'] +
            sleep_score * self.weights['sleep'] +
            stress_score * self.weights['stress']
        ) * 5  # Convert to 0-100 scale
        
        return round(total_score, 1)
    
    def get_discount_percentage(self, wellness_score):
        """Get discount percentage based on wellness score"""
        for min_score, max_score, discount in self.discount_tiers:
            if min_score <= wellness_score <= max_score:
                return discount
        return 0
    
    def get_score_breakdown(self, bmi, exercise_freq, diet_quality, smoker, sleep_hours, stress_level):
        """Get detailed breakdown of wellness score components"""
        return {
            "BMI Score": self.calculate_bmi_score(bmi),
            "Exercise Score": self.calculate_exercise_score(exercise_freq),
            "Diet Score": self.calculate_diet_score(diet_quality),
            "Smoking Score": self.calculate_smoking_score(smoker),
            "Sleep Score": self.calculate_sleep_score(sleep_hours),
            "Stress Score": self.calculate_stress_score(stress_level)
        }
    
    def get_improvement_suggestions(self, bmi, exercise_freq, diet_quality, smoker, sleep_hours, stress_level):
        """Get suggestions for improving wellness score"""
        suggestions = []
        
        if self.calculate_bmi_score(bmi) < 15:
            suggestions.append("Consider maintaining a healthy BMI between 18.5-24.9")
        
        if self.calculate_exercise_score(exercise_freq) < 16:
            suggestions.append("Increase exercise frequency to at least 4-5 days per week")
        
        if self.calculate_diet_score(diet_quality) < 15:
            suggestions.append("Improve diet quality by eating more fruits, vegetables, and whole grains")
        
        if smoker == "yes":
            suggestions.append("Consider quitting smoking for significant health and premium benefits")
        
        if self.calculate_sleep_score(sleep_hours) < 15:
            suggestions.append("Aim for 7-9 hours of quality sleep per night")
        
        if self.calculate_stress_score(stress_level) < 15:
            suggestions.append("Practice stress management techniques like meditation or yoga")
        
        return suggestions
