from flask import Blueprint, jsonify, request, current_app
import os
import sqlite3

api_bp = Blueprint('api', __name__)

def get_db():
    db_path = current_app.config['DATABASE']
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@api_bp.route('/stats')
def stats():
    conn = get_db()
    videos = conn.execute('SELECT COUNT(*) as count FROM videos').fetchone()['count']
    audios = conn.execute('SELECT COUNT(*) as count FROM audios').fetchone()['count']
    games = conn.execute('SELECT COUNT(*) as count FROM games').fetchone()['count']
    stories = conn.execute('SELECT COUNT(*) as count FROM stories').fetchone()['count']
    conn.close()
    return jsonify({'videos': videos, 'audios': audios, 'games': games, 'stories': stories})

@api_bp.route('/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])

    conn = get_db()
    results = []

    # Search videos
    videos = conn.execute("SELECT id, title, 'video' as type FROM videos WHERE title LIKE ?", (f'%{query}%',)).fetchall()
    results.extend([dict(v) for v in videos])

    # Search audios
    audios = conn.execute("SELECT id, title, 'audio' as type FROM audios WHERE title LIKE ?", (f'%{query}%',)).fetchall()
    results.extend([dict(a) for a in audios])

    # Search stories
    stories = conn.execute("SELECT id, title, 'story' as type FROM stories WHERE title LIKE ?", (f'%{query}%',)).fetchall()
    results.extend([dict(s) for s in stories])

    conn.close()
    return jsonify(results)
