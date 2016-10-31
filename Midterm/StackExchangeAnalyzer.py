import os
import json
import requests
from datetime import datetime,date,timedelta
import urllib
import glob
from operator import itemgetter
import csv
import datetime as dt
import sys

#Obtained from stack exchange app
APP_KEY = 'IDWxeTfJypl6G15Nm)h8rg(('
BASE_URL = 'https://api.stackexchange.com/2.2/'
TAGS_URL = 'tags'
BADGES_URL = 'badges'
QUESTIONS_URL = 'questions'
USERS_URL = 'users/'

def showMenu():
	print("Stack Exchange Analysis")
	print("1. User With Longest Activity")
	print("2. Users Per Age Range")
	print("3. Top User Count Per Badge")
	print("4. Tags With Popular Users")
	print("5. Top Questions Per Weightage")
	print("6. Top Tags Among All The Questions")
	print("7. Exit")
	
	reportsFolderExists = os.path.exists('reports')
	if not reportsFolderExists:
		os.mkdir('reports', mode=0o777 )
		
	userInput = input('Enter your choice: ')
	print(userInput)
	if userInput == '1':
		getLogestActiveUser()
		showMenu()
	elif userInput == '2':
		getUsersPerAgeRange()
		showMenu()
	elif userInput == '3':
		getTopUserCountPerBadge()
		showMenu()
	elif userInput == '4':
		getTagsWithPopularUsers()
		showMenu()
	elif userInput == '5':
		#Ask user input
		getTopQuestionsWithWeightage()
		showMenu()
	elif userInput == '6':
		getTopTagsFromQuestions()
		showMenu()
	elif userInput == '7':
		sys.exit(0)
	else:
		sys.exit(0)
		
def getLogestActiveUser():
	logestactiveuseredict = {}
	fileNames = glob.glob('userprofiles/*.json')
	if not fileNames:
		print('Plese Download Data First')
		return
		
	for fileName in fileNames:
		with open(fileName, 'r') as outfile:
			data = json.load(outfile)
			creation_date = dt.datetime.fromtimestamp(data['creation_date'])
			creation_date = creation_date.replace(hour=0, minute=0, second=0, microsecond=0)
			last_access_date = dt.datetime.fromtimestamp(data['last_access_date'])
			last_access_date = last_access_date.replace(hour=0, minute=0, second=0, microsecond=0)
			activedays = last_access_date - creation_date 
			user_id = data['last_access_date']
			display_name = data['display_name'] 
			link = data['link']
			logestactiveuseredict[user_id] = {'display_name':display_name,'link':link, 'days':activedays.days}
			
	sorted_keys = sorted(logestactiveuseredict.keys(), key=lambda y: (logestactiveuseredict[y]['days']), reverse=True)
	dumpTag = open('reports/LogestActiveUser.csv', 'w', newline='', encoding='utf-8')
	try:
		writer = csv.writer(dumpTag)
		writer.writerow( ('user_id','display_name', 'link', 'days') )
		for key in sorted_keys:
			if logestactiveuseredict[key]['days'] > 0:
				writer.writerow((key,logestactiveuseredict[key]['display_name'], logestactiveuseredict[key]['link'], logestactiveuseredict[key]['days'] ))
	finally:
		dumpTag.close()
		
def getUsersPerAgeRange():
	useragerangedict = {}
	fileNames = glob.glob('userprofiles/*.json')
	if not fileNames:
		print('Plese Download Data First')
		return
		
	for fileName in fileNames:
		with open(fileName, 'r') as outfile:
			data = json.load(outfile)
			if 'age' in data:
				age = data['age']
				ageLabel = getAgeLabel(age)
				useragerangedict[ageLabel] = useragerangedict.get(ageLabel,0)+1
			else:
				useragerangedict['undefined'] = useragerangedict.get('undefined',0)+1

	sorted_keys = sorted(useragerangedict.keys(), key=lambda y: (useragerangedict[y]), reverse=True)
	dumpTag = open('reports/UsersPerAgeRange.csv', 'w', newline='', encoding='utf-8')
	try:
		writer = csv.writer(dumpTag)
		writer.writerow( ('age_range', 'users') )
		for key in sorted_keys:
			writer.writerow((key, useragerangedict[key]))
	finally:
		dumpTag.close()

def getAgeLabel(age):
	if age in range(0,11):
		return '0-10'
	elif age in range(11,21):
		return '11-20'
	elif age in range(21,31):
		return '21-30'
	elif age in range(31,41):
		return '31-40'
	elif age in range(41,51):
		return '41-50'
	elif age in range(51,61):
		return '51-60'
	elif age in range(61,71):
		return '61-70'
	elif age in range(71,81):
		return '71-80'
	elif age in range(81,91):
		return '81-90'
	elif age in range(91,101):
		return '91-100'
	else:
		return 'undefined'

def getTopUserCountPerBadge():
	fileNames = glob.glob('usersListWithBadges/*.json')
	if not fileNames:
		print('Plese Download Data First')
		return
		
	userbadgeDict = {}
	for fileName in fileNames:
		with open(fileName, 'r') as outfile:
			data = json.load(outfile)
			data = data['items']
			for dataNode in data:
				badge_id = dataNode['badge_id']
				badge_award_count = dataNode['award_count']
				#Check if badge_id already present
				if badge_id in userbadgeDict:
					userbadgeDict[badge_id]['count'] = userbadgeDict.get(badge_id).get('count') + badge_award_count
				else:
					#Make an entry if record not present
					badge_name = dataNode['name']
					badge_type = dataNode['badge_type']
					badge_rank = dataNode['rank']
					badge_link = dataNode['link']
					badge_award_count = dataNode['award_count']
					userbadgeDict[badge_id] = {'name':badge_name,'badge_type':badge_type ,'rank':badge_rank , 'link':badge_link, 'count':badge_award_count}
	
	sorted_keys = sorted(userbadgeDict.keys(), key=lambda y: (userbadgeDict[y]['count']), reverse=True)
	f = open('reports/TopUserCountPerBadge.csv', 'w', newline='')
	try:
		writer = csv.writer(f)
		writer.writerow( ('badge_id', 'name', 'badge_type', 'badge_rank', 'link', 'count') )
		for key in sorted_keys:
			writer.writerow((key, userbadgeDict[key]['name'], userbadgeDict[key]['badge_type'], userbadgeDict[key]['rank'], userbadgeDict[key]['link']+' ', userbadgeDict[key]['count']))
	finally:
		f.close()
		
def getTagsWithPopularUsers():

	reportsFolderExists = os.path.exists('reports/TagsWithPopularUsers')
	if not reportsFolderExists:
		os.mkdir('reports/TagsWithPopularUsers', mode=0o777 )
		
	tagsWithPopularUsersDict = {}
	fileNames = glob.glob('questions/*.json')
	if not fileNames:
		print('Plese Download Data First')
		return
		
	for fileName in fileNames:
		with open(fileName, 'r') as outfile:
			data = json.load(outfile)
			if 'items' in data:
				data = data['items']
				isTagPresent = True
				for dataNode in data:
					owner = dataNode['owner']
					if 'user_id' in owner:
						user_id = owner['user_id']
						display_name = owner['display_name'] 
						link = owner['link']
						reputation = owner['reputation']
						userdict = {'display_name':display_name,'link':link, 'reputation':reputation}
						tags = dataNode['tags']
						
						for tag in tags:
							if tag not in tagsWithPopularUsersDict:
								tagsWithPopularUsersDict[tag] = {}
							if user_id not in tagsWithPopularUsersDict[tag]:
								tagsWithPopularUsersDict[tag][user_id] = userdict

	for tag in tagsWithPopularUsersDict:
		data = tagsWithPopularUsersDict[tag]
		sorted_keys = sorted(data.keys(), key=lambda y: (data[y]['reputation']), reverse=True)
		dumpTag = open('reports/TagsWithPopularUsers/'+tag+'.csv', 'w', newline='', encoding='utf-8')
		try:
			writer = csv.writer(dumpTag)
			writer.writerow( ('user_id', 'display_name', 'link', 'reputation') )
			for key in sorted_keys:
				writer.writerow((key, data[key]['display_name'], data[key]['link']+' ', data[key]['reputation']))
		finally:
			dumpTag.close()

def getTopQuestionsWithWeightage():
	tags = input('Please enter the tags (Comma separated): ')
	
	questionWeightageDict = {}
	fileNames = glob.glob('questions/*.json')
	if not fileNames:
		print('Plese Download Data First')
		return
	
	taglist = getTags(tags)
	print(taglist)
	for fileName in fileNames:
		with open(fileName, 'r') as outfile:
			data = json.load(outfile)
			if 'items' in data:
				data = data['items']
				isTagPresent = True
				for dataNode in data:
					isTagPresent = all(x in dataNode['tags'] for x in taglist)
					if isTagPresent:
						question_id = dataNode['question_id']
						question_link = dataNode['link']
						questionWeightageDict[question_id] = {'link': question_link,'user_id':0,'weightage':0}
						if 'user_id' in dataNode['owner']:
							user_id = dataNode['owner']['user_id']
							weightage = getWeightage(user_id)
							questionWeightageDict[question_id] = {'link': question_link,'user_id':user_id,'weightage':weightage}
	
	sorted_keys = sorted(questionWeightageDict.keys(), key=lambda y: (questionWeightageDict[y]['weightage']), reverse=True)
	
	f = open('reports/TopQuestionsPerWeightage.csv', 'w', newline='')
	try:
		writer = csv.writer(f)
		writer.writerow( ('question_id', 'link', 'user_id', 'weightage') )
		for key in sorted_keys:
			writer.writerow((key, questionWeightageDict[key]['link']+' ', questionWeightageDict[key]['user_id'], questionWeightageDict[key]['weightage']))
	finally:
		f.close()

def getTags(tags):
	tags = tags.strip().lower()
	taglist = tags.split(',')
	taglist = [n.strip() for n in taglist]
	return taglist

	
def getWeightage(user_id):
	filePath = 'userprofiles/user_'+str(user_id)+'.json'
	exists = os.path.exists(filePath)
	
	weightage = 0
	if exists:
		with open(filePath, 'r') as outfile:
			data = json.load(outfile)
			if 'badge_counts' in data:
				badgeData = data['badge_counts']
				if 'bronze' in badgeData:
					weightage = weightage + (badgeData['bronze']*3)
				
				if 'silver' in badgeData:
					weightage = weightage + (badgeData['silver']*5)
					
				if 'gold' in badgeData:
					weightage = weightage + (badgeData['gold']*10)
		
	return weightage
	
def getTopTagsFromQuestions():
	tagsCountDict = {}
	fileNames = glob.glob('questions/*.json')
	if not fileNames:
		print('Plese Download Data First')
		return
		
	for fileName in fileNames:
		with open(fileName, 'r') as outfile:
			data = json.load(outfile)
			if 'items' in data:
				data = data['items']
				for dataNode in data:
					taglist = dataNode['tags']
					for tag in taglist:
						tagsCountDict[tag] = tagsCountDict.get(tag, 0)+1

	sorted_keys = sorted(tagsCountDict.keys(), key=lambda y: (tagsCountDict[y]), reverse=True)
	dumpTag = open('reports/TopTags.csv', 'w', newline='', encoding='utf-8')
	try:
		writer = csv.writer(dumpTag)
		writer.writerow( ('tag', 'count') )
		for key in sorted_keys:
			writer.writerow((key, tagsCountDict[key]))
	finally:
		dumpTag.close()
		
showMenu()