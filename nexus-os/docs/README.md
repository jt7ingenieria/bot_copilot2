# 🌀 Nexus OS v1.0

Nexus OS es un sistema operativo revolucionario basado en Debian, diseñado para ofrecer el máximo rendimiento, privacidad total y una compatibilidad sin precedentes con aplicaciones de Windows.

## ✨ Características Principales

*   **⚡ Rendimiento Adaptativo:** El sistema detecta tu hardware y se configura automáticamente en modo `HIGH_END` (KDE Plasma) o `LOW_END` (XFCE) para garantizar fluidez en cualquier equipo.
*   **🪟 Compatibilidad Total Windows:** Capas integradas de Wine y virtualización KVM optimizada para ejecutar software profesional como AutoCAD, Adobe Creative Cloud y Affinity.
*   **🤖 Nexus AI Core:** Un motor de IA híbrido que combina modelos locales (Ollama) para privacidad con APIs potentes en la nube para tareas complejas.
*   **🔒 Privacidad por Diseño:** Sin telemetría, sin anuncios y con firewall pre-configurado para proteger tus datos.
*   **🎛️ Centro de Control Nexus:** Una interfaz moderna y centralizada para gestionar todo tu sistema, lanzar apps y comunicarte con la IA.

## 📁 Estructura del Proyecto

*   `scripts/`: Automatización de construcción, detección de hardware e instalación.
*   `nexus-ai-core/`: Cerebro de Inteligencia Artificial del sistema.
*   `nexus-app-manager/`: Motor de decisión para la compatibilidad de aplicaciones.
*   `nexus-control-center/`: Backend y Frontend del panel de control.
*   `installer/`: Configuración del instalador visual Calamares.

## 🚀 Inicio Rápido

Para construir la imagen ISO de Nexus OS:

```bash
cd nexus-os
./scripts/build_iso.sh
```

---
Diseñado por Jules para ofrecer fiabilidad, modernidad y potencia.
