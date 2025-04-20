# -*- coding: utf-8 -*-
"""
Created on Sat Apr 19 20:40:38 2025

@author: joliz
"""
import pandas as pd 
import numpy as np
print("Start of Script")

# Concat CSVs 
stations_a = pd.read_csv("C:/Users/joliz/OneDrive/Documents/APA Final/3997206.csv")
stations_b = pd.read_csv("C:/Users/joliz/OneDrive/Documents/APA Final/3997225.csv")
stations_c = pd.read_csv("C:/Users/joliz/OneDrive/Documents/APA Final/3997229.csv")
concat_weather = pd.concat([stations_a, stations_b, stations_c])

# All Weather Stations List
all_stations = concat_weather[['STATION', 'NAME', 'LATITUDE', 'LONGITUDE']].drop_duplicates(subset='STATION').reset_index(drop=True)

# Cleaning Data to Find Stations with Needed Weather Data for Analysis
    # January - April 
concat_weather['DATE'] = pd.to_datetime(concat_weather['DATE'])
culled_data = concat_weather[concat_weather['DATE'].dt.month.isin([1, 2, 3, 4])].copy()

    # Actually Has TMAX & TMIN data 
culled_data = culled_data.dropna(subset=['TMAX', 'TMIN'])
culled_data = culled_data.drop(columns=['TAVG', 'NAME', 'LATITUDE', 'LONGITUDE', 'TMAX_ATTRIBUTES', 'TMIN_ATTRIBUTES', 'TAVG_ATTRIBUTES', 'ELEVATION'])

    # Creating Indicator Variable "IDEAL"
culled_data["IDEAL"] = np.nan
culled_data["IDEAL"] = np.where(
    (culled_data["TMIN"] >= 15) & (culled_data["TMIN"] <= 32) &
    (culled_data["TMAX"] > 32) & (culled_data["TMAX"] <=50),
    1,
    0
)

# Finding % of Ideal Weather Days for Each Station, BY MONTH 
    # 1) Extracting Month/Year 
culled_data['YEAR_MONTH'] = pd.to_datetime(culled_data['DATE']).dt.to_period('M').astype(str)

    # 2) Quantifying Days with Data 
total_days = culled_data.groupby(['STATION', 'YEAR_MONTH'])['IDEAL'].count().reset_index(name='Total')

    # 3) Quantifying # of Days with Ideal Conditions 
ideal_days = culled_data[culled_data['IDEAL'] == 1].groupby(['STATION', 'YEAR_MONTH'])['IDEAL'].count().reset_index(name='Ideal')

    # 4) Merging Data 
merged = pd.merge(total_days, ideal_days, on=['STATION', 'YEAR_MONTH'], how='left')
merged['Ideal'] = merged['Ideal'].fillna(0)

    # 5) Finding Rates 
merged['Percent_Ideal'] = (merged['Ideal'] / merged['Total']) * 100

    # 6) Restructing with a Pivot Table
station_monthly = merged.pivot(index='STATION', columns='YEAR_MONTH', values='Percent_Ideal').reset_index()


# Adding Location Data 
        # Lat, Long, and Name of Station from all_stations 
station_monthly = pd.merge(
    station_monthly,
    all_stations[['STATION', 'NAME', 'LATITUDE', 'LONGITUDE']],
    on='STATION',
    how='left'
)

    # Adding Zip Codes, Manually 
station_monthly["ZIP"] = np.nan
zip_list = {
    "ANGELICA, NY US": "14709",
    "ITHACA CORNELL UNIVERSITY, NY US": "14850",
    "BATAVIA, NY US": "14020",
    "FULTON, NY US": "13069",
    "LOWVILLE, NY US": "13367",
    "PENN YAN AIRPORT, NY US": "14527",
    "MALONE, NY US": "12953",
    "FRANKLINVILLE, NY US": "14737",
    "WATERTOWN, NY US": "13601",
    "FREEVILLE 1 NE, NY US": "13068",
    "WARSAW 6 SW, NY US": "14043",
    "CANANDAIGUA 3 S, NY US": "14424",
    "WYOMING 3 W, NY US": "14591",
    "COOPERSTOWN, NY US": "13326",
    "JAMESTOWN 4 ENE, NY US": "14701",
    "SARANAC LAKE ADIRONDACK REGIONAL AIRPORT, NY US": "12983",
    "SODUS 1 W, NY US": "14551",
    "WALES, NY US": "14052",
    "GOUVERNEUR 3 NW, NY US": "13646",
    "SHERBURNE NEW YORK, NY US": "13460",
    "FULTON OSWEGO CO AIRPORT, NY US": "13069",
    "STONYKILL NEW YORK, NY US": "12590",
    "MORRISVILLE 6 SW, NY US": "13480",
    "EAST SIDNEY, NY US": "13775",
    "SHERBURNE, NY US": "13460",
    "WHITNEY POINT DAM, NY US": "13862",
    "GLOVERSVILLE 7 NW PECK LAKE, NY US": "12078",
    "DOWNSVILLE DAM, NY US": "13755",
    "NORTH TONAWANDA, NY US": "14120",
    "ITHACA 13 E, NY US": "13053",
    "NORWICH, NY US": "13815",
    "COLTON 2 N, NY US": "13625",
    "SARATOGA SPRINGS 4 SW, NY US": "12866",
    "LAKE PLACID 2 S, NY US": "12946",
    "OGDENSBURG 4 NE, NY US": "13669",
    "WHITEHALL, NY US": "12887",
    "ELLENBURG DEPOT, NY US": "12934",
    "HIGHMARKET 2 W, NY US":"13325",
    "TUPPER LAKE SUNMOUNT, NY US": "12986",
    "STILLWATER RESERVOIR, NY US": "13367",
    "VICTOR 2 NW, NY US": "14564",
    "MACEDON LOCK E30, NY US": "14502",
    "MEXICO 2 SW, NY US": "13114",
    "CANTON 4 SE, NY US": "13617",
    "COBLESKILL 2 ESE, NY US": "12043"
    }
station_monthly["ZIP"] = station_monthly["NAME"].map(zip_list)

# Reordering Columns
cols = station_monthly.columns.tolist()
new_order = ['STATION', 'NAME', 'ZIP', 'LATITUDE', 'LONGITUDE'] + [col for col in cols if col not in ['STATION', 'NAME', 'ZIP', 'LATITUDE', 'LONGITUDE']]
station_monthly = station_monthly[new_order]

# Saving station_monthly
station_monthly.to_csv("station_monthly.csv")

# ------------------------------------------------------------
# Finding % of Ideal Weather Days for Each Station, BY YEAR 
# NOTES: This is basically the same process as by month, check above <3
culled_data['YEAR'] = pd.to_datetime(culled_data['DATE']).dt.year.astype(str)
total_days_year = culled_data.groupby(['STATION', 'YEAR'])['IDEAL'].count().reset_index(name='Total')
ideal_days_year = culled_data[culled_data['IDEAL'] == 1].groupby(['STATION', 'YEAR'])['IDEAL'].count().reset_index(name='Ideal')
merged_year = pd.merge(total_days_year, ideal_days_year, on=['STATION', 'YEAR'], how='left')
merged_year['Ideal'] = merged_year['Ideal'].fillna(0)
merged_year['Percent_Ideal'] = (merged_year['Ideal'] / merged_year['Total']) * 100
station_yearly = merged_year.pivot(index='STATION', columns='YEAR', values='Percent_Ideal').reset_index()
station_yearly = pd.merge(
    station_yearly,
    all_stations[['STATION', 'NAME', 'LATITUDE', 'LONGITUDE']],
    on='STATION',
    how='left'
)
station_yearly["ZIP"] = station_yearly["NAME"].map(zip_list)
station_yearly = station_yearly.drop(columns=["STATION","NAME", "LATITUDE", "LONGITUDE"])
print(station_yearly.columns)
station_yearly.to_csv("Zip_Conditions.csv")

# Station Locations 
station_locations = all_stations.copy()
station_locations = station_locations.dropna(subset=['LATITUDE', 'LONGITUDE']).reset_index(drop=True)
station_locations["INC"] = np.nan
station_locations["INC"] = station_locations["STATION"].isin(station_monthly["STATION"]).astype(int)
    # SAVING
station_locations['LATITUDE'] = station_locations['LATITUDE'].round().astype(int)
station_locations['LONGITUDE'] = station_locations['LONGITUDE'].round().astype(int)
station_locations['INC'] = station_locations['INC'].astype(int)
station_locations.to_csv("station_locations.csv", index=False)

