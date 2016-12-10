import json
from shapely.geometry import shape, Point
import csv
from csv import DictWriter as DictWriter
import pandas as pd
from datetime import datetime
import os
import glob
import requests
import requests.auth
from geopy.geocoders import Nominatim
geolocator = Nominatim()
import sys
import time

def main():
	print('Step 1: Data extraction')
	extractData()
	print('Step 2: Create chunks of the extracted data')
	chunkifyDataFiles()
	print('Step 3: Read the GeoJSON')
	setJS()
	print('Step 4: Update the processed files with pickup_area and dropoff_area')
	update_processed_files_with_location()
	print('Step 5: Request and store ride estimates')
	request_lyft_ride_estimates()

def extractData():
	fileNames = glob.glob('Taxi\\*.csv')
	if len(fileNames) == 0:
		print('Data does not exist for processing. Please download data frist')
		sys.out(0)
	
	for fileName in fileNames:
		print("Reading file: {0}".format(fileName))
		extracted_month = fileName.replace('Taxi\\yellow_tripdata_','').replace('.csv','')
		#Read the csv for the month
		df = pd.read_csv(fileName)
		#Extract and add the travel date in the dataframe
		print("Adding travel date in the dataframe")
		df['travel_date'] = df['tpep_pickup_datetime'].apply(lambda x: datetime.strptime(x , '%Y-%m-%d %H:%M:%S').date())
		print("Creating file structure")
		for i in df.VendorID.unique():
			print("Filtering Vendor: {0}".format(i))
			dfi = df[df['VendorID'] == i]
			#print(dfi.head())
			for dt in dfi.travel_date.unique():
				print("Filtering Date: {0}".format(dt))
				dfidt = dfi[dfi['travel_date'] == dt]
				#Create folder
				data_file_folder = 'Data/'+str(i)+'/'+extracted_month+'/original/'
				if not os.path.exists(data_file_folder):
					os.makedirs(data_file_folder)
				#file format Data/VendorId/Month/original/Day.csv
				data_file_name = data_file_folder+str(dt)+'.csv'
				print("CSV created: {0}".format(data_file_name))
				dfidt.to_csv(data_file_name, sep=',', encoding='utf-8', index=False)
	print('Data extraction complete')

def chunkifyDataFiles():	
	extracted_files = glob.glob('Data\\*\\*\\original\\*.csv')
	for fileName in extracted_files:
		#Read the file
		print("Reading file: {0}".format(fileName))
		df = pd.read_csv(fileName,chunksize= 500)
		i = 0
		#split the filename
		path_list = fileName.split('\\')
		#update the parent folder name
		path_list[-2] = 'processed' 
		folder_path = '\\'.join(path_list[:-1])
		if not os.path.exists(folder_path):
			os.makedirs(folder_path)
		savefile_name = path_list[-1]
		savefile_name = savefile_name.replace('.csv','')
		for chunk in df:
			chunk.to_csv(folder_path+'\\'+savefile_name+'_'+str(i)+'.csv', index=True, index_label='index')
			i = i+1
	print('Data file chunks saved')
	

def setJS():
	resource_file_path = 'Resources\\nyboroughs.geojson'
	
	if not os.path.exists(resource_file_path):
		print('GeoJSON to read coordinates is not present. Please download NYC area GeoJSON, name it as nyboroughs.geojson and place it inside Resources folder')
		sys.exit(0)
	
	global js
	
	with open('Resources\\nyboroughs.geojson') as f:
		js = json.load(f)
	print('NYC area GeoJSON loaded')
	
def getLocation(long, lat):
    point = Point(long,lat)
    area = "Not Specified"
    # check each polygon to see if it contains the point
    for feature in js['features']:
        polygon = shape(feature['geometry'])
        if polygon.contains(point):
            area = feature['properties']['name']
            break
    return area
	
def update_processed_files_with_location():
	extracted_files = glob.glob('Data\\*\\*\\processed\\*.csv')
	location_list = {}
	for fileName in extracted_files:
		#Read the file
		print("Reading file: {0}".format(fileName))
		df = pd.read_csv(fileName)
		for index, row in df.iterrows():
			location_list[index] = {'index': row['index'],
									'pickup_area':getLocation(row['pickup_longitude'],row['pickup_latitude']),
									'dropoff_area':getLocation(row['dropoff_longitude'],row['dropoff_latitude'])}
		
		location_df = pd.DataFrame.from_dict(location_list, orient='index')
		new_df = pd.merge(df, location_df, on='index', how='inner', right_index=False, left_index=False)
		print("Saving file: {0}".format(fileName))
		new_df.to_csv(fileName, sep=',', encoding='utf-8', index=False)
		location_list = {}
		
	print('Location updated in the processed files')
	
def retrieveAccessToken():
    url = "https://api.lyft.com/oauth/token"
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID , CLIENT_SECRET)

    hdrs = {'Content-Type': 'application/json', 'grant_type':'client_credentials', 'scope': 'public'}
    r = requests.post(url, auth=client_auth,data= hdrs)
    if r.status_code == 200:
        #Set access token
        current_token = r.json()['access_token']
        access_token = current_token
    else:
        print('Error retrieving access token')
        sys.exit(0)
    return current_token

def getRideEstimate(row):
    
    if row['pickup_area'] == "Not Specified" or row['dropoff_area'] == "Not Specified":
        return pd.Series(["0.0","0.0","0.0","0.0", "0"], index=['lyft_cost','lyft_plus_cost', 'lyft_line_cost', 'lyft_distance', 'lyft_duration'])
    
    if access_token is not None:
        current_token = access_token
    else:
        current_token = retrieveAccessToken()
    
    ride_estimate_url = "https://api.lyft.com/v1/cost"
    
    payload = {'start_lat':row['pickup_latitude'], 'start_lng': row['pickup_longitude'],
               'end_lat': row['dropoff_latitude'], 'end_lng': row['dropoff_longitude']}

    hdrs = {'Authorization': 'bearer '+ current_token}
    time.sleep(0.004)
    ride_estimate = requests.get(ride_estimate_url, params=payload, headers = hdrs)
    estimates = ride_estimate.json()['cost_estimates']
    dict = {}
    for i in range(0,len(estimates)):
        dict[estimates[i]['ride_type']+'_cost'] = estimateCalculation(estimates[i])
    
    dict['lyft_distance'] = estimates[0]['estimated_distance_miles']
    dict['lyft_duration'] = estimates[0]['estimated_duration_seconds']
    
    estimate_series = pd.Series(data=dict, index=['lyft_cost','lyft_plus_cost', 'lyft_line_cost', 'lyft_distance', 'lyft_duration'])
    return estimate_series
	
def estimateCalculation(estimate):
    
    estimated_cost = (estimate['estimated_cost_cents_max']+ estimate['estimated_cost_cents_min'])/200
    if not estimate['primetime_percentage'] == 0:
        primetime_percentage = int(estimate['primetime_percentage'].replace('%',''))
        
        estimated_cost = (estimated_cost/(100+primetime_percentage))*100
        
    return format(float(estimated_cost), '.2f')

def set_access_token_info():
	global access_token
	global CLIENT_ID
	global CLIENT_SECRET
	
	access_token = None
	CLIENT_ID = 'xLAmv1MmKerS'
	CLIENT_SECRET = 'VzZHSkFTrZQQFJuGROA3nzqVSJTgbmvW'
	
def request_lyft_ride_estimates():
	set_access_token_info()
	extracted_files = glob.glob('Data\\*\\*\\processed\\*.csv')
	for fileName in extracted_files:
		print("Reading file: {0}".format(fileName))
		
		#split the filename
		path_list = fileName.split('\\')
		#update the parent folder name
		path_list[-2] = 'lyftdata' 
		folder_path = '\\'.join(path_list[:-1])
		print(folder_path)
		if not os.path.exists(folder_path):
			os.makedirs(folder_path)
			
		savefile_name = path_list[-1]
		
		full_path = folder_path+'\\'+savefile_name
		
		if os.path.exists(full_path):
			print('file already exists. Skipping this file.')
			continue
			
		if not os.path.exists(folder_path):
			os.makedirs(folder_path)
		
		df = pd.read_csv(fileName)
		data = df.apply(lambda row: getRideEstimate(row), axis=1)
		data.columns = ['lyft_cost','lyft_plus_cost', 'lyft_line_cost', 'lyft_distance', 'lyft_duration']
		df = df.join(data)
		
		#Save the file
		df.to_csv(full_path, sep=',', encoding='utf-8', index=False)
		print("CSV update: {0}".format(full_path))
	
	print('Lyft ride estimates updated')
	
main()