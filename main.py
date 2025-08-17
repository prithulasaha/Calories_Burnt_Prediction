import streamlit as st
import pickle
import pandas as pd


Gender = ['Male','Female']
Height = ['170','175','180','185','190']
XG_model = pickle.load(open('model.pkl','rb'))

st.markdown(
    "<h1 style='text-align: center;'>Calories Burnt Predictor</h1>",
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)
with col1:
    select_gender = st.selectbox('Select Your Gender',sorted(Gender))
with col2:
    select_height = st.number_input('Your Height(cm)')


col3, col4 = st.columns(2)
with col3:
    select_age = st.number_input('Your Age')
with col4:
    select_weight = st.number_input('Your Weight(kg)')
col5, col6, col7 = st.columns(3)
with col5:
    select_duration = st.number_input('How long do you exercise for?(min)')
with col6:
    select_heart_rate = st.number_input('Your Heart Rate(BPM)')
with col7:
    select_body_temp = st.number_input('Your Body Temperature(°C)')


gender = select_gender
age = select_age
weight = select_weight
height = select_height
duration = select_duration
heart_rate = select_heart_rate
body_temp = select_body_temp

# Use CSS to center the button
st.markdown(
        """<style>div.Widget.row-widget.stButton {text-align: center;}</style>""",
        unsafe_allow_html=True
)
if st.button('Predict Probability'):
    MET = 4.0
    calories_per_kg_per_hour = 3.6
    # Calculating BMR using the Harris-Benedict equation
    if gender == 'Male':
        BMR = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:  # Assuming Female
        BMR = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    exercise_calories = MET * weight * (duration / 60) * calories_per_kg_per_hour
    total_calories_burned = BMR + exercise_calories
    input_data = {
        'Gender': [1 if select_gender == 'Female' else 0],
        'Age': [select_age],
        'Height': [select_height],
        'Weight': [select_weight],
        'Duration': [select_duration],
        'Heart_Rate': [select_heart_rate],
        'Body_Temp': [select_body_temp],
         # One-hot encoding for Gender
    }
    input_df = pd.DataFrame(input_data)

    # Making predictions using the XGBoost model
    result = XG_model.predict(input_df)
    st.text(result)