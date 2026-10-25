#!/bin/bash
# Tarea 4 - Instalacion de MongoDB Community Server en hadoop-node1 (Ubuntu 24.04 "noble")
# Ejecutar con: bash /media/sf_Big_Data/Tarea4_mongo/install_mongodb.sh
set -e

echo "=== 1. Paquetes base (gnupg, curl) ==="
sudo apt-get update -y
sudo apt-get install -y gnupg curl

echo "=== 2. Clave GPG oficial de MongoDB ==="
curl -fsSL https://pgp.mongodb.com/server-8.0.asc | sudo gpg -o /usr/share/keyrings/mongodb-server-8.0.gpg --dearmor

echo "=== 3. Repositorio apt oficial de MongoDB 8.0 (noble) ==="
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-8.0.gpg ] https://repo.mongodb.org/apt/ubuntu noble/mongodb-org/8.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-8.0.list

echo "=== 4. Instalar mongodb-org ==="
sudo apt-get update -y
sudo apt-get install -y mongodb-org

echo "=== 5. Arrancar y habilitar el servicio ==="
sudo systemctl start mongod
sudo systemctl enable mongod
sleep 3

echo "=== 6. Verificacion ==="
mongod --version || true
sudo systemctl status mongod --no-pager || true

echo "=== 7. Driver pymongo para Python ==="
pip3 install --break-system-packages pymongo 2>/dev/null || pip3 install pymongo || sudo apt-get install -y python3-pymongo

echo "=== LISTO: MongoDB instalado y corriendo en localhost:27017 ==="
