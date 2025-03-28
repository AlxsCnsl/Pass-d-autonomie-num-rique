# 🚀 PASS D AUTONOMIE NUMERIQUE API

Une API REST développée avec Django et Django REST Framework (DRF) pour [décrire brièvement l'objectif de votre API].

## 📌 Table des matières

- [📦 Prérequis](#-prérequis)
- [⚙️ Installation](#️-installation)
- [🚀 Lancement](#-lancement)
- [📡 Endpoints](#-endpoints)
- [🔑 Authentification](#-authentification)


## 📦 Prérequis

Avant d'installer le projet, assurez-vous d'avoir :

- Python 3.x installé (`python --version`)
- `pip` installé (`pip --version`)
- `virtualenv` (optionnel mais recommandé)
- PostgreSQL / SQLite / MySQL (selon votre configuration)
- `git` installé
---

## ⚙️ Installation

### Clonez le dépôt :

```bash
git clone https://github.com/AlxsCnsl/Pass-d-autonomie-num-rique
cd Pass-d-autonomie-num-rique
```

### créée et active l'environement virtuel :

```python
python3 -m venv .env
```

Sur Windows
```
env\Scripts\activate
```
Sur macOS / Linux
```
source .env/bin/activate
```

### Installez les dépendances :

```
pip install -r requirements.txt
```

### Configurez la base de données :

```
python3 src/manage.py makemigration
python3 src/manage.py makemigration api
python3 src/manage.py migrate
```
et

```
python3 src/manage.py loaddata genres.json situations.json structure-types.json roles.json
python3 src/manage.py loaddata towns.json  orleans_streets.json
```

### Créez un superutilisateur :

```
python3 src/manage.py createsuperuser
```

## 🚀 Lancement

Démarrez le serveur Django :
```
python3 src/manage.py runserver xxxx
```
ou remplace xxxx par le numero de port souhaité (8050 si possible)

L'API sera disponible à l'adresse :
```
http://127.0.0.1:xxxx/
```

## 📡 Endpoints

Voici la liste des endpoints disponibles dans l'API :

```
'port/api/URL'
```
URL = 

### 🔐 Authentification et Gestion des Agents

| Méthode | URL | Description |
|---------|-----|------------|
| `POST`  | `/register/` | Inscription d'un nouvel agent |
| `POST`  | `/login/` | Connexion et obtention d'un token JWT |
| `POST`  | `/token/` | Récupération d'un token JWT |
| `POST`  | `/token/refresh/` | Rafraîchissement du token JWT |
| `POST`  | `/logout/` | Déconnexion de l'agent |
| `GET`   | `/agents/` | Liste des agents |
| `GET`   | `/agents/<int:pk>/` | Détails d'un agent |

### 🏢 Gestion des Structures et Types de Structures

| Méthode | URL | Description |
|---------|-----|------------|
| `GET` / `POST` | `/structure-types/` | Liste et création de types de structures |
| `GET` / `PUT` / `DELETE` | `/structure-types/<int:pk>/` | Détails, modification et suppression d'un type de structure |
| `GET` / `POST` | `/structures/` | Liste et création de structures |
| `GET` / `PUT` / `DELETE` | `/structures/<int:pk>/` | Détails, modification et suppression d'une structure |
| `GET` | `/structures/get/` | Liste filtrée des structures |

### 🏠 Gestion des Lieux (Villes & Rues)

| Méthode | URL | Description |
|---------|-----|------------|
| `GET` / `POST` | `/towns/` | Liste et création de villes |
| `GET` / `PUT` / `DELETE` | `/towns/<int:pk>/` | Détails, modification et suppression d'une ville |
| `GET` / `POST` | `/streets/` | Liste et création de rues |
| `GET` / `PUT` / `DELETE` | `/streets/<int:pk>/` | Détails, modification et suppression d'une rue |

### 👥 Gestion des Bénéficiaires (Recipients)

| Méthode | URL | Description |
|---------|-----|------------|
| `GET` / `POST` | `/recipients/` | Liste et création de bénéficiaires |
| `GET` / `PUT` / `DELETE` | `/recipients/<int:pk>/` | Détails, modification et suppression d'un bénéficiaire |
| `GET` | `/recipients/get/` | Liste filtrée des bénéficiaires |

### 🎭 Gestion des Genres

| Méthode | URL | Description |
|---------|-----|------------|
| `GET` / `POST` | `/genres/` | Liste et création de genres |
| `GET` / `PUT` / `DELETE` | `/genres/<int:pk>/` | Détails, modification et suppression d'un genre |

### 🎓 Gestion des Ateliers

| Méthode | URL | Description |
|---------|-----|------------|
| `GET` / `POST` | `/workshops/` | Liste et création d'ateliers |
| `GET` / `PUT` / `DELETE` | `/workshops/<int:pk>/` | Détails, modification et suppression d'un atelier |

### 💳 Gestion des Chèques

| Méthode | URL | Description |
|---------|-----|------------|
| `GET` / `POST` | `/cheques/` | Liste et création de chèques |
| `GET` / `PUT` / `DELETE` | `/cheques/<int:pk>/` | Détails, modification et suppression d'un chèque |
| `POST` | `/cheques/generate/` | Génération de chèques |
| `GET` | `/cheques/get/` | Liste filtrée des chèques |
| `POST` | `/cheques/assign/` | Attribution de chèques |

### 🚨 Gestion des Besoins et Situations

| Méthode | URL | Description |
|---------|-----|------------|
| `GET` / `POST` | `/needs/` | Liste et création de besoins |
| `GET` / `PUT` / `DELETE` | `/needs/<int:pk>/` | Détails, modification et suppression d'un besoin |
| `GET` / `POST` | `/situations/` | Liste et création de situations |
| `GET` / `PUT` / `DELETE` | `/situations/<int:pk>/` | Détails, modification et suppression d'une situation |

### 🎭 Gestion des Rôles

| Méthode | URL | Description |
|---------|-----|------------|
| `GET` / `POST` | `/roles/` | Liste et création de rôles |
| `GET` / `PUT` / `DELETE` | `/roles/<int:pk>/` | Détails, modification et suppression d'un rôle |

### 📂 Gestion des Fichiers

| Méthode | URL | Description |
|---------|-----|------------|
| `GET` | `/files/cheque/download/<str:file_name>` | Téléchargement d'un fichier de chèques |

--