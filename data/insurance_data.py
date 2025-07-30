import pandas as pd
import numpy as np

def get_insurance_data():
    """
    Generate a comprehensive insurance dataset similar to the Kaggle insurance dataset.
    This creates realistic data for training the ML model.
    """
    np.random.seed(42)
    
    # Generate sample data similar to the Kaggle insurance dataset
    n_samples = 1338
    
    # Age distribution (18-64)
    ages = np.random.randint(18, 65, n_samples)
    
    # Gender distribution (roughly 50/50)
    genders = np.random.choice(['male', 'female'], n_samples)
    
    # BMI distribution (normal distribution around 30 with some variance)
    bmis = np.random.normal(30, 6, n_samples)
    bmis = np.clip(bmis, 15, 50)  # Clip to reasonable range
    
    # Children distribution (0-5, weighted towards fewer children)
    children = np.random.choice([0, 1, 2, 3, 4, 5], n_samples, 
                               p=[0.4, 0.25, 0.2, 0.1, 0.04, 0.01])
    
    # Smoking status (roughly 20% smokers)
    smokers = np.random.choice(['no', 'yes'], n_samples, p=[0.8, 0.2])
    
    # Region distribution
    regions = np.random.choice(['southwest', 'southeast', 'northwest', 'northeast'], n_samples)
    
    # Calculate charges based on realistic factors
    charges = []
    
    for i in range(n_samples):
        # Base charge calculation
        base_charge = 1000 + (ages[i] * 250)  # Age factor
        
        # BMI factor
        if bmis[i] >= 30:
            base_charge *= 1.5  # Obesity penalty
        elif bmis[i] >= 25:
            base_charge *= 1.2  # Overweight penalty
        
        # Smoking factor (major impact)
        if smokers[i] == 'yes':
            base_charge *= 2.5
        
        # Children factor
        base_charge += children[i] * 500
        
        # Gender factor (small difference)
        if genders[i] == 'male':
            base_charge *= 1.05
        
        # Regional factor
        region_multipliers = {
            'southwest': 0.95,
            'southeast': 1.05,
            'northwest': 0.98,
            'northeast': 1.02
        }
        base_charge *= region_multipliers[regions[i]]
        
        # Add some random variation
        base_charge *= np.random.normal(1, 0.15)
        
        # Ensure positive charges
        base_charge = max(base_charge, 1000)
        
        charges.append(round(base_charge, 2))
    
    # Create DataFrame
    df = pd.DataFrame({
        'age': ages,
        'sex': genders,
        'bmi': np.round(bmis, 1),
        'children': children,
        'smoker': smokers,
        'region': regions,
        'charges': charges
    })
    
    return df

def get_data_statistics():
    """Get basic statistics about the insurance dataset"""
    df = get_insurance_data()
    
    stats = {
        'total_records': len(df),
        'avg_age': df['age'].mean(),
        'avg_bmi': df['bmi'].mean(),
        'avg_charges': df['charges'].mean(),
        'smoker_percentage': (df['smoker'] == 'yes').mean() * 100,
        'gender_distribution': df['sex'].value_counts().to_dict(),
        'region_distribution': df['region'].value_counts().to_dict()
    }
    
    return stats
