import json
import requests
import urllib.request
import re
from PIL import Image
import time

tmdbkey = ""

def downPoster(id):
  try:
    url = 'https://image.tmdb.org/t/p/w300_and_h450_bestv2{}'
    p_id = re.sub('\/', '', id)
    path = 'posters/'
    fname = path + p_id
    urllib.request.urlretrieve(url.format(id), fname)
  except:
    print(f'no poster for {id}')
    pass

def downBackdrop(id):
  try:
    url = 'https://image.tmdb.org/t/p/w1920_and_h800_multi_faces/{}'
    p_id = re.sub('\/', '', id)
    path = 'backdrops/'
    fname = path + p_id
    urllib.request.urlretrieve(url.format(id), fname)
  except:
    print(f'no backdrop for {id}')
    pass

def resizeBackdrop(imgname):
  try:
    # open img
    img = Image.open('backdrops' + imgname)
    basewidth = 500
    # determining the height ratio
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    # resize image and save
    img = img.resize((basewidth,hsize), Image.ANTIALIAS)
    img.save('backdrops/thumbnails' + imgname)
  except:
    pass

def resizePoster(imgname):
  try:
    # open img
    img = Image.open('posters' + imgname)
    basewidth = 150
    # determining the height ratio
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    # resize image and save
    img = img.resize((basewidth,hsize), Image.ANTIALIAS)
    img.save('posters/xs' + imgname)
  except:
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
    downPoster(movie['poster'])
    resizePoster(movie['poster'])
  if movie['backdrop'] != '':
    downBackdrop(movie['backdrop'])
    resizeBackdrop(movie['backdrop'])

  time.sleep(res.elapsed.total_seconds())

  return movie


with open('xdata_200607.json', 'r') as f:
    jsondata = json.load(f)
zz = len(jsondata)

movs = []

for item in jsondata:
  m_id = item['tmdb_id']
  movieinfo = getMovieData(m_id)
  movs.append(movieinfo)
  print(f"Got movie {zz}")
  zz -= 1

with open('movies_200523.json', 'w') as f:
    json.dump(movs, f, indent=2)

