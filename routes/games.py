import os
import sqlite3
import zipfile
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_from_directory
from werkzeug.utils import secure_filename

games_bp = Blueprint('games', __name__, template_folder='../templates')

def get_db():
    db_path = current_app.config['DATABASE']
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_games_table():
    conn = get_db()
    conn.execute("""CREATE TABLE IF NOT EXISTS games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        category TEXT,
        file_path TEXT,
        cover_image TEXT,
        is_embed INTEGER DEFAULT 0,
        embed_url TEXT,
        upload_date TEXT,
        folder_name TEXT
    )""")
    conn.commit()
    conn.close()

@games_bp.route('/')
def index():
    init_games_table()
    conn = get_db()
    games = conn.execute('SELECT * FROM games ORDER BY upload_date DESC').fetchall()
    conn.close()
    return render_template('games.html', games=games)

@games_bp.route('/upload', methods=['POST'])
def upload():
    init_games_table()
    title = request.form.get('title', 'Untitled Game')
    description = request.form.get('description', '')
    category = request.form.get('category', 'Arcade')
    embed_url = request.form.get('embed_url', '')

    conn = get_db()

    if embed_url:
        conn.execute('INSERT INTO games (title, description, category, embed_url, is_embed, upload_date) VALUES (?, ?, ?, ?, 1, ?)',
                     (title, description, category, embed_url, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        flash('Embedded game added!', 'success')
        return redirect(url_for('games.index'))

    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('games.index'))

    file = request.files['file']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('games.index'))

    filename = secure_filename(file.filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER_GAMES'], filename)
    file.save(file_path)

    # Handle zip extraction for HTML games
    folder_name = None
    if filename.endswith('.zip'):
        folder_name = filename[:-4]
        extract_path = os.path.join(current_app.config['UPLOAD_FOLDER_GAMES'], folder_name)
        os.makedirs(extract_path, exist_ok=True)
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

    cover = 'default_game.png'
    if 'cover' in request.files:
        cover_file = request.files['cover']
        if cover_file.filename:
            cover = secure_filename(cover_file.filename)
            cover_file.save(os.path.join(current_app.config['UPLOAD_FOLDER_IMAGES'], cover))

    conn.execute('INSERT INTO games (title, description, category, file_path, cover_image, upload_date, folder_name) VALUES (?, ?, ?, ?, ?, ?, ?)',
                 (title, description, category, filename, cover, datetime.now().isoformat(), folder_name))
    conn.commit()
    conn.close()
    flash('Game uploaded successfully!', 'success')
    return redirect(url_for('games.index'))

@games_bp.route('/play/<int:game_id>')
def play(game_id):
    init_games_table()
    conn = get_db()
    game = conn.execute('SELECT * FROM games WHERE id = ?', (game_id,)).fetchone()
    conn.close()
    if not game:
        flash('Game not found', 'error')
        return redirect(url_for('games.index'))
    return render_template('game_player.html', game=game)

@games_bp.route('/delete/<int:game_id>', methods=['POST'])
def delete(game_id):
    init_games_table()
    conn = get_db()
    game = conn.execute('SELECT * FROM games WHERE id = ?', (game_id,)).fetchone()
    if game:
        try:
            if game['file_path']:
                os.remove(os.path.join(current_app.config['UPLOAD_FOLDER_GAMES'], game['file_path']))
            if game['folder_name']:
                import shutil
                shutil.rmtree(os.path.join(current_app.config['UPLOAD_FOLDER_GAMES'], game['folder_name']), ignore_errors=True)
        except:
            pass
    conn.execute('DELETE FROM games WHERE id = ?', (game_id,))
    conn.commit()
    conn.close()
    flash('Game deleted', 'success')
    return redirect(url_for('games.index'))
