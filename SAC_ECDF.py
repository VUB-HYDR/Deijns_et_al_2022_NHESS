IC_DF = IntensityCorrelation.copy()

import numpy as np
import pandas as pd
if 'Ascending' in Direction_list:
    namelist = list(IC_DF['Ascending'].keys())
else:
    namelist = list(IC_DF['Descending'].keys())
averageimage = ['1img', '2img', '3img']


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


ECDF_DF = {}
ECDF_DF_diff = {}
normallydist = {}
for Sat_Direction in Direction_list:
    ECDF_DF[Sat_Direction] = {}
    ECDF_DF_diff[Sat_Direction] = {}
for Sat_Direction in Direction_list:
    for poly in namelist_sat[Sat_Direction]:
        ECDF_DF[Sat_Direction][poly] = {}
        ECDF_DF_diff[Sat_Direction][poly] = {}
        for run in averageimage:
            ECDF_DF_diff[Sat_Direction][poly][run] = pd.DataFrame()
            normallydist[run] = {}

## ECDF
def ecdf(data):
    """Compute ECDF for a one-dimensional array of measurements."""
    # Number of data points: n
    n = len(data)
    # x-data for the ECDF: x
    x = np.sort(data)
    # y-data for the ECDF: y
    y = np.arange(1, n + 1) / n
    return x, y
moving_mean = moving_mean_ECDF
moving_mean_choice =  '_moving mean_4' #'_moving mean_4' #moving_mean #
type = 'Landslides'
if 'Ascending' in Direction_list:
    runlist = list(IC_DF['Ascending']['poly_1'])
if 'Descending' in Direction_list:
    runlist = list(IC_DF['Descending']['poly_1'])
run_1 = [run for run in runlist if run[0] == '1']
run_2 = [run for run in runlist if run[0] == '2']
run_3 = [run for run in runlist if run[0] == '3']

for Sat_Direction in Direction_list:
    print('')
    iteration=1
    for poly in namelist_sat[Sat_Direction]:
        print(Sat_Direction + ' poly (' +str(iteration)+ '/'+str(len(namelist_sat[Sat_Direction]))+')',end="\r")
        # print(poly)
        # n = int(len(IC_DF[Sat_Direction][poly]) /3)  # Number of colors
        # new_colors = [plt.get_cmap('jet')(1. * i / n) for i in range(n)]
        # color_iterator = iter(new_colors)
        for run in IC_DF[Sat_Direction][poly]:
            if run in run_1:
                if run == run_1[0]:
                    # print(run)
                    # fig, ax = plt.subplots(figsize= (9,6))
                    # ax.set_title(poly + '\n' + Sat_Direction+ '\n'+ run[0:4])
                    # title = exportpath + '/' + type + '_' + poly + '_' +run[0:4]+ '_' + mm_name + '_' + Sat_Direction + '.png'
                    runmm = run + moving_mean
                    x, y = ecdf(IC_DF[Sat_Direction][poly][run][runmm])
                    ECDF_DF[Sat_Direction][poly][run[0:4]] = pd.DataFrame(index=y)
                runmm = run + moving_mean
                x, y = ecdf(IC_DF[Sat_Direction][poly][run][runmm])
                runningDF = pd.DataFrame({run[6:9]:x},index=y)
                ECDF_DF[Sat_Direction][poly][run[0:4]] = ECDF_DF[Sat_Direction][poly][run[0:4]].merge(runningDF, left_index=True, right_index=True, how='inner')
                normallydist['1img'] = pd.DataFrame(np.sort(np.random.normal(ECDF_DF[Sat_Direction][poly][run[0:4]].mean().mean(),ECDF_DF[Sat_Direction][poly][run[0:4]].std().mean(),size=len(ECDF_DF[Sat_Direction][poly][run[0:4]]))))
                normallydist['1img'].index = ECDF_DF[Sat_Direction][poly][run[0:4]].index
                    # _ = plt.plot(x, y, color= next(color_iterator))
                # _ = plt.xlabel('IC')
                # _ = plt.ylabel('ECDF')
                # _ = plt.legend(run_1, bbox_to_anchor=(1.05, 1), loc='upper left')
                # _ = plt.subplots_adjust(right=0.8)
                # plt.savefig(title)
        # plt.close('all')
        # n = int(len(IC_DF[Sat_Direction][poly]) / 3)  # Number of colors
        # new_colors = [plt.get_cmap('jet')(1. * i / n) for i in range(n)]
        # color_iterator = iter(new_colors)
        for run in IC_DF[Sat_Direction][poly]:
            if run in run_2:
                if run == run_2[0]:
                    # print(run)
                    # fig, ax = plt.subplots(figsize=(9, 6))
                    # ax.set_title(poly + '\n' + Sat_Direction + '\n' + run[0:4])
                    # title = exportpath + '/' + type + '_' + poly + '_' + run[0:4] + '_' + mm_name + '_' + Sat_Direction + '.png'
                    runmm = run + moving_mean
                    x, y = ecdf(IC_DF[Sat_Direction][poly][run][runmm])
                    ECDF_DF[Sat_Direction][poly][run[0:4]] = pd.DataFrame(index=y)
                runmm = run + moving_mean
                x, y = ecdf(IC_DF[Sat_Direction][poly][run][runmm])
                runningDF = pd.DataFrame({run[6:9]: x}, index=y)
                np.random.seed(1)
                ECDF_DF[Sat_Direction][poly][run[0:4]] = ECDF_DF[Sat_Direction][poly][run[0:4]].merge(runningDF, left_index=True,right_index=True, how='inner')
                normallydist['2img']  = pd.DataFrame(np.sort(np.random.normal(ECDF_DF[Sat_Direction][poly][run[0:4]].mean().mean(),ECDF_DF[Sat_Direction][poly][run[0:4]].std().mean(),size=len(ECDF_DF[Sat_Direction][poly][run[0:4]]))))
                normallydist['2img'].index = ECDF_DF[Sat_Direction][poly][run[0:4]].index
                # _ = plt.plot(x, y, color= next(color_iterator))
                # _ = plt.xlabel('IC')
                # _ = plt.ylabel('ECDF')
                # _ = plt.legend(run_2, bbox_to_anchor=(1.05, 1), loc='upper left')
                # _ = plt.subplots_adjust(right=0.8)
                # plt.savefig(title)
        # plt.close('all')
        # n = int(len(IC_DF[Sat_Direction][poly]) / 3)  # Number of colors
        # new_colors = [plt.get_cmap('jet')(1. * i / n) for i in range(n)]
        # color_iterator = iter(new_colors)
        for run in IC_DF[Sat_Direction][poly]:
            if run in run_3:
                if run == run_3[0]:
                    # print(run)
                    # fig, ax = plt.subplots(figsize=(9, 6))
                    # ax.set_title(poly + '\n' + Sat_Direction+ '\n'+ run[0:4])
                    # title = exportpath + '/' + type + '_' + poly + '_' + run[0:4] + '_' + mm_name + '_' + Sat_Direction + '.png'
                    runmm = run + moving_mean
                    x, y = ecdf(IC_DF[Sat_Direction][poly][run][runmm])
                    ECDF_DF[Sat_Direction][poly][run[0:4]] = pd.DataFrame(index=y)
                runmm = run + moving_mean
                x, y = ecdf(IC_DF[Sat_Direction][poly][run][runmm])
                runningDF = pd.DataFrame({run[6:9]: x}, index=y)
                ECDF_DF[Sat_Direction][poly][run[0:4]] = ECDF_DF[Sat_Direction][poly][run[0:4]].merge(runningDF,left_index=True,right_index=True,how='inner')
                normallydist['3img']  = pd.DataFrame(np.sort(np.random.normal(ECDF_DF[Sat_Direction][poly][run[0:4]].mean().mean(),ECDF_DF[Sat_Direction][poly][run[0:4]].std().mean(),size=len(ECDF_DF[Sat_Direction][poly][run[0:4]]))))
                normallydist['3img'].index = ECDF_DF[Sat_Direction][poly][run[0:4]].index

                # _ = plt.plot(x, y, color= next(color_iterator))
                # _ = plt.xlabel('IC')
                # _ = plt.ylabel('ECDF')
                # _ = plt.legend(run_3, bbox_to_anchor=(1.05, 1), loc='upper left')
                # _ = plt.subplots_adjust(right=0.8)
                # plt.savefig(title)

        # plt.close('all')
        iteration += 1
# find highest standard deviation
# ECDF_DF['Descending']['poly_1']['2img'].std()[ECDF_DF['Descending']['poly_1']['2img'].std() == ECDF_DF['Descending']['poly_1']['2img'].std().max()]
# ECDF_DF['Ascending']['poly_1']['3img'].std()[ECDF_DF['Ascending']['poly_1']['3img'].std() == ECDF_DF['Ascending']['poly_1']['3img'].std().max()]
    for poly in namelist_sat[Sat_Direction]:
        for img in averageimage:
            for run in runlist:
                B = abs(abs(ECDF_DF[Sat_Direction][poly][img][run[6:9]]) - normallydist[img][0])
                ECDF_DF_diff[Sat_Direction][poly][img][run[6:9]] = B


# if df_geometries['Name'][0] != 'Karongi_Event':
runlist = ['2img', '3img']

ECDF_IntensityCorrelation = {}
for Sat_Direction in Direction_list:
    ECDF_IntensityCorrelation[Sat_Direction] = {}
    for poly in namelist_sat[Sat_Direction]:
        ECDF_IntensityCorrelation[Sat_Direction][poly]  = {}
        for run in runlist:
            ECDF_IntensityCorrelation[Sat_Direction][poly] [run] = {}
#
# if df_geometries['Name'][0] != 'Karongi_Event':
#     for poly in namelist:
#         for run in runlist:
#             # print(poly)
#             # print(run)
#             # print('Descending')
#             # print((ECDF_DF['Descending'][poly][run].std()[abs(ECDF_DF['Descending'][poly][run].std()) == abs(ECDF_DF['Descending'][poly][run].std()).max()]).index[0], 'std')
#             # print((ECDF_DF['Descending'][poly][run].var()[abs(ECDF_DF['Descending'][poly][run].var()) == abs(ECDF_DF['Descending'][poly][run].var()).max()]).index[0], 'variance')
#             # print((ECDF_DF['Descending'][poly][run].quantile(q=0.25)[abs(ECDF_DF['Descending'][poly][run].quantile(q=0.25)) == abs(ECDF_DF['Descending'][poly][run].quantile(q=0.25)).max()]).index[0], 'quantile 0.25')
#             # print((ECDF_DF['Descending'][poly][run].quantile(q=0.75)[abs(ECDF_DF['Descending'][poly][run].quantile(q=0.75)) == abs(ECDF_DF['Descending'][poly][run].quantile(q=0.75)).max()]).index[0], 'quantile 0.75')
#             # # print(ECDF_DF['Ascending'][poly][run].mean()[abs(ECDF_DF['Ascending'][poly][run].mean()) == abs(ECDF_DF['Ascending'][poly][run].mean()).max()])
#             # print('Ascending')
#             # print((ECDF_DF['Ascending'][poly][run].std()[abs(ECDF_DF['Ascending'][poly][run].std()) == abs(ECDF_DF['Ascending'][poly][run].std()).max()]).index[0], 'std')
#             # print((ECDF_DF['Ascending'][poly][run].var()[abs(ECDF_DF['Ascending'][poly][run].var()) == abs(ECDF_DF['Ascending'][poly][run].var()).max()]).index[0], 'variance')
#             # print((ECDF_DF['Ascending'][poly][run].quantile(q=0.25)[abs(ECDF_DF['Ascending'][poly][run].quantile(q=0.25)) == abs(ECDF_DF['Ascending'][poly][run].quantile(q=0.25)).max()]).index[0], 'quantile 0.25')
#             # print((ECDF_DF['Ascending'][poly][run].quantile(q=0.75)[abs(ECDF_DF['Ascending'][poly][run].quantile(q=0.75)) == abs(ECDF_DF['Ascending'][poly][run].quantile(q=0.75)).max()]).index[0], 'quantile 0.75')
#
#             # if polyaspect[poly] < 180:
#                 #DESCENDING
#                 # plot highest std
#                 # plt.figure()
#                 maxstd_DSC_STD = ECDF_DF['Descending'][poly][run].std()[abs(ECDF_DF['Descending'][poly][run].std()) == abs(ECDF_DF['Descending'][poly][run].std().max())].index[0]
#                 # IntensityCorrelation['Descending'][poly][run + '__' +  maxstd_DSC_STD][run + '__' + maxstd_DSC_STD+'_moving mean_4'].plot(color = 'black')
#
#                 # maxstd_DSC = ECDF_DF['Descending'][poly][run].var()[abs(ECDF_DF['Descending'][poly][run].var()) == abs(ECDF_DF['Descending'][poly][run].var().max())].index[0]
#                 # IntensityCorrelation['Descending'][poly][run + '__' +  maxstd_DSC][run + '__' + maxstd_DSC+'_moving mean_4'].plot(color = 'green')
#
#                 # # plot highest quantile 0.25
#                 # maxstd_DSC = ECDF_DF['Descending'][poly][run].quantile(q=0.25)[abs(ECDF_DF['Descending'][poly][run].quantile(q=0.25)) == abs(ECDF_DF['Descending'][poly][run].quantile(q=0.25).max())].index[0]
#                 # IntensityCorrelation['Descending'][poly][run + '__' +  maxstd_DSC][run + '__' + maxstd_DSC+'_moving mean_4'].plot(linestyle = 'dashed')
#
#                 # plot highest quantile 0.75
#                 maxstd_DSC_QUAN = ECDF_DF['Descending'][poly][run].quantile(q=0.75)[abs(ECDF_DF['Descending'][poly][run].quantile(q=0.75)) == abs(ECDF_DF['Descending'][poly][run].quantile(q=0.75).max())].index[0]
#                 # IntensityCorrelation['Descending'][poly][run + '__' +  maxstd_DSC_QUAN][run + '__' + maxstd_DSC_QUAN+'_moving mean_4'].plot(linestyle = 'dotted', color = 'red')
#
#                 A = pd.DataFrame(IntensityCorrelation['Descending'][poly][run + '__' + maxstd_DSC_STD][run + '__' + maxstd_DSC_STD + '_moving mean_4'])
#                 A.columns = ['STD']
#                 A['QUANTILE'] = (pd.DataFrame(IntensityCorrelation['Descending'][poly][run + '__' + maxstd_DSC_QUAN][run + '__' + maxstd_DSC_QUAN + '_moving mean_4']))
#                 ECDF_IntensityCorrelation[poly][run] = A
#
#                 # plt.legend(['STD','Quantile 0.75'])
#                 # titlename = poly + ' Descending ' + run
#                 # plt.title(titlename)
#                 # plt.savefig('/home/axel/Documents/Master_MainDisk/Master_Results/5. Landslide Timing/Landside Timing/Figures/' + titlename + '.png')
#             else:
#                 #ASCENDING
#                 # plt.figure()
#                 maxstd_ASC_STD = ECDF_DF['Ascending'][poly][run].std()[abs(ECDF_DF['Ascending'][poly][run].std()) == abs(ECDF_DF['Ascending'][poly][run].std().max())].index[0]
#                 # IntensityCorrelation['Ascending'][poly][run + '__' + maxstd_ASC_STD][run + '__' + maxstd_ASC_STD+'_moving mean_4'].plot(color='black')
#
#                 # maxstd_ASC = ECDF_DF['Ascending'][poly][run].var()[abs(ECDF_DF['Ascending'][poly][run].var()) == abs(ECDF_DF['Ascending'][poly][run].var().max())].index[0]
#                 # IntensityCorrelation['Ascending'][poly][run + '__' + maxstd_ASC][run + '__' + maxstd_ASC + '_moving mean_4'].plot(color='green')
#                 #
#                 # maxstd_ASC = ECDF_DF['Ascending'][poly][run].quantile(q=0.25)[abs(ECDF_DF['Ascending'][poly][run].quantile(q=0.25)) == abs(ECDF_DF['Ascending'][poly][run].quantile(q=0.25).max())].index[0]
#                 # IntensityCorrelation['Ascending'][poly][run + '__' + maxstd_ASC][run + '__' + maxstd_ASC+'_moving mean_4'].plot(linestyle = 'dashed')
#
#                 maxstd_ASC_QUAN = ECDF_DF['Ascending'][poly][run].quantile(q=0.75)[abs(ECDF_DF['Ascending'][poly][run].quantile(q=0.75)) == abs(ECDF_DF['Ascending'][poly][run].quantile(q=0.75).max())].index[0]
#                 # IntensityCorrelation['Ascending'][poly][run + '__' + maxstd_ASC_QUAN][run + '__' + maxstd_ASC_QUAN+'_moving mean_4'].plot(linestyle = 'dotted', color = 'red')
#
#                 A = pd.DataFrame(IntensityCorrelation['Ascending'][poly][run + '__' + maxstd_ASC_STD][run + '__' + maxstd_ASC_STD + '_moving mean_4'])
#                 A.columns = ['STD']
#                 A['QUANTILE'] = (pd.DataFrame(IntensityCorrelation['Ascending'][poly][run + '__' + maxstd_ASC_QUAN][run + '__' + maxstd_ASC_QUAN + '_moving mean_4']))
#                 ECDF_IntensityCorrelation[poly][run] = A
#
#                 # plt.legend(['STD','Quantile 0.75'])
#                 # titlename = poly + ' Ascending ' + run
#                 # plt.title(titlename)
#                 # plt.savefig('/home/axel/Documents/Master_MainDisk/Master_Results/5. Landslide Timing/Landside Timing/Figures/' + titlename + '.png')
#             ECDF_IntensityCorrelation[poly][run] = ECDF_IntensityCorrelation[poly][run].dropna()
# else:
if 'Descending' in Direction_list:
    teller = 0
    dscpolylist=[]
    for poly in namelist_sat['Descending']:
        # plt.figure()
        if ECDF_DF['Descending'][poly]['2img'].isnull().values.any() == True:
            teller += 1
            # print('Descending poly: ('+str(teller)+'/'+str(len(namelist_sat['Descending']))+')',end="\r")
            dscpolylist.append(poly)
            continue
        else:
            for run in runlist:
                maxstd_DSC_STD = ECDF_DF['Descending'][poly][run].std()[abs(ECDF_DF['Descending'][poly][run].std()) == abs(ECDF_DF['Descending'][poly][run].std().max())].index[0]
                # IntensityCorrelation['Descending'][poly][run + '__' + maxstd_DSC_STD][
                #     run + '__' + maxstd_DSC_STD + '_moving mean_4'].plot(color='black')

                # maxstd_DSC = ECDF_DF['Descending'][poly][run].var()[abs(ECDF_DF['Descending'][poly][run].var()) == abs(ECDF_DF['Descending'][poly][run].var().max())].index[0]
                # IntensityCorrelation['Descending'][poly][run + '__' +  maxstd_DSC][run + '__' + maxstd_DSC+'_moving mean_4'].plot(color = 'green')

                # # plot highest quantile 0.25
                # maxstd_DSC = ECDF_DF['Descending'][poly][run].quantile(q=0.25)[abs(ECDF_DF['Descending'][poly][run].quantile(q=0.25)) == abs(ECDF_DF['Descending'][poly][run].quantile(q=0.25).max())].index[0]
                # IntensityCorrelation['Descending'][poly][run + '__' +  maxstd_DSC][run + '__' + maxstd_DSC+'_moving mean_4'].plot(linestyle = 'dashed')

                # plot highest quantile 0.75
                maxstd_DSC_QUAN = ECDF_DF['Descending'][poly][run].quantile(q=0.75)[
                    abs(ECDF_DF['Descending'][poly][run].quantile(q=0.75)) == abs(
                        ECDF_DF['Descending'][poly][run].quantile(q=0.75).max())].index[0]
                # IntensityCorrelation['Descending'][poly][run + '__' + maxstd_DSC_QUAN][
                #     run + '__' + maxstd_DSC_QUAN + '_moving mean_4'].plot(linestyle='dotted', color='red')

                maxdiff_DSC = (ECDF_DF_diff['Descending'][poly][run].sum()[ECDF_DF_diff['Descending'][poly][run].sum() == ECDF_DF_diff['Descending'][poly][run].sum().max()]).index[0]

                A = pd.DataFrame(IntensityCorrelation['Descending'][poly][run + '__' + maxstd_DSC_STD][
                                     run + '__' + maxstd_DSC_STD + moving_mean_choice])
                A.columns = ['STD']
                A['QUANTILE'] = (pd.DataFrame(IntensityCorrelation['Descending'][poly][run + '__' + maxstd_DSC_QUAN][
                                                  run + '__' + maxstd_DSC_QUAN + moving_mean_choice]))

                A['MAX_DIFF'] = (pd.DataFrame(IntensityCorrelation['Descending'][poly][run + '__' + maxdiff_DSC][
                                                  run + '__' + maxdiff_DSC + moving_mean_choice]))

                ECDF_IntensityCorrelation['Descending'][poly][run] = A

                # plt.legend(['STD', 'Quantile 0.75'])
                # titlename = poly + ' Descending ' + run
                # plt.title(titlename)

    # for poly in namelist:
    #     fig, ax = plt.subplots()
    #     for run in runlist:
    #         ECDF_IntensityCorrelation['Descending'][poly][run].plot(ax=ax)
    #         plt.title(poly + ' Descending')
    #     plt.legend(['2img_STD', '2img_QUANTILE', '3img_STD', '3img_QUANTILE'])

            # plt.savefig('/home/axel/Documents/Master_MainDisk/Master_Results/5. Landslide Timing/Landside Timing/Figures/' + titlename + '.png')
    print('')
if 'Ascending' in Direction_list:
    teller_asc = 0
    ascpolylist=[]
    for poly in namelist_sat['Ascending']:
        if ECDF_DF['Ascending'][poly]['2img'].isnull().values.any() == True:
            teller_asc += 1
            # print('Ascending poly: ('+str(teller_asc)+'/'+str(len(namelist_sat['Ascending']))+')',end="\r")
            ascpolylist.append(poly)
            continue
        else:
            for run in runlist:
                # ASCENDING
                maxstd_ASC_STD = ECDF_DF['Ascending'][poly][run].std()[
                    abs(ECDF_DF['Ascending'][poly][run].std()) == abs(ECDF_DF['Ascending'][poly][run].std().max())].index[0]
                # IntensityCorrelation['Ascending'][poly][run + '__' + maxstd_ASC_STD][
                #     run + '__' + maxstd_ASC_STD + '_moving mean_4'].plot(color='black')

                # maxstd_ASC = ECDF_DF['Ascending'][poly][run].var()[abs(ECDF_DF['Ascending'][poly][run].var()) == abs(ECDF_DF['Ascending'][poly][run].var().max())].index[0]
                # IntensityCorrelation['Ascending'][poly][run + '__' + maxstd_ASC][run + '__' + maxstd_ASC + '_moving mean_4'].plot(color='green')
                #
                # maxstd_ASC = ECDF_DF['Ascending'][poly][run].quantile(q=0.25)[abs(ECDF_DF['Ascending'][poly][run].quantile(q=0.25)) == abs(ECDF_DF['Ascending'][poly][run].quantile(q=0.25).max())].index[0]
                # IntensityCorrelation['Ascending'][poly][run + '__' + maxstd_ASC][run + '__' + maxstd_ASC+'_moving mean_4'].plot(linestyle = 'dashed')

                maxstd_ASC_QUAN = ECDF_DF['Ascending'][poly][run].quantile(q=0.75)[
                    abs(ECDF_DF['Ascending'][poly][run].quantile(q=0.75)) == abs(
                        ECDF_DF['Ascending'][poly][run].quantile(q=0.75).max())].index[0]
                # IntensityCorrelation['Ascending'][poly][run + '__' + maxstd_ASC_QUAN][
                #     run + '__' + maxstd_ASC_QUAN + '_moving mean_4'].plot(linestyle='dotted', color='red')

                maxdiff_ASC = (ECDF_DF_diff['Ascending'][poly][run].sum()[
                    ECDF_DF_diff['Ascending'][poly][run].sum() == ECDF_DF_diff['Ascending'][poly][run].sum().max()]).index[0]

                A = pd.DataFrame(IntensityCorrelation['Ascending'][poly][run + '__' + maxstd_ASC_STD][
                                     run + '__' + maxstd_ASC_STD + moving_mean_choice])
                A.columns = ['STD']
                A['QUANTILE'] = (pd.DataFrame(IntensityCorrelation['Ascending'][poly][run + '__' + maxstd_ASC_QUAN][
                                                  run + '__' + maxstd_ASC_QUAN + moving_mean_choice]))
                A['MAX_DIFF'] = (pd.DataFrame(IntensityCorrelation['Ascending'][poly][run + '__' + maxdiff_ASC][
                                                  run + '__' + maxdiff_ASC + moving_mean_choice]))

                ECDF_IntensityCorrelation['Ascending'][poly][run] = A

            # plt.legend(['STD', 'Quantile 0.75'])
            # titlename = poly + ' Ascending ' + run
            # plt.title(titlename)

    # for poly in namelist:
    #     fig, ax = plt.subplots()
    #     for run in runlist:
    #         ECDF_IntensityCorrelation['Ascending'][poly][run].plot(ax=ax)
    #         plt.title(poly + 'Ascending')
    #     plt.legend(['2img_STD', '2img_QUANTILE', '3img_STD', '3img_QUANTILE'])
    #          # plt.savefig('/home/axel/Documents/Master_MainDisk/Master_Results/5. Landslide Timing/Landside Timing/Figures/' + titlename + '.png')
    print('')
    print('Number of excluded polygon DSC: ' +str(teller))
    print('Number of excluded polygon ASC: ' +str(teller_asc))


for satdir in Direction_list:
    print('')
    print(satdir)
    print('Before: ' + str(len(ECDF_IntensityCorrelation[satdir])))
    if satdir == 'Ascending':
        for key in ascpolylist:
          del ECDF_IntensityCorrelation[satdir][key]
        print('After: ' + str(len(ECDF_IntensityCorrelation[satdir])))
    else:
        for key in dscpolylist:
          del ECDF_IntensityCorrelation[satdir][key]
        print('After: ' + str(len(ECDF_IntensityCorrelation[satdir])))

for Sat_Direction in Direction_list:
    for poly in ECDF_IntensityCorrelation[Sat_Direction]:
        for run in runlist:
            ECDF_IntensityCorrelation[Sat_Direction][poly][run] = ECDF_IntensityCorrelation[Sat_Direction][poly][run].dropna()

# plt.close('all')