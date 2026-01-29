# Deijns_et_al_2022_NHESS

This repository presents the code used to do the analysis in:

Deijns, A. A. J., Dewitte, O., Thiery, W., d'Oreye, N., Malet, J.-P., and Kervyn, F.: Timing landslide and flash flood events from SAR satellite: a regionally applicable methodology illustrated in African cloud-covered tropical environments, Nat. Hazards Earth Syst. Sci., 22, 3679–3700, https://doi.org/10.5194/nhess-22-3679-2022, 2022.


This is a copy of the scripts uploaded to ZENODO where you can also find the inventories. See the manuscript for that location. 

SAR_Landslide_Timing.py is the main script to identify the timing of the events. This script requires a Preprocessed SAR dataset using the AmsTer software and a landslide and flash flood event shapefile. All dependant scripts are identified within this script. The GEE_landsat8_trend.txt provides the Google Earth Engine Code to derive NDVI trends using Landsat 8 over a particular event area. 

