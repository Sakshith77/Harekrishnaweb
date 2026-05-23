import os
import sqlite3
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from werkzeug.utils import secure_filename

video_bp = Blueprint('video', __name__, template_folder='../templates')

ALLOWED_VIDEO = {'mp4', 'webm', 'ogg', 'm3u8', 'mkv', 'avi'}

def get_db():
    db_path = current_app.config['DATABASE']
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_video_table():
    conn = get_db()
    conn.execute("""CREATE TABLE IF NOT EXISTS videos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        category TEXT,
        file_path TEXT,
        hls_url TEXT,
        is_link INTEGER DEFAULT 0,
        upload_date TEXT,
        file_size INTEGER
    )""")
    conn.commit()
    conn.close()

@video_bp.route('/')
def index():
    init_video_table()
    conn = get_db()
    videos = conn.execute('SELECT * FROM videos ORDER BY upload_date DESC').fetchall()
    conn.close()
    return render_template('video.html', videos=videos)

@video_bp.route('/upload', methods=['POST'])
def upload():
    init_video_table()
    title = request.form.get('title', 'Untitled')
    description = request.form.get('description', '')
    category = request.form.get('category', 'General')
    hls_url = request.form.get('hls_url', '')

    conn = get_db()

    if hls_url:
        conn.execute('INSERT INTO videos (title, description, category, hls_url, is_link, upload_date) VALUES (?, ?, ?, ?, 1, ?)',
                     (title, description, category, hls_url, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        flash('HLS stream added successfully!', 'success')
        return redirect(url_for('video.index'))

    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('video.index'))

    file = request.files['file']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('video.index'))

    filename = secure_filename(file.filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER_VIDEOS'], filename)
    file.save(file_path)
    file_size = os.path.getsize(file_path)

    conn.execute('INSERT INTO videos (title, description, category, file_path, is_link, upload_date, file_size) VALUES (?, ?, ?, ?, 0, ?, ?)',
                 (title, description, category, filename, datetime.now().isoformat(), file_size))
    conn.commit()
    conn.close()
    flash('Video uploaded successfully!', 'success')
    return redirect(url_for('video.index'))

@video_bp.route('/play/<int:video_id>')
def play(video_id):
    init_video_table()
    conn = get_db()
    video = conn.execute('SELECT * FROM videos WHERE id = ?', (video_id,)).fetchone()
    conn.close()
    if not video:
        flash('Video not found', 'error')
        return redirect(url_for('video.index'))
    return render_template('video_player.html', video=video)

@video_bp.route('/delete/<int:video_id>', methods=['POST'])
def delete(video_id):
    init_video_table()
    conn = get_db()
    video = conn.execute('SELECT * FROM videos WHERE id = ?', (video_id,)).fetchone()
    if video and not video['is_link'] and video['file_path']:
        try:
            os.remove(os.path.join(current_app.config['UPLOAD_FOLDER_VIDEOS'], video['file_path']))
        except:
            pass
    conn.execute('DELETE FROM videos WHERE id = ?', (video_id,))
    conn.commit()
    conn.close()
    flash('Video deleted', 'success')
    return redirect(url_for('video.index'))
