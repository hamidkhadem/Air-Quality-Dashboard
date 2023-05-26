
# Project idea: Air Quality Dashboard
### Team: Andrew Mounir, Ali Elmasri, Hamid Khadem

To see demo of project: [Air Quality Dashboard](hkhadem.pythonanywhere.com)

This project done for ZAKA AI Capstone Project. As Data Professionals, we selected a project to show us technical skills by creating a Dashboard, connecting with the Data Pipeline and reading and writing from Database.
Air-Quality-Dashboard is using The European Air Quality Index (AQI) to show and compare the air quality of desired cities(Dubai, Berlin, Paris, Sydney, Chicago). Also, you can search every city with the selected date range and see the result in Bar Chart.
we extract AQI Data for 5 cities from Air Quality API | Open_Meteo and save it in the CSV file format. It shows the number of days in different (AQI) ranges from good to very poor, from '2022-08-05' to '2023-01-05'.
Another part of the dashboard is a live data pipeline from API to Dashboard. It’s using Open-meteo API to get the AQI data to show you the Air Quality of your city in your selected date range on the Dashboard.
The European Air Quality Index (AQI) ranges from 0-20 (good), 20-40 (fair), 40-60 (moderate), 60-80 (poor), 80-100 (very poor), and exceeds 100 for extremely poor conditions.
We’re using Traffic light color to show the situation of Air Quality in a special city.
We’re using Dash for creating Dashboard. Dash is the original low-code framework for rapidly building data apps in Python. Dash is a Python framework created by plotly for creating interactive web applications and It’s good for creating an Interactive Dashboard.
And with the help of free web hosts like PythonAnyWhere shared the dashboard app on the Internet.
In this project, we're going to ingest Different Data Sources and create ELT, and data pipelines for the Dashboard App.

for configuring the python virtual enviroment:
<li>$ python -m venv py_env</li>
<li>$ pip install pycountry</li>
<li>$ pip install dash</li>

### Get more info:
https://docs.google.com/document/d/1j-eLPE20rUdBJsRyjCg2x0Pl7pIsyTYW8LUeP__b19E/edit?usp=sharing
