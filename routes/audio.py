import os
import sqlite3
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename

audio_bp = Blueprint('audio', __name__, template_folder='../templates')

ALLOWED_AUDIO = {'mp3', 'wav', 'ogg', 'aac', 'flac', 'm4a'}

def get_db():
    db_path = current_app.config['DATABASE']
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_audio_table():
    conn = get_db()
    conn.execute("""CREATE TABLE IF NOT EXISTS audios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        artist TEXT,
        description TEXT,
        category TEXT,
        file_path TEXT NOT NULL,
        upload_date TEXT,
        file_size INTEGER,
        duration TEXT
    )""")
    conn.commit()
    conn.close()

@audio_bp.route('/')
def index():
    init_audio_table()
    conn = get_db()
    audios = conn.execute('SELECT * FROM audios ORDER BY upload_date DESC').fetchall()
    conn.close()
    return render_template('audio.html', audios=audios)

@audio_bp.route('/upload', methods=['POST'])
def upload():
    init_audio_table()
    title = request.form.get('title', 'Untitled')
    artist = request.form.get('artist', 'Unknown')
    description = request.form.get('description', '')
    category = request.form.get('category', 'General')

    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('audio.index'))

    file = request.files['file']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('audio.index'))

    filename = secure_filename(file.filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER_AUDIOS'], filename)
    file.save(file_path)
    file_size = os.path.getsize(file_path)

    conn = get_db()
    conn.execute('INSERT INTO audios (title, artist, description, category, file_path, upload_date, file_size) VALUES (?, ?, ?, ?, ?, ?, ?)',
                 (title, artist, description, category, filename, datetime.now().isoformat(), file_size))
    conn.commit()
    conn.close()
    flash('Audio uploaded successfully!', 'success')
    return redirect(url_for('audio.index'))

@audio_bp.route('/delete/<int:audio_id>', methods=['POST'])
def delete(audio_id):
    init_audio_table()
    conn = get_db()
    audio = conn.execute('SELECT * FROM audios WHERE id = ?', (audio_id,)).fetchone()
    if audio:
        try:
            os.remove(os.path.join(current_app.config['UPLOAD_FOLDER_AUDIOS'], audio['file_path']))
        except:
            pass
    conn.execute('DELETE FROM audios WHERE id = ?', (audio_id,))
    conn.commit()
    conn.close()
    flash('Audio deleted', 'success')
    return redirect(url_for('audio.index'))
