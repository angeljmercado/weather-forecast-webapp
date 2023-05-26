import streamlit as st
import plotly.express as px
from backend import get_data

st.title("Weather Forecast for the Next Days")

place = st.text_input("Place: ")

days = st.slider("Forecast Days", min_value=1, max_value=5,
help="Select the number of days that you want to be forecasted")

option = st.selectbox("Select data to view", ("Temperature", "Sky"))

st.subheader(f"{option} for the next {days} days in {place}")

if place:
    try:
        filtered_data = get_data(place, days)
        if option == "Temperature":
            temperatures = [dict["main"]["temp"] for dict in filtered_data]
            fahrenheit_temps = [int(temperature) / 10 * 1.8 + 32 for temperature in temperatures]
            #celcius_temps = [int(temperature) / 10 for temperature in temperatures]
            dates = [dict["dt_txt"] for dict in filtered_data]
            figure = px.line(x=dates, y=fahrenheit_temps, 
            labels={"x":"Date", "y":"Temperatures(F)"})
            st.plotly_chart(figure)

        if option == "Sky":
            weather_conditions = [dict["weather"][0]["main"] for dict in filtered_data]
            images = {"Clear":"images/clear.png", "Clouds":"images/cloud.png", 
            "Rain":"images/rain.png", "Snow":"images/snow.snow.png"}
            weather_images = [images[condition] for condition in weather_conditions]
            st.image(weather_images, width=115)
    except KeyError:
        st.error("The value you entered doesn't exist")
