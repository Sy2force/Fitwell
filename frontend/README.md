# 🎨 FitWell Frontend - React & Vite

Ce projet est l'application frontend pour l'API FitWell. Il est construit avec **React**, **Vite**, **Tailwind CSS** et **Framer Motion** pour une expérience utilisateur fluide et futuriste.

## 🚀 Installation et Lancement

### Prérequis
- Node.js (v16+)
- Le backend Django doit tourner sur `http://localhost:8000`

### 1. Installation des dépendances
```bash
npm install
```

### 2. Configuration
Le fichier `.env` doit contenir l'URL de l'API (déjà configuré par défaut) :
```
VITE_API_URL=http://localhost:8000/api/
```

### 3. Lancer le serveur de développement
```bash
npm run dev
```
L'application sera accessible sur **http://localhost:5173**.

## 📱 Fonctionnalités et Pages

- **Home (`/`)** : Liste des articles avec recherche dynamique et design en grille.
- **Article Detail (`/articles/:id`)** : Lecture d'un article, affichage de l'image, et section commentaires en temps réel.
- **Login (`/login`) & Register (`/register`)** : Authentification JWT sécurisée avec gestion des erreurs et redirection.
- **Profile (`/profile`)** : Espace privé pour voir ses propres articles et se déconnecter.
- **Create Article (`/create-article`)** : Formulaire complet pour rédiger et publier un nouvel article (titre, catégorie, image, contenu).

## 🛠 Stack Technique

- **Core** : React 18, Vite
- **Style** : Tailwind CSS, clsx
- **Animations** : Framer Motion
- **HTTP** : Axios (avec intercepteurs pour injecter le Token JWT)
- **State** : Zustand (Gestion de l'authentification)
- **Icons** : Lucide React

## 🔗 Connexion avec Django

Le frontend communique avec le backend via `src/api/axios.js`.
- Les tokens d'accès et de rafraîchissement sont stockés dans le `localStorage`.
- Si un token expire, l'utilisateur est redirigé vers le login (ou le token est rafraîchi si implémenté).
