import os
import json
import requests
from datetime import datetime,date,timedelta
import urllib
import time
import glob
import sys

#Obtained from stack exchange app
APP_KEY = 'IDWxeTfJypl6G15Nm)h8rg(('
BASE_URL = 'https://api.stackexchange.com/2.2/'
TAGS_URL = 'tags'
BADGES_URL = 'badges'
QUESTIONS_URL = 'questions'
USERS_URL = 'users/'
SYNONYMS_URL = 'synonyms'


def showMenu():
	print("Stack Exchange Fetcher")
	print("1. Download Questions")
	print('Based on Questions Downloaded')
	print("2. Download User Profiles")
	print("3. Download Users with Badges")
	print("4. Download Users with Tags")
	print("5. Download All The Tags")
	print("6. Download Synonyms Of The Tags")
	print("7. Exit")
	
	userInput = input('Enter your choice: ')
	print(userInput)
	if userInput == '1':
		pg1 = input('Please Enter Start Page: ')
		pg2 = input('Please Enter End Page: ')
		sort = 'creation'
		downloadAndSave(QUESTIONS_URL, int(pg1), int(pg2), sort)
		showMenu()
	elif userInput == '2':
		download_userProfiles()
		showMenu()
	elif userInput == '3':
		download_userBadges()
		showMenu()
	elif userInput == '4':
		download_userTags()
		showMenu()
	elif userInput == '5':
		pg1 = input('Please Enter Start Page: ')
		pg2 = input('Please Enter End Page: ')
		sort = 'name'
		downloadAndSave(TAGS_URL, int(pg1), int(pg2), sort)
		showMenu()
	elif userInput == '6':
		downloadTagSynonyms()
		showMenu()
	elif userInput == '7':
		sys.exit(0)
	else:
		sys.exit(0)

def downloadAndSave(type, startPage, endPage, sort):
	try:
		typeFolderExists = os.path.exists(type)
		if not typeFolderExists:
			os.mkdir(type, mode=0o777 )
			
		url= BASE_URL+type
		print(url)
		hasMore = 'true'
		
		while hasMore:
			payload = {'page': str(startPage), 'pagesize': '100', 'order': 'asc', 'sort': sort, 'site':'stackoverflow', 'key':APP_KEY}
			r = requests.get(url, params=payload)
			time.sleep(0.004)
			with open(type+'/'+type+str(startPage)+'.json', 'w') as outfile:
				json.dump(r.json(), outfile)

			jsonresp = r.json()
			if 'has_more' in jsonresp:
				hasMore = jsonresp['has_more']
			else:
				hasMore = 'false'
				
			if startPage == endPage:
				break
			startPage = startPage+1
	except:
		print("Error Downloading Data:", sys.exc_info()[0])
		print('Error Downloading Data')
			
#downloadAndSave(BADGES_URL,1,1000,'name')


def download_userProfiles():
	users_url= BASE_URL+USERS_URL
	
	fileNames = glob.glob('questions/*.json')
	if not fileNames:
		print('Plese Download Questions fFirst')
		return
	
	usersFolderExists = os.path.exists('users')
	if not usersFolderExists:
		os.mkdir('users', mode=0o777 )
	
	payload = {'order': 'asc', 'pagesize': '100', 'sort': 'name', 'site':'stackoverflow', 'key':APP_KEY }
	i = 0
	for fileName in fileNames:
		print(fileName)
		i = i+1
		ids = getUserProfileIds(fileName)
		if ids == '':
			continue
		ids = urllib.parse.quote(ids)
		url = users_url+ids
		try:
			r = requests.get(url, params=payload)
			if r.status_code == 200:
				with open(USERS_URL+'users'+str(i)+'.json', 'w') as outfile:
					json.dump(r.json(), outfile)
			
			time.sleep(0.004)
		except:
			print(fileName+' failed')
	print('User Downloaded')
	print('User Profiles Extraction Begin')
	extractUserProfile()
	print('User Profiles Extraction End')
			
def getUserProfileIds(fileName):
	ids = ''
	with open(fileName, 'r') as outfile:
		data = json.load(outfile)
		if 'items' in data:
			data = data['items']
			for dataNode in data:
				if 'user_id' in dataNode['owner']:
					ids = ids+ str(dataNode['owner']['user_id'])+';'
		
		ids = ids[:-1]
		return ids

#download_userProfiles()

def extractUserProfile():
	usersProfilesFolderExists = os.path.exists('userprofiles')
	if not usersProfilesFolderExists:
		os.mkdir('userprofiles', mode=0o777 )
		
	fileNames = glob.glob('users/*.json')
	if not fileNames:
		print('Plese Download Questions fFirst')
		return
	for fileName in fileNames:
		with open(fileName, 'r') as outfile:
			print(fileName)
			data = json.load(outfile)
			if 'items' in data:
				data = data['items']
				for dataNode in data:
					newFileName = 'user_'+ str(dataNode['user_id'])
					with open('userprofiles/'+newFileName+'.json', 'w') as datafile:
						json.dump(dataNode, datafile)
						
#extractUserProfile()


def download_userBadges():
	users_url= BASE_URL+USERS_URL
	fileNames = glob.glob('questions/*.json')
	if not fileNames:
		print('Plese Download Questions fFirst')
		return
	
	usersListWithBadgesFolderExists = os.path.exists('usersListWithBadges')
	if not usersListWithBadgesFolderExists:
		os.mkdir('usersListWithBadges', mode=0o777 )
		
	count = 0
	for fileName in fileNames:
		hasMore = 'true'
		i = 0
		print(fileName)
		ids = getUserProfileIds(fileName)
		if ids == '':
			continue
		ids = urllib.parse.quote(ids)
		while hasMore:
			i = i+1
			count = count+1
			payload = {'order': 'asc', 'page':str(i), 'pagesize': '100', 'sort': 'name', 'site':'stackoverflow', 'key':APP_KEY }
			url = users_url+ids+'/'+BADGES_URL
			try:
				r = requests.get(url, params=payload)
				if r.status_code == 200:
					with open('usersListWithBadges/usersbadges'+str(count)+'.json', 'w') as outfile:
						json.dump(r.json(), outfile)
				
				jsonresp = r.json()
				if 'has_more' in jsonresp:
					hasMore = jsonresp['has_more']
				else:
					hasMore = 'false'
				time.sleep(0.004)
			except:
				print(fileName+' failed')
	print('User Badges Saved')
				
def download_userTags():
	users_url= BASE_URL+USERS_URL
	fileNames = glob.glob('questions/*.json')
	if not fileNames:
		print('Plese Download Questions fFirst')
		return
	
	usersWithTagsFolderExists = os.path.exists('usersWithTags')
	if not usersWithTagsFolderExists:
		os.mkdir('usersWithTags', mode=0o777 )
		
	count = 0
	for fileName in fileNames:
		hasMore = 'true'
		i = 0
		print(fileName)
		ids = getUserProfileIds(fileName)
		if ids == '':
			continue
		ids = urllib.parse.quote(ids)
		while hasMore:
			i = i+1
			count = count+1
			payload = {'order': 'asc', 'page':str(i), 'pagesize': '100', 'sort': 'name', 'site':'stackoverflow', 'key':APP_KEY }
			url = users_url+ids+'/'+TAGS_URL
			try:
				r = requests.get(url, params=payload)
				if r.status_code == 200:
					with open('usersWithTags/userstags_'+str(count)+'.json', 'w') as outfile:
						json.dump(r.json(), outfile)
				
				jsonresp = r.json()
				if 'has_more' in jsonresp:
					hasMore = jsonresp['has_more']
				else:
					hasMore = 'false'
				time.sleep(0.004)
			except:
				print(fileName+' failed')
	print('User Tags Saved')
#download_userTags()

def downloadTagSynonyms():
	url = BASE_URL+'/'+TAGS_URL+'/'+SYNONYMS_URL
	
	synonymsFolderExists = os.path.exists('synonyms')
	if not synonymsFolderExists:
		os.mkdir('synonyms', mode=0o777 )
	
	hasMore = 'true'
	i = 0
	while hasMore:
		i = i+1
		payload = {'page': str(i), 'pagesize': '100', 'order': 'asc', 'sort': 'creation', 'site':'stackoverflow', 'key':APP_KEY}
		r = requests.get(url, params=payload)
		time.sleep(0.004)
		with open('synonyms'+'/'+'synonyms_'+str(i)+'.json', 'w') as outfile:
			json.dump(r.json(), outfile)

		jsonresp = r.json()
		if 'has_more' in jsonresp:
			hasMore = jsonresp['has_more']
		else:
			hasMore = 'false'
	print('All Tags Synonyms Saved')
	
showMenu()