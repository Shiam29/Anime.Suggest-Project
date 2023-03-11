from flask import Blueprint, request, redirect, render_template, session;
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import db_connection

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.post('/signup')
def signup_user():
  db_cursor = db_connection.cursor()

  name = request.form.get('name')
  email = request.form.get('email')
  password = request.form.get('password')
  password_hash = generate_password_hash(password)

  db_cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                    [name, email, password_hash])

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

@auth.post('/login')
def login_user():
  user_email = request.form.get('email')
  db_cursor = db_connection.cursor()

  db_cursor.execute("SELECT id, name, email, password FROM users WHERE email = %s;", [user_email])
  result = db_cursor.fetchall()

  db_cursor.close()

  if len(result) == 0:
    return redirect('/login')
  else:
    if not check_password_hash(result[0][3], request.form.get('password')):
      return redirect('/login', 401)

    session['user_id'] = result[0][0]
    session['user_name'] = result[0][1]
    session['user_email'] = result[0][2]
    return redirect('/')


@auth.post('/logout')
def logout_user():
  session.pop('user_id')
  session.pop('user_name')
  session.pop('user_email')

  return render_template('login.html')