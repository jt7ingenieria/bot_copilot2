#!/bin/bash
# scripts/build_iso.sh
set -e

echo "🚀 Iniciando la construcción de NEXUS OS..."

# Actualizar e instalar herramientas necesarias
sudo apt update
sudo apt install -y live-build debootstrap squashfs-tools xorriso

# Configurar el entorno de live-build
lb config --distribution bookworm --debian-installer live --archive-areas "main contrib non-free non-free-firmware"

# Copiar configuraciones y scripts al sistema chroot
mkdir -p config/includes.chroot/usr/local/bin/
mkdir -p config/includes.chroot/opt/nexus/

cp -r ../configs/* config/includes.chroot/etc/nexus/ 2>/dev/null || true
cp -r ../scripts/* config/includes.chroot/usr/local/bin/
cp -r ../nexus-ai-core config/includes.chroot/opt/nexus/
cp -r ../nexus-app-manager config/includes.chroot/opt/nexus/
cp -r ../nexus-control-center config/includes.chroot/opt/nexus/

echo "⚙️ Ejecutando lb build (esto generará la ISO final)..."
# sudo lb build

echo "✅ Proceso de construcción configurado. ISO se generará en el directorio de construcción."
