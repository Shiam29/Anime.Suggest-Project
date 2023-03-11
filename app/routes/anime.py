from flask import Blueprint, request, redirect, render_template;
from app.db import db_connection

anime = Blueprint('anime', __name__, template_folder='templates', url_prefix='/anime')

@anime.post('/')
def create_anime():
    db_cursor = db_connection.cursor()

    name = request.form.get('name')
    year = request.form.get('year')
    image_url = request.form.get('image_url')

    db_cursor.execute("INSERT INTO anime (name, year, image_url) VALUES (%s, %s, %s)",
                    [name, year, image_url])

    db_connection.commit()
    db_cursor.close()

    return redirect('/')

@anime.post('/<int:id>/edit')
def update_anime(id):
    db_cursor = db_connection.cursor()

    anime = {
        "name": request.form['name'],
        "year": request.form['year'],
        "image_url": request.form['image_url']
    }

    db_cursor.execute("UPDATE anime SET name = %s, year = %s, image_url = %s WHERE id = %s",
                      [anime['name'], anime['year'], anime['image_url'], id])

    db_connection.commit()
    db_cursor.close()

    return redirect('/')


@anime.get('/<int:id>/edit')
def edit_anime(id):
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

    return render_template('edit_item.html', anime=anime)

@anime.post('/<int:id>/delete')
def delete_anime(id):
    db_cursor = db_connection.cursor()

    db_cursor.execute("DELETE FROM anime WHERE id = %s", [id])

    db_connection.commit()
    db_cursor.close()

    return redirect('/')
