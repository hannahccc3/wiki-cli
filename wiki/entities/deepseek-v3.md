---
type: entity
title: "DeepSeek-V3"
tags: ["llm", "model", "generative"]
related: ["paper2lkg", "generative-llm"]
sources: ["Chen 等 - 2025 - Open Local Knowledge Graph Construction from Academic Papers Using Generative Large Language Models.md"]
created: 2025-01-01
updated: 2025-01-01
---
# DeepSeek-V3

## Descripción General

**DeepSeek-V3** es un modelo de lenguaje grande generativo utilizado en el sistema de evaluación del pipeline paper2lkg. Fue seleccionado específicamente por su gran límite de contexto, superior a cualquier documento en el conjunto de pruebas.

## Uso en paper2lkg

DeepSeek-V3 sirvió como el rol de **"Maestro"** en el sistema de evaluación mediante aplicación:

### Función de Evaluación

1. **Generación de Preguntas y Respuestas**: DeepSeek-V3 leyó documentos completos y generó 10 pares de preguntas y respuestas como verdad fundamental
2. **Instructivos específicos**: Se le pidió crear preguntas con respuestas objetivas que no pudieran responderse con conocimiento común
3. **Referencia obligatoria**: Las preguntas requerían referencia directa al documento original

### Selección del Modelo

DeepSeek-V3 fue elegido porque:
- Su límite de contexto es mayor que cualquier documento de prueba
- Puede procesar documentos completos de una sola vez
- Proporciona respuestas consistentes para evaluación

## Diferenciación de Modelos

En el diseño de evaluación, se使用了 deliberadamente diferentes LLMs para:
- **Lado Maestro (Teacher)**: DeepSeek-V3 genera preguntas
- **Lado Estudiante (Student)**: paper2lkg construye grafos

Esto asegura que las preguntas no estén adaptadas para ser fácilmente respondidas por el mismo modelo.

## Páginas Relacionadas

- [[paper2lkg]] — Pipeline en evaluación
- [[generative-llm]] — Concepto general
- [[graph-based-rag]] — Sistema evaluado