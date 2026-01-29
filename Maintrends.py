# you have to run 'SAR_Landslide_Timing.py' for the desired Location.
# Now only Rwenzori, Burundi, Uvira and Karongi NDVI and Rainfall data is available.
# If you want to add, theh following scripts should be changed:
#   1. IMERG_DataAnalysis.py
#   2. NDVI_Yearly_Averaged.py


exec(open('/home/axel/PycharmProjects/PhD_Scripts/Scripts/Basic/IMERG_DataAnalysis.py').read())
plt.close('all')

if LocationInput == 'RWENZORI':
    importpath = r'/home/axel/Documents/Master_MainDisk/Master_Results/3.Data/NDVI/Rwenzori/Landsat8_NDVI_TS_PatchedPolygons_Rwenzori.csv'
    # importpath = r'/home/axel/Documents/Master_MainDisk/Master_Results/3.Data/NDVI/Rwenzori/Rwenzori_S2_L1C.csv'
if LocationInput == 'KARONGI':
    importpath = r'/home/axel/Documents/Master_MainDisk/Master_Results/3.Data/NDVI/Karongi/Landsat8_NDVI_TS_PatchedPolygons.csv'
    # importpath = r'/home/axel/Documents/Master_MainDisk/Master_Results/3.Data/NDVI/Karongi/Karongi_S2_L1C.csv'
if LocationInput == 'UVIRA':
    importpath = r'/home/axel/Documents/Master_MainDisk/Master_Results/3.Data/NDVI/Uvira/NDVI_UVIRA_LANDSAT8_TS_Patches.csv'
    # importpath = r'/home/axel/Documents/Master_MainDisk/Master_Results/3.Data/NDVI/Uvira/Uvira_S2_L1C.csv'
if LocationInput == 'BURUNDI':
    # importpath = r'/home/axel/Documents/Master_MainDisk/Master_Results/3.Data/NDVI/Burundi/Burundi_S2_L1A.csv'
    importpath = r'/home/axel/Documents/Master_MainDisk/Master_Results/3.Data/NDVI/Burundi/Landsat8_NDVI_TS_PatchedPolygons_Burundi.csv' 
# 
exec(open('/home/axel/PycharmProjects/PhD_Scripts/Scripts/Basic/NDVI_Yearly_Averaged.py').read())
plt.close('all')


NDVI = B['2016':'2020']
Rainfall = IMERG_df_Month
Rainfall = Rainfall['2016':'2021']

#non-detrended
# fig,ax = plt.subplots()
# Detrended_DF['Amplitude']['GH']['Ascending']['poly_1']['2016':].plot(ax=ax)
# Detrended_DF['Amplitude']['GH']['Descending']['poly_1']['2016':].plot(ax=ax)
# fig1,ax1 = plt.subplots()
# Detrended_DF['Coherence']['GH']['Ascending']['poly_1']['2016':].plot(ax=ax1)
# Detrended_DF['Coherence']['GH']['Descending']['poly_1']['2016':].plot(ax=ax1)
# fig2,ax2 = plt.subplots()
# ECDF_IntensityCorrelation['Ascending']['poly_1']['2img']['MAX_DIFF']['2016':].plot(ax=ax2)
# ECDF_IntensityCorrelation['Descending']['poly_1']['2img']['MAX_DIFF']['2016':].plot(ax=ax2)
#
# #Detrended
# fig3,ax3 = plt.subplots()
# COH['Ascending']['poly_1'].plot(ax=ax3)
# COH['Descending']['poly_1'].plot(ax=ax3)
#
# fig4,ax4 = plt.subplots()
# AMP_normalized['Ascending']['poly_1'].plot(ax=ax4)
# AMP_normalized['Descending']['poly_1'].plot(ax=ax4)
#


fig = plt.figure(figsize=(4,7))
gs = fig.add_gridspec(6, hspace=0)
axs = gs.subplots(sharex=True, sharey=False)
for satdir in Direction_list:
    Detrended_DF['Coherence']['GH'][satdir]['poly_1']['2016':].plot(ax=axs[3],linewidth=1,color='black')
    axs[3].legend(['Ascending','Descending'])
for satdir in Direction_list:
    COH[satdir]['poly_1']['2016':].plot(ax=axs[4],linewidth=1,color='black')
    axs[4].legend(['Ascending','Descending'])
for satdir in Direction_list:
    Detrended_DF['Amplitude']['GH'][satdir]['poly_1']['2016':].plot(ax=axs[0],color='firebrick',linewidth=1,linestyle='solid')
for satdir in Direction_list:
    AMP_normalized[satdir]['poly_1']['2016':].plot(ax=axs[1],color='firebrick',linewidth=1,linestyle='solid')
for satdir in Direction_list:
    ECDF_IntensityCorrelation[satdir]['poly_1']['2img']['MAX_DIFF']['2016':].plot(ax=axs[2],color='darkgreen',linewidth=1,linestyle='solid')
axs[0].get_legend().remove()
axs[1].get_legend().remove()
axs[3].get_legend().remove()
axs[4].get_legend().remove()

#
# axs[2].get_legend().remove()
axs[2].set_xlabel('Time',fontweight='bold')
axs[3].set_ylabel('Coherence',fontweight='bold')
axs[4].set_ylabel('Detrended \ncoherence',fontweight='bold')
axs[0].set_ylabel('Amplitude',fontweight='bold')
axs[1].set_ylabel('Detrended \namplitude',fontweight='bold')
axs[2].set_ylabel('SAC',fontweight='bold')

# ax_rainfall = axs[2].twinx()
axs[5].bar(Rainfall.index, Rainfall[Rainfall.columns[0]], width=32, color='lightblue', alpha = 0.75)
axs[5].set_xlim([datetime.date(2016, 1, 1), datetime.date(2020, 12, 1)])
axs[5].set_ylabel('Monthly \ncumulative \nrainfall (mm)',fontweight='bold')
ax_ndvi = axs[5].twinx()
ax_ndvi.plot(NDVI,color='grey',alpha=0.75)
ax_ndvi.set_ylabel('NDVI',fontweight='bold')
xticks = pd.date_range(datetime.datetime(2016,1,1), datetime.datetime(2021,1,1), freq='YS')
axs[5].set_xticks(xticks)
axs[5].set_xticklabels(['1-2016','1-2017','1-2018','1-2019','1-2020','1-2021'],fontsize=9)

axs[3].set_ylim([-0.05,0.11])
axs[4].set_ylim([-0.03,0.08])
axs[0].set_ylim([-1.7,1.7])
axs[1].set_ylim([-0.5,0.7])
axs[2].set_ylim([-0.4,0.7])
axs[5].set_ylim([0,320])
ax_ndvi.set_ylim([0.35,0.9]) # for L8
# ax_ndvi.set_ylim([0,0.9]) # for S2
plt.xlabel('Time')
plt.tight_layout()

plt.savefig('/home/axel/Documents/Master_MainDisk/Master_Results/14.Paperfigures/Figure 5/'+LocationInput+'_Maintrends.png',dpi=600)

#%%


exec(open('/home/axel/PycharmProjects/PhD_Scripts/Scripts/Basic/IMERG_DataAnalysis.py').read())
plt.close('all')


if LocationInput == 'RWENZORI':
    # importpath = r'/home/axel/Documents/Master_MainDisk/Master_Results/3.Data/NDVI/Rwenzori/Landsat8_NDVI_TS_PatchedPolygons_Rwenzori.csv'
    importpath = r'/home/axel/Documents/Master_MainDisk/Master_Results/3.Data/NDVI/Rwenzori/Rwenzori_S2_L1C.csv'
if LocationInput == 'KARONGI':
    # importpath = r'/home/axel/Documents/Master_MainDisk/Master_Results/3.Data/NDVI/Karongi/Landsat8_NDVI_TS_PatchedPolygons.csv'
    importpath = r'/home/axel/Documents/Master_MainDisk/Master_Results/3.Data/NDVI/Karongi/Karongi_S2_L1C.csv'
if LocationInput == 'UVIRA':
    # importpath = r'/home/axel/Documents/Master_MainDisk/Master_Results/3.Data/NDVI/Uvira/NDVI_UVIRA_LANDSAT8_TS_Patches.csv'
    importpath = r'/home/axel/Documents/Master_MainDisk/Master_Results/3.Data/NDVI/Uvira/Uvira_S2_L1C.csv'
if LocationInput == 'BURUNDI':
    importpath = r'/home/axel/Documents/Master_MainDisk/Master_Results/3.Data/NDVI/Burundi/Burundi_S2_L1A.csv'
    # importpath = r'/home/axel/Documents/Master_MainDisk/Master_Results/3.Data/NDVI/Burundi/Landsat8_NDVI_TS_PatchedPolygons_Burundi.csv' 



exec(open('/home/axel/PycharmProjects/PhD_Scripts/Scripts/Basic/NDVI_Yearly_Averaged.py').read())
plt.close('all')


NDVI = B['2016':'2020']
Rainfall = IMERG_df_Month
Rainfall = Rainfall['2016':'2021']

#non-detrended
# fig,ax = plt.subplots()
# Detrended_DF['Amplitude']['GH']['Ascending']['poly_1']['2016':].plot(ax=ax)
# Detrended_DF['Amplitude']['GH']['Descending']['poly_1']['2016':].plot(ax=ax)
# fig1,ax1 = plt.subplots()
# Detrended_DF['Coherence']['GH']['Ascending']['poly_1']['2016':].plot(ax=ax1)
# Detrended_DF['Coherence']['GH']['Descending']['poly_1']['2016':].plot(ax=ax1)
# fig2,ax2 = plt.subplots()
# ECDF_IntensityCorrelation['Ascending']['poly_1']['2img']['MAX_DIFF']['2016':].plot(ax=ax2)
# ECDF_IntensityCorrelation['Descending']['poly_1']['2img']['MAX_DIFF']['2016':].plot(ax=ax2)
#
# #Detrended
# fig3,ax3 = plt.subplots()
# COH['Ascending']['poly_1'].plot(ax=ax3)
# COH['Descending']['poly_1'].plot(ax=ax3)
#
# fig4,ax4 = plt.subplots()
# AMP_normalized['Ascending']['poly_1'].plot(ax=ax4)
# AMP_normalized['Descending']['poly_1'].plot(ax=ax4)
#


fig = plt.figure(figsize=(4,7))
gs = fig.add_gridspec(6, hspace=0)
axs = gs.subplots(sharex=True, sharey=False)
for satdir in Direction_list:
    Detrended_DF['Coherence']['GH'][satdir]['poly_1']['2016':].plot(ax=axs[3],linewidth=1,color='black')
    axs[3].legend(['Ascending','Descending'])
for satdir in Direction_list:
    COH[satdir]['poly_1']['2016':].plot(ax=axs[4],linewidth=1,color='black')
    axs[4].legend(['Ascending','Descending'])
for satdir in Direction_list:
    Detrended_DF['Amplitude']['GH'][satdir]['poly_1']['2016':].plot(ax=axs[0],color='firebrick',linewidth=1,linestyle='solid')
for satdir in Direction_list:
    AMP_normalized[satdir]['poly_1']['2016':].plot(ax=axs[1],color='firebrick',linewidth=1,linestyle='solid')
for satdir in Direction_list:
    ECDF_IntensityCorrelation[satdir]['poly_1']['2img']['MAX_DIFF']['2016':].plot(ax=axs[2],color='darkgreen',linewidth=1,linestyle='solid')
axs[0].get_legend().remove()
axs[1].get_legend().remove()
axs[3].get_legend().remove()
axs[4].get_legend().remove()

#
# axs[2].get_legend().remove()
axs[2].set_xlabel('Time',fontweight='bold')
axs[3].set_ylabel('Coherence',fontweight='bold')
axs[4].set_ylabel('Detrended \ncoherence',fontweight='bold')
axs[0].set_ylabel('Amplitude',fontweight='bold')
axs[1].set_ylabel('Detrended \namplitude',fontweight='bold')
axs[2].set_ylabel('SAC',fontweight='bold')

# ax_rainfall = axs[2].twinx()
axs[5].bar(Rainfall.index, Rainfall[Rainfall.columns[0]], width=32, color='lightblue', alpha = 0.75)
axs[5].set_xlim([datetime.date(2016, 1, 1), datetime.date(2020, 12, 1)])
axs[5].set_ylabel('Monthly \ncumulative \nrainfall (mm)',fontweight='bold')
ax_ndvi = axs[5].twinx()
ax_ndvi.plot(NDVI,color='grey',alpha=0.75)
ax_ndvi.set_ylabel('NDVI',fontweight='bold')
xticks = pd.date_range(datetime.datetime(2016,1,1), datetime.datetime(2021,1,1), freq='YS')
axs[5].set_xticks(xticks)
axs[5].set_xticklabels(['1-2016','1-2017','1-2018','1-2019','1-2020','1-2021'],fontsize=9)

axs[3].set_ylim([-0.05,0.11])
axs[4].set_ylim([-0.03,0.08])
axs[0].set_ylim([-1.7,1.7])
axs[1].set_ylim([-0.5,0.7])
axs[2].set_ylim([-0.4,0.7])
axs[5].set_ylim([0,320])
# ax_ndvi.set_ylim([0.35,0.9]) # for L8
ax_ndvi.set_ylim([0,0.9]) # for S2
plt.xlabel('Time')
plt.tight_layout()

plt.savefig('/home/axel/Documents/Master_MainDisk/Master_Results/14.Paperfigures/Figure 5/'+LocationInput+'_Maintrends_2.png',dpi=600)


