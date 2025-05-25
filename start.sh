#!/bin/bash

# Lancer le backend
echo "🚀 Démarrage du backend..."
cd backend || exit
python app.py &
BACKEND_PID=$!

# Attendre que le backend soit prêt (à adapter si besoin)
echo "⏳ Attente du lancement du backend..."
sleep 3

# Lancer le frontend
echo "🚀 Démarrage du frontend..."
cd ../ui || exit
npm start

# Arrêter le backend quand le frontend est arrêté
kill $BACKEND_PID
