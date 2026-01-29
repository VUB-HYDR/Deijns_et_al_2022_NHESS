import os, subprocess, contextlib
from osgeo import gdal
# Clean subprocess output for that it is easily readable
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

if 'Ascending' in Direction_list:
    os.chdir(total_path_Ascending)
    image_a =   [s for s in os.listdir() if "sigma0" in s and '.bil' in s and 'flip' not in s][0]
    rasterize_filename_ASC = total_path_Ascending + '/'+ image_a
    image_array_ASC, pixelwidth_ASC, envidata_ASC = ENVI_raster_binary_to_2d_array(rasterize_filename_ASC)
    ASCshape = image_array_ASC.shape
    ASC_x1= envidata_ASC[0][0]
    ASC_x2= envidata_ASC[0][0] + ASCshape[1]*pixelwidth_ASC
    ASC_y1= envidata_ASC[0][3] - ASCshape[0]*pixelwidth_ASC
    ASC_y2= envidata_ASC[0][3]

if 'Descending' in Direction_list:
    os.chdir(total_path_Descending)
    image_b = [s for s in os.listdir() if "sigma0.UTM" in s and '.bil' in s and 'flip' not in s][0]
    rasterize_filename_DSC = total_path_Descending + '/' + image_b
    image_array_DSC, pixelwidth_DSC, envidata_DSC = ENVI_raster_binary_to_2d_array(rasterize_filename_DSC)
    DSCshape = image_array_DSC.shape
    DSC_x1= envidata_DSC[0][0]
    DSC_x2= envidata_DSC[0][0] + DSCshape[1]*pixelwidth_DSC
    DSC_y1= envidata_DSC[0][3] - DSCshape[0]*pixelwidth_DSC
    DSC_y2= envidata_DSC[0][3]

if Masked == 'No':
    if 'Ascending' in Direction_list:
        asc_name = shapefile_location[shapefile_location.rfind('/')+1:]
        geometry_masked_ASC_loc = '"' + shapefile_location + '"'
        if Full_or_Single == 'Full':
            asc_name = 'full_Invenotry_Dissolved.shp'
            geometry_masked_ASC_loc = '"'+ Processingpath + '/' + 'full_Invenotry_Dissolved.shp'+'"'
    if 'Descending' in Direction_list:
        dsc_name = shapefile_location[shapefile_location.rfind('/') + 1:]
        geometry_masked_DSC_loc = '"' + shapefile_location + '"'
        if Full_or_Single == 'Full':
            dsc_name = 'full_Invenotry_Dissolved.shp'
            geometry_masked_DSC_loc = '"'+ Processingpath + '/' + 'full_Invenotry_Dissolved.shp'+'"'

if Masked == 'Yes':
    if 'Ascending' in Direction_list:
        asc_name = 'Single_layoverandshadow_masked_ASC.shp'
        geometry_masked_ASC_loc = '"' + Processingpath+'/'+ asc_name + '"'
        if Full_or_Single == 'Full':
            asc_name = 'masked_full_Invenotry_Dissolved_asc.shp'
            geometry_masked_ASC_loc = '"' + Processingpath+'/'+ asc_name + '"'
    if 'Descending' in Direction_list:
        dsc_name = 'Single_layoverandshadow_masked_DSC.shp'
        geometry_masked_DSC_loc = '"' + Processingpath+'/'+ dsc_name + '"'
        if Full_or_Single == 'Full':
            dsc_name = 'masked_full_Invenotry_Dissolved_dsc.shp'
            geometry_masked_DSC_loc = '"'+ Processingpath+'/'+ dsc_name+'"'

if 'Ascending' in Direction_list:
    ASC_rasterizedgeometry = Processingpath +'/'+ asc_name[:-4] + '_rasterized_ASC.bil'
    gdalcommand = 'gdal_rasterize -l ' + asc_name[:-4] + ' -a id -tr 15.0 15.0 -te ' + str(ASC_x1) + ' ' + str(
        ASC_y1) + ' ' + str(ASC_x2) + ' ' + str(
        ASC_y2) + ' -ot Float32 -of EHdr ' + geometry_masked_ASC_loc + ' ' + ASC_rasterizedgeometry
    SubProcess(gdalcommand)
    ASC_rasterizedgeometry = Processingpath + '/'+ asc_name[:-4]+ '_rasterized_ASC.bil'


if 'Descending' in Direction_list:
    DSC_rasterizedgeometry = Processingpath +'/'+ dsc_name[:-4] + '_rasterized_DSC.bil'
    gdalcommand = 'gdal_rasterize -l ' + dsc_name[:-4] + ' -a id -tr 15.0 15.0 -te ' + str(DSC_x1) + ' ' + str(
        DSC_y1) + ' ' + str(DSC_x2) + ' ' + str(
        DSC_y2) + ' -ot Float32 -of EHdr ' + geometry_masked_DSC_loc + ' ' + DSC_rasterizedgeometry
    SubProcess(gdalcommand)
    DSC_rasterizedgeometry = Processingpath + '/'+ dsc_name[:-4] + '_rasterized_DSC.bil'
