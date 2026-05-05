---
type: entity
title: "Meta-Llama-3-8B-Instruct"
tags: ["llm", "model", "generative", "meta"]
related: ["paper2lkg", "generative-llm", "gpt-4o-mini"]
sources: ["Chen 等 - 2025 - Open Local Knowledge Graph Construction from Academic Papers Using Generative Large Language Models.md"]
created: 2025-01-01
updated: 2025-01-01
---
# Meta-Llama-3-8B-Instruct

## Descripción General

**Meta-Llama-3-8B-Instruct** es un modelo de lenguaje grande generativo desarrollado por Meta (anteriormente Facebook). En el contexto del artículo, se utiliza específicamente la versión cuantizada Q4_0 con un límite de contexto de 8192 tokens.

## Especificaciones Técnicas

| Parámetro | Valor |
|-----------|-------|
| **Parámetros** | 8 mil millones |
| **Tipo** | Generativo, autoregresivo |
| **Límite de contexto** | 8192 tokens |
| **Versión utilizada** | Q4_0 (cuantizada) |
| **Arquitectura** | Transformer |

## Uso en paper2lkg

Meta-Llama-3-8B-Instruct fue uno de los dos LLMs generativos utilizados en los experimentos del pipeline paper2lkg:

### Etapas donde se utiliza

1. **Etapa 1 - Extracción de Menciones**: Genera listas de entidades, conceptos y menciones
2. **Etapa 2 - Enlace de Entidades**: Genera descripciones de menciones
3. **Etapa 3 - Extracción de Relaciones Local**: Extrae tripletas (Sujeto, Predicado, Objeto)
4. **Etapa 4 - Extracción de Relaciones Global**: Extrae relaciones a nivel de documento
5. **Etapa 5 - Generación de Taxonomía**: Genera descripciones para taxonomía

### Comparación de Rendimiento

En los experimentos, LLaMA mostró resultados competitivos:
- **Puntuación RAG promedio**: 0.85
- **Tiempo de ejecución**: Lineal con la longitud del documento

## Ventajas

- **Eficiencia local**: Puede ejecutarse en hardware accesible (RTX 3080 12GB)
- **Código abierto**: Permite modificación y estudio
- **Contexto suficiente**: 8192 tokens es adecuado para la mayoría de secciones de artículos

## Limitaciones

- Menor capacidad comparada con modelos más grandes
- Puede generar alucinaciones en descripciones complejas

## Páginas Relacionadas

- [[paper2lkg]] — Pipeline que utiliza este modelo
- [[generative-llm]] — Concepto general
- [[gpt-4o-mini]] — Otro modelo utilizado en comparación