import json
import requests
import urllib.request
import re
from PIL import Image
import time

tmdbkey = ""

def getImage(imId, imType):
  if imType == 'poster':
    url = 'https://image.tmdb.org/t/p/w300_and_h450_bestv2{}'
    p_id = re.sub('\/', '', imId)
    path = 'posters/'
  elif imType == 'backdrop':
    url = 'https://image.tmdb.org/t/p/w1920_and_h800_multi_faces/{}'
    p_id = re.sub('\/', '', imId)
    path = 'backdrops/'
  fname = path + p_id
  try:
    urllib.request.urlretrieve(url.format(imId), fname)
  except:
    print(f'no {imType} for {imId}')
    pass

def resizeImg(imName, imType):
  if imType == 'poster':
    openpath = 'posters'
    savepath = 'posters/xs'
    basewidth = 150 #pixels
  elif imType == 'backdrop':
    openpath = 'backdrops'
    savepath = 'backdrops/thumbnails'
    basewidth = 500 #pixels
  #try open image
  try:
    img = Image.open(openpath + imName)
    # determine height ratio
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    # resize image and save
    img = img.resize((basewidth,hsize), Image.ANTIALIAS)
    img.save(savepath + imName)
  except:
    print(f'failed to resize image {imName}')
    pass

def getMovieData(id):
  murl = 'https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US'
  vurl = 'https://api.themoviedb.org/3/movie/{}/videos?api_key={}&language=en-US'

  res = requests.get(murl.format(id, tmdbkey))
  mdata = res.json()
  res = requests.get(vurl.format(id, tmdbkey))
  vdata = res.json()
  
  genres = []
  trailers = []

  for x in mdata['genres']:
    genres.append(x['name'])
  for x in vdata['results']:
    trailers.append(x['key'])
  
  movie = {
    'tmdb_id': mdata['id'],
    'title': mdata['title'],
    'tagline': mdata['tagline'],
    'release_date': mdata['release_date'],
    'runtime': mdata['runtime'],
    'genres': genres,
    'overview': mdata['overview'],
    'poster': mdata['poster_path'],
    'backdrop': mdata['backdrop_path'],
    'trailers': trailers
  }
  
  if movie['poster'] != '':
    getImage(movie['poster'], 'poster')
    resizeImg(movie['poster'], 'poster')
  if movie['backdrop'] != '':
    getImage(movie['backdrop'], 'backdrop')
    resizeImg(movie['backdrop'], 'backdrop')

  time.sleep(res.elapsed.total_seconds())

  return movie

# json file with any key name and the value is the tmdb id
with open('xdata.json', 'r') as f:
    jsondata = json.load(f)
zz = len(jsondata)

movs = []

for item in jsondata:
  m_id = item['tmdb_id']
  movieinfo = getMovieData(m_id)
  movs.append(movieinfo)
  print(f"Got movie {zz}")
  zz -= 1

with open('movies_200928.json', 'w') as f:
    json.dump(movs, f, indent=2)

