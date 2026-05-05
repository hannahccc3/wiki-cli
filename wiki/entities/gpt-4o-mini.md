---
type: entity
title: "GPT-4o-mini"
tags: ["llm", "model", "generative", "openai"]
related: ["paper2lkg", "generative-llm", "meta-llama-3-8b-instruct"]
sources: ["Chen 等 - 2025 - Open Local Knowledge Graph Construction from Academic Papers Using Generative Large Language Models.md"]
created: 2025-01-01
updated: 2025-01-01
---
# GPT-4o-mini

## Descripción General

**GPT-4o-mini** es un modelo de lenguaje grande generativo desarrollado por OpenAI. Se caracteriza por ser una versión más ligera y económica de GPT-4o, con un límite de contexto de 128,000 tokens, significativamente mayor que LLaMA.

## Especificaciones Técnicas

| Parámetro | Valor |
|-----------|-------|
| **Modelo base** | GPT-4o |
| **Tipo** | Generativo, autoregresivo |
| **Límite de contexto** | 128,000 tokens |
| **Proveedor** | OpenAI API |

## Uso en paper2lkg

GPT-4o-mini fue utilizado como segundo LLM generativo en los experimentos comparativos del pipeline paper2lkg:

### Comparación con LLaMA

| Métrica | GPT-4o-mini | Meta-Llama-3-8B-Instruct |
|---------|-------------|--------------------------|
| Puntuación RAG promedio | 0.88 | 0.85 |
| Costo por documento | Variable (API) | N/A (local) |
| Límite de contexto | 128k tokens | 8,192 tokens |

### Rol en Evaluación

GPT-4o-mini también se utilizó en:
- **Sistema Q&A**: Para generar respuestas utilizando grafos de conocimiento locales
- **Embedding de documentos**: Para calcular similitud en evaluación por ingeniería inversa

## Ventajas

- **Mayor contexto**: 128k tokens permite procesar documentos más largos en una sola pasada
- **Menor costo**: Más económico que GPT-4o completo
- **Alta calidad**: Mantiene capacidades de razonamiento de la familia GPT-4

## Limitaciones

- **Costo API**: Requiere pago por uso
- **Dependencia de Internet**: No funciona offline
- **No editable**: No se puede modificar el modelo internamente

## Páginas Relacionadas

- [[paper2lkg]] — Pipeline de experimentación
- [[generative-llm]] — Concepto general
- [[meta-llama-3-8b-instruct]] — Modelo comparativo