# Weather App (FastAPI + PostgreSQL)

A beginner‑friendly weather application built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**.  
It allows users to sign up, log in, and check live weather data using the OpenWeather API.  
Users can also save their default city, view recent searches, and store weather snapshots in a database.

---

## Features
- User authentication with JWT tokens (signup & login).
- Secure password hashing with bcrypt.
- Fetch live weather data from OpenWeather API.
- Save and update a default city for each user.
- Store historic weather searches in the database.
- Retrieve recent search history.
- Supports multiple units: Celsius, Fahrenheit, Kelvin.

---

## Tech Stack
- **FastAPI** – web framework
- **SQLAlchemy** – ORM for database models
- **PostgreSQL** – database
- **Passlib** – password hashing
- **Python‑Jose** – JWT authentication
- **Requests** – API calls to OpenWeather

---

## Installation
### 1. Clone the repository
```bash
git clone https://github.com/yourusername/weather-app.git
cd weather-app
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

pip install -r requirements.txt
DATABASE_URL=postgresql://postgres:password@localhost:5432/weather_app
SECRET_KEY=asecureandsecretkey
API_KEY=your_openweathermap_api_key

uvicorn main:app --reload
