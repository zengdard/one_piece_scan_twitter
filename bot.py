import os
import tweepy
import requests
from bs4 import BeautifulSoup


my_secret = os.environ['api key']
my_secret3 = os.environ['api secret']
my_secret2 = os.environ['acces token']
my_secret1 = os.environ['token secret']

API_KEY = my_secret
API_SECRET = my_secret3
ACCESS_TOKEN = my_secret2
ACCESS_TOKEN_SECRET = my_secret1

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN,
                                ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

chapitre = "#"

sommaire = requests.get('https://onepiecechapters.com/mangas/5/one-piece')
soup = BeautifulSoup(sommaire.content, "html.parser")
results2 = soup.find(class_='block border border-border bg-card mb-3 p-3 rounded')

ifo = results2.text
d = 0
for lettre in ifo :
  d = d +1
  for chiffre in range(0,10):
    #print(chiffre)
    if lettre == str(chiffre):
      chapitre= chapitre + lettre
      
    if d == 4 :
      break


#print(results2.get('href'))


URL = f"https://onepiecechapters.com{results2.get('href')}"
print(URL)
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find_all("picture")

#print(results)
images = []
adresse = []
for image in results:
    images.append(image.find('img').get('src'))
    #print(image)

for url in images:
    adresse.append(url)

adresse.pop(1)
import os
c = 1
for urls in adresse:
    try:
      f = open(f'{c}.jpg', '+wb')
      response = requests.get(urls)
      f.write(response.content)
      f.close()
    except:
      pass
    try:
      file = open(f'{c}.jpg', 'rb')
      r2 = api.media_upload(filename =f'{c}.jpg', file = file )
    except:
      pass
    media_ids = [r2.media_id_string]
    api.update_status(media_ids=media_ids, status=(f"{ifo.upper()} \n{c}/{len(adresse)} \n#onepiecescan #onepiece {chapitre.upper()}" ))
    
    os.remove(f"{c}.jpg")
    c = c + 1

