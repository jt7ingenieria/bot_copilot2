#!/bin/bash
# scripts/hardware_detect.sh

RAM=$(free -m | awk '/Mem:/ {print $2}')
CPU_CORES=$(nproc)

echo "🔍 Detectando hardware..."
echo "RAM detectada: $RAM MB"
echo "Núcleos de CPU: $CPU_CORES"

if [ "$RAM" -lt 4000 ]; then
    echo "⚠️ Recursos bajos detectados. Configurando Linux Nexus-Win en modo LOW_END."
    echo "LOW_END" > /etc/nexus_mode
else
    echo "🚀 Recursos suficientes detectados. Configurando Linux Nexus-Win en modo HIGH_END."
    echo "HIGH_END" > /etc/nexus_mode
fi
