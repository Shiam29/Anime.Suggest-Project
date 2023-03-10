from flask import Flask, render_template, request, redirect, session, url_for
from app.routes.anime import anime
import psycopg2
from app.db import db_connection
import os

app = Flask(__name__)
app.register_blueprint(anime)

if os.environ.get('DATABASE_URL'):
  cursor = db_connection.cursor()
  cursor.execute("DROP TABLE IF EXISTS users CASCADE;")
  cursor.execute("DROP TABLE IF EXISTS anime CASCADE;")

  cursor.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name VARCHAR(50), email VARCHAR(50), password VARCHAR(100), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")
  cursor.execute("CREATE TABLE IF NOT EXISTS anime (id SERIAL PRIMARY KEY,name VARCHAR(50),year INT,image_url VARCHAR(200));")

# Set the secret key for sessions
app.secret_key = 'shiem29'

@app.get('/signup')
def render_signup_page():
  return render_template('signup.html')

@app.post('/signup')
def signup_user():
  db_cursor = db_connection.cursor()

  name = request.form.get('name')
  email = request.form.get('email')
  password = request.form.get('password')

  db_cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                    [name, email, password])

  db_connection.commit()

  db_cursor.execute("SELECT id, name, email, password FROM users WHERE email = %s;", [email])
  result = db_cursor.fetchall()

  db_cursor.close()

  if len(result) == 0:
    return redirect('/login')
  else:
    session['user_id'] = result[0][0]
    session['user_name'] = result[0][1]
    session['user_email'] = result[0][2]
    return redirect('/')

@app.get('/signup')
def signup_page():
  return render_template('signup.html')

@app.before_request
def is_users_logged_in():
  path = request.path

  if path != '/login' and path != '/signup' and session.get('user_id') is None and request.method == 'POST':
    return redirect('/login')

@app.post('/logout')
def logout_user():
  session.pop('user_id')
  session.pop('user_name')
  session.pop('user_email')

  return render_template('login.html')

@app.get('/login')
def render_login_page():
  return render_template('login.html')

@app.post('/login')
def login_user():
  user_email = request.form.get('email')
  db_cursor = db_connection.cursor()

  db_cursor.execute("SELECT id, name, email, password FROM users WHERE email = %s;", [user_email])
  result = db_cursor.fetchall()

  db_cursor.close()

  if len(result) == 0:
    return redirect('/login')
  else:
    if request.form.get('password') != result[0][3]:
      return redirect('/login', 401)

    session['user_id'] = result[0][0]
    session['user_name'] = result[0][1]
    session['user_email'] = result[0][2]
    return redirect('/')

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