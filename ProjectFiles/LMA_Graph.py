import geopandas as gpd
import pandas as pd
import plotly.express as px
import plotly.io as pio

# Load shapefiles
lmas = gpd.read_file('Datasets/LocalManagementArea.shp')
overflows = gpd.read_file('Datasets/EGM722_StormOverflows.shp')
wwtws = gpd.read_file('Datasets/EGM722_TreatedDisc.shp')

# Coordinate Reference setting
lmas = lmas.to_crs(overflows.crs)
wwtws = wwtws.to_crs(overflows.crs)

# Spatial Join Overflows and WwTWs to LMAs
overflows = gpd.sjoin(overflows, lmas, predicate='within')
wwtws = gpd.sjoin(wwtws, lmas, predicate='within')

# Count WwTWs per LMA
wwtws_count = wwtws.groupby('NAME').size().reset_index(name='WwTWs')

# Fill Monitored null values as No
overflows['Monitored'] = overflows['Monitored'].fillna('No').str.strip()

# Split overflows by Monitored Status
monitored = overflows[overflows['Monitored'] == 'Yes'].groupby('NAME').size().reset_index(name='Monitored Overflows')
non_monitored = overflows[overflows['Monitored'] == 'No'].groupby('NAME').size().reset_index(name='Non-Monitored Overflows')

# Merge and Drop Duplicates (Noticed duplicate bars being added on top of
data = lmas[['NAME']].drop_duplicates().merge(wwtws_count, on='NAME', how='left')\
                        .merge(monitored, on='NAME', how='left')\
                        .merge(non_monitored, on='NAME', how='left')\
                        .fillna(0)

# Convert counts to integers
data[['WwTWs', 'Monitored Overflows', 'Non-Monitored Overflows']] = data[['WwTWs', 'Monitored Overflows', 'Non-Monitored Overflows']].astype(int)

# Adjust for Plotly
df_melted = data.melt(id_vars=['NAME'], var_name='Type', value_name='Count')

# Create a bar chart (grouped) with colours for each type of discharge
fig = px.bar(df_melted,
             x='NAME',
             y='Count',
             color='Type',
             barmode='group',
             color_discrete_map={
                 'WwTWs': 'purple',
                 'Non-Monitored Overflows': 'black',
                 'Monitored Overflows': 'blue'
             })

# Show the figure
fig.show()

# Save this as a file
pio.write_image(fig, "bar_chart.png", format="png")
