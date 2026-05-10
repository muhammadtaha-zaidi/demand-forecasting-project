import streamlit as st
import pandas as pd
import pickle

# =========================
# Load Model
# =========================
@st.cache_resource
def load_model():
    with open("best_model.pkl", "rb") as f:
        model = pickle.load(f)

    return model


model = load_model()

# =========================
# App Title
# =========================
st.title("Demand Forecasting App")

st.divider()

st.header("Input Features")

# =========================
# Numerical Inputs
# =========================
price = st.number_input(
    "Price",
    min_value=0.0,
    value=50.0
)

discount = st.number_input(
    "Discount (%)",
    min_value=0,
    max_value=100,
    value=10
)

inventory_level = st.number_input(
    "Inventory Level",
    min_value=0,
    value=100
)

units_ordered = st.number_input(
    "Units Ordered",
    min_value=0,
    value=60
)

promotion = st.selectbox(
    "Promotion",
    [0, 1]
)

competitor_pricing = st.number_input(
    "Competitor Pricing",
    min_value=0.0,
    value=45.0
)

epidemic = st.selectbox(
    "Epidemic",
    [0, 1]
)

month = st.selectbox(
    "Month",
    list(range(1, 13))
)

day_of_week = st.selectbox(
    "Day Of Week",
    [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]
)

seasonality = st.selectbox(
    "Seasonality",
    [0, 1]
)

# =========================
# Category Input
# =========================
category = st.selectbox(
    "Category",
    [
        "Clothing",
        "Electronics",
        "Furniture",
        "Groceries",
        "Toys"
    ]
)

# =========================
# Region Input
# =========================
region = st.selectbox(
    "Region",
    [
        "East",
        "North",
        "South",
        "West"
    ]
)

# =========================
# Weather Input
# =========================
weather = st.selectbox(
    "Weather Condition",
    [
        "Sunny",
        "Cloudy",
        "Rainy",
        "Snowy"
    ]
)

st.divider()

# =========================
# Feature Engineering
# =========================
final_price = price - (price * discount / 100)

price_diff = price - competitor_pricing

# =========================
# Day Encoding
# =========================
day_mapping = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6
}

day_of_week_encoded = day_mapping[day_of_week]

# =========================
# Category Encoding
# =========================
cat_clothing = 1 if category == "Clothing" else 0
cat_electronics = 1 if category == "Electronics" else 0
cat_furniture = 1 if category == "Furniture" else 0
cat_groceries = 1 if category == "Groceries" else 0
cat_toys = 1 if category == "Toys" else 0

# =========================
# Region Encoding
# =========================
region_east = 1 if region == "East" else 0
region_north = 1 if region == "North" else 0
region_south = 1 if region == "South" else 0
region_west = 1 if region == "West" else 0

# =========================
# Weather Encoding
# =========================
weather_cloudy = 1 if weather == "Cloudy" else 0
weather_rainy = 1 if weather == "Rainy" else 0
weather_snowy = 1 if weather == "Snowy" else 0
weather_sunny = 1 if weather == "Sunny" else 0

# =========================
# Create Input DataFrame
# =========================
input_data = pd.DataFrame({

    "Inventory Level": [inventory_level],
    "Units Ordered": [units_ordered],
    "Price": [price],
    "Discount": [discount],
    "Promotion": [promotion],
    "Competitor Pricing": [competitor_pricing],
    "Epidemic": [epidemic],

    "Month": [month],
    "DayOfWeek": [day_of_week_encoded],

    "Final_Price": [final_price],
    "Price_Diff": [price_diff],

    "Category_Clothing": [cat_clothing],
    "Category_Electronics": [cat_electronics],
    "Category_Furniture": [cat_furniture],
    "Category_Groceries": [cat_groceries],
    "Category_Toys": [cat_toys],

    "Region_East": [region_east],
    "Region_North": [region_north],
    "Region_South": [region_south],
    "Region_West": [region_west],

    "Weather Condition_Cloudy": [weather_cloudy],
    "Weather Condition_Rainy": [weather_rainy],
    "Weather Condition_Snowy": [weather_snowy],
    "Weather Condition_Sunny": [weather_sunny],

    "Seasonality": [seasonality]

})

# =========================
# Ensure Correct Column Order
# =========================
input_data = input_data[model.feature_names_in_]

# =========================
# Prediction
# =========================
if st.button("Predict Demand"):

    prediction = model.predict(input_data)

    st.success(
        f"Predicted Demand: {int(prediction[0])} units"
    )