import matplotlib.pyplot as plt
import sys
import os
import numpy as np
import pandas as pd
import rasterio.plot
import math
from osgeo import gdal
from shapely import speedups
speedups.disable()
gdal.PushErrorHandler('CPLQuietErrorHandler')
gdal.UseExceptions()

import warnings
warnings.filterwarnings('ignore')

##=================== FUNCTIONS==========================#
# noinspection PyPep8Naming
def ENVI_raster_binary_to_2d_array(file_name):

    #Converts a binary file of ENVI type to a numpy array.
    #Lack of an ENVI .hdr file will cause this to crash.

    driver = gdal.GetDriverByName('ENVI')
    driver.Register()

    inDs = gdal.Open(file_name, gdal.GA_ReadOnly)

    if inDs is None:
        print("Couldn't open this file: " + file_name)
        print('\nPerhaps you need an ENVI .hdr file?')
        sys.exit("Try again!")
    else:
        cols = inDs.RasterXSize
        rows = inDs.RasterYSize
        geotransform = inDs.GetGeoTransform()
        pixelWidth = geotransform[1]

        band = inDs.GetRasterBand(1)
        image_array_from_funct = band.ReadAsArray(0, 0, cols, rows)

        return image_array_from_funct, pixelWidth, (geotransform, inDs)
def sortit(stringname):
    if Sat_Direction == 'Ascending':
        return stringname[8:16]
    if Sat_Direction == 'Descending':
        return stringname[7:15]
#########################################################

namelist_sat = {}
for Sat_Direction in Direction_list:
    namelist_sat[Sat_Direction] = []
    if Masked == 'Yes':
        if Sat_Direction == 'Ascending':
            df_geometries = geometry_masked_ASC
            polygonname = 'geometry_masked_ASC'
        else:
            df_geometries = geometry_masked_DSC
            polygonname = 'geometry_masked_DSC'
        for i in range(0, (df_geometries.shape[0])):  #
            namelist_sat[Sat_Direction] += ['poly_' + str(i + 1)]  # create a list with names for the polygon dataframes
    else:
        for i in range(0, (df_geometries.shape[0])):  #
            namelist_sat[Sat_Direction] += ['poly_' + str(i + 1)]  # create a list with names for the polygon dataframes

IntensityCorrelation = {}
for Sat_Direction in Direction_list:
    IntensityCorrelation[Sat_Direction] = {}
    for whichpoly in namelist_sat[Sat_Direction]:
        IntensityCorrelation[Sat_Direction][whichpoly] = {}
for Sat_Direction in Direction_list:
    ########################################################################################################################
    ################################## ---  Process Data   --- #############################################################
    ########################################################################################################################
    """"Here, the rasterdata is imported, the GH geometries are projected onto the raster & zonal statistics are derived
        additionally plots are made for every image overlain by the geomtries to see if projection is correct"""
    ## create empty dictionaries to fill in the loop ##
    if Masked == 'Yes':
        if Sat_Direction == 'Ascending':
            df_geometries = geometry_masked_ASC
            if Full_or_Single =='Full':
                polygonname = 'Full Event mask _ ASC'
            if Full_or_Single == 'Single':
                polygonname = 'Single Occurrence mask _ ASC'
        else:
            df_geometries = geometry_masked_DSC
            if Full_or_Single == 'Full':
                polygonname = 'Full Event mask _ DSC'
            if Full_or_Single == 'Single':
                polygonname = 'Single Occurrence mask _ DSC'
        print('')
        print(Sat_Direction + ' polygons used:' + polygonname + ' number of polygons: ' + str(len(df_geometries)))

    namelist = namelist_sat[Sat_Direction]
    binaryfilename = {}
    headerfilename = {}
    image_array = {}
    image_date = {}
    pixelwidth = {}
    envidata = {}

    ## ---- locate rasterfile .bil & .hdr ---- ##
    if Sat_Direction == 'Ascending':
        rasterizedgeometry = ASC_rasterizedgeometry
        os.chdir(total_path_Ascending)
    elif Sat_Direction == 'Descending':
        rasterizedgeometry = DSC_rasterizedgeometry
        os.chdir(total_path_Descending)

    prodtypelist = [os.listdir()[i] for i in range(0, len(os.listdir())) if producttype in os.listdir()[i]]  # looks for the variable producttype in the list and gives a list containing only the string under that variable
    iterator = 0
    prodtypelist = sorted(prodtypelist, key=sortit)  # sort list based on dateinfo
    for i in range(0, len(prodtypelist)):
        if '.bil' in prodtypelist[i]:
            binaryfilename[str(iterator)] = prodtypelist[
                i]  # get binaryfilename in dictionary for every file within the folder
            iterator = iterator + 1
    iterator = 0
    for i in range(0, len(prodtypelist)):
        if '.hdr' in prodtypelist[i]:
            headerfilename[str(iterator)] = prodtypelist[
                i]  # get binaryfilename in dictionary for every file within the folder
            iterator = iterator + 1
    ## import rasterized polygons
    rasterized_polygons, pixelwidth_raspol, envidata_raspol = ENVI_raster_binary_to_2d_array(rasterizedgeometry)
    affine_raspol = rasterio.transform.from_origin(envidata_raspol[0][0], envidata_raspol[0][3], envidata_raspol[0][1],
                                                   (envidata_raspol[0][5]))  # create affine for plotting & zonal stats

    image_array_clip = {}
    ########################################################################################################################
    ################################## ---  For-loop over all raster images  --- ###########################################
    ########################################################################################################################
    for i in list(range(0, len(binaryfilename.keys()))):
        image_array[i], pixelwidth[i], envidata[i] = ENVI_raster_binary_to_2d_array(binaryfilename[str(i)])
        if image_array[i].shape == rasterized_polygons.shape:
            affine = rasterio.transform.from_origin(envidata[i][0][0], envidata[i][0][3], envidata[i][0][1],(-1 * envidata[i][0][5]))  # create affine for plotting & zonal stats

            ## ---- Extract date from header file ---- ##
            header = open(headerfilename[str(i)], "r")
            date_from_header = [line for line in header if 'acquisition' in line]
            image_date[i] = (date_from_header[0][70:78])
    print()
    print('TOTAL NUMBER OF: \n   IMAGES: '+ str(len(image_date)) + ' \n   POLYGONS: ' + str(len(df_geometries)))
    print()

    list_geometries = list(df_geometries.id)
    iteration = 0
    for whichpoly in namelist:
        ## ---- create separate maps with values only for the ls polygons ---- ##
        # print()
        # print('1. Create individual maps with only GH pixels')
        print(Sat_Direction + ' poly: ('+str(iteration+1)+'/'+str(len(namelist))+')',end="\r")

        number_of_img = 0
        for date in image_date:
            image_array_clip[image_date[date]] = np.where(rasterized_polygons == list_geometries[iteration], image_array[date],np.nan)
            image_array_clip[image_date[date]] = image_array_clip[image_date[date]][~np.isnan(image_array_clip[image_date[date]])]
            number_of_img += 1

        IC_df = {}
        for img in number_avg_img:
            for perc in Reference_for_IC:
                df_dictname = str(img) + 'img__' + str(int(perc * 100)) + '%'
                IC_df[df_dictname] =  {}

        for img in number_avg_img:
            for perc in Reference_for_IC:
                A_avg = {}
                list_of_keys = list(image_array_clip.keys())
                iterator = 1
                for date in list_of_keys:
                    if date >= image_date[img - 1] <= list(image_date.values())[-img + 1]:
                        if (list_of_keys.index(date) + 1) % img == 0:
                            for i in list_of_keys[iterator - img:iterator]:
                                if i == list_of_keys[iterator - img:iterator][0]:
                                    A_avg[list_of_keys[iterator - img:iterator][-1] + "_" + list_of_keys[iterator - img:iterator][0]] = image_array_clip[i]
                                else:
                                    A_avg[list_of_keys[iterator - img:iterator][-1] + "_" + list_of_keys[iterator - img:iterator][0]] = A_avg[list_of_keys[iterator - img:iterator][-1] + "_" +list_of_keys[iterator - img:iterator][0]] + image_array_clip[i]
                            A_avg[list_of_keys[iterator - img:iterator][-1] + "_" + list_of_keys[iterator - img:iterator][0]] = A_avg[list_of_keys[iterator - img:iterator][-1] + "_" +list_of_keys[iterator - img:iterator][0]] / len(list_of_keys[iterator - img:iterator])
                    iterator += 1

                # create summap, avgmap, and normalize
                """"Here I normalize every individual pixel based on the average pixel value from all the available images. This influences the
                outcome, because every pixel is individually normalized changing the local correlation. Normalization seems to have a large positive effect 
                on the IC outcome. WHY??"""
                summap = {}
                avgmap = {}
                normalize = {}

                for date in A_avg:
                    if date == list(A_avg.keys())[0]:
                        summap = A_avg[date]
                    else:
                        summap = summap + A_avg[date]
                avgmap = summap / len(A_avg)
                for date in A_avg:
                    normalize[date] = A_avg[date] - avgmap

                # ---- I(average) for all maps ---- #
                IC = {}
                mean_m = {}
                mean_n = {}
                I_min_average_m = {}
                I_min_average_n = {}
                toppart = {}
                botpart = {}
                In_2 = {}
                Im_2 = {}
                mean_m = normalize[list(normalize.keys())[int(round(len(normalize) * perc))]].mean()
                for date in normalize:
                    if date != list(normalize.keys())[int(round(len(normalize) * perc))]:
                        mean_n[date] = normalize[date].mean()

                I_min_average_m = normalize[list(normalize.keys())[int(round(len(normalize) * perc))]] - mean_m
                Im_2 = I_min_average_m ** 2
                for date in normalize:
                    if date != list(normalize.keys())[int(round(len(normalize) * perc))]:
                        date_new = date[0:4] + '-' + date[4:6] + '-' + date[6:8]
                        I_min_average_n[date_new] = normalize[date] - mean_n[date]
                        In_2[date_new] = I_min_average_n[date_new] ** 2
                        toppart[date_new] = (I_min_average_n[date_new] * I_min_average_m).sum()
                        botpart[date_new] = (math.sqrt(In_2[date_new].sum() * Im_2.sum()))
                        IC[date_new] = toppart[date_new] / botpart[date_new]
                df_columnname =  str(img) + 'img__' + str(int(perc*100)) + '%'
                IC_df[df_columnname] = pd.DataFrame(pd.DataFrame(IC.values(), index=IC.keys())).rename(columns={0:df_columnname})
        ########################################################################################################################
        ## ---
        for run in IC_df:
            IC_df[run]['datetime'] = IC_df[run].index
            IC_df[run]['datetime'] = pd.to_datetime(IC_df[run]['datetime'])
            IC_df[run] = IC_df[run].set_index('datetime')

        # Dataframe with every polygon and moving means
        for run in IC_df:
            IC_df[run][run + '_moving mean_2'] = IC_df[run][run].dropna().rolling(2, min_periods=1,center=False).mean().reindex(IC_df[run].index)
            IC_df[run][run + '_moving mean_4'] = IC_df[run][run].dropna().rolling(4, min_periods=1,center=False).mean().reindex(IC_df[run].index)
            IC_df[run][run + '_moving mean_8'] = IC_df[run][run].dropna().rolling(8, min_periods=1,center=False).mean().reindex(IC_df[run].index)

        # CREATE A DF FOR EVERY POLYGON -- create a df that includes for every poly all the runs
        IntensityCorrelation[Sat_Direction][whichpoly] = IC_df
        iteration += 1

print('')
print('')
print('ECDF')
print('')

exec(open('/home/axel/PycharmProjects/PhD_Scripts/Scripts/SAR Landslide Timing/SAC_ECDF.py').read())
plt.close('all')

IC