import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score
import streamlit as st
from data.insurance_data import get_insurance_data

class InsurancePremiumPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.encoders = {}
        self.is_trained = False
        
    def train_model(self):
        """Train the Random Forest model on insurance data"""
        try:
            # Get the insurance dataset
            df = get_insurance_data()
            
            # Prepare features
            X = df[['age', 'sex', 'bmi', 'children', 'smoker', 'region']].copy()
            y = df['charges']
            
            # Encode categorical variables
            categorical_cols = ['sex', 'smoker', 'region']
            for col in categorical_cols:
                self.encoders[col] = LabelEncoder()
                X.loc[:, col] = self.encoders[col].fit_transform(X[col])
            
            # Split the data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Train the model
            self.model.fit(X_train, y_train)
            
            # Evaluate the model
            y_pred = self.model.predict(X_test)
            self.mse = mean_squared_error(y_test, y_pred)
            self.r2 = r2_score(y_test, y_pred)
            
            self.is_trained = True
            
        except Exception as e:
            st.error(f"Error training model: {str(e)}")
            self.is_trained = False
    
    def predict_premium(self, age, sex, bmi, children, smoker, region):
        """Predict insurance premium for given parameters"""
        if not self.is_trained:
            st.error("Model not trained yet!")
            return 0
        
        try:
            # Create input dataframe
            input_data = pd.DataFrame({
                'age': [age],
                'sex': [sex],
                'bmi': [bmi],
                'children': [children],
                'smoker': [smoker],
                'region': [region]
            })
            
            # Encode categorical variables
            categorical_cols = ['sex', 'smoker', 'region']
            for col in categorical_cols:
                if col in self.encoders:
                    input_data[col] = self.encoders[col].transform(input_data[col])
            
            # Make prediction
            prediction = self.model.predict(input_data)[0]
            
            return max(prediction, 0)  # Ensure non-negative premium
            
        except Exception as e:
            st.error(f"Error making prediction: {str(e)}")
            return 0
    
    def get_feature_importance(self):
        """Get feature importance from the trained model"""
        if not self.is_trained:
            return None
        
        feature_names = ['age', 'sex', 'bmi', 'children', 'smoker', 'region']
        importance_df = pd.DataFrame({
            'feature': feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        return importance_df
    
    def get_model_metrics(self):
        """Get model performance metrics"""
        if not self.is_trained:
            return None
        
        return {
            'mse': self.mse,
            'rmse': np.sqrt(self.mse),
            'r2': self.r2
        }
