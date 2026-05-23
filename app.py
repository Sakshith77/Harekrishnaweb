import os
from flask import Flask, render_template, send_from_directory
from datetime import datetime
from flask_cors import CORS

# Import blueprints
from routes.video import video_bp
from routes.audio import audio_bp
from routes.games import games_bp
from routes.tools import tools_bp
from routes.stories import stories_bp
from routes.other import other_bp
from routes.api import api_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'hare-krishna-secret-key-2024')
    app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max upload

    # Upload folders
    app.config['UPLOAD_FOLDER_VIDEOS'] = os.path.join(app.root_path, 'uploads', 'videos')
    app.config['UPLOAD_FOLDER_AUDIOS'] = os.path.join(app.root_path, 'uploads', 'audios')
    app.config['UPLOAD_FOLDER_GAMES'] = os.path.join(app.root_path, 'uploads', 'games')
    app.config['UPLOAD_FOLDER_STORIES'] = os.path.join(app.root_path, 'uploads', 'stories')
    app.config['UPLOAD_FOLDER_IMAGES'] = os.path.join(app.root_path, 'uploads', 'images')
    app.config['UPLOAD_FOLDER_TOOLS'] = os.path.join(app.root_path, 'uploads', 'tools')
    app.config['DATABASE'] = os.path.join(app.root_path, 'database', 'app.db')

    # Ensure ALL directories exist
    os.makedirs(os.path.join(app.root_path, 'database'), exist_ok=True)
    for folder in ['videos', 'audios', 'games', 'stories', 'images', 'tools']:
        os.makedirs(os.path.join(app.root_path, 'uploads', folder), exist_ok=True)

    # Enable CORS for GitHub Pages frontend
    # Replace with your actual GitHub Pages URL after deployment
    CORS(app, resources={
        r"/api/*": {
            "origins": [
                "https://sakshith77.github.io",
                "http://localhost:5000",
                "http://127.0.0.1:5000"
            ]
        }
    })

    # Register blueprints
    app.register_blueprint(video_bp, url_prefix='/video')
    app.register_blueprint(audio_bp, url_prefix='/audio')
    app.register_blueprint(games_bp, url_prefix='/games')
    app.register_blueprint(tools_bp, url_prefix='/tools')
    app.register_blueprint(stories_bp, url_prefix='/stories')
    app.register_blueprint(other_bp, url_prefix='/other')
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.route('/')
    def index():
        return render_template('index.html', now=datetime.now())

    @app.route('/manifest.json')
    def manifest():
        return app.send_static_file('manifest.json')

    @app.route('/sw.js')
    def service_worker():
        return app.send_static_file('sw.js')

    # Health check for Render
    @app.route('/health')
    def health():
        return {"status": "healthy", "app": "hare-krishna"}, 200

    return app

# Create app instance for gunicorn
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
