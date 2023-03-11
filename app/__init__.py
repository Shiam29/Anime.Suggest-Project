from flask import Flask, render_template, session, request, redirect
from app.routes.anime import anime
from app.routes.auth import auth
from app.db import db_connection
import os


app = Flask(__name__)
app.register_blueprint(auth)
app.register_blueprint(anime)
# Set the secret key for sessions
app.secret_key = 'shiem29'

# For deployment
if os.environ.get('DATABASE_URL'):
  cursor = db_connection.cursor()
  cursor.execute("DROP TABLE IF EXISTS users CASCADE;")
  cursor.execute("DROP TABLE IF EXISTS anime CASCADE;")

  cursor.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name VARCHAR(50), email VARCHAR(50), password TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")
  cursor.execute("CREATE TABLE IF NOT EXISTS anime (id SERIAL PRIMARY KEY,name VARCHAR(50),year INT,image_url VARCHAR(200));")



@app.before_request
def is_users_logged_in():
  path = request.path

  if path != '/login' and path != '/signup' and session.get('user_id') is None and request.method == 'POST':
    return redirect('/login')

@app.get('/signup')
def render_signup_page():
  return render_template('signup.html')


@app.get('/login')
def render_login_page():
  return render_template('login.html')


@app.get('/create')
def add_anime():
    return render_template("new_anime.html")


@app.route('/')
def index():
  db_cursor = db_connection.cursor()
  db_cursor.execute("SELECT id, name, year, image_url FROM anime;")
  rows = db_cursor.fetchall() 
  
  anime = []
  for row in rows:
    anime.append(
      {
        "id": row[0],
        "name": row[1],
        "year": row[2],
        "image_url": row[3],
      }
    )
  db_cursor.close()

  return render_template('home.html', anime=anime, user_name=session.get('user_name', 'UNKNOWN'))