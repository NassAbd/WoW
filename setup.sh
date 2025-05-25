#!/bin/bash

echo "📦 Installation des dépendances backend..."
cd backend || exit
pip install -r requirements.txt

echo "📦 Installation des dépendances frontend..."
cd ../ui || exit
npm install

echo "✅ Installation terminée."
