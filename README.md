# Chemical Equipment Parameter Visualizer  
## Project Name: Web based Application
**Hybrid Web + Desktop Application**

A full-stack hybrid application for visualizing and analyzing chemical equipment parameters from CSV datasets.  
The system processes operational data to generate structured summaries, highlight abnormal parameter values, and generates automated insights such as health scores, risk alerts, and historical trends.

This project was developed as part of the **FOSSEE Internship Technical Screening Task** to demonstrate practical software engineering skills, including backend API development, frontend integration, data handling with Pandas, and desktop application design.

---

## Key Features

### Data Handling
- CSV upload and parsing using Pandas  
- Validation of required data columns  
- Computation of summary statistics  

### Analytics
- Basic equipment health indicators  
- Detection of safe-range violations  
- Alerts for abnormal parameter values  
- Trend analysis across recent uploads  

### Visualization
- Interactive web dashboard using React  
- Desktop application built with PyQt5  
- Charts rendered using Chart.js and Matplotlib  

### System Features
- REST APIs built with Django REST Framework  
- Authentication using environment variables  
- PDF report generation  
- Upload history tracking  

---

## Architecture Overview

```text
Frontend (Web) ───────┐
                      ├── Django REST API ─── SQLite DB
Desktop (PyQt) ───────┘
```
Both the Web and Desktop applications consume the same backend API, ensuring consistent
data processing and results across platforms.  

---

## Tech Stack

### Backend
- Python
- Django
- Django REST Framework
- Pandas
- SQLite

### Web Frontend
- React
- JavaScript
- Fetch API
- CSS

### Desktop Client
- Python
- PyQt5
- Matplotlib

---

## Project Structure

```text
chemical-equipment-visualizer/
│
├── backend/
│   ├── api/                # Core API logic
│   ├── desktop-app/        # PyQt desktop client
│   ├── backend/            # Django settings
│   └── manage.py
│
└── web-frontend/
    ├── src/
    │   ├── components/
    │   ├── pages/
    │   └── services/
    └── package.json
```

---

## Setup Guide

### Clone Repository

```bash
git clone https://github.com/Sangupta03/FOSSCEE-Task-Submission.git
cd chemical-equipment-visualizer
```

---

## Backend Setup

### Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run migrations

```bash
cd backend
python manage.py migrate
```

### Create admin user

```bash
python manage.py createsuperuser
```

### Start server

```bash
python manage.py runserver
```

API available at:

```
http://127.0.0.1:8000/api
```

---

## Web Frontend Setup

```bash
cd backend/web-frontend
npm install
npm start
```

Frontend runs at:

```
http://localhost:3000
```

---

## Desktop Application

```bash
cd backend/desktop-app
python app.py
```

---

## CSV Format

Uploaded CSV files must follow this structure:

```text
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-1,Pump,120,30,80
Pump-2,Pump,150,32,85
Reactor-1,Reactor,200,50,120
...
```

---

## Environment Variables

Create a `.env` file inside:

```text
backend/web-frontend/.env
```

```env
REACT_APP_API_BASE=http://127.0.0.1:8000/api
REACT_APP_API_USER=your_username
REACT_APP_API_PASS=your_password
```

---

## Why This Project Stands Out (FOSSEE Screening)

This project demonstrates:
- End-to-end full-stack development
- Practical CSV-based data processing and visualization
- Secure configuration management
- Clear separation between backend and frontend layers
- A functional Hybrid Web + Desktop architecture

It simulates an industrial monitoring system and can be extended for predictive maintenance, anomaly detection, and operational intelligence.

---

## Author

**Sanjoli Gupta**  
Chemical Equipment Parameter Visualizer  
FOSSEE Internship Screening Task
