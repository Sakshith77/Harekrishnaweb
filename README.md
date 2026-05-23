# Hare Krishna 🪷

A spiritual multimedia platform built with Flask. Features video/audio players, HTML games, free tools, reading stories, and more.

## Features

- **Video Player** - Upload videos or stream HLS content with adaptive playback
- **Audio Player** - Upload and play audio with playlist support
- **HTML Games** - Upload .zip/.html games or embed external games
- **Free Tools** - Calculator, Base64, JSON formatter, Password generator, Color picker, Text formatter, Image resizer
- **Reading Stories** - Write and read spiritual stories with cover images
- **Other** - Notes and links manager with more modules coming soon
- **PWA** - Installable app with offline support

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
python app.py

# 3. Open in browser
http://localhost:5000
```

## Project Structure

```
hare_krishna_app/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── routes/               # Blueprint modules
│   ├── video.py
│   ├── audio.py
│   ├── games.py
│   ├── tools.py
│   ├── stories.py
│   ├── other.py
│   └── api.py
├── templates/            # Jinja2 templates
│   ├── base.html
│   ├── index.html
│   ├── video.html
│   ├── video_player.html
│   ├── audio.html
│   ├── games.html
│   ├── game_player.html
│   ├── tools.html
│   ├── stories.html
│   ├── story_reader.html
│   ├── other.html
│   └── tool_*.html
├── static/               # Static assets
│   ├── css/style.css
│   ├── js/main.js
│   ├── js/audio-player.js
│   ├── manifest.json
│   └── sw.js
├── uploads/              # User uploads
│   ├── videos/
│   ├── audios/
│   ├── games/
│   ├── stories/
│   ├── images/
│   └── tools/
└── database/             # SQLite database
    └── app.db
```

## Tech Stack

- **Backend**: Flask, SQLite, Jinja2
- **Frontend**: Vanilla HTML/CSS/JS (no heavy frameworks)
- **Video**: Video.js with HLS support
- **PWA**: Service Worker, Manifest, Installable

## Design

- Dark theme with gold/lotus accents
- Cormorant Garamond + Inter fonts
- Glassmorphism-inspired cards
- Smooth transitions and hover effects
- Mobile-first responsive design
- Telegram-style loading animation

## License

MIT License - Hare Krishna 🪷
