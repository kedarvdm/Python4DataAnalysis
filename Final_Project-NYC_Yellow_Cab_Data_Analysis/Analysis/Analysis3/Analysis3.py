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

def calculateTipPercentage(total_amount, tip_amount):
    tip_percentage = 0
    if total_amount == 0 or tip_amount == 0:
        return tip_percentage
    
    tip_percentage = ((total_amount/(total_amount - tip_amount))*100)-100
    return tip_percentage

def main():
	print('Avarage Tip Percentage')
	#Read the VenderId and Month
	venderid, month = parseInput()
	extracted_files = glob.glob('..\\..\\Data\\{0}\\{1}\\processed\\*.csv'.format(venderid, month))
	df = pd.DataFrame()
	list_ = []
	for fileName in extracted_files:
		short_df = pd.read_csv(fileName)
		list_.append(short_df)
	df = pd.concat(list_)
	
	df = df[df['pickup_area'] != 'Not Specified']
	df = df[df['dropoff_area'] != 'Not Specified']
	
	print('Filtering Payments by Credit Card')
	df = df[df['payment_type'] == 1]
	print('Unsual scenario where tip amount is greater than actual fare.')
	print('Filtering these records')
	df = df[df['tip_amount']<df['fare_amount']]
	
	print('Calculating tip percentage')
	df['tip_percentage'] =  df.apply(lambda row: calculateTipPercentage(row['total_amount'], row['tip_amount']), axis=1)
	
	grouped = df['tip_percentage'].groupby([df['dropoff_area']])
	
	group_by_mean_df = grouped.mean().to_frame()
	group_by_mean_df = group_by_mean_df.reset_index()
	group_by_mean_df = group_by_mean_df.rename(columns = {'dropoff_area':'Dropoff Area', 'tip_percentage':'Average Tip'})

	group_by_max_df = grouped.max().to_frame()
	group_by_max_df = group_by_max_df.reset_index()
	group_by_max_df = group_by_max_df.rename(columns = {'dropoff_area':'Dropoff Area', 'tip_percentage':'Max Tip'})

	group_by_min_df = grouped.min().to_frame()
	group_by_min_df = group_by_min_df.reset_index()
	group_by_min_df = group_by_min_df.rename(columns = {'dropoff_area':'Dropoff Area', 'tip_percentage':'Min Tip'})

	grouped_df = group_by_mean_df

	grouped_df = pd.merge(grouped_df, group_by_max_df,how='inner', right_index=False, left_index=False)
	grouped_df = pd.merge(grouped_df, group_by_min_df,how='inner', right_index=False, left_index=False)
	
	grouped_df = grouped_df.round(2)

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
	create_bar_plot(grouped_df, save_file_name)
	print('End')
	
	
def create_bar_plot(grouped_df, save_file_name):
	
	max_lim = grouped_df['Max Tip'].max()
	
	plt.subplots(figsize=(20,10))
	sns.set(style='whitegrid')
	max_plot = sns.barplot(x="Dropoff Area", y="Max Tip", data=grouped_df,
				label="Total", color="#DECF3F")

	avg_plot = sns.barplot(x="Dropoff Area", y="Average Tip", data=grouped_df,
				label="Total", color="#FF8C00")

	min_plot = sns.barplot(x="Dropoff Area", y="Min Tip", data=grouped_df,
				label="Total", color="#DECF3F")

	#Legend
	maxbar = plt.Rectangle((1,1),2,2,fc="#DECF3F", edgecolor = 'none')
	avgbar = plt.Rectangle((1,1),2,2,fc='#9400D3',  edgecolor = 'none')
	minbar = plt.Rectangle((1,1),2,2,fc='#FF8C00',  edgecolor = 'none')
	l = plt.legend([maxbar, avgbar, minbar], ['Min', 'Average', 'Max'], loc=2, ncol = 3, prop={'size':16 , 'weight':'bold'})
	l.draw_frame(False)

	#title
	avg_plot.set_title('Average Tip Percentage')
	avg_plot.title.set_fontsize(36)
	avg_plot.title.set_position([.5, 1.02])
	avg_plot.title.set_fontweight(weight='bold')
	avg_plot.title.set_color('#4D4D4D')

	#XYAxis
	avg_plot.xaxis.get_label().set_fontsize(30)
	avg_plot.xaxis.get_label().set_fontweight(weight='bold')
	avg_plot.xaxis.get_label().set_color('#4D4D4D')

	avg_plot.yaxis.get_label().set_fontsize(30)
	avg_plot.yaxis.get_label().set_fontweight(weight='bold')
	avg_plot.yaxis.get_label().set_color('#4D4D4D')

	#XyTicks
	plt.setp(avg_plot.get_xticklabels(), rotation=45, fontsize=24, color='#B2912F', fontweight='bold')
	plt.setp(avg_plot.get_yticklabels(), fontsize=24, color='#B2912F', fontweight='bold')

	avg_plot.set(xlabel='Dropoff Area', ylabel='Tip Percentage')
	avg_plot.set_ylim(0, 1.2*max_lim)

	font ={'family': 'serif','color':'#00008B','weight': 'bold','size': 20}

	for p in avg_plot.patches:
		percentage = p.get_height()
		avg_plot.text(p.get_x(), percentage+ 2, '%1.2f'%(percentage), fontdict= font)
	#store the output in csv
	report_name = 'reports\\png\\'
	
	#Create reports folder if not exists
	if not os.path.exists(report_name):
		os.makedirs(report_name)
	
	plt.gcf().subplots_adjust(bottom=0.25)
	plt.savefig(report_name+save_file_name+'.png', dpi=200, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=1.0,
        frameon=None)
	print('Graph output stored to: {0}'.format(report_name+save_file_name+'.png'))
	
main()