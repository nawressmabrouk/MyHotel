CREATE DATABASE IF NOT EXISTS hotel;
USE hotel;

-- Table chambres
CREATE TABLE chambres (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero VARCHAR(10) NOT NULL UNIQUE,
    type VARCHAR(50) NOT NULL,          -- simple, double, suite
    prix_nuit DECIMAL(10,2) NOT NULL CHECK (prix_nuit > 0),
    statut ENUM('libre', 'occupee', 'nettoyage') DEFAULT 'libre'
);

-- Table clients
CREATE TABLE clients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telephone VARCHAR(20),
    adresse TEXT
);

-- Table reservations
CREATE TABLE reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    chambre_id INT NOT NULL,
    date_arrivee DATE NOT NULL,
    date_depart DATE NOT NULL,
    statut ENUM('active', 'terminee', 'annulee') DEFAULT 'active',
    FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE,
    FOREIGN KEY (chambre_id) REFERENCES chambres(id) ON DELETE CASCADE,
    CHECK (date_depart > date_arrivee)
);

-- Table factures
CREATE TABLE factures (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reservation_id INT NOT NULL UNIQUE,
    montant_total DECIMAL(10,2) NOT NULL,
    date_paiement DATE,
    mode_paiement VARCHAR(50),
    FOREIGN KEY (reservation_id) REFERENCES reservations(id) ON DELETE CASCADE
);

-- Table des administrateurs (pour l'authentification)
CREATE TABLE admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);