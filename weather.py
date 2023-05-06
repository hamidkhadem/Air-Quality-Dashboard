# Import the required library
import requests, json
from pycountry import countries
from statistics import mean
import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim
import datetime
import time

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

# defined function that return avg European AQI
def get_avg_euro_AQI(city_country_name, start_date, end_date):

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

    # create a new dataframe from "hourly" dictionary in json file
    df = pd.DataFrame(source_json["hourly"])
    
    return df


# function that return dataframe with two column time and value of European AQI - default date is for 5 days
def get_df_euro_AQI(city_country_name, start_date='2022-08-01', end_date='2022-08-05'):

    # get latitude, longitude
    latitude, longitude = get_lat_long(city_country_name)
    api_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={latitude}&longitude={longitude}&hourly=european_aqi&start_date={start_date}&end_date={end_date}"
    # get json format info from desired api_url
    source_json = requests.get(api_url).json()

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
def air_quality_table(df, city_country_name):
    # defined output dataframe
    dic ={'city name': city_country_name, 'total day': 0, 'good': 0, 'fair': 0, 'moderate': 0, 'poor': 0, 'very poor': 0}
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
    result = air_quality_table(df, city_country_name)
    
    return result

"""_summary_
This function get the list of cities or country, start_date,end_date and 
print the number of day in  The European Air Quality Index
"""
def cities_countries_AQI(cities_countries_name, start_date='2022-08-05', end_date='2023-01-05'):
    # defined dataframe for return
    result_df = pd.DataFrame()
    # loop in the list and append to the result_df
    for city_country_name in cities_countries_name:
        # first Extract info from API
        df = get_df_euro_AQI(city_country_name, start_date, end_date)
        # transfer dataframe
        df = clean_df_euro_AQI(df)
        # get the result and transfer to dataframe- it dictionary={'good': 0, 'fair': 0, 'moderate': 0, 'poor': 0, 'very poor': 0, 'total day': 0}
        new_df = pd.DataFrame(air_quality_table(df, city_country_name), index=[0])
        print(new_df.head())
        # append to the result_df
        result_df = pd.concat([result_df, new_df], ignore_index=True)
        result_df.reset_index()
        # create a sleep for don't request from api much
        time.sleep(5)
    
    return result_df

# for test the functions
if __name__=="__main__":
    
    # list cities
    list_cities = ['Dubai', 'Berlin', 'Paris', 'Sydney', 'Chicago']
    df = cities_countries_AQI(list_cities)
    
    print(df.head())

    # save the result in csv file
    df.to_csv("src/air_quality.csv", index=False)
    print("Dataframe was saved!")
    # while(True):
    #     city_country_name = input("Please Enter the your desired city or country name?")
    #     print(
    #         f"AirQuality for {city_country_name} is: \n {city_country_AQI(city_country_name)} \n")
