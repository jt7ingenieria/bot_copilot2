#!/bin/bash
# scripts/wine_setup.sh

echo "🍷 Configurando Wine para compatibilidad con Windows en Linux Nexus-Win..."

# Habilitar soporte para 32 bits
sudo dpkg --add-architecture i386
sudo apt update

# Instalar Wine y herramientas de compatibilidad
sudo apt install -y wine wine32 wine64 winetricks libvulkan1 libvulkan1:i386

# Configurar componentes avanzados
echo "🔧 Instalando DXVK y fuentes de Microsoft vía winetricks..."
winetricks -q dxvk vcrun2019 corefonts

echo "✅ Capa de compatibilidad Wine configurada con éxito."
