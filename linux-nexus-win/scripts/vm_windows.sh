#!/bin/bash
# scripts/vm_windows.sh

echo "🖥️ Configurando soporte de virtualización KVM para compatibilidad total con Windows..."

# Instalar KVM y herramientas de virtualización
sudo apt update
sudo apt install -y qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils virt-manager virt-viewer virt-install

# Habilitar servicios de virtualización
sudo systemctl enable libvirtd
sudo systemctl start libvirtd

echo "📥 Para instalar Windows 11 en Linux Nexus-Win, usa virt-install o virt-manager."
echo "Ejemplo: virt-install --name nexus-win --ram 8192 --vcpus 4 --disk size=100 --os-variant win11 --cdrom /ruta/a/windows.iso"

echo "✅ Virtualización activa."
