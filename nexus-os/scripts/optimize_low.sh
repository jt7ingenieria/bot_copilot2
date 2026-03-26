#!/bin/bash
# scripts/optimize_low.sh

echo "⚡ Aplicando optimizaciones para recursos bajos..."

# Deshabilitar servicios no esenciales
sudo systemctl stop bluetooth cups.service cups-browsed.service
sudo systemctl disable bluetooth cups.service cups-browsed.service

# Configurar Swappiness para reducir el uso de disco swap
echo "vm.swappiness=10" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p

# Habilitar zRAM para mejor gestión de RAM en sistemas limitados
sudo apt update
sudo apt install -y zram-tools
sudo systemctl enable zramswap

echo "✅ Optimizaciones para LOW_END aplicadas."
