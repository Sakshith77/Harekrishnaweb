# 🪷 Hare Krishna - Deployment Guide

## Architecture

```
┌─────────────────────┐         ┌─────────────────────────┐
│   GitHub Pages      │  CORS   │    Render (Free)        │
│   (This frontend)   │◄───────►│    Flask Backend        │
│                     │         │    + SQLite + Uploads   │
└─────────────────────┘         └─────────────────────────┘
     FREE                              FREE
```

---

## Step 1: Deploy Backend to Render (FREE)

### 1.1 Push this repo to GitHub
```bash
git init
git add .
git commit -m "Initial backend setup"
git branch -M main
git remote add origin https://github.com/Sakshith77/Harekrishnaweb.git
git push -u origin main
```

### 1.2 Sign up on Render
1. Go to [render.com](https://render.com)
2. Click **"Get Started for Free"**
3. Sign up with your **GitHub** account

### 1.3 Create Web Service
1. Click **"New +"** → **"Web Service"**
2. Select your `Harekrishnaweb` repository
3. Configure:
   - **Name:** `hare-krishna-backend`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
   - **Plan:** `Free`
4. Click **"Create Web Service"**

### 1.4 Get your backend URL
After deployment, Render will give you a URL like:
```
https://hare-krishna-backend.onrender.com
```

---

## Step 2: Update CORS in Backend

In `app.py`, update the CORS origins with your actual GitHub Pages URL:

```python
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://sakshith77.github.io",           # Your GitHub Pages
            "https://sakshith77.github.io/Harekrishnaweb",  # Full path
            "http://localhost:5000",
            "http://127.0.0.1:5000"
        ]
    }
})
```

Commit and push - Render will auto-deploy.

---

## Step 3: Deploy Frontend to GitHub Pages

### 3.1 Use the `frontend/` folder
The `frontend/index.html` is a lightweight landing page that connects to your Render backend.

### 3.2 Enable GitHub Pages
1. Go to your repo on GitHub
2. Click **Settings** → **Pages**
3. **Source:** Deploy from a branch
4. **Branch:** `main` / `frontend` folder (or root)
5. Click **Save**

Your frontend will be at:
```
https://sakshith77.github.io/Harekrishnaweb
```

### 3.3 Update frontend API URL
In `frontend/index.html`, update:
```javascript
const API_BASE = 'https://hare-krishna-backend.onrender.com';
```

---

## Step 4: Using the Full App

The **full Flask app** (with all features) runs on Render:
```
https://hare-krishna-backend.onrender.com
```

The **GitHub Pages frontend** is just a landing/status page:
```
https://sakshith77.github.io/Harekrishnaweb
```

**For the best experience, use the Render URL directly** - it has the complete UI.

---

## Free Tier Limits

| Service | Limit |
|---------|-------|
| Render Free | Sleeps after 15 min inactivity (30s cold start) |
| Render Free | 512 MB RAM, 0.1 CPU |
| GitHub Pages | 1 GB storage, 100 GB bandwidth/month |
| SQLite | File-based (included) |

---

## Alternative: PythonAnywhere (Always-On)

If you need **no cold starts**:

1. Go to [pythonanywhere.com](https://pythonanywhere.com)
2. Upload files or clone from GitHub
3. Create a **Flask** web app
4. WSGI file: `/home/yourusername/Harekrishnaweb/app.py`
5. Your URL: `yourusername.pythonanywhere.com`

---

## Troubleshooting

### "Unable to open database file"
Make sure the `database/` directory exists. The fixed `app.py` creates it automatically.

### CORS errors
Update the `origins` list in `app.py` with your exact GitHub Pages URL.

### Uploads not working
Free tiers have ephemeral filesystems. Files may disappear after restart. For production, use:
- AWS S3 (free tier: 5GB)
- Cloudinary (free tier: 25GB)
- Supabase Storage (free tier: 1GB)

---

## 🪷 Hare Krishna
