import subprocess

def run_local_model(prompt):
    """
    Ejecuta el modelo local (Llama3 por defecto en Nexus OS).
    Utiliza Ollama como motor de inferencia local.
    """
    try:
        # Comando para correr llama3 vía Ollama de forma asíncrona
        result = subprocess.run(
            ["ollama", "run", "llama3", prompt],
            capture_output=True,
            text=True,
            timeout=30 # Tiempo límite para evitar bloqueos
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"⚠️ Error en motor local Ollama: {result.stderr}"
    except Exception as e:
        return f"❌ Fallo al intentar conectar con Ollama: {str(e)}"
