Smart Health Insurance Estimator & Wellness Rewards Dashboard
🎯 Live App: Smart Health Insurance Estimator

🧠 Project Overview
The Smart Health Insurance Estimator & Wellness Rewards Dashboard is an intelligent, single-page Streamlit web application that helps users estimate their health insurance premiums and unlock wellness rewards based on personalized inputs.

Inspired by modern analytics UI (like Autocoder), the app offers a sleek, scrollable, card-based experience, combining:

A login system for secure access

Real-time premium prediction using a trained ML model

Dynamic discount calculations based on wellness activities

Interactive Plotly visualizations

Wellness score metrics and engagement tips

📌 Features
✅ User Authentication (with streamlit_authenticator)
✅ ML-Based Premium Estimator
✅ Wellness Rewards Logic (with conditional discounts)
✅ Interactive Visuals using Plotly
✅ Modern, Scrollable UI (inspired by Finbot & Autocoder)
✅ Dynamic Card-Based Layout

🚀 Technologies Used
Python

Streamlit – UI framework

scikit-learn – ML model for premium prediction

Plotly – Rich, interactive visualizations

pandas, numpy – Data processing

streamlit-authenticator – Secure login system

📂 Project Structure
bash
Copy
Edit
smart-health-insurance-estimator/
│
├── app.py                  # Main Streamlit application
├── model/
│   └── premium_model.pkl   # Trained ML model
├── utils/
│   └── helpers.py          # Helper functions (discounts, scoring)
├── assets/
│   └── style.css           # Custom styles
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── ...
🔧 Installation (For Local Development)
Clone the repository

bash
Copy
Edit
git clone https://github.com/your-username/smart-health-insurance-estimator.git
cd smart-health-insurance-estimator
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Run the Streamlit app

bash
Copy
Edit
streamlit run app.py
🔒 Login Credentials (For Demo)
Username: user
Password: pass

(Note: This is a dummy login for testing purposes.)

📊 Example Inputs
Age, BMI, Number of Children

Smoking Status

Pre-existing Conditions

Wellness Activities: Steps, Gym Visits, Diet Adherence, etc.

🧮 How Premium Is Calculated
A machine learning regression model predicts base insurance premium

Discounts are applied based on:

Activity score

Wellness habits

Age group and risk factor

📈 Sample Visuals
Premium vs Wellness Score

Discount Trends

Wellness Score Breakdown

✨ Future Enhancements
OAuth2 login (Google/Facebook)

Database integration for persistent user profiles

More granular wellness scoring (sleep, mental health, etc.)

API integration with health data apps (Fitbit, Apple Health)

🤝 Contributing
Pull requests and suggestions are welcome! For major changes, please open an issue first.

👤 Created By
Aatmik Singh Parmar
🔗 LinkedIn Profile

📜 License
This project is licensed under the MIT License – see the LICENSE file for details.
