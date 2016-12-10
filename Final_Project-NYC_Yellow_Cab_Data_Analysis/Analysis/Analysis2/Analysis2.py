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
	print('Average Credit Vs. Cash Per Borough')
	#Read the VenderId and Month
	venderid, month = parseInput()
	extracted_files = glob.glob('..\\..\\Data\\{0}\\{1}\\processed\\*.csv'.format(venderid, month))
	df = pd.DataFrame()
	list_ = []
	for fileName in extracted_files:
		short_df = pd.read_csv(fileName)
		list_.append(short_df)
	df = pd.concat(list_)
	
	group_by_series = df['total_amount'].groupby([df['pickup_area'], df['payment_type']]).mean()
	group_by_df = group_by_series.to_frame()
	group_by_df = group_by_df.reset_index()
	#Filter Cash and Credit payments
	group_by_df = group_by_df[group_by_df['payment_type'].isin([1,2])]
	group_by_df['payment_type'] = group_by_df['payment_type'].apply(lambda x: 'Credit' if x == 1 else 'Cash')
	group_by_df = group_by_df.rename(columns = {'pickup_area':'Pick-Up Area', 'payment_type':'Payment Type', 'total_amount':'Average'})
	
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
	
	group_by_df.to_csv(report_name+save_file_name+'.csv', sep=',', encoding='utf-8', index=False)
	print('CSV output saved to: {0}'.format(report_name+save_file_name+'.csv'))
	create_factor_plot(group_by_df, save_file_name)
	print('End')
	

def create_factor_plot(group_by_df, save_file_name):
	myColors = ["#FF8C00","#DC143C"]
	rc={'font.size': 24, 'axes.labelsize': 24, 'legend.fontsize': 24.0, 
		'axes.titlesize': 32, 'xtick.labelsize': 18, 'ytick.labelsize': 18}
	sns.set(rc=rc)
	factor_plot = sns.factorplot(x="Pick-Up Area", y="Average", hue="Payment Type",
								 data=group_by_df, kind = 'bar' , size = 16, palette=myColors,
								legend=True, legend_out=False)
	factor_plot.despine(left=True)
	factor_plot.set_xlabels('Borough')
	factor_plot.set_ylabels('Total Amount')
	factor_plot.set_xticklabels(rotation=45)
	figure_title = factor_plot.fig.suptitle('Average Credit Vs. Cash Per Borough')
	figure_title.set_position([.5, 1.00])

	font ={'family': 'serif','color':  'darkred','weight': 'normal','size': 16}

	for p in factor_plot.ax.patches:
		percentage = p.get_height()
		factor_plot.ax.text(p.get_x(), percentage+0.5, '%1.2f'%(percentage), fontdict= font)
		
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