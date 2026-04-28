#!/bin/bash
# scripts/adaptive_install.sh

MODE=$(cat /etc/nexus_mode 2>/dev/null || echo "HIGH_END")

echo "📦 Ejecutando instalación adaptativa para el modo: $MODE"

if [ "$MODE" = "LOW_END" ]; then
    echo "☁️ Instalando entorno ligero (XFCE)..."
    sudo apt update
    sudo apt install -y xfce4 xfce4-goodies lightdm
    # Desactivar servicios pesados
    sudo systemctl disable bluetooth cups 2>/dev/null || true
else
    echo "💎 Instalando entorno completo (KDE Plasma)..."
    sudo apt update
    sudo apt install -y kde-standard sddm
    # Habilitar servicios avanzados
    sudo systemctl enable libvirtd 2>/dev/null || true
fi

echo "✅ Instalación adaptativa completada para $MODE."
