# ⚡ FitWell - Elite Athletic Ecosystem

**Version**: 1.0 Production Ready  
**Status**: 🟢 **100% Complete & Tested**

FitWell is a premier full-stack platform engineered for elite human optimization. It combines AI-driven planning, gamified progression, and professional sports science to create a comprehensive operating system for biological performance.

---

## 📌 Overview

**FitWell** is not just a fitness app; it is a complete ecosystem.
- **Elite Planner**: AI-generated workout and nutrition protocols based on detailed biometrics.
- **Gamified Progression**: XP, Levels, Ranks, and Health Score (0-100%) to keep users addicted to progress.
- **Vivid Sport UI**: A high-energy "Cyberpunk/Neon" aesthetic designed to motivate.
- **Admin Command**: Lead generation and system oversight.

---

## ✨ Key Features

### 🏋️ Elite Planner
- **AI Generation**: Creates custom workout and nutrition plans based on Gender, Goal (Weight Loss, Muscle Gain, Endurance), and Activity Level.
- **Health Score**: Real-time analysis of Fitness, Recovery, Lifestyle, and Consistency.
- **Nutrition**: Macro splits (Protein, Fats, Carbs) and meal suggestions.

### 🎮 Gamification
- **XP System**: Earn experience for every action (plans created, articles read).
- **Leveling**: Ascend from *Recruit* to *Elite Athlete*.
- **Badges**: Earn achievements for milestones.
- **Streak**: Track daily consistency.

### 🧠 Intel & Blog
- **Sectors**: Strength, Nutrition, Mindset, Recovery, Bio-Hacking.
- **Interaction**: Likes, Comments, and Sharing.
- **Secure Comms**: Encrypted discussion channels.

### 🛠 Precision Tools
- **BMI Calculator**: Visual body composition analysis.
- **Macro Calculator**: TDEE and fueling strategies.

### 👨‍💼 Admin Command
- **Lead Center**: View and export user data (CSV) for recruitment.
- **System Oversight**: Monitor platform growth.

---

## 🛠 Tech Stack

### Backend (Django REST Framework)
- **Framework**: Django 4.2 + DRF
- **Auth**: JWT (JSON Web Tokens)
- **Database**: SQLite (Local) / PostgreSQL (Production)
- **Docs**: Swagger UI / OpenAPI (`drf-spectacular`)
- **Security**: CORS, CSRF, Password Hashing
- **Apps**: `users`, `blog`, `training`, `wellness`, `gamification`

### Frontend (React + Vite)
- **Framework**: React 18
- **Build Tool**: Vite 5
- **Styling**: TailwindCSS (Vivid Sport Theme)
- **State**: Zustand (Auth Store)
- **Routing**: React Router v6
- **Animations**: Framer Motion
- **HTTP**: Axios + Interceptors
- **i18n**: English / French support

---

## 📂 Project Structure

```
fitwell/
├── backend/              # Django REST API (Root for Render Service)
│   ├── config/           # Settings (base, dev, prod)
│   ├── users/            # Auth, Profiles, Gamification
│   ├── blog/             # Articles, Categories, Comments
│   ├── training/         # Exercises, Programs, Sessions
│   ├── wellness/         # Planner, Health Score, Habits
│   ├── gamification/     # Badges, XP, Levels
│   ├── build.sh          # Render build script
│   └── manage.py
│
├── frontend/             # React Application
│   ├── src/
│   │   ├── pages/        # 11 Complete Pages
│   │   ├── components/   # Reusable UI Components
│   │   ├── store/        # Zustand State Management
│   │   └── api/          # Axios Configuration
│   └── vite.config.js
│
└── render.yaml           # Deployment Configuration (Infrastructure as Code)
```

---

## 🚀 Getting Started (Local Development)

### Prerequisites
- Python 3.10+
- Node.js 18+

### 1. Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
API running at: `http://localhost:8000`

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
App running at: `http://localhost:5173`

### 3. Default Credentials (Seeded Data)
- **Admin**: `admin@example.com` / `password123`
- **Elite User**: `apex_predator@fitwell.net` / `password123`

---

## 🧪 Testing

The system is rigorously tested.

### Backend Tests
13/13 Tests Passed (Coverage: Auth, Blog, Profile, Gamification).
```bash
cd backend
python manage.py test
```

### Frontend Tests
3/3 E2E Tests Passed (Playwright).
```bash
cd frontend
npm run test:e2e
```

---

## 🚢 Deployment Guide (Render)

The project is pre-configured for **Render** via `render.yaml`.

1. **Push to GitHub/GitLab**.
2. **Create New Blueprint** on Render.
3. **Connect Repository**. Render will auto-detect `render.yaml`.
4. **Deploy**.

### Configuration Details
- **Root Directory**: `backend` (for Python service)
- **Build Command**: `./build.sh` (Installs deps, collects static, migrates DB)
- **Start Command**: `gunicorn config.wsgi:application`
- **Frontend Build**: `cd frontend && npm install && npm run build`
- **Environment**:
    - `PYTHON_VERSION`: 3.10.0
    - `ALLOWED_HOSTS`: `.onrender.com`
    - `VITE_API_URL`: Auto-injected

---

## 🌐 API Documentation

Interactive API documentation is available via Swagger UI.
- **Local**: `http://localhost:8000/api/docs/`
- **Production**: `https://your-app.onrender.com/api/docs/`

### Key Endpoints
- `POST /api/auth/register/` - Sign up
- `POST /api/auth/token/` - Login
- `POST /api/wellness/plans/` - Generate Elite Plan
- `GET /api/blog/articles/` - Fetch Intel
- `GET /api/admin/users/` - Lead Center (Admin only)

---

## 📄 License

© 2026 FitWell Ecosystem. All rights reserved.
*Authorized for elite personnel only.*
