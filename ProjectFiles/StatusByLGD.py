import os
import geopandas as gpd
import matplotlib.pyplot as plt
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
import matplotlib.lines as mlines


def generate_handles(labels, colors, edge='k', alpha=1):
    """
    Generate matplotlib patch handles to create a legend of each of the features in the map.

    Parameters
    ----------

    labels : list(str)
        the text labels of the features to add to the legend

    colors : list(matplotlib color)
        the colors used for each of the features included in the map.

    edge : matplotlib color (default: 'k')
        the color to use for the edge of the legend patches.

    alpha : float (default: 1.0)
        the alpha value to use for the legend patches.

    Returns
    -------

    handles : list(matplotlib.patches.Rectangle)
        the list of legend patches to pass to ax.legend()
    """
    lc = len(colors)  # get the length of the color list
    handles = [] # create an empty list
    for ii in range(len(labels)): # for each label and color pair that we're given, make an empty box to pass to our legend
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[ii % lc], edgecolor=edge, alpha=alpha))
    return handles

def scale_bar(ax, length=20, location=(0.92, 0.95)):
    """
    Create a scale bar in a cartopy GeoAxes.

    Parameters
    ----------

    ax : cartopy.mpl.geoaxes.GeoAxes
        the cartopy GeoAxes to add the scalebar to.

    length : int, float (default 20)
        the length of the scalebar, in km

    location : tuple(float, float) (default (0.92, 0.95))
        the location of the center right corner of the scalebar, in fractions of the axis.

    Returns
    -------
    ax : cartopy.mpl.geoaxes.GeoAxes
        the cartopy GeoAxes object

    """
    x0, x1, y0, y1 = ax.get_extent() # get the current extent of the axis
    sbx = x0 + (x1 - x0) * location[0] # get the right x coordinate of the scale bar
    sby = y0 + (y1 - y0) * location[1] # get the right y coordinate of the scale bar

    ax.plot([sbx, sbx-length*1000], [sby, sby], color='k', linewidth=4, transform=ax.projection) # plot a thick black line
    ax.plot([sbx-(length/2)*1000, sbx-length*1000], [sby, sby], color='w', linewidth=2, transform=ax.projection) # plot a white line from 0 to halfway

    ax.text(sbx, sby-(length/4)*1000, f"{length} km", ha='center', transform=ax.projection, fontsize=6) # add a label at the right side
    ax.text(sbx-(length/2)*1000, sby-(length/4)*1000, f"{int(length/2)} km", ha='center', transform=ax.projection, fontsize=6) # add a label in the center
    ax.text(sbx-length*1000, sby-(length/4)*1000, '0 km', ha='center', transform=ax.projection, fontsize=6) # add a label at the left side

    return ax

# load the datasets
LGD = gpd.read_file(os.path.abspath('Datasets/LGD2012.shp'))
towns = gpd.read_file(os.path.abspath('Datasets/Towns.shp'))
overflows = gpd.read_file(os.path.abspath('Datasets/EGM722_StormOverflows.shp'))

ni_utm = ccrs.UTM(29)  # create a Universal Transverse Mercator reference system to transform our data.
# NI is in UTM Zone 29, so we pass 29 to ccrs.UTM()
LGD = LGD.to_crs(ni_utm)
towns = towns.to_crs(ni_utm)
overflows = overflows.to_crs(ni_utm)

# Filter for for council. In this case Fermanagh and Omagh was selected
council = LGD[LGD['LGDNAME']=='Fermanagh and Omagh']

# Filter for unsatisfactory discharges
unsatis_disc = overflows[overflows['Classifica']=='Unsatisfactory']

# Filter for unsatisfactory discharges and town names within the council filter area.
unsatis_disc = unsatis_disc.sjoin(council, predicate="within")
towns_council= towns.sjoin(council, predicate="within")

# Convert new datasets CRS to ni_utm
unsatis_disc = unsatis_disc.to_crs(ni_utm)
towns_council = towns_council.to_crs(ni_utm)

#Set up figure and axes
fig = plt.figure(figsize=(8, 8))
ax = plt.axes(projection=ni_utm)

# Add LGD (all councils) using cartopy's ShapelyFeature
lgd_feature = ShapelyFeature(LGD['geometry'], ni_utm, edgecolor='k', facecolor='w')
ax.add_feature(lgd_feature) # add the features we've created to the map.

xmin, ymin, xmax, ymax = council.total_bounds
# using the boundary of the shapefile features, zoom the map to our area of interest
ax.set_extent([xmin-5000, xmax+5000, ymin-5000, ymax+5000], crs=ni_utm)  # because total_bounds
# gives output as xmin, ymin, xmax, ymax,
# but set_extent takes xmin, xmax, ymin, ymax, we re-order the coordinates here.

# pick colour for LGDs
lgd_colors = ['#0cd9d7']

# add LGDs to the Map
for ind, name in enumerate(LGD['LGDNAME'].unique()):
    feat = ShapelyFeature(LGD.loc[LGD['LGDNAME'] == name, 'geometry'], # first argument is the geometry
                          ccrs.CRS(LGD.crs), # second argument is the CRS
                          edgecolor='k', # outline the feature in black
                          facecolor=lgd_colors, # set the face colour to match lg_colors
                          linewidth=1, # set the outline width to be 1 pt
                          alpha=0.8) # set the alpha (transparency) to be 0.4 (out of 1)
    ax.add_feature(feat) # once we have created the feature, we have to add it to the map using ax.add_feature()

# Add unsatisfactory discharges
overflows_handle = ax.plot(unsatis_disc.geometry.x, unsatis_disc.geometry.y, 'o',
                           color='red', markersize=2.5, transform=ni_utm)

#add Town Names
for ind, row in towns_council.iterrows():
    ax.text(row.geometry.x, row.geometry.y, row['TOWN_NAME'].title(),
            fontsize=7, transform=ni_utm)

# Add Unsatisfactory Discharge count display to the map
    overflow_count = len(unsatis_disc)

    ax.text(xmin + 2000, ymax - 2000, f'Unsatisfactory Discharges: {overflow_count}',
            fontsize=12, color='black', backgroundcolor='white',
            bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'))

# add the scale bar to the axis
scale_bar(ax)

# Get filtered council name
lgd_name = council.iloc[0]['LGDNAME']

#Set up file name to be filtered council name _map.png, with _ in place of any spaces, e.g. Fermanagh_and_Omagh_mapp.png
filename = f"{lgd_name.replace(' ', '_')}_map.png"

# save the figure as map.png, fill print layout (bbox_inches='tight') and a dpi of 300
fig.savefig(filename, bbox_inches='tight', dpi=300)
