import tweepy
from bs4 import BeautifulSoup
import requests

consumer_key = '8DCdltFnoSu1U9gUY25QtnjoR'
consumer_secret = '4wdCN0Aw34sWS4zpWh0xb3fzOCoAUrbKbBxo6izuhYo7YVWGY2'
access_token = '3445803260-9JT4v6sq1RtHPN0dZ0iE4qwbc0B0vtb9VtcFmCj'
access_secret = 'w1JC3HWF6fuaRGz99d6H3r2TshvAIR6HT1eD7wH9N32N0' 

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)    
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

def reply_poke(username, pokemon, status_id):
	url = 'https://www.wikidex.net/wiki/'+pokemon
	page_response = requests.get(url, timeout=5)
	soup = BeautifulSoup(page_response.content, "html.parser")
	parrafo = soup.body.find_all('p')
	descrption = parrafo[0].text
	index = descrption.find('generación')+10
	api.update_status(status='@'+username+' ' + descrption[:index] + '\n' + url, in_reply_to_status_id=status_id)

class MyBotStreamer(tweepy.StreamListener):

	def on_status(self, status):
		username = status.user.screen_name
		status_id = status.id
		poke = status.text
		pokemon = poke[14:]
		reply_poke(username, pokemon, status_id)


myTwitterbot = MyBotStreamer()
stream = tweepy.Stream(auth, myTwitterbot)
stream.filter(track=['@litepokedex'])
	
	

