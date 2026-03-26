#!/bin/bash
# scripts/install_ai.sh

echo "🤖 Instalando Nexus AI Engine local..."

# Instalar Ollama para el manejo de modelos LLM locales
curl -fsSL https://ollama.com/install.sh | sh

# Iniciar el servicio Ollama si no está corriendo
sudo systemctl enable ollama
sudo systemctl start ollama

# Descargar modelos locales ligeros y eficientes
echo "📥 Descargando modelos locales: Llama 3 y Mistral..."
ollama pull llama3
ollama pull mistral

echo "✅ Motor de IA local instalado y listo."
