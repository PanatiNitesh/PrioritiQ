#!/usr/bin/env bash
# Render Build Script for PrioritiQ Full-Stack Unified Deployment
set -o errexit

echo "==> [1/4] Installing Python backend dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "==> [2/4] Initializing and seeding PrioritiQ database..."
mkdir -p data
python -m backend.database.seed

echo "==> [3/4] Installing Node.js dependencies and building frontend..."
cd frontend
npm install
npm run build
cd ..

echo "==> [4/4] Verifying static bundle artifacts..."
if [ -f "frontend/dist/index.html" ]; then
    echo "✓ Production bundle verified: frontend/dist/index.html is ready"
else
    echo "ERROR: frontend/dist/index.html not found!"
    exit 1
fi

echo "==> [SUCCESS] PrioritiQ full-stack build complete and ready for deployment!"
