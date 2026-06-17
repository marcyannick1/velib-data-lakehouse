-- Étape 5 : Modélisation PostgreSQL
-- Créer la base de données velib_db

CREATE DATABASE velib_db
    ENCODING 'UTF8'
    TEMPLATE template0;

\c velib_db

-- Afficher la confirmation
SELECT 'Base de données velib_db créée avec succès' AS message;
