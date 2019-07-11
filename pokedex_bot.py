import tweepy
from bs4 import BeautifulSoup
import requests

# Llaves de acceso a la API de Twitter
consumer_key = ''
consumer_secret = '''
access_token = ''
access_secret = '' 

# Creación de app con tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)    
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

# webscrap de wikidex y reply a usuario con descripción de pokémon y la url para más información
def reply_poke(username, pokemon, status_id):
	url = 'https://www.wikidex.net/wiki/'+pokemon
	page_response = requests.get(url, timeout=5)
	soup = BeautifulSoup(page_response.content, "html.parser")
	parrafo = soup.body.find_all('p')
	descrption = parrafo[0].text
	index = descrption.find('generación')+10
	api.update_status(status='@'+username+' ' + descrption[:index] + '\n' + url, in_reply_to_status_id=status_id)

# stream del bot para leer los tweets que le hagan solicitando un pokémon
class MyBotStreamer(tweepy.StreamListener):

	def on_status(self, status):
		username = status.user.screen_name
		status_id = status.id
		poke = status.text
		pokemon = poke[14:]
		reply_poke(username, pokemon, status_id)


# Instancia del bot 
myTwitterbot = MyBotStreamer()
stream = tweepy.Stream(auth, myTwitterbot)
stream.filter(track=['@litepokedex'])
	
	

