import os
import sqlite3
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename

stories_bp = Blueprint('stories', __name__, template_folder='../templates')

def get_db():
    db_path = current_app.config['DATABASE']
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_stories_table():
    conn = get_db()
    conn.execute("""CREATE TABLE IF NOT EXISTS stories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT,
        description TEXT,
        content TEXT,
        category TEXT,
        cover_image TEXT,
        upload_date TEXT,
        read_time TEXT
    )""")
    conn.commit()
    conn.close()

@stories_bp.route('/')
def index():
    init_stories_table()
    conn = get_db()
    stories = conn.execute('SELECT * FROM stories ORDER BY upload_date DESC').fetchall()
    conn.close()
    return render_template('stories.html', stories=stories)

@stories_bp.route('/upload', methods=['POST'])
def upload():
    init_stories_table()
    title = request.form.get('title', 'Untitled Story')
    author = request.form.get('author', 'Unknown')
    description = request.form.get('description', '')
    content = request.form.get('content', '')
    category = request.form.get('category', 'General')
    read_time = request.form.get('read_time', '5 min')

    cover = 'default_story.png'
    if 'cover' in request.files:
        cover_file = request.files['cover']
        if cover_file.filename:
            cover = secure_filename(cover_file.filename)
            cover_file.save(os.path.join(current_app.config['UPLOAD_FOLDER_IMAGES'], cover))

    conn = get_db()
    conn.execute('INSERT INTO stories (title, author, description, content, category, cover_image, upload_date, read_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                 (title, author, description, content, category, cover, datetime.now().isoformat(), read_time))
    conn.commit()
    conn.close()
    flash('Story added successfully!', 'success')
    return redirect(url_for('stories.index'))

@stories_bp.route('/read/<int:story_id>')
def read(story_id):
    init_stories_table()
    conn = get_db()
    story = conn.execute('SELECT * FROM stories WHERE id = ?', (story_id,)).fetchone()
    conn.close()
    if not story:
        flash('Story not found', 'error')
        return redirect(url_for('stories.index'))
    return render_template('story_reader.html', story=story)

@stories_bp.route('/delete/<int:story_id>', methods=['POST'])
def delete(story_id):
    init_stories_table()
    conn = get_db()
    conn.execute('DELETE FROM stories WHERE id = ?', (story_id,))
    conn.commit()
    conn.close()
    flash('Story deleted', 'success')
    return redirect(url_for('stories.index'))
