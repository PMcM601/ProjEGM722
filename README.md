# ProjEGM722
EGM722: Programming for GIS and Remote Sensing Project

Purpose of project

The aim of this study is to show some data analysis features that could be used based on available data from Department of Agriculture, Environment and Rural Affairs (DAERA), Northern Ireland Environment Agency (NIEA), Northern Ireland Water and Ordnance Survey Northern Ireland (OSNI). Datasets available from sources listed at the bottom of this file.

Output 1: Graph of NI Water Discharges by Type and Local Management Area (LMA).

This looks at the total number of Discharges (Treated, Monitored Overflows, Not-Monitored Overflows) by Local Management Area, using Shapefiles.
Two of the shapefiles were created by editing NI Water data in FME, the other was sourced from DAERA OpenData.

Output 2: A map tool to display Storm Overflow Discharges that are Unsatisfactory, by Local Government District (LGD).

Again this took in to account the Storm Overflows shapefile, and a LGD Shapefile. Town Names were displayed from a shapefile provided as part of the course - however this could be exchanged for OSNI Gazetteer Place Names.

Output 3: Interactive Map, showing Discharges and Water Body status.

This map is an interactive map which plots Treated, Non-Monitored and Monitored discharges imported from .csv files, on a map with NIEA Surface Water Bodies data. Similar to both the NI Water Storm Overflows Map and NIEA Catchment Data Map Viewer with the River, Marine and Lake Waterbody layers activated.

This was also provided as a Jupyter notebook, so that the end user could see the effect of different stages of the script, and perhaps replicate with newer or slightly different datasets.

Instructions for Setup and Use

Files in this repository will demonstrate dependencies of modules required. All analysis is written in python.

Data was sourced from:

LMAs - DAERA https://www.daera-ni.gov.uk/sites/default/files/publications/doe/localmanagementareashp.zip
LGDs - OpenDataNI: https://hub.arcgis.com/api/v3/datasets/eaa08860c50045deb8c4fdc7fa3dac87_2/downloads/data?format=shp&spatialRefId=29902&where=1%3D1
Modelled Spills May 2024 - NI Water: https://www.niwater.com/siteFiles/resources/xls/NIWaterModelledSpillsMay2024v2.xlsx
Wastewater Treatment Works Treated Discharges May 2024 - NI Water: https://www.niwater.com/siteFiles/resources/xls/NIWaterTreatedDischargesMay2024.xlsx
Event Duration Monitor Data - NI Water: https://www.niwater.com/siteFiles/resources/2025/EventDurationMonitorDataApril2025.xlsx
OSNI Gazetteer Place Names - OpenDataNI: https://hub.arcgis.com/api/v3/datasets/c116f31b481044769b75377946afa1c2_1/downloads/data?format=shp&spatialRefId=29902&where=1%3D1
