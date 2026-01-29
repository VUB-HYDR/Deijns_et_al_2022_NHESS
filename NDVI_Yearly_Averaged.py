import pandas as pd
from scipy import signal
from matplotlib import pyplot as plt
#

NDVI_df = pd.read_csv(importpath)
NDVI_df = NDVI_df.dropna(axis=0)
NDVI_df['system:time_start'] = pd.to_datetime(NDVI_df['system:time_start'])
NDVI_df = NDVI_df.set_index(NDVI_df['system:time_start'])
NDVI_df = NDVI_df.drop(labels = 'system:time_start', axis=1)

#linear detrend NDVI values
NDVI_df.insert(1, "Detrend",list(signal.detrend(NDVI_df['NDVI'])), True)

#create index column
NDVI_df['index'] = NDVI_df.index

# plot full NDVI Timeseries
ax = NDVI_df.plot(kind= 'line', x='index', y=NDVI_df.columns[0], color='forestgreen', label = NDVI_df.columns[0],linewidth=1.5)
plt.title('Undisturbed Vegetation patterns ' + area)
plt.xlabel('Date')
plt.ylabel('NDVI')
plt.setp(ax.get_xticklabels(), rotation=45)
plt.tight_layout()


#plot Monthly Averages Seasonality
Y_AVG_D = NDVI_df.groupby([NDVI_df.index.month, NDVI_df.index.day]).mean()
Y_AVG_D = Y_AVG_D.rename_axis(index=["Month","Day"])
Y_AVG_D = Y_AVG_D.reset_index(level=[0,1])
first = Y_AVG_D.columns.get_loc("Month")
Y_AVG_D['Datetime'] = Y_AVG_D.iloc[:,first:first+2].apply(
    lambda x: "-".join(x.astype(str)), axis=1)
Y_AVG_D['Datetime'] = pd.to_datetime(Y_AVG_D['Datetime'], format = '%m-%d', errors='coerce')
Y_AVG_D = Y_AVG_D.set_index(Y_AVG_D['Datetime'])

Y_AVG_D = Y_AVG_D.drop(labels='Month', axis=1)
Y_AVG_D = Y_AVG_D.drop(labels='Day', axis=1)
Y_AVG_D = Y_AVG_D.drop(labels='Datetime', axis=1)
Y_AVG_D = Y_AVG_D.drop(labels='Detrend', axis=1)

#Create index column
Y_AVG_D['index'] = Y_AVG_D.index

#plot seasonal patterns
ax1 = Y_AVG_D.plot(kind= 'line', x='index', y=Y_AVG_D.columns[0], color='forestgreen', label = Y_AVG_D.columns[0],linewidth=1.5)
plt.title('Seasonal Averaged Daily Vegetation patterns ' + area)
plt.xlabel('Date')
plt.ylabel('NDVI')
plt.setp(ax1.get_xticklabels(), rotation=45)
plt.tight_layout()
ticks = [tick.get_text() for tick in ax1.get_xticklabels()]
ticks = pd.to_datetime(ticks).strftime('%b')
ax1.set_xticklabels(ticks)

#plot Monthly Averages Seasonality
Y_AVG_M = NDVI_df.groupby([NDVI_df.index.month, NDVI_df.index.month]).mean()
Y_AVG_M = Y_AVG_M.rename_axis(index=["Month","Day"])
Y_AVG_M = Y_AVG_M.reset_index(level=[0,1])
first = Y_AVG_M.columns.get_loc("Month")
Y_AVG_M['Datetime'] = Y_AVG_M.iloc[:,first:first+2].apply(
    lambda x: "-".join(x.astype(str)), axis=1)
Y_AVG_M['Datetime'] = pd.to_datetime(Y_AVG_M['Datetime'], format = '%m-%d', errors='coerce')
Y_AVG_M = Y_AVG_M.set_index(Y_AVG_M['Datetime'])

Y_AVG_M = Y_AVG_M.drop(labels='Month', axis=1)
Y_AVG_M = Y_AVG_M.drop(labels='Day', axis=1)
Y_AVG_M = Y_AVG_M.drop(labels='Datetime', axis=1)
Y_AVG_M = Y_AVG_M.drop(labels='Detrend', axis=1)

#Create index column
Y_AVG_M['index'] = Y_AVG_M.index

#plot seasonal patterns
ax2 = Y_AVG_M.plot(kind= 'line', x='index', y=Y_AVG_M.columns[0], color='forestgreen', label = Y_AVG_M.columns[0],linewidth=1.5)
plt.title('Seasonal Averaged Monthly Vegetation patterns ' + area)
plt.xlabel('Date')
plt.ylabel('NDVI')
plt.setp(ax2.get_xticklabels(), rotation=45)
plt.tight_layout()
ticks = [tick.get_text() for tick in ax2.get_xticklabels()]
ticks = pd.to_datetime(ticks).strftime('%b')
ax2.set_xticklabels(ticks)

#Resample NDVI
Resampled_M = NDVI_df.resample('M').mean()
B = Resampled_M.rolling(4, min_periods=1).mean()['NDVI']
plt.figure()
ax3 = B.plot(kind= 'line', x=B.index, y=B.values, color='forestgreen', label = 'NDVI',linewidth=1.5)
plt.title('NDVI _ monthly average + movmean=4  ' + area)
plt.xlabel('Date')
plt.ylabel('NDVI')
plt.setp(ax3.get_xticklabels(), rotation=0)
plt.tight_layout()
ticks = [tick.get_text() for tick in ax3.get_xticklabels()]
ticks = pd.to_datetime(ticks).strftime('%Y')
ax3.set_xticklabels(ticks)