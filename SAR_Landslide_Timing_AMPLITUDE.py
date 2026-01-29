#########################################################################################################################
#  SAR_Landslide_Timing_AMPLITUDE.py  (c) A.A.J. DEIJNS, Royal Musuem for Central Africa, Belgium                       #
#                                                                                                                       #
#  DESCRIPTION: SCRIPT TO PROCESS THE AMPLITUDE IMAGERY AND CREATE TIME SERIES PER POLYGON. ASCENDING AND DESCENDING    #
#               ARE EXECTUED IN PARALLEL USING TWO CPU                                                                  #
#                                                                                                                       #
#           DEPENDANCIES:                                                                                               #
#               1. Dependant on the correct identification of the amplitude images location                             #
#                                                                                                                       #
#   OUTPUT:  DICTIONARY OF DATAFRAMES SEPERATED PER ORBIT (ASC, OR DSC)                                                                                                                      #
#                                                                                                                       #
#   VERSION 25-08-2021                                                                                                  #
#   -                                                                                                                   #
#########################################################################################################################



import sys
import os
import pandas as pd
from osgeo import gdal
from osgeo.gdalconst import *
from shapely import speedups
speedups.disable()
from rasterstats import zonal_stats
import rasterio.plot
import warnings
warnings.filterwarnings('ignore')
from multiprocessing import Pool


print('')
gdal.PushErrorHandler('CPLQuietErrorHandler')
gdal.UseExceptions()
#=================== FUNCTIONS==========================#
def ENVI_raster_binary_to_2d_array(file_name):
    '''
    Converts a binary file of ENVI type to a numpy array.
    Lack of an ENVI .hdr file will cause this to crash.
    '''
    driver = gdal.GetDriverByName('ENVI')
    driver.Register()

    inDs = gdal.Open(file_name, GA_ReadOnly)

    if inDs is None:
        print("Couldn't open this file: " + file_name)
        print('\nPerhaps you need an ENVI .hdr file?')
        sys.exit("Try again!")
    else:
        # print("%s opened successfully" % file_name)
        # print('~~~~~~~~~~~~~~')
        # print('Get image size')
        # print('~~~~~~~~~~~~~~')
        cols = inDs.RasterXSize
        rows = inDs.RasterYSize
        bands = inDs.RasterCount

        # print("columns: %i" % cols)
        # print("rows: %i" % rows)
        # print("bands: %i" % bands)

        # print('~~~~~~~~~~~~~~')
        # print('Get georeference information')
        # print('~~~~~~~~~~~~~~')
        geotransform = inDs.GetGeoTransform()
        originX = geotransform[0]
        originY = geotransform[3]
        pixelWidth = geotransform[1]
        pixelHeight = geotransform[5]

        # print("origin x: %i" % originX)
        # print("origin y: %i" % originY)
        # print("width: %2.2f" % pixelWidth)
        # print("height: %2.2f" % pixelHeight)

        # Set pixel offset.....
        # print('~~~~~~~~~~~~~~')
        # print('Convert image to 2D array')
        # print('~~~~~~~~~~~~~~')
        band = inDs.GetRasterBand(1)
        image_array = band.ReadAsArray(0, 0, cols, rows)
        image_array_name = file_name
        # print(type(image_array))
        # print(image_array.shape)

        return image_array, pixelWidth, (geotransform, inDs)
def sortit(stringname):
    if Sat_Direction == 'Ascending':
        return stringname[8:16]
    if Sat_Direction == 'Descending':
        return stringname[7:15]
#########################################################

AMP_normalized = {}
def process_images(satellitedir):
    global nametag
    global affine
    global Sat_Direction
    global image_date
    global i
    global df_geometries
    Sat_Direction = satellitedir
    if Masked == 'Yes':
        if Sat_Direction == 'Ascending':
            df_geometries = geometry_masked_ASC
            polygonname = 'geometry_masked_ASC'
        else:
            df_geometries = geometry_masked_DSC
            polygonname = 'geometry_masked_DSC'
        # print(Sat_Direction + ' polygons used:'+ polygonname + ' number of polygons: '+ str(len(df_geometries)))

    namelist = []  #
    for i in range(0, df_geometries.shape[0]):  #
        namelist += ['poly_' + str(i + 1)]  # create a list with names for the polygon dataframes


    polygonlist = {}
    polygonlist_normalized = {}

    for name in namelist:
        polygonlist[name] = pd.DataFrame()
        polygonlist_normalized[name] = pd.DataFrame()


    ########################################################################################################################
    ################################## ---  Process Data   --- #############################################################
    ########################################################################################################################
    """"Here, the rasterdata is imported, the GH geometries are projected onto the raster & zonal statistics are derived
        additionally plots are made for every image overlain by the geomtries to see if projection is correct"""
    ## create empty dictionaries to fill in the loop ##
    binaryfilename = {}
    headerfilename = {}
    image_array = {}
    image_date = {}
    image_date_check = {}
    pixelwidth = {}
    envidata = {}

    ## ---- locate rasterfile .bil & .hdr ---- ##
    if Sat_Direction == 'Ascending':
        os.chdir(total_path_Ascending)
    elif Sat_Direction == 'Descending':
        os.chdir(total_path_Descending)

    prodtypelist = [os.listdir()[i] for i in range(0,len(os.listdir())) if producttype in os.listdir()[i]] ## looks for the variable producttype in the list and gives a list containing only the string under that variable
    iterator = 0
    prodtypelist = sorted(prodtypelist, key = sortit)# sort list based on dateinfo
    for i in range(0, len(prodtypelist)):
        if '.bil' in prodtypelist[i]:
            binaryfilename[str(iterator)] = prodtypelist[i] # get binaryfilename in dictionary for every file within the folder
            iterator = iterator + 1
    iterator = 0
    for i in range(0, len(prodtypelist)):
        if '.hdr' in prodtypelist[i]:
            headerfilename[str(iterator)] = prodtypelist[i] # get binaryfilename in dictionary for every file within the folder
            iterator = iterator + 1

    ########################################################################################################################
    ################################## ---  For-loop over all raster images  --- ###########################################
    ########################################################################################################################
    for i in list(range(0,len(binaryfilename.keys()))):
        image_array[i], pixelwidth[i], envidata[i] =  ENVI_raster_binary_to_2d_array(binaryfilename[str(i)])
        print('Amplitude: ' + Sat_Direction +'  ('+ str(i) +'/'+str(len(binaryfilename.keys())-1)+')' ,end="\r")
        affine = rasterio.transform.from_origin(envidata[i][0][0], envidata[i][0][3], envidata[i][0][1], (-1 * envidata[i][0][5])) # create affine for plotting & zonal stats
        header = open(headerfilename[str(i)], "r")
        date_from_header = [line for line in header if 'acquisition' in line ]
        image_date[i] = (date_from_header[0][70:78])
        image_date_check[i] = (date_from_header[0][70:78])

        zs = zonal_stats(df_geometries, image_array[i], stats=['min', 'max', 'mean', 'count', 'sum', 'median', 'majority', 'minority', 'percentile_25', 'percentile_75', 'std'], affine=affine, all_touched=True)
        df_TS = pd.DataFrame(zs)
        df_TS['date'] = image_date[i]
        df_TS['area'] = df_geometries.area
        df_TS['datetime'] = pd.to_datetime(df_TS['date'])
        for name, j in zip(namelist, list(range(0, len(namelist)))):
            polygonlist[name] = pd.concat([polygonlist[name], pd.DataFrame.transpose(pd.DataFrame(df_TS.iloc[j]))])  # create a dictionary containing all the DataFrames

    for name in namelist:
        polygonlist[name] = polygonlist[name].set_index('datetime')
        polygonlist[name].drop(['date'], axis=1, inplace=True)

    total_mean = {}
    for name in polygonlist:
        total_mean[name] = polygonlist[name]['mean'].mean()
    for name in polygonlist:
        polygonlist[name] = polygonlist[name][polygonlist[name]['count'] != 0]
        polygonlist_normalized[name] = pd.DataFrame(polygonlist[name].apply(lambda x: x['mean'] - total_mean[name], axis =1))
    AMP_normalized[Sat_Direction] = polygonlist_normalized

    return AMP_normalized[Sat_Direction] , namelist, df_geometries,df_read,binaryfilename
    print(Sat_Direction)

if __name__ == '__main__':
    pool = Pool()
    data = pool.map(process_images, Direction_list)

iter = 0
binaryfilename = {}
for sat in Direction_list:
    AMP_normalized[sat] = data[iter][0]
    namelist = data[iter][1]
    df_geometries = data[iter][2]
    df_read = data[iter][3]
    binaryfilename[sat] = data[iter][4]
    iter += 1

# print('Amplitude: ' + 'Ascending' +'  ('+ str(len(binaryfilename['Ascending'].keys())-1) +'/'+str(len(binaryfilename['Ascending'].keys())-1)+')')
print('Amplitude: ' + 'Descending' +'  ('+ str(len(binaryfilename['Descending'].keys())-1) +'/'+str(len(binaryfilename['Descending'].keys())-1)+')')

