import os
import sqlite3
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from werkzeug.utils import secure_filename

tools_bp = Blueprint('tools', __name__, template_folder='../templates')

def get_db():
    db_path = current_app.config['DATABASE']
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_tools_table():
    conn = get_db()
    conn.execute("""CREATE TABLE IF NOT EXISTS tools (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        category TEXT,
        icon TEXT,
        route TEXT,
        upload_date TEXT
    )""")
    conn.commit()
    conn.close()

@tools_bp.route('/')
def index():
    init_tools_table()
    conn = get_db()
    tools = conn.execute('SELECT * FROM tools ORDER BY category, name').fetchall()
    conn.close()

    # Default tools if none exist
    default_tools = [
        {'name': 'File Converter', 'description': 'Convert files between formats', 'category': 'Converter', 'icon': 'fa-exchange-alt', 'route': 'tools.converter'},
        {'name': 'Image Resizer', 'description': 'Resize and compress images', 'category': 'Image', 'icon': 'fa-image', 'route': 'tools.image_resizer'},
        {'name': 'Text Formatter', 'description': 'Format and clean text', 'category': 'Text', 'icon': 'fa-font', 'route': 'tools.text_formatter'},
        {'name': 'Calculator', 'description': 'Simple scientific calculator', 'category': 'Math', 'icon': 'fa-calculator', 'route': 'tools.calculator'},
        {'name': 'Base64 Encoder', 'description': 'Encode/decode Base64', 'category': 'Text', 'icon': 'fa-code', 'route': 'tools.base64'},
        {'name': 'JSON Formatter', 'description': 'Format and validate JSON', 'category': 'Developer', 'icon': 'fa-brackets-curly', 'route': 'tools.json_formatter'},
        {'name': 'Password Generator', 'description': 'Generate secure passwords', 'category': 'Security', 'icon': 'fa-key', 'route': 'tools.password_gen'},
        {'name': 'Color Picker', 'description': 'Pick and convert colors', 'category': 'Design', 'icon': 'fa-palette', 'route': 'tools.color_picker'},
    ]

    return render_template('tools.html', tools=tools, default_tools=default_tools)

@tools_bp.route('/converter')
def converter():
    return render_template('tool_converter.html')

@tools_bp.route('/image-resizer')
def image_resizer():
    return render_template('tool_image.html')

@tools_bp.route('/text-formatter')
def text_formatter():
    return render_template('tool_text.html')

@tools_bp.route('/calculator')
def calculator():
    return render_template('tool_calculator.html')

@tools_bp.route('/base64')
def base64_tool():
    return render_template('tool_base64.html')

@tools_bp.route('/json-formatter')
def json_formatter():
    return render_template('tool_json.html')

@tools_bp.route('/password-gen')
def password_gen():
    return render_template('tool_password.html')

@tools_bp.route('/color-picker')
def color_picker():
    return render_template('tool_color.html')
