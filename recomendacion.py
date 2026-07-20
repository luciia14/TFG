from google import genai

def generar_recomendacion_con_ia(datos_sesion, historial_usuario):
    # Inicializamos el cliente con la nueva librería
    client = genai.Client(api_key="AQ.Ab8RN6LQuGNEwR0qktwYq5MO8a9GGUEWWibr0QjNr37ZQ2GkDA")
    
    contexto_packs = """
    Packs de entrenamiento:
    - Pack 1: Enfocado en mas Hombros y Codos.
    - Pack 2: Enfocado en Hombros y más Codos.
    - Pack 3: Cuello, Torso y un poco de Brazos.
    - Pack 4: Piernas, Cuello, Torso y Brazos.
    - Pack 5: Piernas intenso (fuerte).
    """
    
    prompt = f"""
    Eres un entrenador postural experto. Datos actuales: {datos_sesion}. 
    Historial: {historial_usuario}.
    {contexto_packs}
    
    Reglas:
    1. Si hay fallos altos en una zona, recomienda el Pack que más la trabaje.
    2. Si el usuario nunca ha entrenado piernas, recomiéndale el Pack 4 o 5.
    3. Equilibra la carga: si ha entrenado mucho piernas, sugiérele compensar con torso/brazos (Pack 1, 2 o 3).
    4. Recomienda 2 packs específicos explicando el motivo brevemente.
    
    Respuesta motivadora, directa y de máximo 3 líneas.
    """

    try:
        # Usamos la API de interacciones (la forma correcta en 2026)
        interaction = client.interactions.create(
            model="gemini-3.5-flash", 
            input=prompt
        )
        return interaction.output_text.strip()
        
    except Exception as e:
        print(f"DEBUG: Error en la API moderna: {e}")
        return "¡Buen entrenamiento! Sigue practicando para mejorar tu alineación global."