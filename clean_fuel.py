
import pandas as pd
import numpy as np
import openpyxl
import matplotlib.pyplot as plt
import seaborn as sns

# Use the correct filename case for the Excel file
fuel_price = pd.read_excel("Fuel_July_2024.xlsx")
state_to_zone = {'Abia': 'South East', 'Adamawa': 'North East', 'Akwa Ibom': 'South South', 'Anambra': 'South East','Bauchi': 'North East', 'Bayelsa': 'South South', 'Benue': 'North Central', 'Borno': 'North East','Cross River': 'South South', 'Delta': 'South South', 'Ebonyi': 'South East', 'Edo': 'South South','Ekiti': 'South West', 'Enugu': 'South East', 'FCT': 'North Central', 'Gombe': 'North East','Imo': 'South East', 'Jigawa': 'North West', 'Kaduna': 'North West', 'Kano': 'North West','Katsina': 'North West', 'Kebbi': 'North West', 'Kogi': 'North Central', 'Kwara': 'North Central','Lagos': 'South West', 'Nassarawa': 'North Central', 'Niger': 'North Central', 'Ogun': 'South West','Ondo': 'South West', 'Osun': 'South West', 'Oyo': 'South West', 'Plateau': 'North Central','Rivers': 'South South', 'Sokoto': 'North West', 'Taraba': 'North East', 'Yobe': 'North East','Zamfara': 'North West'}

# The column name has a trailing space: 'State '
fuel_price['Geopolitical Zone'] = fuel_price['State'].map(state_to_zone)

# Display the first few rows of the dataframe
print("\nFuel Price Data with Geopolitical Zones:")
print(fuel_price.head())

transprt_fare=pd.read_excel('TRANSPORT_COST_Watch_JULY_2024.xlsx',sheet_name='State Transport')
transprt_fare.columns = transprt_fare.columns.str.strip()
fuel_price.columns = fuel_price.columns.str.strip()
transprt_petrol=pd.merge(fuel_price,transprt_fare,on='State')
transprt_petrol.head(10)

# Rename specific columns with prefix
rename_dict = {'Jul-23': 'Fuel Price Jul-23','Jun-24': 'Fuel Price Jun-24','Jul-24': 'Fuel Price Jul-24'}
transprt_petrol = transprt_petrol.rename(columns=rename_dict)
#to clean up the column names
transprt_petrol.head(10)

transprt_petrol.info()
cols_with_na=[features for features in transprt_petrol.columns if transprt_petrol[features].isnull().sum()>=1]

for features in cols_with_na:
    print(features,np.round(transprt_petrol[features].isnull().sum(),2))
transprt_petrol.head(26)

import matplotlib.pyplot as plt  # Ensure pyplot is imported

columns_to_plot = ['Fuel Price Jul-23', 'Fuel Price Jun-24', 'Fuel Price Jul-24']
for feature in columns_to_plot:
    medians = transprt_petrol.groupby('Geopolitical Zone')[feature].median()
    medians.plot(kind='bar')
    plt.title(f'Barplot of Median {feature} by Geopolitical Zone')
    plt.xlabel('Geopolitical Zone')
    plt.ylabel('Median Fuel Price')
    plt.xticks(rotation=45)
    plt.show()

# Assuming transport fare columns are named e.g., 'Transport Jul-23'
fare_columns = ['Transport Jul-23', 'Transport Jun-24', 'Transport Jul-24']  # Adjust based on actual names
for price_col, fare_col in zip(columns_to_plot, fare_columns):
    correlation = transprt_petrol[price_col].corr(transprt_petrol[fare_col])
    print(f'Correlation between {price_col} and {fare_col}: {correlation:.2f}')
    
