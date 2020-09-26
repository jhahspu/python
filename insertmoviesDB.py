import mysql.connector
from mysql.connector import Error
import json

try:
  conn = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="test"
  )
  if conn.is_connected():
        db_Info = conn.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        # cursor = connection.cursor()
        # cursor.execute("select database();")
        # record = cursor.fetchone()
        # print("You're connected to database: ", record)
except Error as e:
    print("Error while connecting to MySQL", e)


def read(db):
  print("reading..")
  cursor = db.cursor()
  sql = "SELECT * FROM testmov"

  try:
    print('...query')
    cursor.execute(sql)
    results = cursor.rowcount()
    print(results)
    for row in results:
      print (row[0])
  except Error as e:
    print("ERROR: unable to fetch data", e)

def create(db, tmdbid, title, tagline, releasedate, runtime, genres, overview, poster, backdrop, trailers, i):
  cursor = db.cursor()
  sql = """INSERT INTO movies(id,
   tmdb_id, title, tagline, release_date, runtime, genres, overview, poster, backdrop, trailers)
   VALUES (null, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
  val = (tmdbid, title, tagline, releasedate, runtime, genres, overview, poster, backdrop, trailers)
  try:
    cursor.execute(sql, val)
    db.commit()
    print("commited: " + str(i))
  except Error as e:
    db.rollback()
    print("ERROR: unable to add data", e)

# read(conn)

with open('movies_200607.json', 'r') as f:
  data = json.load(f)
i = len(data)

for d in data:
  m_id = d['tmdb_id']
  m_title = d['title']
  m_tagline = d['tagline']
  m_reldate = d['release_date']
  m_runtime = d['runtime']
  m_gens = ''
  for g in d['genres']:
    m_gens = m_gens + g + ' '
  m_overview = d['overview']
  m_poster = d['poster']
  m_backdrop = d['backdrop']
  m_trailers = ''
  for t in d['trailers']:
    m_trailers = m_trailers + t + ' '
  create(conn, m_id, m_title, m_tagline, m_reldate, m_runtime, m_gens, m_overview, m_poster, m_backdrop, m_trailers, i)
  i -= 1

conn.close()