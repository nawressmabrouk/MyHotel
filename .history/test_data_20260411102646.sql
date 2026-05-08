INSERT INTO chambres (numero, type, prix_nuit, statut) VALUES
('101', 'simple', 50.00, 'libre'),
('102', 'double', 80.00, 'libre'),
('103', 'suite', 150.00, 'occupee');

INSERT INTO clients (nom, email, telephone, adresse) VALUES
('Jean Dupont', 'jean@example.com', '0612345678', '10 rue de Paris'),
('Marie Martin', 'marie@example.com', '0698765432', '5 avenue des Lilas');

INSERT INTO reservations (client_id, chambre_id, date_arrivee, date_depart, statut) VALUES
(1, 1, '2025-04-10', '2025-04-12', 'active'),
(2, 3, '2025-04-15', '2025-04-18', 'active');

-- Facture pour la réservation 1 (à calculer manuellement ici)
INSERT INTO factures (reservation_id, montant_total, date_paiement, mode_paiement) VALUES
(1, 100.00, '2025-04-10', 'carte bancaire');

