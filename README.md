# Patil-NGO-application
Patil NGO Website and Admin CMS built using Python Flask. Includes a dynamic home page, banner slider, vision &amp; mission manager, statistics, initiatives, and full admin dashboard with CRUD features. Supports image uploads, SQLite database, and easy deployment on Render, Railway, or Heroku.
# Patil NGO Website (Python Flask + Admin CMS)

This repository contains the complete dynamic website and admin CMS 
for Patil NGO, built using Python Flask, SQLite, Tailwind, and HTML/JS.

## Features
- Dynamic home page (Banner, Vision/Mission, Stats, Initiatives)
- Admin panel (Login + Dashboard)
- CRUD operations for all homepage sections
- File upload support (images)
- SQLite database (included in /instance)
- Ready for deployment (Render / Heroku / Railway)

## Installation
pip install -r requirements.txt
python seed.py
python app.py

## Admin Login
Username: admin  
Password: admin

## Deployment (Render)
Build command:
pip install -r requirements.txt

Start command:
gunicorn app:create_app()
