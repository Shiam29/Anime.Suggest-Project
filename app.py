from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2

app = Flask(__name__)

# Set the secret key for sessions
app.secret_key = 'shiem29'

@app.before_request
def is_users_logged_in():
  path = request.path

  if path != '/login' and session.get('users_id') is None:
    return redirect('/login')

@app.post('/logout')
def logout_user():
  session.pop('users_id')
  session.pop('users_name')
  session.pop('users_email')
  session.pop('users_password')

  return render_template('login.html')

@app.get('/login')
def render_login_page():
  return render_template('login.html')

@app.post('/login')
def login_user():
  user_email = request.form.get('email')
  db_connection = psycopg2.connect("dbname=anime")
  db_cursor = db_connection.cursor()

  db_cursor.execute("SELECT id, name, email, password FROM users WHERE email = %s;", [user_email])
  result = db_cursor.fetchall()

  db_cursor.close()
  db_connection.close()

  if result is None or len(result) < 3:
    return redirect('/login')
  else:
    session['users_id'] = result[0]
    session['users_name'] = result[1]
    session['users_email'] = result[2]
    session['users_password'] = result[3]
    return redirect('/')

@app.route('/')
def index():
  db_connection = psycopg2.connect("dbname=anime")
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
  db_connection.close()

  return render_template('home.html', anime=anime, users_name=session.get('users_name', 'UNKNOWN'))
