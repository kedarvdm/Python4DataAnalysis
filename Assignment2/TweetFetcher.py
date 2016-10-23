import os
import json
import requests
import argparse
from requests_oauthlib import OAuth1
from datetime import datetime,date,timedelta
import urllib

CONSUMER_KEY = "ryxOkcrWcED4fXXtVP0GPRJuA"
CONSUMER_SECRET = "xWtgC6bScNgDU2LaOl42gAdbvEmHEfCpOJoCPz5yofLKhaU75V"
OAUTH_TOKEN = "154482426-WSqWuzGOfhessNSlg8wttW1mSwNazvCDLORTMN78"
OAUTH_TOKEN_SECRET = "brpAKavkEv6HlsPu5YBgr5tnZEJS1EZdMV4GKufAqmA0e"

oauth = OAuth1(CONSUMER_KEY,  
         client_secret=CONSUMER_SECRET,  
         resource_owner_key=OAUTH_TOKEN,  
         resource_owner_secret=OAUTH_TOKEN_SECRET)
		 
		 
def generateTweets():
	#Read the input arguments
	search, count, lang = parseInput()
	search = search.rstrip().lower()
	
	for searchItem in search.split(','):
		print('Searching for:{0} Count:{1} Language:{2}'.format(searchItem, count, lang))
		print('fetching tweets for: '+searchItem)
		urlifysearch = urllib.parse.quote(searchItem)
		timeNow = datetime.now()
		filename = timeNow.strftime('%Y-%m-%d_%H_%M_%S')+".json"
		savePath =  "tweets/"+searchItem+"/"+str(timeNow.year)+"-"+str(timeNow.month)+"-"+str(timeNow.day)
		fullpath = savePath+"/"+filename
		r = requestTweets(urlifysearch,count, lang)
		if r!=None:
			#Create if not exists
			os.makedirs(savePath, mode=0o777, exist_ok=True)
			with open(savePath+"/"+filename, 'w') as outfile:
				json.dump(r.json(), outfile)
		else:
			print('Cannot download tweets for: '+searchItem)
			

def requestTweets(search, count, lang):
	url="https://api.twitter.com/1.1/search/tweets.json?q={0}&count={1}&lang={2}&result_type=recent".format(search,count, lang)
	print(url)
	r = None
	try:
		if search != '':
			r = requests.get(url, auth=oauth)
			print(r.status_code)
		else:
			print('Invalid search term provided')
	except requests.ConnectionError:
		print("failed to connect")
	return r
		
def parseInput():
	parser = argparse.ArgumentParser()
	parser.add_argument("search", help="Enter the search term")
	parser.add_argument("--count", help="Enter the desired number of tweets, max allowed is 100", type=int, default=15)
	parser.add_argument("--lang", help="Enter the desired languange of the tweet", default='')
	args = parser.parse_args()
	if args.search == '':
		sys.exit('Search parameter is required')
	return args.search,args.count,args.lang


def checkFolder(path,name):
	filePath=path+"/"+name
	return os.path.isdir(filePath)

def createFolder(path,name):
	fullpath = path+"/"+name
	os.makedirs(fullpath)

generateTweets()