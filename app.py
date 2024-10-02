import streamlit as st
import joblib
import pandas as pd

# Load the trained Random Forest model
model = joblib.load('random_forest_model.joblib')

# Define your categories as done during training
categories = [
    "Category_Alcohol & Bars", "Category_Auto Insurance", "Category_Coffee Shops",
    "Category_Credit Card Payment", "Category_Electronics & Software",
    "Category_Entertainment", "Category_Fast Food", "Category_Food & Dining",
    "Category_Gas & Fuel", "Category_Groceries", "Category_Haircut",
    "Category_Home Improvement", "Category_Internet", "Category_Mobile Phone",
    "Category_Mortgage & Rent", "Category_Movies & DVDs", "Category_Music",
    "Category_Paycheck", "Category_Restaurants", "Category_Shopping",
    "Category_Television", "Category_Utilities"
]

# Streamlit app
st.title('Smart Personal Expense Tracker')

# Input fields for user data
budget = st.number_input("Enter Budget", min_value=0.0)
overspent = st.number_input("Enter Overspent Amount", min_value=0.0)
amount_spent = st.number_input("Enter Amount Spent", min_value=0.0)
category = st.selectbox("Select Category", options=[
    "Alcohol & Bars", "Auto Insurance", "Coffee Shops",
    "Credit Card Payment", "Electronics & Software",
    "Entertainment", "Fast Food", "Food & Dining",
    "Gas & Fuel", "Groceries", "Haircut", "Home Improvement",
    "Internet", "Mobile Phone", "Mortgage & Rent", 
    "Movies & DVDs", "Music", "Paycheck", "Restaurants", 
    "Shopping", "Television", "Utilities"
])

# Expanded currency selector with conversion rates
currency_options = {
    "Rupees (₹)": 82.50,  # Example exchange rate for INR
    "Dollars ($)": 1.00,   # USD as the base
    "Euros (€)": 0.94,     # Example exchange rate for EUR
    "Pounds (£)": 0.81,    # Example exchange rate for GBP
    "Yen (¥)": 110.50,     # Example exchange rate for JPY
    "Canadian Dollars (C$)": 1.28,
    "Australian Dollars (A$)": 1.40,
    "Swiss Franc (CHF)": 0.91,
    "Singapore Dollars (S$)": 1.36,
    "Hong Kong Dollars (HK$)": 7.85,
    "New Zealand Dollars (NZ$)": 1.44,
    "Indian Rupees (INR)": 82.50,
    "Brazilian Reais (R$)": 5.20,
    "South African Rand (R)": 14.50,
    "Mexican Pesos (MX$)": 20.50,
    "Russian Rubles (₽)": 70.00
}

currency = st.selectbox("Select Currency", options=list(currency_options.keys()))

if st.button("Predict Spending"):
    # Prepare the input data
    input_data = pd.DataFrame({
        'Budget': [budget],
        'Overspent': [overspent],
    })
    
    # One-hot encode the category column
    category_encoded = pd.get_dummies([category], prefix='Category')
    category_encoded = category_encoded.reindex(columns=categories, fill_value=0)
    
    # Combine input data and one-hot encoded category
    input_data = pd.concat([input_data, category_encoded], axis=1)

    # Make prediction
    prediction = model.predict(input_data)[0]  # Get the predicted value

    # Convert prediction to selected currency
    conversion_rate = currency_options[currency]
    converted_prediction = prediction * conversion_rate

    # Display the prediction in the selected currency
    st.write(f"Predicted Future Spending: {currency}{converted_prediction:.2f}")
