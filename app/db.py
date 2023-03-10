import psycopg2
import urllib.parse as urlparse
import os

url = urlparse.urlparse(os.environ.get('DATABASE_URL'))
dbname = url.path[1:]
user = url.username
password = url.password
host = url.hostname
port = url.port

db_connection = psycopg2.connect(
    dbname=dbname,
    user=user,
    password=password,
    host=host,
    port=port
) if os.environ.get('DATABASE_URL') else psycopg2.connect('dbname=library')