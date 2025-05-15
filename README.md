# LangGraph Multi-Turn Chatbot Example

## Descripción

Este repositorio es un ejemplo educativo de cómo construir un **chatbot conversacional multi-turno** utilizando [LangGraph](https://langchain-ai.github.io/langgraph/) y modelos de lenguaje (LLM). Permite interactuar con el bot en la terminal, manteniendo el historial de la conversación y generando respuestas dinámicas.

## Características principales

- **Chat multi-turno:** Mantiene el historial de mensajes y responde de manera contextual.
- **Integración con LLM:** Utiliza modelos como OpenAI GPT para generar respuestas.
- **Arquitectura modular:** Separación clara entre vectorstore, agentes y grafo conversacional.
- **Extensible:** Base sólida para agregar herramientas, memoria, o agentes adicionales.
- **Buenas prácticas:** Tipado explícito, manejo de estado, y configuración segura por variables de entorno.

## Instalación

1. Clona el repositorio y entra en la carpeta del proyecto.
2. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

3. Crea un archivo `.env` en la raíz con tus claves y configuración:

   ```env
   OPENAI_API_KEY=tu_api_key
   OPENAI_MODEL=gpt-3.5-turbo
   EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
   BOOK_URL=https://ruta/a/tu/libro.pdf
   ```

## Uso interactivo (modo chat)

Ejecuta el bot en la terminal:

```bash
python main.py
```

Interactúa escribiendo tus preguntas. Escribe `salir`, `exit` o `quit` para terminar la conversación.

**Ejemplo:**

```bash
Tú: ¿Quién es el personaje principal?
Bot: El personaje principal es...
Tú: ¿Dónde ocurre la historia?
Bot: La historia ocurre en...
Tú: salir
Adiós!
```

## Arquitectura

- **VectorStoreManager:** Gestiona la indexación y recuperación de documentos con FAISS y embeddings.
- **Agentes:** Implementan la lógica de síntesis de respuestas usando LLM.
- **Grafo conversacional:** Orquesta el flujo de mensajes y mantiene el historial.

## Extensibilidad

- Puedes agregar herramientas externas, memoria, o nuevos agentes siguiendo la arquitectura modular.
- El grafo puede adaptarse para flujos más complejos, integración de APIs, o lógica condicional avanzada.

## Buenas prácticas

- Uso de tipado explícito (`TypedDict`, `Annotated`).
- Separación de responsabilidades por módulo.
- Configuración segura por variables de entorno.
- Cumple con las recomendaciones de la [documentación oficial de LangGraph](https://langchain-ai.github.io/langgraph/tutorials/introduction/).

## Recursos y referencias

- [Documentación oficial de LangGraph](https://langchain-ai.github.io/langgraph/)
- [Ejemplo de chat multi-turno en LangGraph](https://langchain-ai.github.io/langgraph/tutorials/introduction/)

---

Este repositorio es ideal para aprender, experimentar y construir asistentes conversacionales avanzados con LangGraph y LLMs.
