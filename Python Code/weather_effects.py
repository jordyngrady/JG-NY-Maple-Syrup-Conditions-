# -*- coding: utf-8 -*-
"""
Created on Sat Apr 19 22:14:19 2025

@author: joliz
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
print("---Start of Script---")

# Importing Data 
ny_producers = pd.read_csv("ny_producers.csv")
producersbyzip = pd.read_csv("producersbyzip.csv")
station_monthly = pd.read_csv("station_monthly.csv")

# ZIP Codes in station_monthly 
zip_codes = station_monthly['ZIP'].dropna().unique().tolist()

# Building Final Dataframe
    # Producers with weather data 
producers_with_data = ny_producers[ny_producers['ZIP'].isin(zip_codes)].copy()
    # Merge weather station data into producer list using ZIP
producer_conditions = pd.merge(
    producers_with_data,
    station_monthly,
    on='ZIP',
    how='left'
)
    # Renaming columns
producer_conditions = producer_conditions.rename(columns={
    'NAME_x': 'PRODUCER',
    'NAME_y': 'STATION_NAME'
})

    # SAving to CSV
producer_conditions.to_csv("producers_idealconditions.csv")
print(producers_with_data.shape)
print(producers_conditions.head)

# ---------- LINE GRAPH 
value_vars = [col for col in producer_conditions.columns if '-' in col]
long_df = producer_conditions.melt(
    id_vars=['PRODUCER'],
    value_vars=value_vars,
    var_name='Month_Year',
    value_name='Percent_Ideal'
)

long_df['Year'] = long_df['Month_Year'].str[:4]
long_df['Month'] = long_df['Month_Year'].str[5:]
month_order = ['01', '02', '03', '04']
month_labels = ['Jan', 'Feb', 'Mar', 'Apr']
month_map = dict(zip(month_order, month_labels))
long_df['Month_Label'] = long_df['Month'].map(month_map)
long_df = long_df[long_df['Month'].isin(month_order)]

sns.set(style="whitegrid")
g = sns.FacetGrid(
    long_df,
    col="Year",
    col_order=['2019', '2020', '2021', '2022', '2023'],
    col_wrap=5,
    height=4.5,
)

g.map_dataframe(
    sns.lineplot,
    x="Month_Label",
    y="Percent_Ideal",
    hue="PRODUCER",
    errorbar=None,
    legend=False,
    linewidth=1.5,
    marker='o'
)

g.set_titles("{col_name}")
g.set_axis_labels("Month", "% Days with Ideal Conditions")
g.set(ylim=(0, 100))

for ax in g.axes.flat:
    if ax.legend_:
        ax.legend_.remove()

plt.subplots_adjust(top=0.85)
g.fig.suptitle("% of Days with Ideal Conditions for Maple Production, By Month and Producer (2019–2023)", fontsize=16)
plt.tight_layout()
plt.savefig("ideal_conditions_lineplot.png", dpi=300)
plt.show()


# ---------- BOX & WHISKERS 

value_vars = [col for col in producer_conditions.columns if '-' in col]
long_df = producer_conditions.melt(
    id_vars=['PRODUCER'],
    value_vars=value_vars,
    var_name='Month_Year',
    value_name='Percent_Ideal'
)

long_df['Year'] = long_df['Month_Year'].str[:4]
long_df['Month'] = long_df['Month_Year'].str[5:]
month_order = ['01', '02', '03', '04']
month_labels = ['Jan', 'Feb', 'Mar', 'Apr']
month_map = dict(zip(month_order, month_labels))
long_df['Month_Label'] = long_df['Month'].map(month_map)
long_df = long_df[long_df['Month'].isin(month_order)]

sns.set(style="whitegrid")
g = sns.FacetGrid(
    long_df,
    col="Year",
    col_order=['2019', '2020', '2021', '2022', '2023'],
    col_wrap=5,
    height=4.5,
    sharey=True
)

g.map_dataframe(
    sns.boxplot,
    x="Month_Label",
    y="Percent_Ideal",
    palette="pastel"
)
overall_avg = long_df['Percent_Ideal'].mean()
for ax in g.axes.flat:
    ax.axhline(overall_avg, color='red', linestyle='--', linewidth=1)
    
g.set_titles("{col_name}")
g.set_axis_labels("Month", "% Days with Ideal Conditions")
g.set(ylim=(0, 100))

plt.subplots_adjust(top=0.85)
g.fig.suptitle("Distrbution of Ideal Conditions for Maple Production, By Month (2019–2023)", fontsize=16)
plt.tight_layout()
plt.savefig("ideal_conditions_boxplot.png", dpi=300)
plt.show()


