import pandas as pd
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import argparse
sns.set()

def parseInput():
	parser = argparse.ArgumentParser()
	parser.add_argument("--venderid", help="Enter the venderid", default='*')
	parser.add_argument("--month", help="Enter the month to run analysis for. Format (YYYY-MM)", default='*')
	args = parser.parse_args()
	return args.venderid,args.month

def calculate_estimated_lyft_cost(row):
    passenger_count = row['passenger_count']
    #as lyft estimation does not contain tips, substracting tip from Yellow taxi total_amount
    cost_without_tip = row['total_amount'] - row['tip_amount']
    estimated_lyft_cost = 0
    if 0 <= passenger_count <= 1:
        #for 1 passenger lyft line is economical
        estimated_lyft_cost = row['lyft_line_cost']
    elif 2<= passenger_count <=4:
        #for passenger count between 2 to max 4 lyft is economical
        estimated_lyft_cost = row['lyft_cost']
    else:
        #for passenger count between 2 to max 4 lyft is economical
        estimated_lyft_cost = row['lyft_plus_cost']
    
    return pd.Series([cost_without_tip, estimated_lyft_cost])	

def main():
	print('Comparison of Lyft Vs Yellow Cab Ride Costs')
	#Read the VenderId and Month
	venderid, month = parseInput()
	extracted_files = glob.glob('..\\..\\Data\\{0}\\{1}\\lyftdata\\*.csv'.format(venderid, month))
	df = pd.DataFrame()
	list_ = []
	for fileName in extracted_files:
		short_df = pd.read_csv(fileName)
		list_.append(short_df)
	df = pd.concat(list_)
	
	print('Unsual scenario where tip amount is greater than actual fare.')
	print('Filtering these records')
	df = df[df['tip_amount']<df['fare_amount']]
	df['passenger_count'] = df['passenger_count'].apply(lambda x: 1 if x == 0 else x)
	
	data =  df.apply(lambda row: calculate_estimated_lyft_cost(row), axis=1)
	data.columns = ['cost_without_tip', 'estimated_lyft_cost']
	df = df.join(data)
	
	grouped_yellow_cab_series_df = df['cost_without_tip'].groupby(df['passenger_count']).mean()
	grouped_lyft_series_df = df['estimated_lyft_cost'].groupby(df['passenger_count']).mean()
	grouped_yellow_cab_df = grouped_yellow_cab_series_df.to_frame()

	grouped_lyft_df = grouped_lyft_series_df.to_frame()
	grouped_df = grouped_yellow_cab_df.join(grouped_lyft_df)

	grouped_df = grouped_df.reset_index()
	
	#store the output in csv
	report_name = 'reports\\csv\\'
	
	#Create reports folder if not exists
	if not os.path.exists(report_name):
		os.makedirs(report_name)
	
	save_file_name = None
	if not venderid == '*':
		save_file_name = venderid+'_'
	else:
		save_file_name = 'All_'
		
	if not month == '*':
		save_file_name = save_file_name+month+'_'
	else:
		save_file_name = save_file_name+'All_'
	
	save_file_name = save_file_name+dt.datetime.strftime(dt.datetime.now(),'%Y_%m_%d_%H_%M_%S')
	
	grouped_df.to_csv(report_name+save_file_name+'.csv', sep=',', encoding='utf-8', index=False)
	print('CSV output saved to: {0}'.format(report_name+save_file_name+'.csv'))
	create_bidirectional_bar_plot(grouped_df, save_file_name)
	
	yellow_cost_df = grouped_df[['passenger_count', 'cost_without_tip']]
	yellow_cost_df['Cab Type'] = 'Yellow'
	yellow_cost_df = yellow_cost_df.rename(columns={'cost_without_tip':'cost'})
	
	lyft_cost_df = grouped_df[['passenger_count', 'estimated_lyft_cost']]
	lyft_cost_df['Cab Type'] = 'lyft'
	lyft_cost_df = lyft_cost_df.rename(columns={'estimated_lyft_cost':'cost'})
	
	joined_df = pd.concat([yellow_cost_df,lyft_cost_df])
	create_grouped_bar_plot(joined_df, save_file_name)
	print('End')
	
def create_bidirectional_bar_plot(grouped_df, save_file_name):
	x1 = grouped_df['cost_without_tip']
	x2 = grouped_df['estimated_lyft_cost']

	bar_labels = grouped_df['passenger_count'].unique()

	fig = plt.figure(figsize=(20,10))

	y_pos = np.arange(len(x1))
	y_pos = [x for x in y_pos]
	plt.yticks(y_pos, bar_labels, fontsize=10)

	plot1 = plt.barh(y_pos,x1,align='center',alpha=0.4,color='#FFD700')

	plt.barh(y_pos,-x2,align='center',alpha=0.4,color='#FF1493')

	# annotation and labels
	t = plt.title('Comparison of Lyft Vs Yellow Cab Ride Costs')
	plt.xlabel('Ride Cost')
	plt.ylabel('Passenger Count')
	plt.ylim([-1,len(x1)+0.1])
	plt.xlim([-max(x2)-5, max(x1)+5])

	plt.rcParams['xtick.labelsize'] = 18 
	plt.rcParams['ytick.labelsize'] = 18 
	plt.rcParams['axes.labelsize'] = 24
	plt.rcParams['axes.titlesize'] = 32
	
	#store the output in csv
	report_name = 'reports\\png\\'
	
	#Create reports folder if not exists
	if not os.path.exists(report_name):
		os.makedirs(report_name)
	
	plt.savefig(report_name+save_file_name+'_bidirectional.png', dpi=200, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=1.0,
        frameon=None)
	print('Bidirectonal Bar Graph output stored to: {0}'.format(report_name+save_file_name+'_bidirectional.png'))
	
def create_grouped_bar_plot(joined_df, save_file_name):
	ymax = joined_df.cost.max().round()
	
	myColors = ["#FFD700","#FF1493"]
	rc={'font.size': 24, 'axes.labelsize': 24, 'legend.fontsize': 24.0, 
		'axes.titlesize': 36, 'xtick.labelsize': 18, 'ytick.labelsize': 18}
	sns.set(rc=rc)
	factor_plot = sns.factorplot(x="passenger_count", y="cost", hue="Cab Type",
								 data=joined_df, kind = 'bar' , size = 18, palette=myColors,
								legend=True, legend_out=False)
	plt.ylim(0, 18)
	factor_plot.set()
	factor_plot.despine(left=True)
	factor_plot.set_xlabels('Passenger Count')
	factor_plot.set_ylabels('Cost')
	figure_title = factor_plot.fig.suptitle('Yellow Cab Vs. Lyft Cost comparison')
	figure_title.set_position([.5, 1.03])

	factor_plot.ax.xaxis.label.set_color('#FF0000')
	factor_plot.ax.yaxis.label.set_color('#FF0000')

	font ={'family': 'serif','color':  'darkred','weight': 'normal','size': 16}

	for p in factor_plot.ax.patches:
		percentage = p.get_height()
		factor_plot.ax.text(p.get_x(), percentage+0.1, '%1.2f'%(percentage), fontdict= font)
	
	#store the output in csv
	report_name = 'reports\\png\\'
	
	#Create reports folder if not exists
	if not os.path.exists(report_name):
		os.makedirs(report_name)
	
	plt.savefig(report_name+save_file_name+'_bar_plot.png', dpi=200, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=1.0,
        frameon=None)
	print('Grouped Graph output stored to: {0}'.format(report_name+save_file_name+'_bar_plot.png'))
	
main()