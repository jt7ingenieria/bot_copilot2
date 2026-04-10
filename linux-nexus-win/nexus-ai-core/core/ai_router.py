import os
import json
import subprocess
from .task_classifier import classify_task
from ..local.llama_runner import run_local_model
from ..cloud.open_source_apis import call_open_api
from ..cloud.subscription_apis import call_premium_api

CONFIG_PATH = os.getenv('NEXUS_AI_CONFIG', '/etc/nexus/ai_config.json')

class AIRouter:
    def __init__(self):
        try:
            with open(CONFIG_PATH, 'r') as f:
                self.config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.config = {
                "mode": "auto",
                "local_ai": True,
                "cloud_ai": True,
                "privacy": True
            }

    def ask(self, prompt):
        mode = self.config.get("mode", "auto")

        # Filtro de privacidad básico
        if self.config.get("privacy", True):
             # Aquí se podría añadir lógica de redacción de datos personales
             pass

        if mode == "offline":
            return run_local_model(prompt)

        task_type = classify_task(prompt)

        if task_type == "simple" or not self.config.get("cloud_ai", True):
            return run_local_model(prompt)

        if task_type == "technical":
            return call_open_api(prompt)

        if task_type == "advanced":
            return call_premium_api(prompt)

        return run_local_model(prompt)
