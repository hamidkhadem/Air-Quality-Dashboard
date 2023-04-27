# Import the required library
import requests, json
from pycountry import countries
from statistics import mean
import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim
import datetime

# use geopy lib to defined a function to return latitude and longitude of a country or city name
def get_lat_long(city_country_name):
    # Initialize Nominatim API
    geolocator = Nominatim(user_agent="MyApp")
    # search for desired name
    location = geolocator.geocode(city_country_name)

    return location.latitude, location.longitude

# defined function that return avg European AQI
def get_avg_euro_AQI(city_country_name):
    """he API endpoint /v1/air-quality accepts a geographical coordinate,
    a list of weather variables and responds with a JSON hourly air quality forecast for 5 days.
    Time always starts at 0:00 today.
    """
    # get latitude, longitude
    latitude, longitude = get_lat_long(city_country_name)
    api_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={latitude}&longitude={longitude}&hourly=european_aqi&domains=cams_global&timezone=auto"
    
    # get json format info from desired api_url
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

# function that return dataframe with two column time and value of European AQI
def get_df_euro_AQI(city_country_name):
    """he API endpoint /v1/air-quality accepts a geographical coordinate,
    a list of weather variables and responds with a JSON hourly air quality forecast from 22/8/1 to 23/4/1.
    Time always starts at 0:00 today.
    """
    # get latitude, longitude
    latitude, longitude = get_lat_long(city_country_name)
    api_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={latitude}&longitude={longitude}&hourly=european_aqi&start_date=2022-08-01&end_date=2022-08-10"
    # get json format info from desired api_url
    source_json = requests.get(api_url).json()
    # get the list of two desired column
    european_aqi_column = source_json["hourly"]['european_aqi']
    time_column = source_json["hourly"]['time']
    # create a new dataframe from "hourly" dictionary in json file
    df = pd.DataFrame(source_json["hourly"])
    
    return df

# function that return a clean dataframe euro AQI
# by removing Nane value and replace avrage value of AQI for one day
def clean_df_euro_AQI(df):
    # first drop Nan value
    df = df.dropna()
    df = df.reset_index()
    # change the value of time column from hourly("2023-04-21T00:00") to daily("2023-04-21")
    df['time'] = df['time'].map(lambda x: datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M").date())
    # calculate the avrage of AQI for same date
    avg_series = df.groupby('time')["european_aqi"].mean()
    new_df = pd.DataFrame({'time':avg_series.index, 'avg_AQI': avg_series.values})
    
    return new_df


"""_summary_
    function is geting a clean euro AQI dataframe and
    return dictionary of the number of day according AQI
    Note: The European Air Quality Index (AQI) ranges
    from 0-20 (good), 20-40 (fair), 40-60 (moderate),
    60-80 (poor), 80-100 (very poor) and exceeds 100 for extremely poor conditions.
"""
def air_quality_table(df):
    # defined output dataframe
    dic ={'good': 0, 'fair': 0, 'moderate': 0, 'poor': 0, 'very poor': 0, 'total day': 0}
    # loop for counting day in those classified
    df.reset_index()
    for index, values in df.iterrows():
        dic['total day'] += 1
        cp = values['avg_AQI']
        if cp <= 20:
            dic['good'] += 1
        elif cp <= 40:
            dic['fair'] += 1
        elif cp <= 60:
            dic['moderate'] += 1
        elif cp <= 80:
            dic['poor'] += 1
        else:
            dic['very poor'] += 1
    
    return dic


"""_summary_
This function get the name of city or country and 
print the number of day in  The European Air Quality Index
"""
def city_country_AQI(city_country_name):
    # first Extract info from API
    df = get_df_euro_AQI(city_country_name)
    # transfer dataframe
    df = clean_df_euro_AQI(df)
    # get the result
    result = air_quality_table(df)
    
    return result

# for test the functions
if __name__=="__main__":

    while(True):
        city_country_name = input("Please Enter the your desired city or country name?")
        print(
            f"AirQuality for {city_country_name} is: \n {city_country_AQI(city_country_name)} \n")
