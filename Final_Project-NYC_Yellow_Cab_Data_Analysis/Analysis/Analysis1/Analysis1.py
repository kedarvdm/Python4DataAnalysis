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


def main():
	print('Borough to Borough Revenue Distribution')
	#Read the VenderId and Month
	venderid, month = parseInput()
	extracted_files = glob.glob('..\\..\\Data\\{0}\\{1}\\processed\\*.csv'.format(venderid, month))
	df = pd.DataFrame()
	list_ = []
	for fileName in extracted_files:
		short_df = pd.read_csv(fileName)
		list_.append(short_df)
	df = pd.concat(list_)
	df = df.rename(columns = {'pickup_area':'Pick-Up', 'dropoff_area':'Dropoff'})
	
	group_by_series = df['total_amount'].groupby([df['Pick-Up'], df['Dropoff']]).sum()
	group_by_df = group_by_series.to_frame()
	group_by_df = group_by_df.reset_index()
	
	reshaped = group_by_df.pivot_table('total_amount', 'Pick-Up', 'Dropoff')
	reshaped = reshaped.fillna(0.0)
	reshaped = reshaped.round(2)
	
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
	
	reshaped.to_csv(report_name+save_file_name+'.csv', sep=',', encoding='utf-8')
	print('CSV output saved to: {0}'.format(report_name+save_file_name+'.csv'))
	create_cost_heatmap(reshaped, save_file_name)
	print('End')
	
def create_cost_heatmap(reshaped, save_file_name):
	plt.subplots(figsize=(20,10))
	sns.set_style('whitegrid')
	cost_heatmap = sns.heatmap(reshaped, annot=True,
							   annot_kws={"size": 20, "color":'#DAA520' , 'weight':'bold'},
							   linewidths=.5, fmt='.2f', cmap='Blues_r',
							   cbar=True)

	#XYTick
	plt.setp(cost_heatmap.get_xticklabels(), rotation=45, fontsize=24, color='#B2912F', fontweight='bold')
	plt.setp(cost_heatmap.get_yticklabels(), rotation=45, fontsize=24, color='#B2912F', fontweight='bold')

	#title
	figure_title = cost_heatmap.set_title('Borough to Borough Revenue Distribution', weight='bold')
	figure_title.set_position([.5, 1.07])
	cost_heatmap.title.set_fontsize(36)
	cost_heatmap.title.set_color('#4D4D4D')

	#XYLabels
	cost_heatmap.xaxis.get_label().set_fontsize(30)
	cost_heatmap.xaxis.set_label_text('Dropoff Area', weight='bold')
	cost_heatmap.xaxis.get_label().set_color('#4D4D4D')

	cost_heatmap.yaxis.get_label().set_fontsize(30)
	cost_heatmap.yaxis.set_label_text('Pick-Up Area', weight='bold')
	cost_heatmap.yaxis.get_label().set_color('#4D4D4D')
	
	#store the output in csv
	report_name = 'reports\\png\\'
	
	#Create reports folder if not exists
	if not os.path.exists(report_name):
		os.makedirs(report_name)
	
	plt.savefig(report_name+save_file_name+'.png', dpi=200, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=1.0,
        frameon=None)
	print('Graph output stored to: {0}'.format(report_name+save_file_name+'.png'))
	
main()