import json
import subprocess
import sys
import os

RULES_PATH = os.getenv('NEXUS_RULES_PATH', '/opt/nexus/nexus-app-manager/core/rules.json')

def load_rules():
    try:
        with open(RULES_PATH, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error al cargar reglas de aplicaciones: {str(e)}")
        return {}

def launch_app(app_name):
    rules = load_rules()

    # Modo por defecto: nativo Linux
    mode = rules.get(app_name, "native")

    print(f"🚀 Iniciando '{app_name}' en modo: {mode}")

    if mode == "native":
        # Ejecutar binario nativo de Linux
        try:
             subprocess.Popen([app_name.lower()])
        except FileNotFoundError:
             # Si no se encuentra el binario, intentar como comando directo
             subprocess.Popen([app_name])

    elif mode == "wine":
        # Ejecutar vía capa de compatibilidad Wine
        subprocess.Popen(["wine", f"{app_name}.exe"])

    elif mode == "vm":
        # Iniciar la Máquina Virtual de Windows integrada
        print(f"🌀 Iniciando entorno Windows aislado para '{app_name}'...")
        subprocess.run(["virsh", "start", "nexus-win"])
        # Aquí se podría añadir lógica para abrir la app específica dentro de la VM vía SSH o RDP

    elif mode == "web":
        # Ejecutar como Aplicación Web Progresiva (PWA) vía Chromium/Chrome
        url_map = {
            "Canva": "https://www.canva.com",
            "Perplexity": "https://www.perplexity.ai",
            "ChatGPT": "https://chatgpt.com",
            "Google Docs": "https://docs.google.com",
            "Gmail": "https://mail.google.com"
        }
        url = url_map.get(app_name, f"https://www.google.com/search?q={app_name}")
        subprocess.Popen(["chromium", "--app=" + url])

    else:
        print(f"⚠️ Modo desconocido '{mode}' para la aplicación '{app_name}'.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 engine.py <nombre_app>")
        sys.exit(1)

    launch_app(sys.argv[1])
