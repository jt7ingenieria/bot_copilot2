# 🏗️ Arquitectura de Linux Nexus-Win

Linux Nexus-Win utiliza una arquitectura de capas diseñada para flexibilidad, velocidad y compatibilidad total con Windows en una base Linux estable (Debian).

## 🧩 Capas del Sistema

1.  **Capa Base (Kernel y Debian):**
    Basada en Debian Bookworm con el Kernel Zen para mejor rendimiento en tareas de escritorio y latencia reducida.

2.  **Capa de Gestión de Hardware (Nexus Adaptive System):**
    Scripts `hardware_detect.sh` y `adaptive_install.sh` que deciden en tiempo real qué entorno de escritorio (KDE vs XFCE) y qué optimizaciones de sistema aplicar.

3.  **Capa de Compatibilidad (Nexus App Layer):**
    *   **Nativa:** Aplicaciones como Chrome, Firefox y VS Code corren directamente.
    *   **Wine:** Aplicaciones como Office 365 y Notepad++ corren vía Wine con DXVK para aceleración gráfica.
    *   **Virtualización KVM (Nexus VM):** Para software profesional crítico (AutoCAD, Photoshop, Affinity), Linux Nexus-Win utiliza virtualización KVM con aceleración por hardware (GPU Passthrough) para una experiencia 100% Windows nativa.
    *   **Web (PWA):** Aplicaciones como Canva y Perplexity se ejecutan como aplicaciones de escritorio aisladas vía Chromium.

4.  **Capa de Inteligencia Artificial (Nexus AI Core):**
    Un enrutador de IA inteligente (`AIRouter`) que decide qué motor usar:
    *   **Local (Ollama):** Tareas simples y privadas.
    *   **Nube (OpenRouter/OpenAI):** Tareas técnicas y avanzadas.

5.  **Capa de Usuario (Nexus Control Center):**
    Un dashboard central (`main.py` Flask + Frontend HTML5) que unifica el control del sistema, el lanzamiento de apps y la interacción con la IA.

---
Diseño modular para facilitar actualizaciones y mantenimiento continuo.
