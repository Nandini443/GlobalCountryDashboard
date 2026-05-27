"""
Generate world_countries.csv dataset for the Global Country Dashboard.
Run: python generate_data.py
"""
import pandas as pd

countries = [
    'United States','China','India','Germany','United Kingdom','France','Japan','Canada','Australia','Brazil',
    'South Korea','Italy','Spain','Mexico','Indonesia','Netherlands','Saudi Arabia','Turkey','Switzerland','Argentina',
    'Sweden','Poland','Belgium','Norway','Austria','United Arab Emirates','Nigeria','South Africa','Egypt','Thailand',
    'Denmark','Finland','Singapore','Malaysia','Vietnam','Bangladesh','Pakistan','Philippines','Chile','Colombia',
    'Portugal','Greece','Czech Republic','Romania','Hungary','New Zealand','Israel','Ukraine','Kazakhstan','Ethiopia',
    'Kenya','Ghana','Morocco','Algeria','Peru','Venezuela','Ecuador','Bolivia','Uruguay','Cuba',
    'Nepal','Sri Lanka','Myanmar','Cambodia','Mongolia','Azerbaijan','Georgia','Belarus','Lithuania','Latvia',
    'Estonia','Slovenia','Croatia','Slovakia','Bulgaria','Serbia','Iceland','Luxembourg','Malta','Cyprus'
]
continents = [
    'North America','Asia','Asia','Europe','Europe','Europe','Asia','North America','Oceania','South America',
    'Asia','Europe','Europe','North America','Asia','Europe','Asia','Asia','Europe','South America',
    'Europe','Europe','Europe','Europe','Europe','Asia','Africa','Africa','Africa','Asia',
    'Europe','Europe','Asia','Asia','Asia','Asia','Asia','Asia','South America','South America',
    'Europe','Europe','Europe','Europe','Europe','Oceania','Asia','Europe','Asia','Africa',
    'Africa','Africa','Africa','Africa','South America','South America','South America','South America','South America','North America',
    'Asia','Asia','Asia','Asia','Asia','Asia','Asia','Europe','Europe','Europe',
    'Europe','Europe','Europe','Europe','Europe','Europe','Europe','Europe','Europe','Europe'
]
pop = [
    335.9,1412.2,1428.6,84.6,67.7,68.4,124.5,38.8,26.5,215.3,
    51.7,59.0,47.4,128.4,277.5,17.9,36.4,85.3,8.8,45.5,
    10.5,37.6,11.7,5.4,9.1,10.0,220.1,60.1,105.9,71.8,
    5.9,5.5,5.9,33.6,98.2,169.4,231.4,115.6,19.6,51.9,
    10.3,10.7,10.9,19.0,9.7,5.1,9.7,43.5,19.1,126.5,
    54.0,33.5,37.5,44.7,32.5,28.3,18.0,12.1,3.5,11.3,
    29.7,21.9,54.4,17.0,3.4,10.1,3.7,9.4,2.8,1.9,
    1.3,2.1,4.0,5.5,6.9,7.0,0.4,0.6,0.5,1.3
]
gdp = [
    25462.7,17963.2,3385.1,4072.2,3070.7,2782.9,4231.1,2139.8,1675.4,1920.1,
    1665.2,1996.9,1397.3,1322.8,1319.1,1008.8,1040.7,906.5,800.8,641.1,
    585.9,688.1,579.3,482.4,471.0,507.1,472.6,399.0,387.1,495.4,
    395.3,281.2,424.1,373.0,362.6,460.2,376.5,371.8,301.0,343.6,
    255.3,213.9,290.9,301.2,176.7,247.4,488.5,160.5,220.6,126.9,
    98.8,74.3,118.9,169.9,242.6,97.5,98.8,44.0,71.1,107.6,
    40.4,88.0,65.0,27.4,16.9,78.7,24.3,71.5,69.0,38.8,
    36.8,57.8,14.1,71.5,89.1,53.3,27.6,86.0,14.5,27.7
]
hdi = [
    0.926,0.768,0.633,0.942,0.929,0.903,0.920,0.936,0.946,0.754,
    0.925,0.895,0.905,0.758,0.705,0.946,0.875,0.838,0.962,0.842,
    0.947,0.880,0.942,0.966,0.916,0.911,0.535,0.713,0.728,0.800,
    0.948,0.940,0.939,0.803,0.703,0.661,0.544,0.699,0.855,0.752,
    0.866,0.887,0.900,0.821,0.851,0.937,0.919,0.773,0.802,0.463,
    0.601,0.632,0.683,0.683,0.762,0.705,0.740,0.703,0.790,0.764,
    0.601,0.782,0.585,0.593,0.737,0.746,0.802,0.808,0.875,0.869,
    0.860,0.918,0.862,0.864,0.795,0.816,0.959,0.951,0.933,0.896
]
life_exp = [
    78.9,77.1,70.8,81.1,81.4,82.5,84.3,82.9,83.4,75.9,
    83.7,83.4,83.6,75.1,71.7,82.6,76.5,78.0,83.8,77.1,
    82.8,77.8,81.8,82.9,81.4,78.0,54.7,64.6,72.7,79.6,
    81.3,81.9,83.9,76.3,75.6,72.4,67.4,71.5,80.2,77.4,
    81.4,82.4,79.1,75.7,75.9,82.1,83.0,73.0,73.2,66.0,
    67.8,64.1,75.9,76.6,76.1,72.1,76.8,71.9,77.8,78.2,
    70.8,77.0,67.4,70.0,70.7,73.0,74.1,75.2,82.7,82.1,
    81.3,80.0,79.1,78.9,75.4,77.6,83.1,82.3,83.0,80.5
]
co2 = [
    14.24,8.20,1.96,8.09,5.55,4.81,8.73,14.26,15.22,2.25,
    11.85,5.55,5.17,3.66,2.29,9.14,18.73,5.94,4.24,3.86,
    3.82,8.16,8.17,7.68,7.03,20.57,0.59,7.55,2.46,3.82,
    5.21,7.50,9.43,8.74,3.81,0.47,0.92,1.08,4.41,1.90,
    4.42,6.12,9.15,3.97,4.55,6.57,6.62,5.24,14.36,0.13,
    0.34,0.56,1.79,3.78,2.44,6.22,2.36,1.79,2.22,3.18,
    0.52,0.94,0.51,0.40,5.35,3.70,2.50,3.58,9.39,3.56,
    5.42,7.55,6.14,6.25,4.63,6.22,9.72,15.30,2.10,6.50
]
internet = [
    91.8,73.7,46.3,91.7,94.8,86.0,82.9,93.4,91.7,81.3,
    97.6,79.8,87.3,73.5,62.1,92.6,95.7,81.0,97.2,88.4,
    97.3,86.0,94.0,98.5,90.7,99.0,51.1,72.2,72.2,88.0,
    98.0,94.0,97.0,89.3,73.2,39.4,36.5,76.0,94.4,73.9,
    82.0,81.8,87.3,71.5,82.0,93.3,93.3,79.4,89.9,19.1,
    29.5,53.3,84.7,71.6,74.3,72.5,60.3,43.8,89.0,67.0,
    48.1,57.3,26.2,43.3,67.4,80.3,71.4,87.7,99.0,95.2,
    95.5,96.0,91.2,88.7,76.7,82.7,99.0,99.0,94.0,88.0
]
military = [
    877.0,225.0,81.4,55.8,68.5,53.6,46.0,26.9,32.3,20.2,
    46.4,29.0,17.9,8.4,9.5,14.3,75.0,10.6,5.8,2.7,
    8.4,14.0,5.5,7.9,4.3,22.8,4.5,3.3,4.4,5.4,
    4.6,6.0,11.5,4.7,7.3,1.1,10.3,3.2,5.4,4.5,
    4.0,2.7,3.8,3.8,2.0,3.8,24.4,5.9,3.3,0.5,
    1.1,0.4,1.9,5.4,3.1,4.3,2.4,0.6,0.8,0.1,
    0.4,2.0,6.4,0.6,0.1,2.7,0.4,0.8,0.2,0.8,
    0.8,1.3,0.7,1.2,1.4,0.8,0.0,0.6,0.1,0.4
]
education = [
    0.900,0.706,0.574,0.945,0.937,0.874,0.854,0.938,0.941,0.726,
    0.877,0.859,0.847,0.703,0.640,0.938,0.755,0.763,0.944,0.780,
    0.916,0.873,0.900,0.915,0.903,0.839,0.500,0.697,0.620,0.749,
    0.920,0.918,0.845,0.736,0.638,0.524,0.404,0.669,0.786,0.700,
    0.818,0.836,0.875,0.759,0.803,0.921,0.854,0.778,0.786,0.388,
    0.539,0.584,0.596,0.601,0.704,0.649,0.702,0.645,0.742,0.740,
    0.501,0.742,0.511,0.525,0.643,0.810,0.734,0.748,0.889,0.844,
    0.834,0.866,0.832,0.839,0.738,0.758,0.930,0.921,0.880,0.860
]
unemployment = [
    3.5,5.2,7.8,3.0,3.7,7.3,2.6,5.1,3.7,8.9,
    2.9,7.6,12.9,2.8,5.4,3.6,6.0,10.5,2.2,6.7,
    8.5,2.9,5.6,3.6,5.1,2.7,4.2,29.1,7.2,1.1,
    5.0,7.2,2.1,3.5,2.3,4.9,6.2,2.5,8.0,10.8,
    6.4,13.0,2.2,5.5,4.2,3.2,3.8,18.8,4.8,19.0,
    5.3,4.5,10.5,11.7,4.9,6.4,3.8,3.6,7.9,0.9,
    11.4,4.7,0.9,0.3,7.0,5.8,18.9,3.9,2.8,5.6,
    3.8,4.1,7.9,4.3,5.3,5.1,3.4,5.9,4.5,6.8
]
capital = [
    'Washington D.C.','Beijing','New Delhi','Berlin','London','Paris','Tokyo','Ottawa','Canberra','Brasília',
    'Seoul','Rome','Madrid','Mexico City','Jakarta','Amsterdam','Riyadh','Ankara','Bern','Buenos Aires',
    'Stockholm','Warsaw','Brussels','Oslo','Vienna','Abu Dhabi','Abuja','Pretoria','Cairo','Bangkok',
    'Copenhagen','Helsinki','Singapore','Kuala Lumpur','Hanoi','Dhaka','Islamabad','Manila','Santiago','Bogotá',
    'Lisbon','Athens','Prague','Bucharest','Budapest','Wellington','Jerusalem','Kyiv','Nur-Sultan','Addis Ababa',
    'Nairobi','Accra','Rabat','Algiers','Lima','Caracas','Quito','Sucre','Montevideo','Havana',
    'Kathmandu','Sri Jayawardenepura','Naypyidaw','Phnom Penh','Ulaanbaatar','Baku','Tbilisi','Minsk','Vilnius','Riga',
    'Tallinn','Ljubljana','Zagreb','Bratislava','Sofia','Belgrade','Reykjavik','Luxembourg City','Valletta','Nicosia'
]
currency = [
    'USD','CNY','INR','EUR','GBP','EUR','JPY','CAD','AUD','BRL',
    'KRW','EUR','EUR','MXN','IDR','EUR','SAR','TRY','CHF','ARS',
    'SEK','PLN','EUR','NOK','EUR','AED','NGN','ZAR','EGP','THB',
    'DKK','EUR','SGD','MYR','VND','BDT','PKR','PHP','CLP','COP',
    'EUR','EUR','CZK','RON','HUF','NZD','ILS','UAH','KZT','ETB',
    'KES','GHS','MAD','DZD','PEN','VES','USD','BOB','UYU','CUP',
    'NPR','LKR','MMK','KHR','MNT','AZN','GEL','BYN','EUR','EUR',
    'EUR','EUR','EUR','EUR','BGN','RSD','ISK','EUR','EUR','EUR'
]
area = [
    9833517,9596960,3287263,357114,242495,640679,377930,9984670,7692024,8515767,
    100210,301340,505990,1964375,1904569,41543,2149690,783562,41285,2780400,
    450295,312679,30528,385207,83871,83600,923768,1219090,1001449,513120,
    42924,338424,721,329847,331212,147570,881913,300000,756102,1141748,
    92212,131957,78866,238397,93028,270467,22072,603550,2724900,1104300,
    582650,238533,446550,2381741,1285216,916445,283561,1098581,176215,109884,
    147181,65610,676578,181035,1564116,86600,69700,207600,65300,64589,
    45228,20273,56594,49035,110879,77474,103000,2586,316,9251
]

import pandas as pd
df = pd.DataFrame({
    'Country': countries, 'Continent': continents,
    'Population_M': pop, 'GDP_Billion_USD': gdp,
    'HDI': hdi, 'Life_Expectancy': life_exp,
    'CO2_Tons_Per_Capita': co2, 'Internet_Penetration_Pct': internet,
    'Military_Spend_Billion_USD': military, 'Education_Index': education,
    'Unemployment_Rate_Pct': unemployment, 'Capital_City': capital,
    'Currency': currency, 'Area_Km2': area
})
df['GDP_Per_Capita_USD'] = ((df['GDP_Billion_USD']*1e9)/(df['Population_M']*1e6)).round(0).astype(int)
df['Population_Density'] = (df['Population_M']*1e6/df['Area_Km2']).round(2)
df.to_csv('world_countries.csv', index=False)
print(f"✅ Dataset saved: {len(df)} countries × {len(df.columns)} columns")
