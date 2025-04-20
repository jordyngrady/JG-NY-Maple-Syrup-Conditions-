# -*- coding: utf-8 -*-
"""
Created on Sun Apr 20 14:19:31 2025

@author: joliz
"""
import pandas as pd
import numpy as np
print("---Start of Script---")

# Importing Data 
weather2024 = pd.read_csv("C:/Users/joliz/OneDrive/Documents/APA Final/weather2024ny.csv")
weather2023 = pd.read_csv("C:/Users/joliz/OneDrive/Documents/APA Final/weather2023ny.csv")
weather2022 = pd.read_csv("C:/Users/joliz/OneDrive/Documents/APA Final/weather2022ny.csv")
weather2021 = pd.read_csv("C:/Users/joliz/OneDrive/Documents/APA Final/weather2021ny.csv")
weather2020 = pd.read_csv("C:/Users/joliz/OneDrive/Documents/APA Final/weather2020ny.csv")

print("2024",weather2024.columns)
print("2023",weather2023.columns)
print("2022",weather2022.columns)
print("2021",weather2021.columns)
print("2020",weather2020.columns)

# Concating Date
weather_5year = pd.concat([weather2020, weather2021, weather2022, weather2023, weather2024], ignore_index=True)
weather_5year = weather_5year.drop(columns=["ELEVATION", "DATE", "TMAX_ATTRIBUTES", "TMIN_ATTRIBUTES"])

# Keeping Data we Want 
    # Actually Has TMAX & TMIN data 
weather_5year = weather_5year.dropna(subset=['TMAX', 'TMIN'])

    # Creating Indicator Variable "IDEAL"
weather_5year["IDEAL"] = np.nan
weather_5year["IDEAL"] = np.where(
    (weather_5year["TMIN"] >= 15) & (weather_5year["TMIN"] <= 32) &
    (weather_5year["TMAX"] > 32) & (weather_5year["TMAX"] <=50),
    1,
    0) 

# Quantifying Ideal Days in 2024
ideal5year = weather_5year.groupby(['STATION', 'NAME', 'LATITUDE', 'LONGITUDE'])['IDEAL'].agg(
    Total_Days='count',
    Ideal_Days='sum'
).reset_index()

# Calculate percent of ideal days
ideal5year['Percent_Ideal'] = (ideal5year['Ideal_Days'] / ideal5year['Total_Days']) * 100

# SAVE WEATHER DATA
ideal5year.to_csv("ideal5year.csv", index=False)

print(ideal5year)