import os
import sqlite3
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from werkzeug.utils import secure_filename

other_bp = Blueprint('other', __name__, template_folder='../templates')

def get_db():
    db_path = current_app.config['DATABASE']
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_other_table():
    conn = get_db()
    conn.execute("""CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT,
        category TEXT,
        created_date TEXT,
        updated_date TEXT
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS links (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        url TEXT NOT NULL,
        description TEXT,
        category TEXT,
        created_date TEXT
    )""")
    conn.commit()
    conn.close()

@other_bp.route('/')
def index():
    init_other_table()
    conn = get_db()
    notes = conn.execute('SELECT * FROM notes ORDER BY updated_date DESC').fetchall()
    links = conn.execute('SELECT * FROM links ORDER BY created_date DESC').fetchall()
    conn.close()
    return render_template('other.html', notes=notes, links=links)

@other_bp.route('/add-note', methods=['POST'])
def add_note():
    init_other_table()
    title = request.form.get('title', 'Untitled')
    content = request.form.get('content', '')
    category = request.form.get('category', 'General')
    now = datetime.now().isoformat()

    conn = get_db()
    conn.execute('INSERT INTO notes (title, content, category, created_date, updated_date) VALUES (?, ?, ?, ?, ?)',
                 (title, content, category, now, now))
    conn.commit()
    conn.close()
    flash('Note added!', 'success')
    return redirect(url_for('other.index'))

@other_bp.route('/add-link', methods=['POST'])
def add_link():
    init_other_table()
    title = request.form.get('title', 'Untitled')
    url = request.form.get('url', '')
    description = request.form.get('description', '')
    category = request.form.get('category', 'General')

    conn = get_db()
    conn.execute('INSERT INTO links (title, url, description, category, created_date) VALUES (?, ?, ?, ?, ?)',
                 (title, url, description, category, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    flash('Link added!', 'success')
    return redirect(url_for('other.index'))

@other_bp.route('/delete-note/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    init_other_table()
    conn = get_db()
    conn.execute('DELETE FROM notes WHERE id = ?', (note_id,))
    conn.commit()
    conn.close()
    flash('Note deleted', 'success')
    return redirect(url_for('other.index'))

@other_bp.route('/delete-link/<int:link_id>', methods=['POST'])
def delete_link(link_id):
    init_other_table()
    conn = get_db()
    conn.execute('DELETE FROM links WHERE id = ?', (link_id,))
    conn.commit()
    conn.close()
    flash('Link deleted', 'success')
    return redirect(url_for('other.index'))
