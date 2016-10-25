1) Please run TweetFetcher to generate the tweets.
2) Then run the TweetAnalyzer to permorm the analysis.

TweetFetcher
Function- Fetches tweets from rest api using requests.
Required paramaters:
searchTerm		(e.g. python TweetFetcher.py "#trump, #hilary")
		You can give comma separated search terms
		
Optional Parameters:
1) --count  (e.g. python TweetFetcher.py "#trump, #hilary" --count=20)	default is 15 tweets
2) --lang	(e.g. python TweetFetcher.py "#trump, #hilary" --lang=fr)	default is no lang

Creates a folder for search term and the date the term was searched

TweetAnalyser
Function- Analyze the stored data stored using the TweetFetcher.
Used input for reports