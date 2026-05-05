---
type: entity
title: "paper2lkg"
tags: ["tool", "pipeline", "knowledge-graph", "nlp", "llm"]
related: ["deep-document-model", "local-knowledge-graph-construction", "generative-llm", "mention-extraction", "entity-linking", "relation-extraction", "taxonomy-generation"]
sources: ["Chen 等 - 2025 - Open Local Knowledge Graph Construction from Academic Papers Using Generative Large Language Models.md"]
created: 2025-01-01
updated: 2025-01-01
---
# paper2lkg

## Descripción General

**paper2lkg** es un pipeline de construcción de grafos de conocimiento locales diseñado específicamente para transformar artículos académicos individuales en representaciones estructuradas de Grafos de Conocimiento (KG). El nombre "paper2lkg" significa "Paper to Local Knowledge Graph" (De Artículo a Grafo de Conocimiento Local).

El pipeline aprovecha modelos de lenguaje generativos grandes (LLMs) para automatizar tareas clave de Procesamiento de Lenguaje Natural (NLP) en la construcción de grafos de conocimiento.

## Arquitectura del Pipeline

paper2lkg procesa documentos en cinco etapas secuenciales:

### Etapa 1: Extracción de Menciones
Sustituye la tarea tradicional de Reconocimiento de Entidades Nombradas (NER). Utiliza un enfoque de "estrechez a amplitud" que primero extrae solo entidades nombradas, luego entidades nombradas más conceptos generales, y finalmente todas las entidades.

### Etapa 2: Enlace de Entidades
Agrupa menciones que se refieren a la misma entidad en nodos de entidad únicos. Utiliza descripciones generadas por LLM y similitud de coseno de embeddings para determinar cuándo múltiples menciones representan la misma entidad.

### Etapa 3: Extracción de Relaciones Local
Extrae relaciones entre entidades dentro de un contexto limitado (Sección, Párrafo u Oración específicos).

### Etapa 4: Extracción de Relaciones Global
Extrae relaciones que potencialmente abarcan todo el documento, como ("Este documento", "Concluye", "XXX").

### Etapa 5: Generación de Taxonomía y Resolución de Predicados
Construye estructura taxonómica derivando relaciones jerárquicas semánticamente desde el documento original, y agrupa predicados similares.

## Entrada y Salida

| Componente | Descripción |
|------------|-------------|
| **Entrada** | Modelo de Documento Profundo (DDM) del artículo académico |
| **Salida** | DDM más representación de grafo de conocimiento local |

## Componentes de la Salida

Los grafos resultantes consisten en:
- **Entidades**: Con atributos como etiquetas, alias y descripciones
- **Predicados**: Enlaces que conectan entidades
- **Menciones**: Ocurrencias de entidades vinculadas a oraciones específicas en el documento

### Clasificación de Entidades

El sistema categoriza entidades en tres clases mutuamente excluyentes:
1. **Entidades Nombradas**: Objetos del mundo real únicos y específicos (ej: "ANU")
2. **Conceptos Generales**: Cosas abstractas ampliamente reconocidas (ej: "Universidad")
3. **Otras Entidades**: Expresiones compuestas, pronombres o expresiones referenciales no resueltas

## Métricas de Rendimiento

- **Retención de información**: ~88-90%
- **Puntuación RAG**: 0.85-0.88
- **Complejidad**: Lineal con respecto a longitud del documento, entidades, menciones o relaciones

## Repositorio

El artefacto está disponible en: https://w3id.org/kgcp/paper2lkg

## Páginas Relacionadas

- [[deep-document-model]] — Formato de entrada
- [[local-knowledge-graph-construction]] — Concepto general
- [[generative-llm]] — Tecnología subyacente
- [[mention-extraction]] — Etapa 1
- [[entity-linking]] — Etapa 2
- [[relation-extraction]] — Etapas 3 y 4
- [[taxonomy-generation]] — Etapa 5