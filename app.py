from flask import Flask, render_template, request, redirect, session, url_for
import psycopg2

app = Flask(__name__)

# Set the secret key for sessions
app.secret_key = 'shiem29'

@app.before_request
def is_users_logged_in():
  path = request.path

  if path != '/login' and session.get('user_id') is None:
    return redirect('/login')

@app.post('/logout')
def logout_user():
  session.pop('user_id')
  session.pop('user_name')
  session.pop('user_email')
  session.pop('user_password')

  return render_template('login.html')

@app.get('/login')
def render_login_page():
  return render_template('login.html')

@app.post('/login')
def login_user():
  user_email = request.form.get('email')
  db_connection = psycopg2.connect("dbname=library")
  db_cursor = db_connection.cursor()

  db_cursor.execute("SELECT id, name, email, password FROM users WHERE email = %s;", [user_email])
  result = db_cursor.fetchall()

  db_cursor.close()
  db_connection.close()

  if len(result) == 0:
    return redirect('/login')
  else:
    session['user_id'] = result[0][0]
    session['user_name'] = result[0][1]
    session['user_email'] = result[0][2]
    session['user_password'] = result[0][3]
    return redirect('/')

@app.get('/create')
def add_food_item():
    return render_template("new_anime.html")

@app.route('/')
def index():
  db_connection = psycopg2.connect("dbname=library")
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

  return render_template('home.html', anime=anime, user_name=session.get('user_name', 'UNKNOWN'))

@app.post('/anime/<int:id>/edit')
def update_food_item(id):
    db_connection = psycopg2.connect("dbname=library")
    db_cursor = db_connection.cursor()

    anime = {
        "name": request.form['name'],
        "year": request.form['price'],
        "image_url": request.form['image_url']
    }

    db_cursor.execute("UPDATE anime SET name = %s, year = %s, image_url = %s WHERE id = %s",
                      [anime['name'], anime['price'], anime['image_url'], id])

    db_connection.commit()
    db_cursor.close()
    db_connection.close()

    return redirect('/')


@app.get('/anime/<int:id>/edit')
def edit_food_item(id):
    db_connection = psycopg2.connect("dbname=library")
    db_cursor = db_connection.cursor()

    db_cursor.execute("SELECT id, name, year, image_url FROM anime WHERE id = %s", [id])

    row = db_cursor.fetchone()

    if row is None:
        return "Anime not found", 404

    anime = {
        "id": row[0],
        "name": row[1],
        "year": row[2],
        "image_url": row[3],
    }

    db_cursor.close()
    db_connection.close()

    return render_template('edit_item.html', anime=anime)

@app.post('/food-items/<int:id>/delete')
def delete_food_item(id):
    db_connection = psycopg2.connect("dbname=library")
    db_cursor = db_connection.cursor()

    db_cursor.execute("DELETE FROM anime WHERE id = %s", [id])

    db_connection.commit()
    db_cursor.close()
    db_connection.close()

    return redirect('/')
