# 📚 Documentation API - FitWell

## Vue d'ensemble

L'API REST de FitWell est construite avec Django REST Framework et fournit des endpoints pour gérer l'authentification, les utilisateurs, les articles de blog, et les plans de wellness.

**Base URL** : `http://127.0.0.1:8000/api/`

**Documentation Interactive** : `http://127.0.0.1:8000/swagger/`

---

## 🔐 Authentication

### JWT Token

FitWell utilise JWT (JSON Web Tokens) pour l'authentification.

#### Obtenir un token

```http
POST /api/token/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Rafraîchir un token

```http
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Utiliser le token

Incluez le token dans le header `Authorization` :

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

---

## 👤 Users

### Inscription

```http
POST /api/register/
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

### Profil utilisateur

```http
GET /api/users/me/
Authorization: Bearer {token}
```

**Response:**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "profile": {
    "bio": "Fitness enthusiast",
    "avatar": "https://...",
    "level": 5,
    "xp": 1250,
    "current_streak": 14,
    "health_score": 88,
    "scores": {
      "fitness": 92,
      "recovery": 75,
      "lifestyle": 85,
      "consistency": 95
    }
  }
}
```

---

## 📝 Blog

### Lister les articles

```http
GET /api/articles/
```

**Query Parameters:**
- `category` : Filtrer par slug de catégorie
- `search` : Recherche textuelle dans titre/contenu

**Response:**
```json
{
  "count": 25,
  "results": [
    {
      "id": 1,
      "title": "Les bases de la nutrition",
      "slug": "les-bases-de-la-nutrition",
      "author_username": "admin",
      "category_name": "Nutrition",
      "content": "...",
      "image_url": "https://...",
      "created_at": "2026-03-15T10:30:00Z",
      "likes_count": 42,
      "is_liked": false
    }
  ]
}
```

### Détails d'un article

```http
GET /api/articles/{id}/
```

### Liker un article

```http
POST /api/articles/{id}/like/
Authorization: Bearer {token}
```

### Commentaires

#### Créer un commentaire

```http
POST /api/comments/
Authorization: Bearer {token}
Content-Type: application/json

{
  "article": 1,
  "content": "Excellent article !"
}
```

#### Supprimer un commentaire

```http
DELETE /api/comments/{id}/
Authorization: Bearer {token}
```

---

## 🏋️ Wellness Plans

### Générer un plan

```http
POST /api/wellness-plans/
Authorization: Bearer {token}
Content-Type: application/json

{
  "age": 28,
  "gender": "male",
  "height": 180,
  "weight": 75,
  "goal": "muscle_gain",
  "activity_level": "active"
}
```

**Response:**
```json
{
  "id": 1,
  "user": 1,
  "workout_plan": {
    "schedule": "6 jours/semaine - Split PPL",
    "exercises": [...],
    "split": {...}
  },
  "nutrition_plan": {
    "calories": 2800,
    "macros": {
      "protein": "150g",
      "carbs": "350g",
      "fats": "93g"
    },
    "meals": {...}
  },
  "created_at": "2026-03-21T20:15:00Z"
}
```

---

## 🏆 Workout Sessions

### Démarrer une session

```http
POST /api/workout-sessions/
Authorization: Bearer {token}
Content-Type: application/json

{
  "notes": "Séance jambes"
}
```

### Ajouter un set

```http
POST /api/exercise-sets/
Authorization: Bearer {token}
Content-Type: application/json

{
  "session": 1,
  "exercise": 5,
  "set_number": 1,
  "reps": 10,
  "weight": 100,
  "rest_seconds": 90
}
```

### Compléter une session

```http
POST /api/workout-sessions/{id}/complete/
Authorization: Bearer {token}
```

---

## 📊 Permissions

| Endpoint | Lecture | Écriture |
|----------|---------|----------|
| `/api/articles/` | Public | Admin uniquement |
| `/api/comments/` | Public | Authentifié |
| `/api/users/` | Authentifié | Propriétaire |
| `/api/wellness-plans/` | Propriétaire | Propriétaire |
| `/api/workout-sessions/` | Propriétaire | Propriétaire |

---

## 🔒 Codes d'erreur

| Code | Description |
|------|-------------|
| 200 | Succès |
| 201 | Créé |
| 400 | Requête invalide |
| 401 | Non authentifié |
| 403 | Permission refusée |
| 404 | Non trouvé |
| 500 | Erreur serveur |

---

## 💡 Exemples d'utilisation

### Python (requests)

```python
import requests

# Login
response = requests.post('http://localhost:8000/api/token/', json={
    'email': 'user@example.com',
    'password': 'password123'
})
token = response.json()['access']

# Get profile
headers = {'Authorization': f'Bearer {token}'}
profile = requests.get('http://localhost:8000/api/users/me/', headers=headers)
print(profile.json())
```

### JavaScript (fetch)

```javascript
// Login
const response = await fetch('http://localhost:8000/api/token/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password123'
  })
});
const { access } = await response.json();

// Get articles
const articles = await fetch('http://localhost:8000/api/articles/', {
  headers: { 'Authorization': `Bearer ${access}` }
});
console.log(await articles.json());
```

---

© 2026 FitWell Systems Inc.
