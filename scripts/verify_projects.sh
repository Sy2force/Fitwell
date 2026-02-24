#!/bin/bash

# Script de vérification globale des projets HackerU
# Vérifie : Django Backend, React Frontend, Node.js Backend

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🔍 Démarrage de la vérification des projets...${NC}\n"

# 1. Vérification Django Backend
echo -e "${YELLOW}👉 Vérification Django Backend (fitwell)...${NC}"
if [ -f "manage.py" ] && [ -f "requirements.txt" ]; then
    echo -e "${GREEN}✅ Structure Django détectée.${NC}"
    if [ -f ".env" ]; then
        echo -e "${GREEN}✅ Fichier .env présent.${NC}"
    else
        echo -e "${RED}❌ Fichier .env manquant ! Copiez .env.example.${NC}"
    fi
    if [ -d "venv" ]; then
        echo -e "${GREEN}✅ Environnement virtuel 'venv' détecté.${NC}"
    else
        echo -e "${YELLOW}⚠️  Environnement virtuel non trouvé (venv). Lancez 'make install'.${NC}"
    fi
else
    echo -e "${RED}❌ Projet Django introuvable ou incomplet dans le dossier courant.${NC}"
fi
echo ""

# 2. Vérification React Frontend
echo -e "${YELLOW}👉 Vérification React Frontend (fitwell-frontend)...${NC}"
if [ -d "fitwell-frontend" ]; then
    if [ -f "fitwell-frontend/package.json" ] && [ -f "fitwell-frontend/vite.config.js" ]; then
        echo -e "${GREEN}✅ Structure React/Vite détectée.${NC}"
        if [ -f "fitwell-frontend/.env" ]; then
             echo -e "${GREEN}✅ Fichier .env présent.${NC}"
        else
             echo -e "${RED}❌ Fichier .env manquant dans frontend !${NC}"
        fi
    else
        echo -e "${RED}❌ Fichiers React manquants.${NC}"
    fi
else
    echo -e "${RED}❌ Dossier fitwell-frontend introuvable.${NC}"
fi
echo ""

# 3. Vérification Node.js Backend
echo -e "${YELLOW}👉 Vérification Node.js Backend (nodejs-hackeru-project)...${NC}"
NODE_PROJECT_PATH="../nodejs-hackeru-project"

if [ -d "$NODE_PROJECT_PATH" ]; then
    if [ -f "$NODE_PROJECT_PATH/package.json" ] && [ -f "$NODE_PROJECT_PATH/server.js" ]; then
        echo -e "${GREEN}✅ Structure Node.js détectée.${NC}"
        if [ -f "$NODE_PROJECT_PATH/.env" ]; then
            echo -e "${GREEN}✅ Fichier .env présent.${NC}"
        else
            echo -e "${RED}❌ Fichier .env manquant dans Node.js project !${NC}"
        fi
    else
        echo -e "${RED}❌ Fichiers Node.js manquants.${NC}"
    fi
else
    echo -e "${RED}❌ Dossier nodejs-hackeru-project introuvable (attendu: ../nodejs-hackeru-project).${NC}"
fi

echo -e "\n${YELLOW}📊 Résumé terminé.${NC}"
echo -e "Si tout est vert, vos projets sont prêts à être lancés ! 🚀"
