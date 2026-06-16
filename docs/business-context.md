# Contexte métier - Optimisation de la disponibilité Vélib

## Présentation

Le service Vélib est un réseau de vélos en libre-service permettant aux utilisateurs de se déplacer dans Paris et sa métropole.

Le réseau est composé de nombreuses stations réparties sur le territoire. Chaque station possède un nombre limité de vélos et de places disponibles.

La disponibilité des vélos évolue en permanence selon :
- les déplacements des utilisateurs
- les horaires
- les jours de la semaine
- les événements
- la localisation des stations

---

# Problème métier

L'exploitation d'un réseau de vélos partagés nécessite de maintenir un bon équilibre entre l'offre et la demande.

Certaines stations peuvent rencontrer deux problèmes principaux :

## Stations en rupture

Une station possède trop peu de vélos disponibles.

Conséquences :
- utilisateur incapable de trouver un vélo
- baisse de satisfaction
- perte d'utilisation du service

---

## Stations saturées

Une station possède trop peu de places libres.

Conséquences :
- utilisateur incapable de déposer son vélo
- déplacement interrompu
- mauvaise expérience utilisateur

---

Le besoin métier identifié est donc :

> Mettre en place une plateforme data permettant de surveiller la disponibilité des stations Vélib, d'identifier les situations critiques et d'aider les équipes opérationnelles à optimiser la redistribution des vélos.

---

# Utilisateurs concernés

## Équipe exploitation

Besoin :
- identifier les stations problématiques
- prioriser les interventions terrain
- améliorer la redistribution

---

## Responsable mobilité

Besoin :
- analyser les tendances d'utilisation
- comprendre les zones à forte demande
- prendre des décisions d'amélioration du réseau

---

## Utilisateurs Vélib

Bénéfice indirect :
- meilleure disponibilité des vélos
- moins de recherches inutiles
- expérience améliorée

---

# Données utilisées

Les données Vélib permettent de suivre l'état du réseau.

## Informations station

Données :
- identifiant station
- nom
- localisation GPS
- capacité

Utilité :
- analyser la répartition géographique
- comparer les stations

---

## Disponibilité en temps réel

Données :
- vélos disponibles
- vélos électriques disponibles
- places disponibles
- état de fonctionnement

Utilité :
- détecter les stations critiques
- mesurer la qualité du service

---

## Historisation

Les données sont stockées dans le temps afin de permettre :

- analyse historique
- détection de tendances
- comparaison des périodes

---

# Valeur apportée

La plateforme permettra de transformer des données temps réel en informations décisionnelles.

## Valeur opérationnelle

Les équipes peuvent :

- détecter rapidement les anomalies
- cibler les interventions
- réduire les stations vides ou saturées

---

## Valeur analytique

Les responsables peuvent suivre :

- évolution de la disponibilité
- zones les plus utilisées
- périodes de forte demande

---

## Valeur stratégique

L'analyse des historiques permet de :

- mieux dimensionner le réseau
- identifier les besoins futurs
- améliorer la qualité globale du service

---

# KPI métier

## Disponibilité moyenne

Formule :

disponibilité = vélos disponibles / capacité station


Objectif :
mesurer l'état global du réseau.


---

## Taux de rupture

Formule :

stations avec disponibilité < seuil / nombre total de stations


Objectif :
identifier les problèmes de disponibilité.


---

## Taux de saturation

Formule :

stations avec places libres < seuil / nombre total de stations


Objectif :
identifier les stations où les utilisateurs ne peuvent pas déposer leur vélo.


---

## Nombre de stations critiques

Une station est critique si :

- disponibilité vélo < 10%

OU

- places disponibles < 10%

---

# Solution proposée

La plateforme Data Lakehouse sera composée de :

API Vélib
↓
Data Lake MinIO
↓
PostgreSQL
↓
Couche analytique SQL
↓
Dashboard
↓
Alertes Telegram


Elle permettra une surveillance continue du réseau et une aide à la décision basée sur les données.