# 🛠️ Instalación de Linux Nexus-Win

Este documento detalla los pasos necesarios para instalar y configurar Linux Nexus-Win en hardware real o en una máquina virtual.

## 📋 Requisitos Previos

*   Un dispositivo USB de al menos 8GB para crear el medio de arranque.
*   Conexión a internet estable durante el proceso de instalación de post-arranque.
*   Hardware con soporte para virtualización (Intel VT-x o AMD-V) habilitado en la BIOS para compatibilidad completa con Windows.

## 🚀 Proceso de Instalación

1.  **Creación del Medio de Arranque:**
    Usa una herramienta como Rufus o Ventoy para grabar la ISO generada (`linux-nexus-win.iso`) en tu unidad USB.

2.  **Arranque Inicial:**
    Arranca tu equipo desde la unidad USB y selecciona "Live Session" o "Start Installer".

3.  **Instalador Visual Calamares:**
    *   Sigue los pasos en pantalla (Idioma, Región, Teclado).
    *   Elige el particionado de disco (recomendado: "Borrar disco").
    *   Crea tu cuenta de usuario y contraseña.

4.  **Detección y Configuración Adaptativa:**
    Al finalizar la instalación visual, Linux Nexus-Win ejecutará automáticamente sus scripts de post-instalación:
    *   `hardware_detect.sh`: Detectará tu RAM y CPU.
    *   `adaptive_install.sh`: Instalará KDE Plasma o XFCE según los recursos de tu PC.
    *   `wine_setup.sh`: Configurará la capa de compatibilidad para aplicaciones Windows.
    *   `install_ai.sh`: Instalará Ollama y descargará modelos locales de IA.
    *   `vm_windows.sh`: Habilitará el soporte de virtualización KVM.

5.  **Reinicio Final:**
    Una vez que el proceso de post-instalación termine, reinicia tu PC, retira el USB y disfruta de Linux Nexus-Win.

---
Para más detalles sobre la arquitectura del sistema, consulta `ARCHITECTURE.md`.
