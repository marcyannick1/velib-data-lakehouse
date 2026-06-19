# 🚲 Velib Data Lakehouse

Projet de Data Engineering permettant la collecte, le stockage, la transformation, l'analyse et la supervision des données temps réel des stations Vélib' de Paris.

L'architecture repose sur :

- **API Vélib' Open Data**
- **MinIO** — Data Lake
- **PostgreSQL** — Data Warehouse
- **Airflow** — Orchestration
- **Metabase** — Dashboarding
- **Telegram Bot** — Alerting & consultation KPI

---

## 📌 Architecture du projet

```
velib-data-lakehouse/
│
├── airflow/
│   ├── dags/
│   │   └── velib_pipeline.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── ingestion/
│   ├── api_client.py
│   ├── config.py
│   ├── extract_pipeline.py
│   ├── staging_pipeline.py
│   ├── curated_pipeline.py
│   ├── pipeline.py
│   ├── storage.py
│   ├── minio_client.py
│   ├── staging_processor.py
│   ├── curated_processor.py
│   └── main.py
│
├── postgres/
│   ├── connection.py
│   ├── loader.py
│   ├── load_time_dimension.py
│   ├── init.sql
│   └── __init__.py
│
├── analytics/
│   └── analytics.sql
│
├── automation/
│   ├── config.py
│   ├── telegram_sender.py
│   ├── alert_checker.py
│   ├── telegram_bot.py
│   ├── handle_command.py
│   └── run.sh
│
├── scripts/
│   └── init_database.sh
│
├── docs/
│   └── business-context.md
│
├── .env
├── docker-compose.yml
├── Dockerfile.telegram
├── README.md
└── .gitignore
```

---

## 🎯 Objectifs du projet

Construire une plateforme complète de données permettant :

- Ingestion temps réel des stations Vélib'
- Stockage brut dans un Data Lake
- Transformation multi-couches
- Alimentation d'un Data Warehouse
- Calcul de KPI
- Visualisation dans Metabase
- Alertes automatiques Telegram
- Consultation des KPI directement depuis Telegram

---

## 🏗️ Architecture Data Lakehouse

```
      Vélib API
          │
          ▼
   Extraction Layer
          │
          ▼
   MinIO Raw Zone
          │
          ▼
 Staging Transformation
          │
          ▼
 MinIO Staging Zone
          │
          ▼
 Curated Transformation
          │
          ▼
 PostgreSQL Warehouse
          │
   ┌──────┴──────┐
   ▼             ▼
Metabase   Telegram Bot
```

---

## 🚀 Stack Technique

| Outil | Usage |
|-------|-------|
| Python | ETL |
| PostgreSQL | Data Warehouse |
| MinIO | Data Lake |
| Apache Airflow | Orchestration |
| Metabase | Dashboard |
| Telegram Bot | Alerting |
| Docker | Conteneurisation |

---

## 📥 Source de données

**API OpenData Vélib'** — `https://opendata.paris.fr`

Données collectées :

- Stations & coordonnées GPS
- Capacité
- Vélos disponibles & vélos électriques
- Bornes libres
- Timestamp

---

## 📂 Data Lake

### Raw Layer

Données brutes récupérées depuis l'API.

Format : `raw/YYYY/MM/DD/HH/`

Exemple : `raw/2026/06/18/15/`

### Staging Layer

Données nettoyées :

- Suppression des colonnes inutiles
- Typage
- Standardisation

### Curated Layer

Données enrichies :

- Calcul de taux d'occupation
- Normalisation métier
- Préparation analytique

---

## 🗄️ Data Warehouse

### `fact_station_status` — Table de faits

Historique des états des stations.

| Colonne | Description |
|---------|-------------|
| `station_id` | Identifiant station |
| `event_time` | Horodatage |
| `bikes_available` | Vélos disponibles |
| `ebikes_available` | Vélos électriques |
| `docks_available` | Bornes libres |

### `dim_station` — Dimension Station

Informations descriptives des stations.

| Colonne | Description |
|---------|-------------|
| `station_id` | Identifiant |
| `station_code` | Code station |
| `name` | Nom |
| `capacity` | Capacité totale |
| `latitude` | Latitude GPS |
| `longitude` | Longitude GPS |

### `dim_time` — Dimension Temps

Permet les analyses temporelles.

| Colonne | Description |
|---------|-------------|
| `time_id` | Identifiant |
| `date` | Date complète |
| `hour` | Heure |
| `day` | Jour |
| `month` | Mois |
| `year` | Année |
| `day_of_week` | Jour de la semaine |

---

## 📊 Couche Analytique

Vues SQL définies dans `analytics/analytics.sql`.

### `vw_global_kpi` — KPI Global

- Nombre de stations
- Vélos disponibles & électriques
- Bornes libres
- Moyenne de vélos par station

### `vw_station_availability` — Disponibilité par station

- Occupation d'une station
- Capacité restante

### `vw_station_alert` — Alertes stations

Détecte automatiquement les situations critiques :

| Alerte | Règle |
|--------|-------|
| `LOW_BIKES` | `bikes_available <= 3` |
| `NO_SPACE` | `docks_available <= 2` |

### `vw_hourly_usage` — Occupation par heure

Occupation moyenne par heure de la journée.

### `vw_daily_usage` — Occupation par jour

Occupation moyenne par jour de la semaine.

### `vw_top_busy_stations` — Top stations

Stations les plus utilisées.

### `vw_critical_stations` — Stations critiques

Classement des stations régulièrement en alerte.

---

## ⚙️ Orchestration Airflow

DAG principal : `velib_pipeline`

```
extract
  ↓
staging
  ↓
curated
  ↓
load_postgres
  ↓
populate_time_dimension
  ↓
analytics_views
  ↓
alerting
```

---

## 🔔 Alerting Telegram

Script : `automation/alert_checker.py`

Le système :

1. Interroge `vw_station_alert`
2. Génère un message formaté
3. Envoie une notification Telegram

Exemple de notification :

```
🚨 12 station(s) critique(s)

📍 Gare de Lyon
🚲 vélos : 2
🅿️ places : 45
⚠️ LOW_BIKES
```

---

## 🤖 Bot Telegram

Script : `automation/telegram_bot.py`

Permet de consulter les KPI sans ouvrir Metabase.

### Commandes disponibles

| Commande | Description |
|----------|-------------|
| `/start` | Message de bienvenue |
| `/kpi` | KPI globaux (stations, vélos, bornes, dernière MAJ) |
| `/alerts` | Stations critiques en temps réel |
| `/stations` | Liste des stations disponibles |
| `/help` | Liste des commandes |

---

## 📈 Dashboard Metabase

Metabase est connecté directement à PostgreSQL.

### Vue Exécutive

Cartes de synthèse : stations totales, vélos disponibles, vélos électriques, bornes libres.

### Vue Opérationnelle

- Occupation moyenne par heure
- Occupation par jour
- Stations critiques
- Top stations

### Carte géographique

Visualisation des stations sur Paris.

---

## 🐳 Déploiement Docker

```bash
# Lancement
docker compose up -d

# Reconstruction Airflow
docker compose build airflow

# Reconstruction Telegram Bot
docker compose build telegram_bot

# Vérification
docker ps
```

---

## 🔐 Variables d'environnement

Fichier `.env` :

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=velib

MINIO_ROOT_USER=minio
MINIO_ROOT_PASSWORD=minio123

TELEGRAM_BOT_TOKEN=xxxxxxxx
TELEGRAM_CHAT_ID=xxxxxxxx
```

---

## 📚 Compétences démontrées

- Data Engineering (ETL/ELT, Data Lakehouse)
- PostgreSQL & SQL Analytics
- Apache Airflow
- Docker
- Monitoring & Alerting
- Data Visualization
- API Integration
- Telegram Bot Development

---

## 👨‍💻 Auteur

Projet réalisé dans le cadre d'un portfolio Data Engineering autour des données temps réel Vélib' de Paris.

**Stack :** Python • PostgreSQL • MinIO • Airflow • Metabase • Telegram • Docker 🚀