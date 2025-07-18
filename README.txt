# 🧠 BDC Project – Extraction & Analyse des Bons de Commande

Ce projet a pour objectif d'extraire, traiter, filtrer et visualiser automatiquement les **Bons de Commande (BDC)** publiés sur la plateforme [marchespublics.gov.ma](https://www.marchespublics.gov.ma).

## 📁 Structure du projet

- `backend-python/` : Extraction avec Selenium ou Playwright, API FastAPI, traitement des données.
- `frontend-next/` : Interface web (Next.js) avec affichage des BDC et authentification.
- `data/` : Données extraites (JSON, fichiers CSV...).
- `docs/` : Documentation technique et fonctionnelle.

## ⚙️ Technologies utilisées

- **Python 3**, **FastAPI**, **Playwright/Selenium**
- **Next.js**, **React**, **Tailwind CSS**
- **MongoDB** pour la base de données
- **JWT** pour l'authentification
- **GitHub + Git LFS** pour la gestion de version

## 🚀 Lancer le projet localement

### Backend FastAPI
```bash
cd backend-python
uvicorn main:app --reload
