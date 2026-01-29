Distributions= {}
Distributions_SAC = {}
if Coherence_data == 'Yes':
    if 'Ascending' in Direction_list and 'Descending' in Direction_list:
        satellites= ['COH_Concat_ASC_norm','COH_Concat_DSC_norm']
    if 'Ascending' in Direction_list and not 'Descending' in Direction_list:
        satellites = ['COH_Concat_ASC_norm']
    if 'Ascending' not in Direction_list and 'Descending' in Direction_list:
        satellites = ['COH_Concat_DSC_norm']
    for sat in satellites:
        if sat == 'COH_Concat_ASC_norm':
            satellite = 'Ascending'
        if sat == 'COH_Concat_DSC_norm':
            satellite = 'Descending'
        Distributions[satellite] = Diff_Timing[sat]['ordinal'].value_counts()
if SAC_data == 'Yes':
    for sat in Direction_list:
        Distributions_SAC[sat] = Diff_Timing_SAC[sat]['ordinal'].value_counts()
from matplotlib import pyplot as plt
import pandas as pd
import datetime as dt


if Coherence_data == 'Yes':
    satellites= Direction_list
    Distributions_df = {}
    i=0
    for sat in satellites:
        Distributions_df[sat] = pd.DataFrame(Distributions[sat])
        Distributions_df[sat] = Distributions_df[sat].sort_index()
        Distributions_df[sat]['ordinaltime'] = Distributions_df[sat].index
        Distributions_df[sat]['ordinaltime'] = Distributions_df[sat]['ordinaltime'].apply(dt.datetime.fromordinal)
        Distributions_df[sat].index = Distributions_df[sat]['ordinaltime']
        Distributions_df[sat] = Distributions_df[sat].drop(columns='ordinaltime')
        if i == 0:
            ax = Distributions_df[sat].plot(legend=False,marker='o')
        else:
            Distributions_df[sat].plot(legend=False, marker='o',ax=ax)
        i += 1
        plt.gcf()
        plt.xlabel('Date')
        plt.ylabel('Number of estimations')
        plt.legend(['Ascending','Descending'])
        plt.title('Coherence Date distribution')

if SAC_data == 'Yes':
    satellites= Direction_list
    Distributions_df = {}
    i=0
    for sat in satellites:
        Distributions_df[sat] = pd.DataFrame(Distributions_SAC[sat])
        Distributions_df[sat] = Distributions_df[sat].sort_index()
        Distributions_df[sat]['ordinaltime'] = Distributions_df[sat].index
        Distributions_df[sat]['ordinaltime'] = Distributions_df[sat]['ordinaltime'].apply(dt.datetime.fromordinal)
        Distributions_df[sat].index = Distributions_df[sat]['ordinaltime']
        Distributions_df[sat] = Distributions_df[sat].drop(columns='ordinaltime')
        if i == 0:
            ax = Distributions_df[sat].plot(legend=False,marker='o')
        else:
            Distributions_df[sat].plot(legend=False, marker='o',ax=ax)
        i += 1
        plt.gcf()
        plt.xlabel('Date')
        plt.ylabel('Number of estimations')
        plt.legend(['Ascending','Descending'])
        plt.title('Spatial Amplitude Correlation Date distribution')




# if SAC_data == 'Yes':
#     plt.savefig('/home/axel/Documents/Master_MainDisk/Master_Results/10.PaperFiguresIDEAS/Distributions/TIMINGDIST/SAC/'+LocationInput+'.png')
# if Coherence_data == 'Yes':
#     plt.savefig('/home/axel/Documents/Master_MainDisk/Master_Results/10.PaperFiguresIDEAS/Distributions/TIMINGDIST/COH/'+LocationInput+'.png')
# if Amplitude_data == 'Yes':
#     plt.savefig('/home/axel/Documents/Master_MainDisk/Master_Results/10.PaperFiguresIDEAS/Distributions/TIMINGDIST/AMP/' + LocationInput + '.png')
