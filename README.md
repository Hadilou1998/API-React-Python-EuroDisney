# API-React-Python-EuroDisney
**Technologies : ReactJS / Python (FastAPI ou Flask) / MySQL**

---

## 1. Objectif du projet
Mettre en place une plateforme de gestion pour le site EuroDisney, permettant :
-   La gestion des visiteurs, réservations et billets.
-   La gestion des attractions, spectacles et restaurants.
-   L'administration via une interface ReactJS connectée à une API REST sécurisée.

---

## 2. Architecture technique
-   **Frontend** : ReactJS avec une interface utilisateur intuitive.
-   **Backend** : Python (FastAPI ou Flask) pour la gestion des API et la logique métier.
-   **Base de données** : MySQL pour stocker les informations des visiteurs, réservations, attractions, etc.
-   **Conteneurisation**: Docker & docker-compose.
-   **Gestion du code**: Git / Github.
-   **Déploiement** : Docker (avec un dossier `docker /` contenant les fichiers).

---

## 3. Fonctionnalités principales
### 3.1 Gestion des visiteurs
-   Création, lecture, modification et suppression des comptes visiteurs.
-   Authentification (JWT).
-   Historique des réservations et billets.

### 3.2 Gestion des attractions
-   CRUD sur les attractions (nom, description, capacité, horaires).
-   Gestion de l'état (ouvert, fermé, maintenance).

### 3.3 Gestion des billets et réservations
-   Réservation de billets par les visiteurs.
-   Génération de QR Codes.
-   Gestion des paiements (simulation ou intégration d'API).

### 3.4 Gestion du personnel
-   Ajout et gestion des employés.
-   Attribution à des attractions, restaurants ou spectacles.

### 3.5 Tableau de bord d'administration
-   Statistiques (nombre de visiteurs, taux de remplissage, ventes).
-   Gestion centralisée des ressources.

---

## 4. Modèle de données
-   **Users** (id, name, password, email, role).
-   **Attractions** (id, name, description, capacity, status).
-   **Tickets** (id, user_id, attraction_id, date, qr_code, status).
-   **Reservations** (id, user_id, restaurant/spectacle, date, nb_personnes).
-   **Employees** (id, name, job, assignment).

---

## 5. Endpoints API
-   `POST /auth/register` -> inscription utilisateur.
-   `POST /auth/login` -> connexion (JWT).
-   `GET /attractions` -> liste des attractions.
-   `GET /attractions/{id}` -> détails d'une attraction.
-   `POST /attractions` -> ajouter une attraction (admin).
-   `PUT /attractions/{id}` -> modifier une attraction (admin).
-   `DELETE /attractions/{id}` -> supprimer une attraction (admin).
-   `POST /tickets` -> réserver un billet.
-   `GET /tickets` -> liste des billets.
-   `GET /tickets/{id}` -> détails d'un billet.
-   `PUT /tickets/{id}` -> modifier un billet (admin).
-   `DELETE /tickets/{id}` -> supprimer un billet (admin).
-   `POST /employees` -> ajouter un employé (admin).
-   `GET /employees` -> liste des employés.
-   `GET /employees/{id}` -> détails d'un employé.
-   `PUT /employees/{id}` -> modifier un employé (admin).
-   `DELETE /employees/{id}` -> supprimer un employé (admin).
-   `GET /users/{id}/tickets` -> historique des billets.

---

## 6. Sécurité
-   Authentification JWT.
-   Gestion des rôles (user, employee, admin).
-   Chiffrement des mots de passe (bcrypt).
-   Validation des données (pydantic).

---

## 7. Déploiement
-   Dossier `docker/` contenant :
    -   `docker-compose.yml` (services : frontend, backend, db).
    -   `Dockerfile` pour ReactJS (frontend).
    -   `Dockerfile` pour Python (FastAPI).       
    -   Volume persistant pour MySQL.

---

## 8. Recommandations
-   Respect des normes RESTful.
-   Documentation API via **OpenAPI/Swagger**.
-   Tests unitaires (Pytest, React Testing Library).
-   CI/CD possible via Github Actions.

---