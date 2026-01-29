#########################################################################################################################
#  SAR_Landslide_Timing_COHERENCE.py  (c) A.A.J. DEIJNS, Royal Musuem for Central Africa, Belgium                       #
#                                                                                                                       #
#  DESCRIPTION: SCRIPT TO PROCESS THE COHERENCE IMAGERY AND CREATE TIME SERIES PER POLYGON. ASCENDING AND DESCENDING    #
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
import warnings
import pandas as pd
from osgeo import gdal
from shapely import speedups
speedups.disable()
from rasterstats import zonal_stats
import rasterio.plot
from multiprocessing import Pool
warnings.filterwarnings('ignore')

gdal.PushErrorHandler('CPLQuietErrorHandler')
gdal.UseExceptions()

print('')
#=================== FUNCTIONS==========================#
def ENVI_raster_binary_to_2d_array(file_name):
    '''
    Converts a binary file of ENVI type to a numpy array.
    Lack of an ENVI .hdr file will cause this to crash.
    '''

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
        bands = inDs.RasterCount

        geotransform = inDs.GetGeoTransform()
        originX = geotransform[0]
        originY = geotransform[3]
        pixelWidth = geotransform[1]
        pixelHeight = geotransform[5]

        band = inDs.GetRasterBand(1)
        image_array = band.ReadAsArray(0, 0, cols, rows)
        image_array_name = file_name


        return image_array, pixelWidth, (geotransform, inDs)
def ENVI_raster_binary_from_2d_array(envidata, file_out, post, image_array):
    # util.check_output_dir(file_out)
    original_geotransform, inDs = envidata

    rows, cols = image_array.shape
    bands = 1

    # Creates a new raster data source
    outDs = driver.Create(file_out, cols, rows, bands, gdal.GDT_Float32)

    # Write metadata
    originX = original_geotransform[0]
    originY = original_geotransform[3]

    outDs.SetGeoTransform([originX, post, 0.0, originY, 0.0, -post])
    outDs.SetProjection(inDs.GetProjection())

    # Write raster datasets
    outBand = outDs.GetRasterBand(1)
    outBand.WriteArray(image_array)

    new_geotransform = outDs.GetGeoTransform()
    new_projection = outDs.GetProjection()

    return new_geotransform, new_projection, file_out
def sortit(stringname):
    if Sat_Direction == 'Descending':
        replacestring = producttype + '.VV-VV.UTM.15x15.bil_S1_' + DSC_trackname + '-'
    else:
        replacestring = producttype + '.VV-VV.UTM.15x15.bil_S1_' + ASC_trackname + '-'

    stringname = stringname.replace(replacestring,'')
    if int(stringname[8:16]) < int(stringname[17:25]):
        return stringname[8:16]
    else:
        return stringname[17:25]
#########################################################

COH = {}
COH_normalized = {}

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

    namelist = []                           #
    for i in range(0,df_geometries.shape[0]):       #
        namelist += ['poly_' + str(i+1)]    # create a list with names for the polygon dataframes

    polygonlist = {}
    polygonlist_normalized = {}

    for name in namelist:
        polygonlist[name] = pd.DataFrame()
        polygonlist_normalized[name] = pd.DataFrame()

    ########################################################################################################################
    ################################## ---  Process Data   --- #############################################################
    ########################################################################################################################
    binaryfilename = {}
    headerfilename = {}
    image_array = {}
    image_date = {}
    pixelwidth = {}
    envidata = {}


    if Sat_Direction == 'Ascending':
        os.chdir(total_path_Ascending)
    elif Sat_Direction == 'Descending':
        os.chdir(total_path_Descending)

    prodtypelist = [os.listdir()[i] for i in range(0,len(os.listdir())) if producttype in os.listdir()[i]] ## looks for the variable producttype in the list and gives a list containing only the string under that variable
    iterator = 0
    prodtypelist = sorted(prodtypelist, key = sortit)# sort list based on dateinfo
    for i in range(0, len(prodtypelist)):
        if '.hdr' not in prodtypelist[i]:
            binaryfilename[str(iterator)] = prodtypelist[i] # get binaryfilename in dictionary for every file within the folder
            iterator = iterator + 1
    iterator = 0
    for i in range(0, len(prodtypelist)):
        if '.hdr' in prodtypelist[i]:
            headerfilename[str(iterator)] = prodtypelist[i] # get binaryfilename in dictionary for every file within the folder
            iterator = iterator + 1

    for i in list(range(0,len(binaryfilename.keys()))):
        image_array[i], pixelwidth[i], envidata[i] =  ENVI_raster_binary_to_2d_array(binaryfilename[str(i)])
        print('Coherence: ' + Sat_Direction +'  ('+ str(i) +'/'+str(len(binaryfilename.keys())-1)+')' ,end="\r")
        affine = rasterio.transform.from_origin(envidata[i][0][0], envidata[i][0][3], envidata[i][0][1], (-1 * envidata[i][0][5])) # create affine for plotting & zonal stats
        header = headerfilename[str(i)]

        if Sat_Direction == 'Descending':
            replacestring = producttype + '.VV-VV.UTM.15x15.bil_S1_' + DSC_trackname + '-'
        else:
            replacestring = producttype + '.VV-VV.UTM.15x15.bil_S1_' + ASC_trackname + '-'
        header = header.replace(replacestring, '')
        if int(header[8:16]) < int(header[17:25]):
            image_date[i] =  header[8:16]
        else:
            image_date[i] =  header[17:25]

        zs = zonal_stats(df_geometries, image_array[i], stats= ['min','max', 'mean', 'count','sum'],affine=affine, all_touched=True)
        df_TS = pd.DataFrame(zs)
        df_TS['date'] = image_date[i]
        df_TS['area'] = df_geometries.area
        df_TS['datetime'] = pd.to_datetime(df_TS['date'])
        for name, j in zip(namelist, list(range(0, len(namelist)))):  #
            polygonlist[name] = pd.concat([polygonlist[name], pd.DataFrame.transpose(pd.DataFrame(df_TS.iloc[j]))])  # create a dictionary containing all the DataFrames

    for name in namelist:
        polygonlist[name] = polygonlist[name].set_index('datetime')
        polygonlist[name].drop(['date'],axis=1, inplace=True)

    total_mean = {}
    for name in polygonlist:
        total_mean[name] = polygonlist[name]['mean'].mean()

    for name in polygonlist:
        polygonlist[name] = polygonlist[name][polygonlist[name]['count'] != 0]
        polygonlist_normalized[name] = pd.DataFrame(polygonlist[name].apply(lambda x: x['mean'] - total_mean[name], axis =1))

    for name in polygonlist:
        polygonlist[name] = polygonlist[name]['mean']

    COH[Sat_Direction] = polygonlist
    COH_normalized[Sat_Direction] = polygonlist_normalized
    return COH[Sat_Direction] , COH_normalized[Sat_Direction] , namelist, df_geometries,df_read, binaryfilename

if __name__ == '__main__':
    pool = Pool()
    data = pool.map(process_images,Direction_list)


iter=0
binaryfilename = {}
for sat in Direction_list:
    COH[sat]= data[iter][0]
    COH_normalized[sat]=data[iter][1]
    namelist=data[iter][2]
    df_geometries=data[iter][3]
    df_read=data[iter][4]
    binaryfilename[sat] = data[iter][5]
    iter+=1

# print('Coherence: ' + 'Ascending' +'  ('+ str(len(binaryfilename['Ascending'].keys())-1) +'/'+str(len(binaryfilename['Ascending'].keys())-1)+')')
print('Coherence: ' + 'Descending' +'  ('+ str(len(binaryfilename['Descending'].keys())-1) +'/'+str(len(binaryfilename['Descending'].keys())-1)+')')
