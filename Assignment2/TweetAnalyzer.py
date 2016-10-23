import os
import json
import glob
import sys
from datetime import datetime,date,timedelta
from operator import itemgetter
import pandas as pd
import urllib
import requests

pd.options.display.max_colwidth = -1
def showMenu():
	print("Twitter Analysis")
	print("1. User reach")
	print("2. Top 10 Retweets Per Day")
	print("3. Tweet Language Distribution Per Day")
	print("4. Tweets Count Per Time Zone Per Day")
	print("5. Sentiment Analysis Per Search Term")
	print("6. Exit")
	
	userInput = input('Enter your choice: ')
	print(userInput)
	if userInput == '1':
		userReachCalculation()
	elif userInput == '2':
		try:
			retweetCalculation()
		except:
			print("You might need to run \'chcp 65001\' command to display tweets properly")
			sys.exit(0)
	elif userInput == '3':
		languageDistribution()
	elif userInput == '4':
		timeZoneDistribution()
	elif userInput == '5':
		sentimentAnalysis()
	elif userInput == '6':
		sys.exit(0)
	
	showMenu()

def userReachCalculation():
	searchTerm = input('Enter the search term: ')
	searchTerm = searchTerm.lower()
	specificDate = input('Do you want to search for specific date range?(y/n)')
	date1 = None
	date2 = None
	
	specificDate = specificDate.strip().lower()
	
	if specificDate == 'y':
		date1 = input('Enter the start date (yyyy-mm-dd): ')
		date2 = input('Enter the end date (yyyy-mm-dd): ')
	
	for searchItem in searchTerm.split(','):
		searchItem = searchItem.strip()
		print('Searching for: '+searchItem)
		searchPath =  "tweets/"+searchItem
		print(searchPath)
		if not os.path.exists(searchPath):
			printMessageAndShowMenu('Search term doesn\'t exists')
		
		averageUserReach = 0
		
		userFollowerDict = {}
		
		if specificDate == 'y':
			dateList = resolveDates(date1, date2)
			for currentDate in dateList:
				if os.path.exists(searchPath+'/'+currentDate):
					fileNames = glob.glob(searchPath+'/'+currentDate+'/*.json')
					for fileName in fileNames:
						#print(fileName)
						fileDict = getUserFollowerCountDictionaryFile(fileName)
						userFollowerDict.update(fileDict)
						
		else:
			for fileName in glob.iglob(searchPath +'/**/*.json', recursive=True):
				#print(fileName)
				fileDict = getUserFollowerCountDictionaryFile(fileName)
				userFollowerDict.update(fileDict)
			
		userCount = 0
		followersCount = 0
		for key in userFollowerDict.keys():
				userCount = userCount + 1
				followersCount = followersCount + userFollowerDict[key]
		
		averageUserReach = followersCount/userCount
		
		print('Average user reach for search term {0} is {1}'.format(searchItem,averageUserReach))

def getUserFollowerCountDictionaryFile(filePath):
	with open(filePath, 'r') as data_file:
		userFollowerDict = {}
		data = json.load(data_file)["statuses"]
		userCount = 0;
		followersCount = 0;
		for dataNode in data:
			screenName = dataNode['user']['screen_name']
			followersCount = dataNode['user']['followers_count']
			userFollowerDict[screenName] = int(followersCount)
		
		return userFollowerDict		
		

def retweetCalculation():
	searchTerm = input('Enter the search term: ')
	searchTerm = searchTerm.lower()
	specificDate = input('Do you want to search for specific date range?(y/n)')
	date1 = None
	date2 = None
	
	specificDate = specificDate.strip().lower()
	
	if specificDate == 'y':
		date1 = input('Enter the start date (yyyy-mm-dd): ')
		date2 = input('Enter the end date (yyyy-mm-dd): ')
	
	for searchItem in searchTerm.split(','):
		searchItem = searchItem.strip()
		print('Searching for: '+searchItem)
		searchPath =  "tweets/"+searchItem
		if not os.path.exists(searchPath):
			printMessageAndShowMenu('Search term doesn\'t exists')
		
		if specificDate == 'y':
			dateList = resolveDates(date1, date2)
			for currentDate in dateList:
				currentDayRetweetDict = {}
				if os.path.exists(searchPath+'/'+currentDate):
					fileNames = glob.glob(searchPath+'/'+currentDate+'/*.json')
					print('DAY: '+currentDate)
					for fileName in fileNames:
						fileDict = getRetweetedDictionaryFile(fileName)
						currentDayRetweetDict.update(fileDict)
						
				#print the dictionary with retweet count
				finalData = sorted(currentDayRetweetDict.items(), key=itemgetter(1), reverse=True)[:10]
				df = pd.DataFrame(finalData, columns=['Tweet', 'Count'])
				print(df)
		
		else:
			#Read all the dictionaries
			directoryList = [x[0] for x in os.walk(searchPath)][1:]
			for currentDate in directoryList:
				currentDayRetweetDict = {}
				dirname = currentDate.split(os.path.sep)[-1]
				fileNames = glob.glob(currentDate+'/*.json')
				print('DAY: '+dirname)
				for fileName in fileNames:
					fileDict = getRetweetedDictionaryFile(fileName)
					currentDayRetweetDict.update(fileDict)
						
				#print the dictionary with retweet count
				finalData = sorted(currentDayRetweetDict.items(), key=itemgetter(1), reverse=True)[:10]
				df = pd.DataFrame(finalData, columns=['Tweet', 'Count'])
				print(df)
		
		

def getRetweetedDictionaryFile(filePath):
	with open(filePath, 'r') as data_file:
		retweetDict = {}
		data = json.load(data_file)["statuses"]
		userCount = 0;
		followersCount = 0;
		for dataNode in data:
			#print(dataNode['retweet_count'])
			tweetText = str(dataNode['text'])
			retweetCount = dataNode['retweet_count']
			if not int(retweetCount) == 0:
				retweetDict[tweetText] = int(retweetCount)
		
		return retweetDict
		
def languageDistribution():
	searchTerm = input('Enter the search term: ')
	searchTerm = searchTerm.lower()
	specificDate = input('Do you want to search for specific date range?(y/n)')
	date1 = None
	date2 = None
	
	specificDate = specificDate.strip().lower()
	
	if specificDate == 'y':
		date1 = input('Enter the start date (yyyy-mm-dd): ')
		date2 = input('Enter the end date (yyyy-mm-dd): ')
	
	for searchItem in searchTerm.split(','):
		searchItem = searchItem.strip()
		print('Searching for: '+searchItem)
		searchPath =  "tweets/"+searchItem
		if not os.path.exists(searchPath):
			printMessageAndShowMenu('Search term doesn\'t exists')
		
		if specificDate == 'y':
			dateList = resolveDates(date1, date2)
			for currentDate in dateList:
				currentDayLangDict = {}
				if os.path.exists(searchPath+'/'+currentDate):
					fileNames = glob.glob(searchPath+'/'+currentDate+'/*.json')
					print('DAY: '+currentDate)
					for fileName in fileNames:
						fileDict = getLanguangeDistributionPerFile(fileName)
						currentDayLangDict = upsertDictionary(currentDayLangDict,fileDict)
						
				#print the dictionary with retweet count
				finalData = sorted(currentDayLangDict.items(), key=itemgetter(1), reverse=True)
				df = pd.DataFrame(finalData, columns=['Language', 'Count'])
				print(df)
		
		else:
			#Read all the dictionaries
			directoryList = [x[0] for x in os.walk(searchPath)][1:]
			for currentDate in directoryList:
				currentDayLangDict = {}
				dirname = currentDate.split(os.path.sep)[-1]
				fileNames = glob.glob(currentDate+'/*.json')
				print('DAY: '+dirname)
				for fileName in fileNames:
					fileDict = getLanguangeDistributionPerFile(fileName)
					currentDayLangDict = upsertDictionary(currentDayLangDict,fileDict)
						
				#print the dictionary with retweet count
				finalData = sorted(currentDayLangDict.items(), key=itemgetter(1), reverse=True)
				
				df = pd.DataFrame(finalData, columns=['Language', 'Count'])
				print(df)
				

def getLanguangeDistributionPerFile(filePath):
	with open(filePath, 'r') as data_file:
		occuranceTable = {}
		data = json.load(data_file)["statuses"]
		userCount = 0;
		followersCount = 0;
		for dataNode in data:
			lang = str(dataNode['lang'])
			occuranceTable[lang] = occuranceTable.get(lang, 0) + 1
		
		return occuranceTable
		

def timeZoneDistribution():
	searchTerm = input('Enter the search term: ')
	searchTerm = searchTerm.lower()
	specificDate = input('Do you want to search for specific date range?(y/n)')
	date1 = None
	date2 = None
	
	specificDate = specificDate.strip().lower()
	
	if specificDate == 'y':
		date1 = input('Enter the start date (yyyy-mm-dd): ')
		date2 = input('Enter the end date (yyyy-mm-dd): ')
	
	for searchItem in searchTerm.split(','):
		searchItem = searchItem.strip()
		print('Searching for: '+searchItem)
		searchPath =  "tweets/"+searchItem
		if not os.path.exists(searchPath):
			printMessageAndShowMenu('Search term doesn\'t exists')
		
		if specificDate == 'y':
			dateList = resolveDates(date1, date2)
			for currentDate in dateList:
				currentDayLangDict = {}
				if os.path.exists(searchPath+'/'+currentDate):
					fileNames = glob.glob(searchPath+'/'+currentDate+'/*.json')
					print('DAY: '+currentDate)
					for fileName in fileNames:
						fileDict = getTimeZoneDistributionPerFile(fileName)
						currentDayLangDict = upsertDictionary(currentDayLangDict,fileDict)
						
				#print the dictionary with retweet count
				finalData = sorted(currentDayLangDict.items(), key=itemgetter(1), reverse=True)
				df = pd.DataFrame(finalData, columns=['Timezone', 'Count'])
				print(df)
		
		else:
			#Read all the dictionaries
			directoryList = [x[0] for x in os.walk(searchPath)][1:]
			for currentDate in directoryList:
				currentDayLangDict = {}
				dirname = currentDate.split(os.path.sep)[-1]
				fileNames = glob.glob(currentDate+'/*.json')
				print('DAY: '+dirname)
				for fileName in fileNames:
					fileDict = getTimeZoneDistributionPerFile(fileName)
					currentDayLangDict = upsertDictionary(currentDayLangDict,fileDict)
						
				#print the dictionary with retweet count
				finalData = sorted(currentDayLangDict.items(), key=itemgetter(1), reverse=True)
				df = pd.DataFrame(finalData, columns=['Timezone', 'Count'])
				print(df)

def getTimeZoneDistributionPerFile(filePath):
	with open(filePath, 'r') as data_file:
		occuranceTable = {}
		data = json.load(data_file)["statuses"]
		userCount = 0;
		followersCount = 0;
		for dataNode in data:
			lang = str(dataNode['user']['time_zone'])
			occuranceTable[lang] = occuranceTable.get(lang, 0) + 1
		
		return occuranceTable
		
def sentimentAnalysis():
	searchTerm = input('Enter the search term: ')
	searchTerm = searchTerm.lower()
	specificDate = input('Do you want to search for specific date range?(y/n)')
	date1 = None
	date2 = None
	
	specificDate = specificDate.strip().lower()
	
	if specificDate == 'y':
		date1 = input('Enter the start date (yyyy-mm-dd): ')
		date2 = input('Enter the end date (yyyy-mm-dd): ')
	
	for searchItem in searchTerm.split(','):
		searchItem = searchItem.strip()
		print('Searching for: '+searchItem)
		searchPath =  "tweets/"+searchItem
		print(searchPath)
		if not os.path.exists(searchPath):
			printMessageAndShowMenu('Search term doesn\'t exists')
		
		averageUserReach = 0
		
		sentimentTable = {}
		
		if specificDate == 'y':
			dateList = resolveDates(date1, date2)
			for currentDate in dateList:
				if os.path.exists(searchPath+'/'+currentDate):
					fileNames = glob.glob(searchPath+'/'+currentDate+'/*.json')
					for fileName in fileNames:
						#print(fileName)
						fileDict = getSentimentsPerFile(fileName)
						sentimentTable = upsertDictionary(sentimentTable,fileDict)
						
		else:
			for fileName in glob.iglob(searchPath +'/**/*.json', recursive=True):
				#print(fileName)
				fileDict = getSentimentsPerFile(fileName)
				sentimentTable = upsertDictionary(sentimentTable,fileDict)
		
		finalData = sorted(sentimentTable.items(), key=itemgetter(1), reverse=True)
		df = pd.DataFrame(finalData, columns=['Sentiment', 'Count'])
		print(df)
		

def getSentimentsPerFile(filePath):
	with open(filePath, 'r') as data_file:
		sentimentTable = {}
		data = json.load(data_file)["statuses"]
		userCount = 0;
		followersCount = 0;
		for dataNode in data:
			tweetText = str(dataNode['text'])
			sentiment = getTweetSentiment(tweetText)
			sentimentTable[sentiment] = sentimentTable.get(sentiment, 0) + 1
		
		return sentimentTable
		

def getTweetSentiment(tweet):
	url="http://text-processing.com/api/sentiment/"
	sentiment = 'neutral'
	tweet = urllib.parse.quote(tweet)
	try:
		if tweet != '':
			r = requests.post(url, data = {'text':tweet})
			result = r.json()
			sentiment = result['label']
		else:
			print('Invalid search term provided')
	except requests.ConnectionError:
		print("failed to connect")
	return sentiment
		
def upsertDictionary(langDir, subLangDir):
	for key in subLangDir.keys():
		langDir[key] = langDir.get(key, 0) + subLangDir.get(key)
	return langDir

def resolveDates(date1, date2):
	checkDate(str(date1))
	checkDate(str(date2))
	
	d1 =  datetime.strptime(date1, '%Y-%m-%d')
	d2 =  datetime.strptime(date2, '%Y-%m-%d')
	
	if d1 > d2:
		printMessageAndShowMenu('Start date cannot be greater than end date')
		
	timeNow = datetime.now()
	
	if d1 > timeNow or d2 > timeNow:
		printMessageAndShowMenu('dates cannot be grater than current date')
		
	delta = d2 - d1
	
	if delta.days > 365:
		printMessageAndShowMenu('Cannot searh for this date range')
		
	dateList = []
	
	for i in range(delta.days + 1):
		dt = d1 + timedelta(days=i)
		value = str(dt).split(' ')[0]
		dateList.append(value)
		
	return dateList

def printMessageAndShowMenu(message):
	print(message)
	showMenu()

def checkDate(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Cannot read date entered, the format should be YYYY-MM-DD")
		
showMenu()