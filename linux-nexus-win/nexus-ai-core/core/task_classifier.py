def classify_task(prompt):
    """
    Clasifica el prompt del usuario para decidir qué motor de IA usar.
    """
    prompt_lower = prompt.lower()

    # Palabras clave para tareas técnicas (Código, scripts, etc.)
    technical_keywords = ["script", "bash", "python", "instalar", "configurar", "bug", "error"]

    # Palabras clave para tareas avanzadas (Diseño, planes complejos, etc.)
    advanced_keywords = ["diseño", "plan de negocio", "arquitectura", "matemática compleja", "simulación"]

    if any(keyword in prompt_lower for keyword in technical_keywords):
        return "technical"

    if any(keyword in prompt_lower for keyword in advanced_keywords):
        return "advanced"

    return "simple"
