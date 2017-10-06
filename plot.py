#Max/Add-----------------------------
import pandas as pd
import sys
import matplotlib 
matplotlib.use('Agg')
import matplotlib.pyplot
import matplotlib.pyplot as plt

#inputs------------------------------------------
Addd= sys.argv[1]
Maxx= sys.argv[2]
count= sys.argv[3]
#outputs
add_cluster= sys.argv[4]
max_cluster= sys.argv[5]
count_plot= sys.argv[6]
#-----------------------------

df= pd.DataFrame.from_csv(Addd, sep='\t')
df1= pd.DataFrame.from_csv(Maxx, sep='\t')
df2= pd.DataFrame.from_csv(count, sep='\t')

for column in df:
	df[column].plot()
	plt.xlabel('Timeline (per hour)', fontsize=22)
	plt.ylabel('Total Intensity of Topic Cluster', fontsize=23)
	plt.xticks(fontsize=15)
	plt.yticks(fontsize=18)
	plt.savefig(add_cluster + column + ".png", bbox_inches='tight')   #50_acluster_1.png
	plt.clf()


for column in df1:
	df1[column].plot()
	plt.xlabel('Timeline (per hour)', fontsize=22)
	plt.ylabel('Usage of Most Intense Hashtag', fontsize=23)
	plt.xticks(fontsize=15)
	plt.yticks(fontsize=18)
	plt.savefig(max_cluster + column + ".png", bbox_inches='tight') 
	plt.clf()

def plot_count():
	df2.plot(x='usercount', y='tweetcount', style='o')
	plt.xlabel('Topic users count', fontsize=25)
	plt.ylabel('Topic tweets count', fontsize=25)
	plt.xticks(fontsize=18)
	plt.yticks(fontsize=18)	
	plt.savefig(count_plot + ".png", bbox_inches='tight') 
	plt.clf()

plot_count()

#========================================================================================================
