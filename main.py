import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

def faster(df):
        s = df["hsh"].str.split(', ', expand=True).stack()
        i = s.index.get_level_values(0)
        df2 = df.loc[i].copy()
        df2["hsh"] = s.values
        df2.drop_duplicates(subset=['time','hsh'], keep='first', inplace=True)
        return df2

d= pd.read_csv('smplcmpostn.txt', header=None, sep="\t")
df1 = pd.read_csv('sjune', header=None, sep="\t")
df1.columns=["time","user","tweets"]
df2=df1.tweets.str.findall(r'#.*?(?=\s|$)')
df=pd.concat([df1.time, df2], axis=1)
df.columns=('time','hsh')
df.hsh=df['hsh'].apply(lambda x: ', '.join(x))
df=faster(df)
df['Max'] = d.idxmax(axis=1)
d1=pd.concat([df.Max, df1.user, df1.tweets], axis=1)
d1=d1[~d1.index.duplicated()]


t_index = pd.DatetimeIndex(start='2009-06-01', end='2009-06-30 23:00:00', freq='1h')

#--------------------------------------------------------------------------------------------
#//create time series dataframe(df3):
appended_data = []

with open ("hsh.txt", 'r') as f:
        strings=f.read().split('\n')

for s in strings:
        tstamp=df.loc[df['hsh']== s, ['time']]
        tstamp['time'] = pd.to_datetime(tstamp['time'])
        tseries = tstamp.resample('1h', on='time').count().reindex(t_index).fillna(0)
        # store DataFrame in list
        appended_data.append(tseries)

df3 = pd.concat(appended_data, axis=1)
df3.columns=strings
df3.drop(df3.columns[len(df3.columns)-1], axis=1, inplace=True)
df3.to_csv(r'df3.txt', sep='\t')
#--------------------------------------------------------------------------------------------

tweetcount=[]
usercount=[]
added=[]
maxed=[]

for i in range(len(d.columns)):
	k= df.loc[df['Max']== i, 'hsh']
	k= k.str.cat(sep=',')
	l=k.split(',')          #l contains hashtags of a cluster
	l= list(set(l))
	l = set(strings).intersection(l)
	data = df3[df3.columns.intersection(l)]
	Ad=data.sum(axis=1)           #df3[l] dataframe of a single Cluster
	added.append(Ad)
	Mx=data.apply(max, axis=1)
	maxed.append(Mx)
	tc= d1.loc[d1['Max']== i, 'tweets']
	tcl= len(tc)
	uc= d1.loc[d1['Max']== i, 'user']
	uc=uc[~uc.duplicated()]
	ucl= len(uc)
	tweetcount.append(tcl)
	usercount.append(ucl)

df4 = pd.concat(added, axis=1)    #df4 contains summed columns for all topics 
df5 = pd.concat(maxed, axis=1)    #df5 contains maximum values for all topics 
df6 = pd.DataFrame({'tweetcount': tweetcount, 'usercount': usercount})

df4.to_csv(r'df4.txt', sep='\t')
df5.to_csv(r'df5.txt', sep='\t')
df6.to_csv(r'df6.txt', sep='\t')


#print type(Mx)
#df.to_csv(r'df4.txt', index=None, sep='\t')  
