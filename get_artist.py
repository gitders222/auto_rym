import requests
import urllib3.request
import time
from bs4 import BeautifulSoup


def get_song(url):

	headers = {
	        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',}
	response = requests.get(url,headers=headers)

	print(response)
	time.sleep(3)

	soup = BeautifulSoup(response.text, 'html.parser')

	linenr = 1
	album = []
	artist = []
	type_list = True

	def filter(string):
	    temp = string.replace('-', ' ')
	    temp = temp.replace('_', ' ')
	    filtered_string = temp
	    return filtered_string

	for link in soup.find_all('a'):
	    temp = link.get('href')
	    if temp != None:
	        if type_list:
	            if (('/release/album/' in temp) or ('/release/ep/' in temp) or ('/release/single/' in temp)): #!= ('?' in temp):
	                #print('temp', temp)
	                alb_split = temp.split('/')
	                alb_split[3] = filter(alb_split[3])
	                alb_split[4] = filter(alb_split[4])
	                alb_split[4] = alb_split[4][:-1]
	                if not album:
	                    album.append(alb_split[4])
	                if not artist:
	                    artist.append(alb_split[3])
	                if album[-1] != alb_split[4] and artist[-1] != alb_split[3]:
	                    album.append(alb_split[4])
	                    artist.append(alb_split[3])

	                    
	        #else:

	return album, artist
