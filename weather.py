# Import the required library
import requests, json
from pycountry import countries
from statistics import mean
import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim


# use geopy lib to defined a function to return latitude and longitude of a country or city name
def get_lat_long(country_name):
    # Initialize Nominatim API
    geolocator = Nominatim(user_agent="MyApp")
    # search for desired name
    location = geolocator.geocode(country_name)

    return int(location.latitude), int(location.longitude)

# defined function that return avg European AQI
def get_avg_euro_AQI(country_name):
    """he API endpoint /v1/air-quality accepts a geographical coordinate,
    a list of weather variables and responds with a JSON hourly air quality forecast for 5 days.
    Time always starts at 0:00 today.
    """
    # get latitude, longitude
    latitude, longitude = get_lat_long(country_name)
    api_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={latitude}&longitude={longitude}&hourly=european_aqi&domains=cams_global&timezone=auto"
    
    # get json file from desired api_url
    source_json = requests.get(api_url).json()
    # get the list of hourly air quality forecast for 5 days
    european_aqi_list = source_json["hourly"]['european_aqi']
    # remove none value
    european_aqi_series = pd.Series(european_aqi_list).dropna()
    # find avarage
    avg_european_aqi = european_aqi_series.mean()
    
    return int(avg_european_aqi)

# defined a function that get list of countries and return dataframe of weather info
def get_weather_df(countries_list):
    # change country name to standard
    countries_list = [countries.search_fuzzy(
        country_name)[0].name for country_name in countries_list]
    # get country 3chars ID
    country_code_list = [countries.search_fuzzy(
        country_name)[0].alpha_3 for country_name in countries_list]
    
    # avarage list of euro air quality
    avg_euro_aqi = list(map(lambda country_name : get_avg_euro_AQI(country_name), countries_list))
    
    # create weather dic and return pandas dataframe
    dic_weather = {
        "country_id": country_code_list,
        "country_name": countries_list,
        "avg_euro_aqi": avg_euro_aqi,
    }
    return pd.DataFrame(dic_weather)

    
# for test the functions
if __name__=="__main__":
    # defined list of countries name
    countries_list = ["lebanon", "United Arab", "Canada", "Germany"]
    # get dataframe and print head of them
    df = get_weather_df(countries_list)
    print(df.head())
