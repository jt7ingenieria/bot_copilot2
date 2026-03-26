from flask import Flask, jsonify, request
import subprocess
import os

app = Flask(__name__)

@app.route("/api/system/info")
def system_info():
    try:
        cpu_usage = subprocess.getoutput(r"top -bn1 | grep 'Cpu(s)' | sed 's/.*, *\([0-9.]*\)%* id.*/\1/' | awk '{print 100 - $1\"%\"}'")
        ram_usage = subprocess.getoutput("free -m | awk '/Mem:/ { printf \"%.2f%%\", $3/$2*100 }'")
        mode = subprocess.getoutput("cat /etc/nexus_mode 2>/dev/null") or "HIGH_END"

        return jsonify({
            "status": "online",
            "cpu": cpu_usage,
            "ram": ram_usage,
            "mode": mode,
            "os": "Nexus OS v1.0"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/system/set-mode", methods=["POST"])
def set_mode():
    data = request.json
    mode = data.get("mode")

    if mode in ["LOW_END", "HIGH_END"]:
        os.system(f"echo '{mode}' | sudo tee /etc/nexus_mode")
        # Aquí se ejecutarían los scripts de optimización correspondientes
        if mode == "LOW_END":
            subprocess.Popen(["/usr/local/bin/optimize_low.sh"])
        else:
             # Script para restaurar recursos si existiera
             pass
        return jsonify({"success": True, "new_mode": mode})

    return jsonify({"error": "Modo inválido"}), 400

@app.route("/api/launch", methods=["POST"])
def launch_app():
    data = request.json
    app_name = data.get("app")

    if app_name:
        # Llamar al motor de Nexus App Manager
        subprocess.Popen(["python3", "/opt/nexus/nexus-app-manager/core/engine.py", app_name])
        return jsonify({"success": True, "launched": app_name})

    return jsonify({"error": "Nombre de app no proporcionado"}), 400

@app.route("/api/ai/ask", methods=["POST"])
def ask_ai():
    data = request.json
    prompt = data.get("prompt")

    if prompt:
        # Importación dinámica del motor de IA
        import sys
        sys.path.append("/opt/nexus/nexus-ai-core")
        from core.ai_router import AIRouter

        router = AIRouter()
        response = router.ask(prompt)
        return jsonify({"success": True, "response": response})

    return jsonify({"error": "Prompt no proporcionado"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
