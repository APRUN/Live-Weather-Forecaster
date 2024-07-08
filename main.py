import requests
import streamlit as st
import geonamescache
import re

api_key = 'b8db2b329e104b16dc9e6e086050e346'

url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

# Streamlit interface
st.title("Weather")
user_input = st.text_input("Enter the city name: ")
gc = geonamescache.GeonamesCache()
cities = gc.get_cities()

def extract_city_name(user_input, cities):
    pattern = r'\b(' + '|'.join(re.escape(city) for city in cities) + r')\b'
    match = re.search(pattern, user_input, re.IGNORECASE)
    if match:
        return match.group(0)
    return None
# city_name=extract_city_name(user_input, cities)
city_name=user_input
if city_name:
    response = requests.get(url.format(user_input, api_key))
    if response.status_code == 200:
        weather_data = response.json()
        data = weather_data['weather'][0]['main']
        temp = weather_data['main']['temp']
        st.write(f"Weather: {data}")
        st.write(f"Temperature: {temp - 273.15:.2f}°C")  # Convert from Kelvin to Celsius
        st.write(f'The weather in {user_input} is {data} and the temperature is {temp} K')
        st.snow()
    else:
        st.write("City not found!")
else:
    st.write("Please enter a city name.")
