#########################################################################################################################
#  SAR_Landslide_Timing.py  (c) A.A.J. DEIJNS, Royal Musuem for Central Africa, Belgium                                                          #
#                                                                                                                       #
#  DESCRIPTION: SCRIPT TO ESTIMATE THE TIMING OF A LANDSLIDE AND/OR FLASH FLOOD EVENT USING SAR AMPLITUDE AND COHERENCE #
#  DATA.                                                                                                                #
#                                                                                                                       #
#           DEPENDANCIES:                                                                                               #
# #               1. SAR_landslide_Timing_AMPLITUDE.py                                                                  #
#                         A SCRIPT THAT PROCESSES THE AMPLITUDE IMAGES AND CREATES TIMESERIES PER POLYGON (1 IF ALL     #
#                         POLYGONS ARE DISSOLVED INTO ONE, AND MULTIPLE IF NOT) OUTPUT IN DATAFRAMES BOTH ORIGINAL AND  #
#                         NORMALIZED, SEPERATED BETWEEN ASCENDING AND DESCENDING                                        #
#                 2. SAR_Landslide_Timing_COHERENCE.py                                                                  #
#                         A SCRIPT THAT PROCESSES THE COHERENCE IMAGES AND CREATES TIMESERIES PER POLYGON (1 IF ALL     #
#                         POLYGONS ARE DISSOLVED INTO ONE, AND MULTIPLE IF NOT) OUTPUT IN DATAFRAMES BOTH ORIGINAL AND  #
#                         NORMALIZED, SEPERATED BETWEEN ASCENDING AND DESCENDING                                        #
#                 3. SAR_Landslide_Timing_SAC.py                                                                        #
#                         A SCRIPT THAT USES THE AMPLITUDE IMAGERY AND CALCULATES THE AMPLITUDE CORRELATION FOR EVERY   #
#                         IMAGE PAIR IN THE TIMESERIES, SEPERATED BETWEEN ASCENDING AND DESCENDING.                     #
#                 4. SAC_ECDF.py                                                                                        #
#                         A SCRIPT THAT FINDS THE MOST DEVIATING AMPLITUDE CORRELATION TIMESERIES BY COMPARING ALL ITS  #
#                         EMPIRICAL CUMULATIVE DISTRIBUTION FUNCTIONS WITH A NORMALLY DISTRIBUTED EMPIRICAL CUMULATIVE  #
#                         DISTRIBUTION CURVE BASED USING THE MEAN AND STD OF ALL THE TIME SERIES.                       #
#                 5. density distribution.py                                                                            #
#                         A SCRIPT THAT IS CALLED WHEN YOU PROCESS MULTIPLE POLYGONS WITHIN ONE EVENT, THAT DISPLAYS    #
#                         THE DISTRUBTION OF DATES ESTIMATED BY THE SCRIPT.                                             #
#                                                                                                                       #
#                 6. Rasterize shapefiles.py                                                                            #
#                           A SCRIPT THAT IS CALLED TO RASTERIZE THE SHAPEFILES ON AMPLITUDE                            #
#                           ASCENDING AND DESCENDING TRACK IMAGERY - FOR SAC CALCULATIONS                               #
#                                                                                                                       #
#                                                                                                                       #
#   INPUT RULES:                                                                                                        #
#   1. The input shapefile should at least consist of a column called 'id'                                              #
#   2. the amplitude and coherence image directory structure should follow the general output structure of the MasTer   #
#   Toolbox example: COHERENCE/S1/Rwenzori_A_174/RWENZORI/_ALL_COH_GEOC, where the trackname (here Rwenzori_A_174)      #
#   is manually defined under ASC_ or DSC_trackname. The trackname should be coherence throughout the whole             #
#   datastructure                                                                                                       #
#                                                                                                                       #
#   OUTPUT:                                                                                                             #
#       1. DERIVED TIMING FOR COHERENCE AND SAC INCLUDING THE NUMBER OF POLYGONS THAT ESTIMATED THE SAME DATE           #
#       2. WHEN MULTIPLE POLYGONS ARE PRESENT A GRAPH DISPLAYING THE DISTRIBUTION OF THE ESTIMATED DATES                #
#                                                                                                                       #
#                                                                                                                       #
#   VERSION 25-08-2021                                                                                                  #
#   - Only estimated timing using Spatial amplitude correlation and coherence available, amplitude is left out          #
#     due to                                                                                                            #
#########################################################################################################################
import sys

# Date_of_GH_Event = '2019-12-06'
Date_of_GH_Event = sys.argv[2]

Amplitude_data = 'Yes'
amplitudestartyear = '2016'
SAC_data = 'Yes'
Coherence_data = 'Yes'

Masked = 'Yes'
Full_or_Single = 'Single'

# Location = 'RWENZORI'#'BURUNDI' #'KUVAMBWE'#
Location = sys.argv[1]
# print(Location)

# ASC_trackname = 'UG_Rwenzori_A_174'#ASC_trackname = 'RW_KARONGI_A_174'#'Rwenzori_A_174'#'Burundi_A_174' #'DRC_UVIRA_A_174'#
# DSC_trackname = 'UG_Rwenzori_D_21'#'Kuvambwe_D_21' #'DRC_UVIRA_D_21'#'Burundi_D_21'  #'DRC_UVIRA_D_21'#
ASC_trackname = sys.argv[3]
DSC_trackname = sys.argv[4]



#Geocoded input paths
# AmplitudePath = '/media/axel/AxD31/AxD3_Processing/SAR_SM/AMPLITUDES'#'/media/axel/AxD31/AxD3_Processing/SAR_SM/AMPLITUDES' #'/media/axel/Data1/Sentinel-1/Maxime_AMPLITUDE' ## needs to be in the general structure output of the MasTer Toolbox
# CoherencePath = '/media/axel/AxD31/AxD3_Processing/SAR_SM/COHERENCE' #'/media/axel/AxD31/AxD3_Processing/SAR_SM/COHERENCE'  # needs to be in the general structure output of the MasTer Toolbox = coherencepath /S1/Location.uppercase()/trackname ...
#
AmplitudePath = sys.argv[5]
CoherencePath = sys.argv[6]

# shapefile_location = shape
# shapefile_GH = '/home/axel/Documents/Master_MainDisk/Master_Results/7.CaseStudies/Rwenzori/Input/Shapefiles/Rwenzori_LS_IMCLASS_multipart.shp'#'/home/axel/Documents/Master_MainDisk/Master_Results/7.CaseStudies/Burundi/Input/Shapefiles/Burundi_LS_IMCLASS_multipart.shp' #'/media/axel/Data1/Sentinel-1/shapefiles/NewTry.shp' #
shapefile_GH = sys.argv[7]
#
Processingpath = '/home/axel/Documents/Master_MainDisk/Master_Results/12.PROCESSING'

Detrend = 'No' # NOT POSSIBLE IF FULL_OR_SINGLE = SINGLE
# if Detrend is Yes provide additional .shp!!
# shapefile_detrend = '/home/axel/Documents/Master_MainDisk/Master_Results/7.CaseStudies/Rwenzori/Input/Shapefiles/detrend_square_Rwenzori.shp'#'/home/axel/Documents/Master_MainDisk/Master_Results/7.CaseStudies/Burundi/Input/Shapefiles/detrend_square_Burundi.shp'#'/media/axel/Data1/Sentinel-1/shapefiles/detrend_shape_apr2019.shp' # must contain 'detrend'  in the name
# shapefile_detrend = sys.argv[8]

Direction_list = ['Ascending','Descending']

sensitivityAnalysis = sys.argv[8]
# sensitivityAnalysis = 'No'


# Location='BURUNDI' 			#1. Location
# Date_of_GH_Event='2019-12-05' 	#2. Date of Actual GH event occurrence 

# ASC_trackname='Burundi_A_174'		#3. Trackname for the ascending track
# DSC_trackname='Burundi_D_21'		#4. Trackname for the descending track
 
# AmplitudePath='/media/axel/AxD31/AxD3_Processing/SAR_SM/AMPLITUDES'	#5. Full path to the location of the amplitude imagery
# CoherencePath='/media/axel/AxD31/AxD3_Processing/SAR_SM/COHERENCE'	#6. Full path to the location of the coherence imagery

# shapefile_GH='/home/axel/Documents/Master_MainDisk/Master_Results/7.CaseStudies/Burundi/Input/Shapefiles/Burundi_LS_IMCLASS_multipart.shp' #7. Shapefile of the GH event
# sensitivityAnalysis='Yes'

exportcsv='/home/axel/Documents/Master_MainDisk/Master_Results/14.Paperfigures/Figure7/Burundi_SensitivityAnalysis.csv'


########################################################################################################################################
# region #========================== Imports ===================================#
import sys
import geopandas as gpd
from matplotlib import pyplot as plt
import numpy as np
import ruptures as rpt
import time
import pandas as pd
import datetime
import os, subprocess, contextlib
from osgeo import gdal
start = time.time()
gdal.PushErrorHandler('CPLQuietErrorHandler')
gdal.UseExceptions()
# =====================================================================================================================#
# endregion
#%%region#========================== FUNCTIONS==================================#
def unbuffered(proc, stream='stdout'):
    newlines = ['\n', '\r\n', '\r']  # Unix, Windows and old Macintosh end-of-line

    stream = getattr(proc, stream)
    with contextlib.closing(stream):
        while True:
            out = []
            last = stream.read(1)
            # Don't loop forever
            if last == '' and proc.poll() is not None:
                break
            while last not in newlines:
                # Don't loop forever
                if last == '' and proc.poll() is not None:
                    break
                out.append(last)
                last = stream.read(1)
            out = ''.join(out)
            yield out
def SubProcess(command):
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            universal_newlines=True)
    for line in unbuffered(proc):
        print(line)
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
def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)
#%%endregion


print('########################################################################################################################################')
print('########################################################################################################################################')
print('####                                                LANDSLIDE TIMING ESTIMATION                                                     ####')
print('########################################################################################################################################')
print('########################################################################################################################################')

actualdate=pd.to_datetime(Date_of_GH_Event)
Detrended_DF = {}
Detrended_DF['Amplitude'] = {}
Detrended_DF['Coherence'] = {}

if Detrend == 'Yes' and Full_or_Single == 'Full':
    shapefiles = [shapefile_detrend,shapefile_GH]
else:
    shapefiles = [shapefile_GH]

for shapefile_location in shapefiles:
    if 'detrend' in shapefile_location:
        Masked = 'No'
    LocationInput = Location
    SACvariable_A = '2img'
    SACvariable_B = 'MAX_DIFF'

    geometry = shapefile_location
    df_read = gpd.read_file(geometry)
    df_geometries = df_read

    if sensitivityAnalysis == 'Yes':
        Givenvariable = int(sys.argv[9])
        steps = int(sys.argv[10])
        Param = sys.argv[11]
 
        # Givenvariable = 3000
        # steps = 1000
        # Param = 'Area'
        
        print(Masked)
        print("")
        print("Iterating over: "+Param)
        print("Current iteration: "+str(Givenvariable)+'-'+str(Givenvariable+steps))
        
        
        # Givenvariable = 2
        # steps = 1
        # Param = 'LandUse'

        if Param == 'Area':
            param = 'Area'
        if Param == 'Slope':
            param = 'Slopemean'
        if Param == 'LandUse':
            param = 'LandUsemaj'
        if Param == 'Aspect':
            param = 'Aspect'

        if param == 'LandUsemaj':
            df_read = gpd.read_file(geometry)  # add polygons to geoDataFrame
            df_read = df_read[df_read[param] == Givenvariable]
            df_geometries = df_read
            print('number of polygons: ' + str(len(df_geometries)))
            print("")
        else:
            df_read = gpd.read_file(geometry)  # add polygons to geoDataFrame
            df_read = df_read[df_read[param] > Givenvariable]
            df_read = df_read[df_read[param] < Givenvariable + steps]
            df_geometries = df_read
            print('number of polygons: ' + str(len(df_geometries)))
            print("")


    if Full_or_Single == 'Full':
        if Masked == 'Yes':
            if 'Descending' in Direction_list:
                geometry_masked_DSC = df_geometries[df_geometries['DSC_MASKma'] == 0]
                dsc_name = 'masked_full_Inventory_inprocess_dsc'
                masked_shapefileloc_dsc = Processingpath + '/' + Location + '__' + dsc_name + '.shp'
                geometry_masked_DSC.to_file(masked_shapefileloc_dsc)
                shapefilename_dsc = masked_shapefileloc_dsc[masked_shapefileloc_dsc.rfind('/') + 1:][:-4]
                gdalcommand_dsc = 'ogr2ogr ' + Processingpath + '/' + 'masked_full_Invenotry_Dissolved_dsc.shp' + ' "' + masked_shapefileloc_dsc + '"' + ' -nlt PROMOTE_TO_MULTI -dialect sqlite -sql ' + r'"SELECT ST_Union(geometry) AS geometry,* FROM \"' + shapefilename_dsc + r'\"" -f "ESRI Shapefile"'
                SubProcess(gdalcommand_dsc)
                dsc_name = 'masked_full_Invenotry_Dissolved_dsc.shp'
                geometry_masked_DSC_loc = Processingpath + '/' + dsc_name
                geometry_masked_DSC = gpd.read_file(geometry_masked_DSC_loc)
                print('Full event layover and shadow masked === number of all polygons DESCENDING: ' + str(len(geometry_masked_DSC)))

            if 'Ascending' in Direction_list:
                geometry_masked_ASC = df_geometries[df_geometries['ASC_MASKma'] == 0]
                asc_name = 'masked_full_Inventory_inprocess_asc'
                masked_shapefileloc_asc = Processingpath + '/' + Location + '__' + asc_name + '.shp'
                geometry_masked_ASC.to_file(masked_shapefileloc_asc)
                shapefilename_asc = masked_shapefileloc_asc[masked_shapefileloc_asc.rfind('/') + 1:][:-4]
                gdalcommand_asc = 'ogr2ogr ' + Processingpath + '/' + 'masked_full_Invenotry_Dissolved_asc.shp' + ' "' + masked_shapefileloc_asc + '"' + ' -nlt PROMOTE_TO_MULTI -dialect sqlite -sql ' + r'"SELECT ST_Union(geometry) AS geometry,* FROM \"' + shapefilename_asc + r'\"" -f "ESRI Shapefile"'
                SubProcess(gdalcommand_asc)
                asc_name = 'masked_full_Invenotry_Dissolved_asc.shp'
                geometry_masked_ASC_loc = Processingpath + '/' + asc_name
                geometry_masked_ASC = gpd.read_file(geometry_masked_ASC_loc)
                print('Full event layover and shadow masked === number of all polygons ASCENDING: ' + str(len(geometry_masked_ASC)))


        if Masked == 'No':
            namecommand = shapefile_location[shapefile_location.rfind('/') + 1:][:-4]
            gdalcommand = 'ogr2ogr ' + Processingpath + '/' + 'full_Invenotry_Dissolved.shp' + ' "' + shapefile_location + '"' + ' -nlt PROMOTE_TO_MULTI -dialect sqlite -sql ' + r'"SELECT ST_Union(geometry) AS geometry,* FROM \"' + namecommand + r'\"" -f "ESRI Shapefile"'
            SubProcess(gdalcommand)
            df_geometries = gpd.read_file(Processingpath + '/' + 'full_Invenotry_Dissolved.shp')
            print('number of all polygons: ' + str(len(df_geometries)))
    if Full_or_Single == 'Single':
        if Masked == 'Yes':
            if 'Ascending' in Direction_list:
                geometry_masked_ASC = df_geometries[df_geometries['ASC_MASKma'] == 0]
                print('Single occurrence layover and shadow masked === number of polygons ASC: ' + str(len(geometry_masked_ASC)))
                 # to shapefile
                asc_name = 'Single_layoverandshadow_masked_ASC.shp'
                geometry_masked_ASC_loc = Processingpath+'/'+ asc_name
                geometry_masked_ASC.to_file(geometry_masked_ASC_loc)

            if 'Descending' in Direction_list:
                geometry_masked_DSC = df_geometries[df_geometries['DSC_MASKma'] == 0]
                print('Single occurrence layover and shadow masked === number of polygons DSC: ' + str(len(geometry_masked_DSC)))
                dsc_name = 'Single_layoverandshadow_masked_DSC.shp'
                geometry_masked_DSC_loc = Processingpath+'/'+ dsc_name
                geometry_masked_DSC.to_file(geometry_masked_DSC_loc)


    print('')
    print('Process Amplitude data ? = '+Amplitude_data)
    print('Process Spatial Amplitude correlation data ?= '+SAC_data)
    print('Process Coherence data ?= '+Coherence_data)

    print('')
    print('')
    print('LOCATION: ' + LocationInput)
    print('')
    print('')


    slopelist = []
    timing_ASC = []
    timing_DSC = []
    percentage_ASC = []
    percentage_DSC = []
    percentage_within_month_ASC= []
    percentage_within_month_DSC= []
    percentage_seven_days_ASC = []
    percentage_seven_days_DSC = []

    timing_ASC_COH = []
    timing_DSC_COH = []
    percentage_ASC_COH = []
    percentage_DSC_COH = []
    percentage_within_month_ASC_COH = []
    percentage_within_month_DSC_COH = []
    percentage_seven_days_ASC_COH = []
    percentage_seven_days_DSC_COH = []

    timing_ASC_COH_nodet = []
    timing_DSC_COH_nodet = []
    percentage_ASC_COH_nodet = []
    percentage_DSC_COH_nodet = []
    percentage_within_month_ASC_COH_nodet = []
    percentage_within_month_DSC_COH_nodet = []
    percentage_seven_days_ASC_COH_nodet = []
    percentage_seven_days_DSC_COH_nodet = []


    timing_ASC_AMP = []
    timing_DSC_AMP = []
    percentage_ASC_AMP = []
    percentage_DSC_AMP = []
    percentage_within_month_ASC_AMP = []
    percentage_within_month_DSC_AMP = []
    percentage_seven_days_ASC_AMP = []
    percentage_seven_days_DSC_AMP = []

    timing_ASC_AMP_nodet = []
    timing_DSC_AMP_nodet = []
    percentage_ASC_AMP_nodet = []
    percentage_DSC_AMP_nodet = []
    percentage_within_month_ASC_AMP_nodet = []
    percentage_within_month_DSC_AMP_nodet = []
    percentage_seven_days_ASC_AMP_nodet = []
    percentage_seven_days_DSC_AMP_nodet = []



    geometrylenlist = []

    timing_ASC_SAC = []
    timing_DSC_SAC = []
    percentage_ASC_SAC = []
    percentage_DSC_SAC = []
    percentage_within_month_ASC_SAC= []
    percentage_within_month_DSC_SAC= []
    percentage_seven_days_ASC_SAC = []
    percentage_seven_days_DSC_SAC = []

    number_avg_img = [1, 2, 3]
    Reference_for_IC = list(np.arange(0, 0.98, 0.01)) # in fraction out of 1
    moving_mean_ECDF = '' #or for example {'_moving mean_4'} underscore before the name is necessary ## The data can be smoothed in order to find better SAC

    if Amplitude_data == 'Yes' or SAC_data == 'Yes':
        # Define Input locations
        if 'Ascending' in Direction_list:
            os.chdir(AmplitudePath+'/S1/'+ ASC_trackname +'/')
            AMP_total_path_Ascending = os.getcwd() + '/'+ os.listdir()[0] + '/_GEOCAMPLI'
        if 'Descending' in Direction_list:
            os.chdir(AmplitudePath+'/S1/'+ DSC_trackname +'/')
            AMP_total_path_Descending = os.getcwd() + '/'+ os.listdir()[0] + '/_GEOCAMPLI'

    if Coherence_data == 'Yes':
        if 'Ascending' in Direction_list:
            os.chdir(CoherencePath+'/S1/'+ ASC_trackname +'/')
            COH_total_path_Ascending = os.getcwd() + '/'+ os.listdir()[0] + '/_ALL_COH_GEOC'
        if 'Descending' in Direction_list:
            os.chdir(CoherencePath+'/S1/'+ DSC_trackname +'/')
            COH_total_path_Descending = os.getcwd() + '/'+ os.listdir()[0] + '/_ALL_COH_GEOC'

    #region #========================== Amplitude, SAC and Coherence Script Excecution ===================================#
    ## EXECUTE TIMESERIES SCRIPTS
    # EXECUTE AMPLITUDE
    if Amplitude_data == 'Yes':
        print('\n ================================================= AMPLITUDE ===================================================================== \n')
        if 'Ascending' in Direction_list:
            total_path_Ascending = AMP_total_path_Ascending
        if 'Descending' in Direction_list:
            total_path_Descending = AMP_total_path_Descending
        producttype = 'sigma0.UTM'
        exec(open('/home/axel/PycharmProjects/PhD_Scripts/Scripts/SAR Landslide Timing/SAR_Landslide_Timing_AMPLITUDE.py').read())
        print('')

    # EXECUTE COHERENCE
    if Coherence_data == 'Yes':
        print('\n ================================================== COHERENCE ================================================================== \n')
        if 'Ascending' in Direction_list:
            total_path_Ascending = COH_total_path_Ascending
        if 'Descending' in Direction_list:
            total_path_Descending = COH_total_path_Descending
        producttype = 'coherence'
        exec(open('/home/axel/PycharmProjects/PhD_Scripts/Scripts/SAR Landslide Timing/SAR_Landslide_Timing_COHERENCE.py').read())
        print('')
        print('\n ============================================================================================================================== \n')
    #endregion

    if Detrend == 'Yes':
        if 'detrend' in shapefile_location:
            shapename = 'Detrend'
        else:
            shapename = 'GH'
        if Coherence_data == 'Yes':
            Detrended_DF['Coherence'][shapename] = {}
            Detrended_DF['Coherence'][shapename]= COH_normalized
        if Amplitude_data == 'Yes':
            Detrended_DF['Amplitude'][shapename] = {}
            Detrended_DF['Amplitude'][shapename] = AMP_normalized


if Detrend == 'Yes' and Full_or_Single == 'Full':
    if Coherence_data == 'Yes':
        COH = {}
        if 'Ascending' in Direction_list:
            COH['Ascending'] = {}
            COH['Ascending']['poly_1'] = Detrended_DF['Coherence']['GH']['Ascending']['poly_1'] - Detrended_DF['Coherence']['Detrend']['Ascending']['poly_1']
        if 'Descending' in Direction_list:
            COH['Descending'] = {}
            COH['Descending']['poly_1'] = Detrended_DF['Coherence']['GH']['Descending']['poly_1'] - Detrended_DF['Coherence']['Detrend']['Descending']['poly_1']

    if Amplitude_data == 'Yes':
        AMP_normalized = {}
        if 'Ascending' in Direction_list:
            AMP_normalized['Ascending'] = {}
            AMP_normalized['Ascending']['poly_1'] = Detrended_DF['Amplitude']['GH']['Ascending']['poly_1'] - Detrended_DF['Amplitude']['Detrend']['Ascending']['poly_1']
        if 'Descending' in Direction_list:
            AMP_normalized['Descending'] = {}
            AMP_normalized['Descending']['poly_1'] = Detrended_DF['Amplitude']['GH']['Descending']['poly_1'] - Detrended_DF['Amplitude']['Detrend']['Descending']['poly_1']


# EXECUTE SPATIAL AMPLITUDE CORRELATION
if SAC_data == 'Yes':
    print('\n =====================================================AMPLITUDE SPATIAL CORRELATION=============================================== \n')
    if 'Ascending' in Direction_list:
        total_path_Ascending = AMP_total_path_Ascending
    if 'Descending' in Direction_list:
        total_path_Descending = AMP_total_path_Descending
    producttype = 'sigma0.UTM'
    exec(open('/home/axel/PycharmProjects/PhD_Scripts/Scripts/SAR Landslide Timing/Rasterize shapefiles.py').read())
    exec(open('/home/axel/PycharmProjects/PhD_Scripts/Scripts/SAR Landslide Timing/SAR_Landslide_Timing_SAC.py').read())
    print('')

##region Create the namelist of all the processed polygons
namelist = {}
if Masked == 'Yes':
    for Sat_Direction in Direction_list:
        namelist[Sat_Direction] = []
        if Sat_Direction == 'Ascending':
            df_geometries = geometry_masked_ASC
            polygonname = 'geometry_masked_ASC'
        else:
            df_geometries = geometry_masked_DSC
            polygonname = 'geometry_masked_DSC'
        for i in range(0, (df_geometries.shape[0])):  #
            namelist[Sat_Direction] += ['poly_' + str(i + 1)]  # create a list with names for the polygon dataframes
else:
    for Sat_Direction in Direction_list:
        namelist[Sat_Direction] = []
        for i in range(0, (df_geometries.shape[0])):  #
            namelist[Sat_Direction] += ['poly_' + str(i + 1)]  # create a list with names for the polygon dataframes
#endregion
###region process AMPLITUDE and COHERENCE data into useable PANDAS DATAFRAMES

# Amplitude
if Amplitude_data == 'Yes':
    Amplist_ASC = [];
    Amplist_DSC = [];
    for Sat in Direction_list:
        for poly in AMP_normalized[Sat]:
            # print(poly)
            if Sat == 'Ascending':
                Amplist_ASC.append(AMP_normalized[Sat][poly])
            else:
                Amplist_DSC.append(AMP_normalized[Sat][poly])

    if 'Ascending' in Direction_list:
        Concat_ASC= pd.concat(Amplist_ASC,axis=1) # concatenate muliple polygons into one dataframe
        Concat_ASC_rol = Concat_ASC.rolling(4, min_periods=1).mean(); # Apply moving mean on top of raw amplitude data
        # rename columns
        Concat_ASC.columns = namelist['Ascending']
        Concat_ASC_rol.columns = namelist['Ascending']
        Concat_ASC['mean'] = Concat_ASC.mean(axis=1) # create a mean value of all polygons raw amplitude
        Concat_ASC_rol['mean'] = Concat_ASC_rol.mean(axis=1)  # create a mean value of all polygons movmean amplitude

    if 'Descending' in Direction_list:
        Concat_DSC= pd.concat(Amplist_DSC,axis=1) # concatenate muliple polygons into one dataframe
        Concat_DSC_rol = Concat_DSC.rolling(4, min_periods=1).mean(); # Apply moving mean on top of raw amplitude data
        Concat_DSC.columns = namelist['Descending']
        Concat_DSC_rol.columns = namelist['Descending']
        Concat_DSC['mean'] = Concat_DSC.mean(axis=1) # create a mean value of all polygons raw amplitude
        Concat_DSC_rol['mean'] = Concat_DSC_rol.mean(axis=1) # create a mean value of all polygons  movmean amplitude
# Coherence
if Coherence_data == 'Yes':
    if 'Ascending' in Direction_list:
        Coherence_ASC = [];
        Coherence_ASC_norm = [];
    if 'Descending' in Direction_list:
        Coherence_DSC = [];
        Coherence_DSC_norm = [];
    for Sat in Direction_list:
        for poly in namelist[Sat]:
            # print(poly)
            if Sat == 'Ascending':
                Coherence_ASC.append(COH[Sat][poly])
            else:
                Coherence_DSC.append(COH[Sat][poly])

    for Sat in Direction_list:
        for poly in namelist[Sat]:
            # print(poly)
            if Sat == 'Ascending':
                Coherence_ASC_norm.append(COH_normalized[Sat][poly])
            else:
                Coherence_DSC_norm.append(COH_normalized[Sat][poly])

    if 'Ascending' in Direction_list:
        COH_Concat_ASC = pd.concat(Coherence_ASC, axis=1)
        COH_Concat_ASC_norm = pd.concat(Coherence_ASC_norm, axis=1)
        # COH_Concat_ASC_rol = COH_Concat_ASC.rolling(4, min_periods=1).mean();
        # COH_Concat_ASC_norm_rol = COH_Concat_ASC_norm.rolling(4, min_periods=1).mean();
        COH_Concat_ASC.columns = namelist['Ascending']
        COH_Concat_ASC_norm.columns = namelist['Ascending']
        # COH_Concat_ASC_rol.columns = namelist['Ascending']
        # COH_Concat_ASC_norm_rol.columns = namelist['Ascending']
        COH_Concat_ASC['mean'] = COH_Concat_ASC.mean(axis=1)
        COH_Concat_ASC_norm['mean'] = COH_Concat_ASC_norm.mean(axis=1)
        # COH_Concat_ASC_rol['mean'] = COH_Concat_ASC_rol.mean(axis=1)
        # COH_Concat_ASC_norm_rol['mean'] = COH_Concat_ASC_norm_rol.mean(axis=1)

    if 'Descending' in Direction_list:
        COH_Concat_DSC = pd.concat(Coherence_DSC, axis=1)
        COH_Concat_DSC_norm = pd.concat(Coherence_DSC_norm, axis=1)
        # COH_Concat_DSC_rol = COH_Concat_DSC.rolling(4, min_periods=1).mean();
        # COH_Concat_DSC_norm_rol = COH_Concat_DSC_norm.rolling(4, min_periods=1).mean();
        COH_Concat_DSC.columns = namelist['Descending']
        COH_Concat_DSC_norm.columns = namelist['Descending']
        # COH_Concat_DSC_rol.columns  = namelist['Descending']
        # COH_Concat_DSC_norm_rol.columns  = namelist['Descending']
        COH_Concat_DSC['mean'] = COH_Concat_DSC.mean(axis=1)
        COH_Concat_DSC_norm['mean'] = COH_Concat_DSC_norm.mean(axis=1)
        # COH_Concat_DSC_rol['mean'] = COH_Concat_DSC_rol.mean(axis=1)
        # COH_Concat_DSC_norm_rol['mean'] = COH_Concat_DSC_norm_rol.mean(axis=1)
#endregion

if Amplitude_data == 'Yes':
    print('AMPLITUDE')
    if Detrend == 'Yes':
        # region KDE regular
        Differencedict = {}
        Timelist = {}
        if 'Ascending' in Direction_list and 'Descending' in Direction_list:
            SATLIST = ['Ascending', 'Descending']
        if 'Ascending' in Direction_list and not 'Descending' in Direction_list:
            SATLIST = ['Ascending']
        if 'Descending' in Direction_list and not 'Ascending' in Direction_list:
            SATLIST = ['Descending']

        xmaxlist = []
        percentagelist = []
        percentagelist_seven_days = []
        percentagelist_within_month = []
        dirlist = []
        figiter = 0
        Diff_Timing = {}
        for sat in SATLIST:
            Diff_Timing[sat] = {}

        count = 0
        for sat in SATLIST:
            Timelist = {}
            if sat == 'Ascending':
                A = Detrended_DF['Amplitude']['GH']['Ascending']
            else:
                A = Detrended_DF['Amplitude']['GH']['Descending']
            if bool(A) != False:
                if sat == 'Ascending':
                    satdir = 'Ascending'
                    dirlist.append(satdir)
                else:
                    satdir = 'Descending'
                    dirlist.append(satdir)
                for i in A:
                    if A[i].isnull().values.any() == False:
                        A[i] = A[i][amplitudestartyear:]
                        points = np.array(A[i])
                        Timelist[i] = []
                        diflist = []
                        timlist = []
                        Differencedict[i] = {}

                        model = "l2"
                        algo = rpt.Binseg(model=model).fit(points)
                        my_bkps = algo.predict(n_bkps=1)
                        # print('binary segmentation based timing')
                        Timelist[i].append(A[i][A[i] == A[i].iloc[my_bkps[0] - 1]].dropna().index[0])

                Diff_Timing[sat] = pd.DataFrame(Timelist)
                Diff_Timing[sat] = Diff_Timing[sat].transpose()
                Diff_Timing[sat] = Diff_Timing[sat].dropna()
                Diff_Timing[sat]['ordinal'] = [x.toordinal() for x in Diff_Timing[sat][0]]

                if len(Diff_Timing[sat]) == int(Diff_Timing[sat]['ordinal'].value_counts().max()):
                    if count == 1:
                        dirlist = []
                        dirlist.append('Descending')
                    ABC = Diff_Timing[sat][0].value_counts()
                    xmax = Diff_Timing[sat]['ordinal'].value_counts()[
                        Diff_Timing[sat]['ordinal'].value_counts() == Diff_Timing[sat][
                            'ordinal'].value_counts().max()].index[0]
                    xmaxlabel = str(Diff_Timing[sat][0].value_counts()[
                                        Diff_Timing[sat][0].value_counts() == Diff_Timing[sat][
                                            0].value_counts().max()].index[0])[
                                0:10]  # [datetime.datetime.fromordinal(int(x)).strftime('%Y-%m-%d') for x in xmax][0]
                    xmaxlist.append(xmaxlabel)

                    number_of_Correct_predict = len(Diff_Timing[sat][0][Diff_Timing[sat][0] == xmaxlabel])
                    total_amount_of_predict = len(namelist[sat])
                    percentage = (number_of_Correct_predict / total_amount_of_predict) * 100
                    percentagelist.append(percentage)

                    if 'actualdate' in locals():
                        number_of_predict_within_seven_days_of_actual = len(
                            Diff_Timing[sat][0][abs(Diff_Timing[sat][0] - actualdate).dt.days <= 7])
                        number_of_predict_within_one_month_of_actual = len(
                            Diff_Timing[sat][0][abs(Diff_Timing[sat][0] - actualdate).dt.days <= 31])
                        percentage_seven_days = (
                                                            number_of_predict_within_seven_days_of_actual / total_amount_of_predict) * 100
                        percentage_within_month = (
                                                              number_of_predict_within_one_month_of_actual / total_amount_of_predict) * 100
                        percentagelist_seven_days.append(percentage_seven_days)

                    count += 1
                else:
                    ABC = Diff_Timing[sat][0].value_counts()
                    xmax = Diff_Timing[sat]['ordinal'].value_counts()[
                        Diff_Timing[sat]['ordinal'].value_counts() == Diff_Timing[sat][
                            'ordinal'].value_counts().max()].index[0]
                    xmaxlabel = str(Diff_Timing[sat][0].value_counts()[
                                        Diff_Timing[sat][0].value_counts() == Diff_Timing[sat][
                                            0].value_counts().max()].index[0])[
                                0:10]  # [datetime.datetime.fromordinal(int(x)).strftime('%Y-%m-%d') for x in xmax][0]
                    xmaxlist.append(xmaxlabel)

                    # print(Diff_Timing[sat][0])
                    number_of_Correct_predict = len(Diff_Timing[sat][0][Diff_Timing[sat][0] == xmaxlabel])

                    total_amount_of_predict = len(namelist[sat])
                    percentage = (number_of_Correct_predict / total_amount_of_predict) * 100
                    percentagelist.append(percentage)

                    if 'actualdate' in locals():
                        number_of_predict_within_seven_days_of_actual = len(
                            Diff_Timing[sat][0][abs(Diff_Timing[sat][0] - actualdate).dt.days <= 7])
                        number_of_predict_within_one_month_of_actual = len(
                            Diff_Timing[sat][0][abs(Diff_Timing[sat][0] - actualdate).dt.days <= 31])
                        percentage_seven_days = (
                                                            number_of_predict_within_seven_days_of_actual / total_amount_of_predict) * 100
                        percentage_within_month = (
                                                              number_of_predict_within_one_month_of_actual / total_amount_of_predict) * 100
                        percentagelist_seven_days.append(percentage_seven_days)
                        percentagelist_within_month.append(percentage_within_month)

        if bool(A) != False:
            if len(Direction_list) > 0:
                xmaxlist_dict = {'Sat': Direction_list, 'Date_of_Occurence': xmaxlist}
                xmaxdf = pd.DataFrame(xmaxlist_dict)
                xmaxdf.index = xmaxdf['Sat']
                xmaxdf = xmaxdf.drop(columns='Sat')

                if 'Ascending' in Direction_list:
                    timing_ASC_AMP_nodet.append(xmaxdf['Date_of_Occurence']['Ascending'])
                    percentage_ASC_AMP_nodet.append(percentagelist[0])
                if 'Descending' in Direction_list:
                    timing_DSC_AMP_nodet.append(xmaxdf['Date_of_Occurence']['Descending'])
                    if 'Descending' in Direction_list and 'Ascending' not in Direction_list:
                        percentage_DSC_AMP_nodet.append(percentagelist[0])
                    else:
                        percentage_DSC_AMP_nodet.append(percentagelist[1])

                if 'actualdate' in locals():
                    if 'Ascending' in Direction_list:
                        percentage_seven_days_ASC_AMP_nodet.append(percentagelist_seven_days[0])
                        percentage_within_month_ASC_AMP_nodet.append(percentagelist_within_month[0])

                    if 'Descending' in Direction_list:
                        percentage_seven_days_DSC_AMP_nodet.append(percentagelist_seven_days[1])
                        percentage_within_month_DSC_AMP_nodet.append(percentagelist_within_month[1])

        plt.close('all')
    plt.close('all')
    #region KDE regular
    Differencedict = {}
    Timelist = {}
    if 'Ascending' in Direction_list and 'Descending' in Direction_list:
        SATLIST = ['Ascending', 'Descending']
    if 'Ascending' in Direction_list and not 'Descending' in Direction_list:
        SATLIST = ['Ascending']
    if 'Descending' in Direction_list and not 'Ascending' in Direction_list:
        SATLIST = ['Descending']

    xmaxlist = []
    percentagelist=[]
    percentagelist_seven_days = []
    percentagelist_within_month = []
    dirlist=[]
    figiter = 0
    Diff_Timing = {}
    for sat in SATLIST:
        Diff_Timing[sat] = {}

    count=0
    for sat in SATLIST:
        Timelist = {}
        if sat == 'Ascending':
            A = AMP_normalized['Ascending']
        else:
            A = AMP_normalized['Descending']
        if bool(A) != False:
            if sat == 'Ascending':
                satdir = 'Ascending'
                dirlist.append(satdir)
            else:
                satdir = 'Descending'
                dirlist.append(satdir)
            for i in A:
                if A[i].isnull().values.any() == False:
                    A[i] = A[i][amplitudestartyear:]
                    points = np.array(A[i])
                    Timelist[i] = []
                    diflist = []
                    timlist = []
                    Differencedict[i] = {}

                    model = "l2"
                    algo = rpt.Binseg(model=model).fit(points)
                    my_bkps = algo.predict(n_bkps=1)
                    # print('binary segmentation based timing')
                    Timelist[i].append(A[i][A[i] == A[i].iloc[my_bkps[0] - 1]].dropna().index[0])

            Diff_Timing[sat] = pd.DataFrame(Timelist)
            Diff_Timing[sat] = Diff_Timing[sat].transpose()
            Diff_Timing[sat] = Diff_Timing[sat].dropna()
            Diff_Timing[sat]['ordinal'] = [x.toordinal() for x in Diff_Timing[sat][0]]

            if len(Diff_Timing[sat]) == int(Diff_Timing[sat]['ordinal'].value_counts().max()):
                if count == 1:
                    dirlist = []
                    dirlist.append('Descending')
                ABC = Diff_Timing[sat][0].value_counts()
                xmax = Diff_Timing[sat]['ordinal'].value_counts()[
                    Diff_Timing[sat]['ordinal'].value_counts() == Diff_Timing[sat][
                        'ordinal'].value_counts().max()].index[0]
                xmaxlabel = str(Diff_Timing[sat][0].value_counts()[
                                    Diff_Timing[sat][0].value_counts() == Diff_Timing[sat][
                                        0].value_counts().max()].index[0])[
                            0:10]  # [datetime.datetime.fromordinal(int(x)).strftime('%Y-%m-%d') for x in xmax][0]
                xmaxlist.append(xmaxlabel)

                number_of_Correct_predict = len(Diff_Timing[sat][0][Diff_Timing[sat][0] == xmaxlabel])
                total_amount_of_predict = len(namelist[sat])
                percentage = (number_of_Correct_predict / total_amount_of_predict) * 100
                percentagelist.append(percentage)

                if 'actualdate' in locals():
                    number_of_predict_within_seven_days_of_actual = len(Diff_Timing[sat][0][abs(Diff_Timing[sat][0]-actualdate).dt.days <= 7])
                    number_of_predict_within_one_month_of_actual = len(Diff_Timing[sat][0][abs(Diff_Timing[sat][0]-actualdate).dt.days <= 31])
                    # print(Diff_Timing[sat][0][abs(Diff_Timing[sat][0]-actualdate).dt.days <= 31])
                    percentage_seven_days = (number_of_predict_within_seven_days_of_actual / total_amount_of_predict) * 100
                    percentage_within_month = (number_of_predict_within_one_month_of_actual / total_amount_of_predict) * 100
                    percentagelist_seven_days.append(percentage_seven_days)
                    percentagelist_within_month.append(percentage_within_month)
                    print('')
                    print('track: '+sat)
                    print('within one month number: '+str(number_of_predict_within_one_month_of_actual))
                    print('total number: '+str(total_amount_of_predict))
                    print('')
                count += 1
            else:
                ABC=Diff_Timing[sat][0].value_counts()
                xmax = Diff_Timing[sat]['ordinal'].value_counts()[Diff_Timing[sat]['ordinal'].value_counts() == Diff_Timing[sat]['ordinal'].value_counts().max()].index[0]
                xmaxlabel = str(Diff_Timing[sat][0].value_counts()[Diff_Timing[sat][0].value_counts() == Diff_Timing[sat][0].value_counts().max()].index[0])[ 0:10]  # [datetime.datetime.fromordinal(int(x)).strftime('%Y-%m-%d') for x in xmax][0]
                xmaxlist.append(xmaxlabel)

                # print(Diff_Timing[sat][0])
                number_of_Correct_predict = len(Diff_Timing[sat][0][Diff_Timing[sat][0] == xmaxlabel])

                total_amount_of_predict = len(namelist[sat])
                percentage = (number_of_Correct_predict / total_amount_of_predict) * 100
                percentagelist.append(percentage)

                if 'actualdate' in locals():
                    number_of_predict_within_seven_days_of_actual = len(Diff_Timing[sat][0][abs(Diff_Timing[sat][0] - actualdate).dt.days <= 7])
                    number_of_predict_within_one_month_of_actual = len(Diff_Timing[sat][0][abs(Diff_Timing[sat][0] - actualdate).dt.days <= 31])
                    # print(Diff_Timing[sat][0][abs(Diff_Timing[sat][0]-actualdate).dt.days <= 31])
                    percentage_seven_days = (number_of_predict_within_seven_days_of_actual / total_amount_of_predict) * 100
                    percentage_within_month = (number_of_predict_within_one_month_of_actual / total_amount_of_predict) * 100
                    percentagelist_seven_days.append(percentage_seven_days)
                    percentagelist_within_month.append(percentage_within_month)
                    print('')
                    print('track: '+sat)
                    print('within one month number: '+str(number_of_predict_within_one_month_of_actual))
                    print('total number: '+str(total_amount_of_predict))
                    print('')
                    

    if bool(A) != False:
        if len(Direction_list) > 0:
            xmaxlist_dict = {'Sat': Direction_list, 'Date_of_Occurence': xmaxlist}
            xmaxdf = pd.DataFrame(xmaxlist_dict)
            xmaxdf.index = xmaxdf['Sat']
            xmaxdf = xmaxdf.drop(columns='Sat')

            if 'Ascending' in Direction_list:
                timing_ASC_AMP.append(xmaxdf['Date_of_Occurence']['Ascending'])
                percentage_ASC_AMP.append(percentagelist[0])
            if 'Descending' in Direction_list:
                timing_DSC_AMP.append(xmaxdf['Date_of_Occurence']['Descending'])
                if 'Descending' in Direction_list and 'Ascending' not in Direction_list:
                    percentage_DSC_AMP.append(percentagelist[0])
                else:
                    percentage_DSC_AMP.append(percentagelist[1])

            if 'actualdate' in locals():
                if 'Ascending' in Direction_list:
                    percentage_seven_days_ASC_AMP.append(percentagelist_seven_days[0])
                    percentage_within_month_ASC_AMP.append(percentagelist_within_month[0])

                if 'Descending' in Direction_list:
                    percentage_seven_days_DSC_AMP.append(percentagelist_seven_days[1])
                    percentage_within_month_DSC_AMP.append(percentagelist_within_month[1])

    plt.close('all')
plt.close('all')

#region TIMING ESTIMATION COHERENCE & SAC
if Coherence_data == 'Yes':
    print('COHERENCE')
    if Detrend == 'Yes':
        # region KDE regular
        Differencedict = {}
        Timelist = {}
        if 'Ascending' in Direction_list and 'Descending' in Direction_list:
            SATLIST = ['Ascending', 'Descending']
        if 'Ascending' in Direction_list and not 'Descending' in Direction_list:
            SATLIST = ['Ascending']
        if 'Descending' in Direction_list and not 'Ascending' in Direction_list:
            SATLIST = ['Descending']

        xmaxlist = []
        percentagelist = []
        percentagelist_seven_days = []
        percentagelist_within_month = []
        dirlist = []
        figiter = 0
        Diff_Timing = {}
        for sat in SATLIST:
            Diff_Timing[sat] = {}

        count = 0
        for sat in SATLIST:
            Timelist = {}
            if sat == 'Ascending':
                A = Detrended_DF['Coherence']['GH']['Ascending']
            else:
                A = Detrended_DF['Coherence']['GH']['Descending']
            if bool(A) != False:
                if sat == 'Ascending':
                    satdir = 'Ascending'
                    dirlist.append(satdir)
                else:
                    satdir = 'Descending'
                    dirlist.append(satdir)
                for i in A:
                    if A[i].isnull().values.any() == False:
                        points = np.array(A[i])
                        Timelist[i] = []
                        diflist = []
                        timlist = []
                        Differencedict[i] = {}

                        model = "l2"
                        algo = rpt.Binseg(model=model).fit(points)
                        my_bkps = algo.predict(n_bkps=1)
                        # print('binary segmentation based timing')
                        Timelist[i].append(A[i][A[i] == A[i].iloc[my_bkps[0] - 1]].dropna().index[0])

                Diff_Timing[sat] = pd.DataFrame(Timelist)
                Diff_Timing[sat] = Diff_Timing[sat].transpose()
                Diff_Timing[sat] = Diff_Timing[sat].dropna()
                Diff_Timing[sat]['ordinal'] = [x.toordinal() for x in Diff_Timing[sat][0]]

                if len(Diff_Timing[sat]) == int(Diff_Timing[sat]['ordinal'].value_counts().max()):
                    if count == 1:
                        dirlist = []
                        dirlist.append('Descending')
                    ABC = Diff_Timing[sat][0].value_counts()
                    xmax = Diff_Timing[sat]['ordinal'].value_counts()[
                        Diff_Timing[sat]['ordinal'].value_counts() == Diff_Timing[sat][
                            'ordinal'].value_counts().max()].index[0]
                    xmaxlabel = str(Diff_Timing[sat][0].value_counts()[
                                        Diff_Timing[sat][0].value_counts() == Diff_Timing[sat][
                                            0].value_counts().max()].index[0])[
                                0:10]  # [datetime.datetime.fromordinal(int(x)).strftime('%Y-%m-%d') for x in xmax][0]
                    xmaxlist.append(xmaxlabel)

                    number_of_Correct_predict = len(Diff_Timing[sat][0][Diff_Timing[sat][0] == xmaxlabel])
                    total_amount_of_predict = len(namelist[sat])
                    percentage = (number_of_Correct_predict / total_amount_of_predict) * 100
                    percentagelist.append(percentage)

                    if 'actualdate' in locals():
                        number_of_predict_within_seven_days_of_actual = len(
                            Diff_Timing[sat][0][abs(Diff_Timing[sat][0] - actualdate).dt.days <= 7])
                        number_of_predict_within_one_month_of_actual = len(
                            Diff_Timing[sat][0][abs(Diff_Timing[sat][0] - actualdate).dt.days <= 31])
                        percentage_seven_days = (
                                                        number_of_predict_within_seven_days_of_actual / total_amount_of_predict) * 100
                        percentage_within_month = (
                                                          number_of_predict_within_one_month_of_actual / total_amount_of_predict) * 100
                        percentagelist_seven_days.append(percentage_seven_days)
                        percentagelist_within_month.append(percentage_within_month)

                    plt.close()
                    count += 1
                else:
                    ABC = Diff_Timing[sat][0].value_counts()
                    xmax = Diff_Timing[sat]['ordinal'].value_counts()[
                        Diff_Timing[sat]['ordinal'].value_counts() == Diff_Timing[sat][
                            'ordinal'].value_counts().max()].index[0]
                    xmaxlabel = str(Diff_Timing[sat][0].value_counts()[
                                        Diff_Timing[sat][0].value_counts() == Diff_Timing[sat][
                                            0].value_counts().max()].index[0])[
                                0:10]  # [datetime.datetime.fromordinal(int(x)).strftime('%Y-%m-%d') for x in xmax][0]
                    xmaxlist.append(xmaxlabel)

                    # print(Diff_Timing[sat][0])
                    number_of_Correct_predict = len(Diff_Timing[sat][0][Diff_Timing[sat][0] == xmaxlabel])

                    total_amount_of_predict = len(namelist[sat])
                    percentage = (number_of_Correct_predict / total_amount_of_predict) * 100
                    percentagelist.append(percentage)

                    if 'actualdate' in locals():
                        number_of_predict_within_seven_days_of_actual = len(
                            Diff_Timing[sat][0][abs(Diff_Timing[sat][0] - actualdate).dt.days <= 7])
                        number_of_predict_within_one_month_of_actual = len(
                            Diff_Timing[sat][0][abs(Diff_Timing[sat][0] - actualdate).dt.days <= 31])
                        percentage_seven_days = (
                                                        number_of_predict_within_seven_days_of_actual / total_amount_of_predict) * 100
                        percentage_within_month = (
                                                          number_of_predict_within_one_month_of_actual / total_amount_of_predict) * 100
                        percentagelist_seven_days.append(percentage_seven_days)
                        percentagelist_within_month.append(percentage_within_month)

        if bool(A) != False:
            if len(Direction_list) > 0:
                xmaxlist_dict = {'Sat': Direction_list, 'Date_of_Occurence': xmaxlist}
                xmaxdf = pd.DataFrame(xmaxlist_dict)
                xmaxdf.index = xmaxdf['Sat']
                xmaxdf = xmaxdf.drop(columns='Sat')

                if 'Ascending' in Direction_list:
                    timing_ASC_COH_nodet.append(xmaxdf['Date_of_Occurence']['Ascending'])
                    percentage_ASC_COH_nodet.append(percentagelist[0])
                if 'Descending' in Direction_list:
                    timing_DSC_COH_nodet.append(xmaxdf['Date_of_Occurence']['Descending'])
                    if 'Descending' in Direction_list and 'Ascending' not in Direction_list:
                        percentage_DSC_COH_nodet.append(percentagelist[0])
                    else:
                        percentage_DSC_COH_nodet.append(percentagelist[1])

                if 'actualdate' in locals():
                    if 'Ascending' in Direction_list:
                        percentage_seven_days_ASC_COH_nodet.append(percentagelist_seven_days[0])
                        percentage_within_month_ASC_COH_nodet.append(percentagelist_within_month[0])

                    if 'Descending' in Direction_list:
                        percentage_seven_days_DSC_COH_nodet.append(percentagelist_seven_days[1])
                        percentage_within_month_DSC_COH_nodet.append(percentagelist_within_month[1])

        plt.close('all')
        # region KDE regular
        Differencedict = {}
        Timelist = {}
        if 'Ascending' in Direction_list and 'Descending' in Direction_list:
            SATLIST = ['Ascending', 'Descending']
        if 'Ascending' in Direction_list and not 'Descending' in Direction_list:
            SATLIST = ['Ascending']
        if 'Descending' in Direction_list and not 'Ascending' in Direction_list:
            SATLIST = ['Descending']

        xmaxlist = []
        percentagelist = []
        percentagelist_seven_days = []
        percentagelist_within_month = []
        dirlist = []
        figiter = 0
        Diff_Timing = {}
        for sat in SATLIST:
            Diff_Timing[sat] = {}

        count = 0
        for sat in SATLIST:
            Timelist = {}
            if sat == 'Ascending':
                A = COH['Ascending']
            else:
                A = COH['Descending']
            if bool(A) != False:
                if sat == 'Ascending':
                    satdir = 'Ascending'
                    dirlist.append(satdir)
                else:
                    satdir = 'Descending'
                    dirlist.append(satdir)
                for i in A:
                    if A[i].isnull().values.any() == False:
                        A[i] = A[i].copy()
                        points = np.array(A[i])
                        Timelist[i] = []
                        diflist = []
                        timlist = []
                        Differencedict[i] = {}

                        model = "l2"
                        algo = rpt.Binseg(model=model).fit(points)
                        my_bkps = algo.predict(n_bkps=1)
                        # print('binary segmentation based timing')
                        Timelist[i].append(A[i][A[i] == A[i].iloc[my_bkps[0] - 1]].dropna().index[0])


                Diff_Timing[sat] = pd.DataFrame(Timelist)
                Diff_Timing[sat] = Diff_Timing[sat].transpose()
                Diff_Timing[sat] = Diff_Timing[sat].dropna()
                Diff_Timing[sat]['ordinal'] = [x.toordinal() for x in Diff_Timing[sat][0]]

                if len(Diff_Timing[sat]) == int(Diff_Timing[sat]['ordinal'].value_counts().max()):
                    if count == 1:
                        dirlist = []
                        dirlist.append('Descending')

                    ABC = Diff_Timing[sat][0].value_counts()
                    xmax = Diff_Timing[sat]['ordinal'].value_counts()[
                        Diff_Timing[sat]['ordinal'].value_counts() == Diff_Timing[sat][
                            'ordinal'].value_counts().max()].index[0]
                    xmaxlabel = str(Diff_Timing[sat][0].value_counts()[
                                        Diff_Timing[sat][0].value_counts() == Diff_Timing[sat][
                                            0].value_counts().max()].index[0])[
                                0:10]  # [datetime.datetime.fromordinal(int(x)).strftime('%Y-%m-%d') for x in xmax][0]
                    xmaxlist.append(xmaxlabel)

                    number_of_Correct_predict = len(Diff_Timing[sat][0][Diff_Timing[sat][0] == xmaxlabel])
                    total_amount_of_predict = len(namelist[sat])
                    percentage = (number_of_Correct_predict / total_amount_of_predict) * 100
                    percentagelist.append(percentage)

                    if 'actualdate' in locals():
                        number_of_predict_within_seven_days_of_actual = len(
                            Diff_Timing[sat][0][abs(Diff_Timing[sat][0] - actualdate).dt.days <= 7])
                        number_of_predict_within_one_month_of_actual = len(
                            Diff_Timing[sat][0][abs(Diff_Timing[sat][0] - actualdate).dt.days <= 31])
                        percentage_seven_days = (
                                                        number_of_predict_within_seven_days_of_actual / total_amount_of_predict) * 100
                        percentage_within_month = (
                                                          number_of_predict_within_one_month_of_actual / total_amount_of_predict) * 100
                        percentagelist_seven_days.append(percentage_seven_days)
                        percentagelist_within_month.append(percentage_within_month)
                        

                    count += 1
                else:
                    ABC = Diff_Timing[sat][0].value_counts()
                    xmax = Diff_Timing[sat]['ordinal'].value_counts()[
                        Diff_Timing[sat]['ordinal'].value_counts() == Diff_Timing[sat][
                            'ordinal'].value_counts().max()].index[0]
                    xmaxlabel = str(Diff_Timing[sat][0].value_counts()[
                                        Diff_Timing[sat][0].value_counts() == Diff_Timing[sat][
                                            0].value_counts().max()].index[0])[
                                0:10]  # [datetime.datetime.fromordinal(int(x)).strftime('%Y-%m-%d') for x in xmax][0]
                    xmaxlist.append(xmaxlabel)

                    # print(Diff_Timing[sat][0])
                    number_of_Correct_predict = len(Diff_Timing[sat][0][Diff_Timing[sat][0] == xmaxlabel])

                    total_amount_of_predict = len(namelist[sat])
                    percentage = (number_of_Correct_predict / total_amount_of_predict) * 100
                    percentagelist.append(percentage)

                    if 'actualdate' in locals():
                        number_of_predict_within_seven_days_of_actual = len(
                            Diff_Timing[sat][0][abs(Diff_Timing[sat][0] - actualdate).dt.days <= 7])
                        number_of_predict_within_one_month_of_actual = len(
                            Diff_Timing[sat][0][abs(Diff_Timing[sat][0] - actualdate).dt.days <= 31])
                        percentage_seven_days = (
                                                        number_of_predict_within_seven_days_of_actual / total_amount_of_predict) * 100
                        percentage_within_month = (
                                                          number_of_predict_within_one_month_of_actual / total_amount_of_predict) * 100
                        percentagelist_seven_days.append(percentage_seven_days)
                        percentagelist_within_month.append(percentage_within_month)

        if bool(A) != False:
            if len(Direction_list) > 0:
                xmaxlist_dict = {'Sat': Direction_list, 'Date_of_Occurence': xmaxlist}
                xmaxdf = pd.DataFrame(xmaxlist_dict)
                xmaxdf.index = xmaxdf['Sat']
                xmaxdf = xmaxdf.drop(columns='Sat')

                if 'Ascending' in Direction_list:
                    timing_ASC_COH.append(xmaxdf['Date_of_Occurence']['Ascending'])
                    percentage_ASC_COH.append(percentagelist[0])
                if 'Descending' in Direction_list:
                    timing_DSC_COH.append(xmaxdf['Date_of_Occurence']['Descending'])
                    if 'Descending' in Direction_list and 'Ascending' not in Direction_list:
                        percentage_DSC_COH.append(percentagelist[0])
                    else:
                        percentage_DSC_COH.append(percentagelist[1])

                if 'actualdate' in locals():
                    if 'Ascending' in Direction_list:
                        percentage_seven_days_ASC_COH.append(percentagelist_seven_days[0])
                        percentage_within_month_ASC_COH.append(percentagelist_within_month[0])

                    if 'Descending' in Direction_list:
                        percentage_seven_days_DSC_COH.append(percentagelist_seven_days[1])
                        percentage_within_month_DSC_COH.append(percentagelist_within_month[1])

        plt.close('all')
    else:
        #region KDE regular
        Differencedict = {}
        Timelist = {}
        if 'Ascending' in Direction_list and 'Descending' in Direction_list:
            SATLIST = ['COH_Concat_ASC_norm', 'COH_Concat_DSC_norm']
        if 'Ascending' in Direction_list and not 'Descending' in Direction_list:
            SATLIST = ['COH_Concat_ASC_norm']
        if 'Descending' in Direction_list and not 'Ascending' in Direction_list:
            SATLIST = ['COH_Concat_DSC_norm']

        xmaxlist = []
        percentagelist=[]
        percentagelist_seven_days = []
        percentagelist_within_month = []
        dirlist=[]
        figiter = 0
        Diff_Timing = {}
        for sat in SATLIST:
            Diff_Timing[sat] = {}

        count=0
        for sat in SATLIST:
            Timelist = {}
            if sat == 'COH_Concat_ASC_norm':
                A = COH_Concat_ASC_norm
                A = A.drop(columns='mean')
            else:
                A = COH_Concat_DSC_norm
                A = A.drop(columns='mean')
            if A.empty == False:
                if sat == 'COH_Concat_ASC_norm':
                    satdir = 'Ascending'
                    dirlist.append(satdir)
                else:
                    satdir = 'Descending'
                    dirlist.append(satdir)
                for i in A:
                    if A[i].isnull().values.any() == False:
                        points = np.array(A[i])
                        Timelist[i] = []
                        diflist = []
                        timlist = []
                        Differencedict[i] = {}

                        model = "l2"
                        algo = rpt.Binseg(model=model).fit(points)
                        my_bkps = algo.predict(n_bkps=1)
                        # print('binary segmentation based timing')
                        Timelist[i].append(A[i][A[i]== A[i].iloc[my_bkps[0] - 1]].index[0])

                Diff_Timing[sat] = pd.DataFrame(Timelist)
                Diff_Timing[sat] = Diff_Timing[sat].transpose()
                Diff_Timing[sat] = Diff_Timing[sat].dropna()
                Diff_Timing[sat]['ordinal'] = [x.toordinal() for x in Diff_Timing[sat][0]]

                if len(Diff_Timing[sat]) == int(Diff_Timing[sat]['ordinal'].value_counts().max()):
                    if count == 1:
                        dirlist = []
                        dirlist.append('Descending')

                    ABC = Diff_Timing[sat][0].value_counts()
                    xmax = Diff_Timing[sat]['ordinal'].value_counts()[
                        Diff_Timing[sat]['ordinal'].value_counts() == Diff_Timing[sat][
                            'ordinal'].value_counts().max()].index[0]
                    xmaxlabel = str(Diff_Timing[sat][0].value_counts()[
                                        Diff_Timing[sat][0].value_counts() == Diff_Timing[sat][
                                            0].value_counts().max()].index[0])[
                                0:10]  # [datetime.datetime.fromordinal(int(x)).strftime('%Y-%m-%d') for x in xmax][0]
                    xmaxlist.append(xmaxlabel)

                    number_of_Correct_predict = len(Diff_Timing[sat][0][Diff_Timing[sat][0] == xmaxlabel])
                    total_amount_of_predict = len(namelist[satdir])
                    percentage = (number_of_Correct_predict / total_amount_of_predict) * 100
                    percentagelist.append(percentage)

                    if 'actualdate' in locals():
                        number_of_predict_within_seven_days_of_actual = len(Diff_Timing[sat][0][abs(Diff_Timing[sat][0]-actualdate).dt.days <= 7])
                        number_of_predict_within_one_month_of_actual = len(Diff_Timing[sat][0][abs(Diff_Timing[sat][0]-actualdate).dt.days <= 31])
                        # print(Diff_Timing[sat][0][abs(Diff_Timing[sat][0]-actualdate).dt.days <= 31])
                        percentage_seven_days = (number_of_predict_within_seven_days_of_actual / total_amount_of_predict) * 100
                        percentage_within_month = (number_of_predict_within_one_month_of_actual / total_amount_of_predict) * 100
                        percentagelist_seven_days.append(percentage_seven_days)
                        percentagelist_within_month.append(percentage_within_month)
                        print('')
                        print('track: '+sat)
                        print('within one month number: '+str(number_of_predict_within_one_month_of_actual))
                        print('total number: '+str(total_amount_of_predict))
                        print('')

                    count += 1
                else:
                    ABC=Diff_Timing[sat][0].value_counts()
                    xmax = Diff_Timing[sat]['ordinal'].value_counts()[Diff_Timing[sat]['ordinal'].value_counts() == Diff_Timing[sat]['ordinal'].value_counts().max()].index[0]
                    xmaxlabel = str(Diff_Timing[sat][0].value_counts()[Diff_Timing[sat][0].value_counts() == Diff_Timing[sat][0].value_counts().max()].index[0])[ 0:10]  # [datetime.datetime.fromordinal(int(x)).strftime('%Y-%m-%d') for x in xmax][0]
                    xmaxlist.append(xmaxlabel)

                    # print(Diff_Timing[sat][0])
                    number_of_Correct_predict = len(Diff_Timing[sat][0][Diff_Timing[sat][0] == xmaxlabel])

                    total_amount_of_predict = len(namelist[satdir])
                    percentage = (number_of_Correct_predict / total_amount_of_predict) * 100
                    percentagelist.append(percentage)

                    if 'actualdate' in locals():
                        number_of_predict_within_seven_days_of_actual = len(Diff_Timing[sat][0][abs(Diff_Timing[sat][0] - actualdate).dt.days <= 7])
                        number_of_predict_within_one_month_of_actual = len(Diff_Timing[sat][0][abs(Diff_Timing[sat][0] - actualdate).dt.days <= 31])
                        # print(Diff_Timing[sat][0][abs(Diff_Timing[sat][0]-actualdate).dt.days <= 31])
                        percentage_seven_days = (number_of_predict_within_seven_days_of_actual / total_amount_of_predict) * 100
                        percentage_within_month = (number_of_predict_within_one_month_of_actual / total_amount_of_predict) * 100
                        percentagelist_seven_days.append(percentage_seven_days)
                        percentagelist_within_month.append(percentage_within_month)
                        print('')
                        print('track: '+sat)
                        print('within one month number: '+str(number_of_predict_within_one_month_of_actual))
                        print('total number: '+str(total_amount_of_predict))
                        print('')

        if A.empty == False:
            if len(Direction_list) > 0:
                xmaxlist_dict = {'Sat': Direction_list, 'Date_of_Occurence': xmaxlist}
                xmaxdf = pd.DataFrame(xmaxlist_dict)
                xmaxdf.index = xmaxdf['Sat']
                xmaxdf = xmaxdf.drop(columns='Sat')

                if 'Ascending' in Direction_list:
                    timing_ASC_COH.append(xmaxdf['Date_of_Occurence']['Ascending'])
                    percentage_ASC_COH.append(percentagelist[0])
                if 'Descending' in Direction_list:
                    timing_DSC_COH.append(xmaxdf['Date_of_Occurence']['Descending'])
                    if 'Descending' in Direction_list and 'Ascending' not in Direction_list:
                        percentage_DSC_COH.append(percentagelist[0])
                    else:
                        percentage_DSC_COH.append(percentagelist[1])

                if 'actualdate' in locals():
                    if 'Ascending' in Direction_list:
                        percentage_seven_days_ASC_COH.append(percentagelist_seven_days[0])
                        percentage_within_month_ASC_COH.append(percentagelist_within_month[0])

                    if 'Descending' in Direction_list:
                        percentage_seven_days_DSC_COH.append(percentagelist_seven_days[1])
                        percentage_within_month_DSC_COH.append(percentagelist_within_month[1])

        plt.close('all')
plt.close('all')

if SAC_data == 'Yes':
    print('SAC')
    Diff_Timing_SAC = {}
    if SAC_data == 'Yes':
        count = 0
        counter = 0
        figiter = 0
        dirlist = []
        xmaxlist = []
        percentagelist = []
        percentagelist_seven_days = []
        percentagelist_within_month = []
        for sat in Direction_list:
            ECDF_sat = ECDF_IntensityCorrelation[sat]
            Diff_Timing_SAC[sat] = {}
            Timelist = []

            if ECDF_sat:
                counter += 1
                if sat == 'Ascending':
                    dirlist.append(sat)
                else:
                    dirlist.append(sat)
            for A in ECDF_sat:
                # print(A)
                timinglist = []
                maxlist = []
                typelist=[SACvariable_B]
                for SACvariable_B in typelist:
                    # Change point detection - Binary Segmentation method
                    dataset = ECDF_sat[A][SACvariable_A][SACvariable_B].loc['2016-06-01':]
                    points = np.array(dataset)
                    model = "l2"
                    algo = rpt.Binseg(model=model).fit(points)
                    my_bkps = algo.predict(n_bkps=1)
                    Timelist.append(dataset[dataset == dataset.iloc[my_bkps[0] - 1]].index[0])

            # print(Timelist)
            Diff_Timing_SAC[sat] = pd.DataFrame(Timelist)
            Diff_Timing_SAC[sat] = Diff_Timing_SAC[sat].dropna()
            Diff_Timing_SAC[sat]['ordinal'] = [x.toordinal() for x in Diff_Timing_SAC[sat][0]]

            if len(Diff_Timing_SAC[sat]) == int(Diff_Timing_SAC[sat]['ordinal'].value_counts().max()):
                ABC = Diff_Timing_SAC[sat][0].value_counts()
                xmax = Diff_Timing_SAC[sat]['ordinal'].value_counts()[
                    Diff_Timing_SAC[sat]['ordinal'].value_counts() == Diff_Timing_SAC[sat][
                        'ordinal'].value_counts().max()].index[0]
                xmaxlabel = str(Diff_Timing_SAC[sat][0].value_counts()[
                                    Diff_Timing_SAC[sat][0].value_counts() == Diff_Timing_SAC[sat][
                                        0].value_counts().max()].index[0])[
                            0:10]  # [datetime.datetime.fromordinal(int(x)).strftime('%Y-%m-%d') for x in xmax][0]
                xmaxlist.append(xmaxlabel)

                number_of_Correct_predict = len(Diff_Timing_SAC[sat][0][Diff_Timing_SAC[sat][0] == xmaxlabel])
                total_amount_of_predict = len(namelist[sat])
                percentage = (number_of_Correct_predict / total_amount_of_predict) * 100
                percentagelist.append(percentage)

                if 'actualdate' in locals():
                    number_of_predict_within_seven_days_of_actual = len(Diff_Timing_SAC[sat][0][abs(Diff_Timing_SAC[sat][0] - actualdate).dt.days <= 7])
                    number_of_predict_within_one_month_of_actual = len(Diff_Timing_SAC[sat][0][abs(Diff_Timing_SAC[sat][0] - actualdate).dt.days <= 31])
                    # print(Diff_Timing_SAC[sat][0][abs(Diff_Timing_SAC[sat][0]-actualdate).dt.days <= 31])
                    percentage_seven_days = (number_of_predict_within_seven_days_of_actual / total_amount_of_predict) * 100
                    percentage_within_month = (number_of_predict_within_one_month_of_actual / total_amount_of_predict) * 100
                    percentagelist_seven_days.append(percentage_seven_days)
                    percentagelist_within_month.append(percentage_within_month)
                    print('')
                    print('track: '+sat)
                    print('within one month number: '+str(number_of_predict_within_one_month_of_actual))
                    print('total number: '+str(total_amount_of_predict))
                    print('')

                count += 1
            else:
                ABC = Diff_Timing_SAC[sat][0].value_counts()
                xmax = Diff_Timing_SAC[sat]['ordinal'].value_counts()[
                    Diff_Timing_SAC[sat]['ordinal'].value_counts() == Diff_Timing_SAC[sat][
                        'ordinal'].value_counts().max()].index[0]
                xmaxlabel = str(Diff_Timing_SAC[sat][0].value_counts()[
                                    Diff_Timing_SAC[sat][0].value_counts() == Diff_Timing_SAC[sat][
                                        0].value_counts().max()].index[0])[
                            0:10]  # [datetime.datetime.fromordinal(int(x)).strftime('%Y-%m-%d') for x in xmax][0]
                xmaxlist.append(xmaxlabel)

                number_of_Correct_predict = len(Diff_Timing_SAC[sat][0][Diff_Timing_SAC[sat][0] == xmaxlabel])


                total_amount_of_predict = len(namelist[sat])
                percentage = (number_of_Correct_predict / total_amount_of_predict) * 100
                percentagelist.append(percentage)

                if 'actualdate' in locals():
                    number_of_predict_within_seven_days_of_actual = len(Diff_Timing_SAC[sat][0][abs(Diff_Timing_SAC[sat][0] - actualdate).dt.days <= 7])
                    number_of_predict_within_one_month_of_actual = len( Diff_Timing_SAC[sat][0][abs(Diff_Timing_SAC[sat][0] - actualdate).dt.days <= 31])
                    # print(Diff_Timing_SAC[sat][0][abs(Diff_Timing_SAC[sat][0]-actualdate).dt.days <= 31])
                    percentage_seven_days = (number_of_predict_within_seven_days_of_actual / total_amount_of_predict) * 100
                    percentage_within_month = (number_of_predict_within_one_month_of_actual / total_amount_of_predict) * 100
                    percentagelist_seven_days.append(percentage_seven_days)
                    percentagelist_within_month.append(percentage_within_month)
                    print('')
                    print('track: '+sat)
                    print('within one month number: '+str(number_of_predict_within_one_month_of_actual))
                    print('total number: '+str(total_amount_of_predict))
                    print('')

        if len(Direction_list) > 0:
            xmaxlist_dict = {'Sat': Direction_list, 'Date_of_Occurence': xmaxlist}
            xmaxdf = pd.DataFrame(xmaxlist_dict)
            xmaxdf.index = xmaxdf['Sat']
            xmaxdf = xmaxdf.drop(columns='Sat')

            if 'Ascending' in Direction_list:
                timing_ASC_SAC.append(xmaxdf['Date_of_Occurence']['Ascending'])
                percentage_ASC_SAC.append(percentagelist[0])
            if 'Descending' in Direction_list:
                timing_DSC_SAC.append(xmaxdf['Date_of_Occurence']['Descending'])

                if 'Descending' in Direction_list and 'Ascending' not in Direction_list:
                    percentage_DSC_SAC.append(percentagelist[0])
                else:
                    percentage_DSC_SAC.append(percentagelist[1])

            if 'actualdate' in locals():
                if 'Ascending' in Direction_list:
                    percentage_seven_days_ASC_SAC.append(percentagelist_seven_days[0])
                    percentage_within_month_ASC_SAC.append(percentagelist_within_month[0])

                if 'Descending' in Direction_list:
                    percentage_seven_days_DSC_SAC.append(percentagelist_seven_days[1])
                    percentage_within_month_DSC_SAC.append(percentagelist_within_month[1])
    plt.close('all')
plt.close('all')
#endregion

#Elapsed time
end = time.time()
print('Elapsed time: ' + str(int((end - start)/60)) + ' Minutes and ' + str(int((((end-start)/60)-int((end - start)/60))*60)) + ' Seconds')
# geometrylenlist.append(len(df_geometries))
# gc.collect()

# geometry_masked_DSC = df_geometries
# geometry_masked_ASC = df_geometries

# if Amplitude_data == 'Yes':
#     if Masked == 'Yes':
#         if 'Ascending' in Direction_list and 'Descending' in Direction_list:
#             trenddict = dict({'Ascending_predict': timing_ASC_AMP, 'Descending_predict': timing_DSC_AMP,
#                               'Percentage_ASC': percentage_ASC_AMP, 'Percentage_DSC': percentage_DSC_AMP,
#                               'number of Polygons ASC': len(geometry_masked_ASC),
#                               'number of polygons DSC': len(geometry_masked_DSC)})
#             trendDF = pd.DataFrame(trenddict)
#
#         if 'Ascending' in Direction_list and not 'Descending' in Direction_list:
#             trenddict = dict({'Ascending_predict': timing_ASC_AMP,
#                               'Percentage_ASC': percentage_ASC_AMP,
#                               'number of Polygons ASC': len(geometry_masked_ASC)})
#             trendDF = pd.DataFrame(trenddict)
#
#         if 'Descending' in Direction_list and not 'Ascending' in Direction_list:
#             trenddict = dict({'Descending_predict': timing_DSC_AMP, 'Percentage_DSC': percentage_DSC_AMP,
#                               'number of polygons DSC': len(geometry_masked_DSC)})
#             trendDF = pd.DataFrame(trenddict)
#     else:
#         if 'Ascending' in Direction_list and 'Descending' in Direction_list:
#             trenddict = dict({'Ascending_predict': timing_ASC_AMP, 'Descending_predict': timing_DSC_AMP,
#                               'Percentage_ASC': percentage_ASC_AMP, 'Percentage_DSC': percentage_DSC_AMP,
#                               'number of Polygons': geometrylenlist})
#             trendDF = pd.DataFrame(trenddict)
#         if 'Ascending' in Direction_list and not 'Descending' in Direction_list:
#             trenddict = dict({'Ascending_predict': timing_ASC_AMP,
#                               'Percentage_ASC': percentage_ASC_AMP,
#                               'number of Polygons': geometrylenlist})
#             trendDF = pd.DataFrame(trenddict)
#         if 'Descending' in Direction_list and not 'Ascending' in Direction_list:
#             trenddict = dict({'Descending_predict': timing_DSC_AMP, 'Percentage_DSC': percentage_DSC_AMP,
#                               'number of Polygons': geometrylenlist})
#             trendDF = pd.DataFrame(trenddict)
# if Coherence_data == 'Yes':
#     if Masked == 'Yes':
#         if 'Ascending' in Direction_list and 'Descending' in Direction_list:
#             trenddict = dict({'Ascending_predict': timing_ASC, 'Descending_predict': timing_DSC,
#                               'Percentage_ASC': percentage_ASC, 'Percentage_DSC': percentage_DSC,
#                               'number of Polygons ASC': len(geometry_masked_ASC),
#                               'number of polygons DSC': len(geometry_masked_DSC)})
#             trendDF = pd.DataFrame(trenddict)
#
#         if 'Ascending' in Direction_list and not 'Descending' in Direction_list:
#             trenddict = dict({'Ascending_predict': timing_ASC,
#                               'Percentage_ASC': percentage_ASC,
#                               'number of Polygons ASC': len(geometry_masked_ASC)})
#             trendDF = pd.DataFrame(trenddict)
#
#         if 'Descending' in Direction_list and not 'Ascending' in Direction_list:
#             trenddict = dict({'Descending_predict': timing_DSC, 'Percentage_DSC': percentage_DSC,
#                               'number of polygons DSC': len(geometry_masked_DSC)})
#             trendDF = pd.DataFrame(trenddict)
#     else:
#         if 'Ascending' in Direction_list and 'Descending' in Direction_list:
#             trenddict = dict({'Ascending_predict': timing_ASC, 'Descending_predict': timing_DSC,
#                               'Percentage_ASC': percentage_ASC, 'Percentage_DSC': percentage_DSC,
#                               'number of Polygons': geometrylenlist})
#             trendDF = pd.DataFrame(trenddict)
#         if 'Ascending' in Direction_list and not 'Descending' in Direction_list:
#             trenddict = dict({'Ascending_predict': timing_ASC,
#                               'Percentage_ASC': percentage_ASC,
#                               'number of Polygons': geometrylenlist})
#             trendDF = pd.DataFrame(trenddict)
#         if 'Descending' in Direction_list and not 'Ascending' in Direction_list:
#             trenddict = dict({'Descending_predict': timing_DSC, 'Percentage_DSC': percentage_DSC,
#                               'number of Polygons': geometrylenlist})
#             trendDF = pd.DataFrame(trenddict)
# if SAC_data == 'Yes':
#     if Masked == 'Yes':
#         if 'Ascending' in Direction_list and 'Descending' in Direction_list:
#             trenddict = dict({'Ascending_predict': timing_ASC_SAC, 'Descending_predict': timing_DSC_SAC,
#                               'Percentage_ASC': percentage_ASC_SAC, 'Percentage_DSC': percentage_DSC_SAC,
#                               'number of Polygons ASC': len(geometry_masked_ASC),
#                               'number of polygons DSC': len(geometry_masked_DSC)})
#             trendDF = pd.DataFrame(trenddict)
#
#         if 'Ascending' in Direction_list and not 'Descending' in Direction_list:
#             trenddict = dict({'Ascending_predict': timing_ASC_SAC,
#                               'Percentage_ASC': percentage_ASC_SAC,
#                               'number of Polygons ASC': len(geometry_masked_ASC)})
#             trendDF = pd.DataFrame(trenddict)
#
#         if 'Descending' in Direction_list and not 'Ascending' in Direction_list:
#             trenddict = dict({'Descending_predict': timing_DSC_SAC, 'Percentage_DSC': percentage_DSC_SAC,
#                               'number of polygons DSC': len(geometry_masked_DSC)})
#             trendDF = pd.DataFrame(trenddict)
#     else:
#         if 'Ascending' in Direction_list and 'Descending' in Direction_list:
#             trenddict = dict({'Ascending_predict': timing_ASC_SAC, 'Descending_predict': timing_DSC_SAC,
#                               'Percentage_ASC': percentage_ASC_SAC, 'Percentage_DSC': percentage_DSC_SAC,
#                               'number of Polygons': geometrylenlist})
#             trendDF = pd.DataFrame(trenddict)
#         if 'Ascending' in Direction_list and not 'Descending' in Direction_list:
#             trenddict = dict({'Ascending_predict': timing_ASC_SAC,
#                               'Percentage_ASC': percentage_ASC_SAC,
#                               'number of Polygons': geometrylenlist})
#             trendDF = pd.DataFrame(trenddict)
#         if 'Descending' in Direction_list and not 'Ascending' in Direction_list:
#             trenddict = dict({'Descending_predict': timing_DSC_SAC, 'Percentage_DSC': percentage_DSC_SAC,
#                               'number of Polygons': geometrylenlist})
#             trendDF = pd.DataFrame(trenddict)


# if 'actualdate' in locals():
#     if Amplitude_data == 'Yes':
#         if Masked== 'Yes':
#             trenddict = dict({'Ascending_predict': timing_ASC_AMP, 'Descending_predict': timing_DSC_AMP,'Percentage_ASC':percentage_ASC_AMP,'Percentage_DSC':percentage_DSC_AMP,'number of Polygons ASC':len(geometry_masked_ASC),'number of polygons DSC':len(geometry_masked_DSC),'ASC_within seven days':percentage_seven_days_ASC_AMP, 'DSC_within seven days':percentage_seven_days_DSC_AMP,'ASC_within one month':percentage_within_month_ASC_AMP, 'DSC_within one month':percentage_within_month_DSC_AMP})
#             trendDF = pd.DataFrame(trenddict)
#         else:
#             trenddict = dict({'Ascending_predict': timing_ASC_AMP, 'Descending_predict': timing_DSC_AMP,'Percentage_ASC':percentage_ASC_AMP,'Percentage_DSC':percentage_DSC_AMP,'number of Polygons':geometrylenlist,'ASC_within seven days':percentage_seven_days_ASC_AMP, 'DSC_within seven days':percentage_seven_days_DSC_AMP,'ASC_within one month':percentage_within_month_ASC_AMP, 'DSC_within one month':percentage_within_month_DSC_AMP})
#             trendDF = pd.DataFrame(trenddict)
#
#     if Coherence_data == 'Yes':
#         if Masked== 'Yes':
#             trenddict = dict({'Ascending_predict': timing_ASC, 'Descending_predict': timing_DSC,'Percentage_ASC':percentage_ASC,'Percentage_DSC':percentage_DSC,'number of Polygons ASC':len(geometry_masked_ASC),'number of polygons DSC':len(geometry_masked_DSC),'ASC_within seven days':percentage_seven_days_ASC, 'DSC_within seven days':percentage_seven_days_DSC,'ASC_within one month':percentage_within_month_ASC, 'DSC_within one month':percentage_within_month_DSC})
#             trendDF = pd.DataFrame(trenddict)
#         else:
#             trenddict = dict({'Ascending_predict': timing_ASC, 'Descending_predict': timing_DSC,'Percentage_ASC':percentage_ASC,'Percentage_DSC':percentage_DSC,'number of Polygons':geometrylenlist,'ASC_within seven days':percentage_seven_days_ASC, 'DSC_within seven days':percentage_seven_days_DSC,'ASC_within one month':percentage_within_month_ASC, 'DSC_within one month':percentage_within_month_DSC})
#             trendDF = pd.DataFrame(trenddict)
#
#     if SAC_data == 'Yes':
#         if Masked == 'Yes':
#             trenddict = dict({'Ascending_predict': timing_ASC_SAC, 'Descending_predict': timing_DSC_SAC,'Percentage_ASC':percentage_ASC_SAC,'Percentage_DSC':percentage_DSC_SAC,'number of Polygons ASC':len(geometry_masked_ASC),'number of polygons DSC':len(geometry_masked_DSC),'ASC_within seven days':percentage_seven_days_ASC_SAC, 'DSC_within seven days':percentage_seven_days_DSC_SAC,'ASC_within one month':percentage_within_month_ASC_SAC, 'DSC_within one month':percentage_within_month_DSC_SAC})
#             trendDF = pd.DataFrame(trenddict)
#         else:
#             trenddict = dict({'Ascending_predict': timing_ASC_SAC, 'Descending_predict': timing_DSC_SAC,'Percentage_ASC':percentage_ASC_SAC,'Percentage_DSC':percentage_DSC_SAC,'number of Polygons':geometrylenlist,'ASC_within seven days':percentage_seven_days_ASC_SAC, 'DSC_within seven days':percentage_seven_days_DSC_SAC,'ASC_within one month':percentage_within_month_ASC_SAC, 'DSC_within one month':percentage_within_month_DSC_SAC})
#             trendDF = pd.DataFrame(trenddict)
#


plt.close('all')
if Full_or_Single == 'Full':
    geometry_masked_ASC = ['one']
    geometry_masked_DSC = ['one']


print('')
print('')
print('########################################################################################################################################')
print('########################################################################################################################################')
print('####                                                                                                                                ####')
print('####                                                Location ' +Location+ '                                                                ####')
if Amplitude_data == 'Yes':
    print('####                                                                                                                                ####')
    if Detrend == 'Yes':
        print('####                                                  Amplitude                                                                      ####')
        if 'Ascending' in Direction_list:
            print('####                                        Timing ASC ' + str(timing_ASC_AMP_nodet[0]) + ' (' + str(
                int(percentage_ASC_AMP_nodet[0] / 100 * len(geometry_masked_ASC))) + '/' + str(
                int(len(geometry_masked_ASC))) + ')                                                            ####')
        if 'Descending' in Direction_list:
            print('####                                        Timing DSC ' + str(timing_DSC_AMP_nodet[0]) + ' (' + str(
                int(percentage_DSC_AMP_nodet[0] / 100 * len(geometry_masked_DSC))) + '/' + str(
                int(len(geometry_masked_DSC))) + ')                                                            ####')

        print('####                                             Detrended Amplitude                                                                 ####')
    else:
        print(
            '####                                                   Amplitude                                                                    ####')
    if 'Ascending' in Direction_list:
        print('####                                        Timing ASC ' +  str(timing_ASC_AMP[0]) + ' (' +str(int(percentage_ASC_AMP[0] /100 * len(geometry_masked_ASC)))+'/'+str(int(len(geometry_masked_ASC))))#+')    Within one month: '+ str(round(percentage_within_month_ASC_AMP[0],2)) + '%                               ####')
    if 'Descending' in Direction_list:
        print('####                                        Timing DSC ' +  str(timing_DSC_AMP[0]) + ' (' +str(int(percentage_DSC_AMP[0] /100 * len(geometry_masked_DSC)))+'/'+str(int(len(geometry_masked_DSC))))#+')    Within one month: '+ str(round(percentage_within_month_DSC_AMP[0],2)) + '%                               ####')
if Coherence_data == 'Yes':
    print('####                                                                                                                                ####')
    if Detrend == 'Yes':
        print('####                                                  Coherence                                                                      ####')
        if 'Ascending' in Direction_list:
            print('####                                        Timing ASC ' + str(timing_ASC_COH_nodet[0]) + ' (' + str(
                int(percentage_ASC_COH_nodet[0] / 100 * len(geometry_masked_ASC))) + '/' + str(
                int(len(geometry_masked_ASC))) + ')                                                            ####')
        if 'Descending' in Direction_list:
            print('####                                        Timing DSC ' + str(timing_DSC_COH_nodet[0]) + ' (' + str(
                int(percentage_DSC_COH_nodet[0] / 100 * len(geometry_masked_DSC))) + '/' + str(
                int(len(geometry_masked_DSC))) + ')                                                            ####')

        print('####                                             Detrended COHERENCE                                                                 ####')
    else:
        print(
            '####                                                   COHERENCE                                                                    ####')
    if 'Ascending' in Direction_list:
        print('####                                        Timing ASC ' +  str(timing_ASC_COH[0]) + ' (' +str(int(percentage_ASC_COH[0] /100 * len(geometry_masked_ASC)))+'/'+str(int(len(geometry_masked_ASC))))#+')    Within one month: '+ str(round(percentage_within_month_ASC_COH[0],2)) + '%                               ####')
    if 'Descending' in Direction_list:
        print('####                                        Timing DSC ' +  str(timing_DSC_COH[0]) + ' (' +str(int(percentage_DSC_COH[0] /100 * len(geometry_masked_DSC)))+'/'+str(int(len(geometry_masked_DSC))))#+')    Within one month: '+ str(round(percentage_within_month_DSC_COH[0],2)) + '%                               ####')
    print('####                                                                                                                                ####')
if SAC_data == 'Yes':
    print('####                                         SPATIAL AMPLITUDE CORRELATION                                                          ####')
    if 'Ascending' in Direction_list:
        print('####                                        Timing ASC ' +  str(timing_ASC_SAC[0]) + ' (' +str(int(percentage_ASC_SAC[0] /100 * len(geometry_masked_ASC)))+'/'+str(int(len(geometry_masked_ASC))))#+')    Within one month: '+ str(round(percentage_within_month_ASC_SAC[0],2)) + '%                               ####')
    if 'Descending' in Direction_list:
        print('####                                        Timing DSC ' +  str(timing_DSC_SAC[0]) + ' (' +str(int(percentage_DSC_SAC[0] /100 * len(geometry_masked_DSC)))+'/'+str(int(len(geometry_masked_DSC))))#+')    Within one month: '+ str(round(percentage_within_month_DSC_SAC[0],2)) + '%                               ####')
    print('####                                                                                                                                ####')
    print('########################################################################################################################################')
    print('########################################################################################################################################')
else:
    print('####                                                                                                                                ####')
    print('########################################################################################################################################')
    print('########################################################################################################################################')
plt.close('all')

# if Full_or_Single == 'Full':
#     if SAC_data == 'Yes':
#         for A in ECDF_IntensityCorrelation:
#             ECDF_IntensityCorrelation[A]['poly_1'][SACvariable_A][SACvariable_B].loc['2016-06-01':].plot()
#         plt.title('Full Inventory Spatial Amplitude Correlation')
#         plt.xlabel('Time')
#         plt.ylabel('SAC')
#         plt.legend(['Ascending','Descending'])

# if Full_or_Single == 'Full':
#     for sat in Direction_list:
#         if Coherence_data == 'Yes':
#             COH[sat]['poly_1'].plot()
#             plt.title('Coherence')
#         if Amplitude_data == 'Yes':
#             AMP_normalized[sat]['poly_1'].plot()
#             plt.title('Amplitude')



# execute maintrend
if Full_or_Single == 'Full':
    exec(open('/home/axel/PycharmProjects/PhD_Scripts/Scripts/Basic/Maintrends.py').read())

# # execute distribution script
# if Full_or_Single == 'Single':
#     exec(open(
#         '/home/axel/PycharmProjects/PhD_Scripts/Scripts/SAR Landslide Timing/density distribution.py').read())

# plt.close('all')

# if os.path.isfile(exportcsv) == False:
#     df = pd.DataFrame([])
#     df.to_csv(exportcsv)

list = [percentage_within_month_ASC_AMP[0],percentage_within_month_DSC_AMP[0],percentage_within_month_ASC_COH[0],percentage_within_month_DSC_COH[0],percentage_within_month_ASC_SAC[0],percentage_within_month_DSC_SAC[0],len(geometry_masked_ASC),len(geometry_masked_DSC)]
newdf = pd.DataFrame(list)
newdf = newdf.rename(columns={0:Givenvariable})
newdf.index = ['AMP asc','AMP dsc','COH asc','COH dsc','SAC asc','SAC dsc','poly asc','poly dsc']
olddf = pd.read_csv(sys.argv[12])
# olddf = pd.read_csv(exportcsv)
olddf.index = olddf['RUN']
olddf = olddf.drop(columns='RUN')
olddf = olddf.join(newdf)
olddf.to_csv(sys.argv[12], index=True)
# olddf.to_csv(exportcsv, index=True)
print("")
print('DONE')
print("")                 