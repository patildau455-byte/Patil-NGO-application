# Patil NGO - Flask Project (with Admin UI)

## What is included
- Flask backend (SQLite) with APIs for banners, vision/mission, statistics, initiatives
- Simple Admin UI (static pages) to manage content (demo login: admin/admin)
- File uploads saved to /uploads
- Procfile for deployment with gunicorn
- seed.py to populate sample data

## How to run locally
1. Create virtualenv and install:
   ```
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```
2. Seed the DB (optional):
   ```
   python seed.py
   ```
3. Run:
   ```
   python app.py
   ```
4. Open http://127.0.0.1:5000 for site, http://127.0.0.1:5000/admin for admin login.

## Deploy
- You can deploy to Render / Railway / Heroku by connecting a GitHub repo and using the Procfile.
- Use Python runtime, and the web command in Procfile.

