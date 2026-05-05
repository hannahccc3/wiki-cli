---
type: source
title: "Construcción Abierta de Grafos de Conocimiento Locales a partir de Artículos Académicos Utilizando Modelos de Lenguaje Generativos Grandes"
authors: ["Haoting Chen", "Sergio José Rodríguez Méndez", "Pouya Ghiasnezhad Omran"]
year: 2025
url: "https://doi.org/10.1145/3701716.3717820"
venue: "WWW Companion '25 - Companion Proceedings of the ACM Web Conference 2025"
tags: ["Knowledge Graph Construction", "Natural Language Processing", "Large Language Model", "Entity Recognition", "Relation Extraction", "Academic Papers", "Information Extraction", "Semantic Networks", "Document Representation", "Generative AI"]
related: ["paper2lkg", "local-knowledge-graph-construction", "generative-llm", "mention-extraction", "entity-linking", "relation-extraction", "taxonomy-generation", "knowledge-graph-alignment", "hallucination", "graph-based-rag"]
sources: ["Chen 等 - 2025 - Open Local Knowledge Graph Construction from Academic Papers Using Generative Large Language Models.md"]
created: 2025-01-01
updated: 2025-01-01
---
# Construcción Abierta de Grafos de Conocimiento Locales a partir de Artículos Académicos Utilizando Modelos de Lenguaje Generativos Grandes

## Resumen

Este documento presenta **paper2lkg**, un pipeline innovador para construir grafos de conocimiento locales a partir de artículos académicos utilizando modelos de lenguaje generativos grandes. El pipeline abarca cinco etapas: extracción de menciones, enlace de entidades, extracción de relaciones local y global, y generación de taxonomía. Los resultados experimentales demuestran que los grafos generados retienen información con alta fidelidad (88-90%) y son útiles para sistemas de问答 basados en RAG, aunque el costo computacional sigue siendo significativo.

## Contribuciones Principales

El documento logra tres objetivos principales:

1. **Desarrollo de pipeline funcional**: Se presenta un prototipo de pipeline de construcción de grafos de conocimiento locales adaptado específicamente para artículos académicos, cubriendo todas las tareas clave de KGC.

2. **Enriquecimiento de grafos académicos**: Los grafos de conocimiento locales resultantes pueden enriquecer grafos académicos existentes como ASKG o servir como bloques de construcción para nuevos grafos.

3. **Exploración de eficacia y eficiencia**: Se evalúa brevemente la eficacia y eficiencia de los LLMs generativos en KGC a través de la evaluación del prototipo construido.

## Pipeline paper2lkg

El pipeline paper2lkg transforma documentos académicos individuales en representaciones estructuradas de Grafos de Conocimiento locales. La entrada es cualquier artículo académico que ha sido preprocesado a partir de un archivo de documento sin formato (como PDF) a una representación semiestructurada llamada Modelo de Documento Profundo (DDM).

### Etapas del Pipeline

| Etapa | Descripción | Complejidad |
|-------|-------------|-------------|
| **1. Extracción de Menciones** | Extrae menciones de entidades nombradas, conceptos generales y otras entidades | O(3n) |
| **2. Enlace de Entidades** | Agrupa menciones que se refieren a la misma entidad | O(2m) |
| **3. Extracción de Relaciones Local** | Extrae relaciones dentro de contexto limitado (Sección/Párrafo/Oración) | O(3n) |
| **4. Extracción de Relaciones Global** | Extrae relaciones potencialmente a través de todo el documento | O(n + m²) |
| **5. Generación de Taxonomía** | Construye estructura taxonómica y resuelve predicados | O(e × p + t) |

## Resultados Experimentales

### Retención de Información

Los grafos generados retienen información con alta fidelidad:
- **Puntuación de ingeniería inversa**: ~0.9 (90%) de similitud entre documento original y reconstruido
- **Puntuación RAG**: 0.88 para GPT y 0.85 para LLaMA

### Métricas Generales

Los experimentos muestran crecimiento lineal de entidades, menciones y relaciones con respecto a la longitud del documento, lo que confirma la complejidad lineal del pipeline.

### Costos Computacionales

A pesar de la complejidad lineal, el procesamiento sigue siendo computacionalmente costoso:
- Procesar un artículo de 5000 tokens puede tomar hasta 200 minutos
- El alto costo se debe principalmente al uso de LLMs generativos

## Comparación con Trabajos Relacionados

El enfoque de paper2lkg se diferencia de trabajos anteriores en varios aspectos:

- **Enfoque integral**: A diferencia de estudios previos que se centran en pasos específicos (como solo NER), paper2lkg cubre todo el pipeline de KGC
- **Extracción abierta**: Utiliza extracción de información abierta sin限制了 tipos de entidades o relaciones
- **Enfoque académico**: Diseñado específicamente para artículos académicos, que frecuentemente introducen nuevas entidades no reconocidas por enfoques tradicionales
- **Proceso de EL explícito**: Incluye un proceso de enlace de entidades que muchos otros modelos carecen

## Limitaciones y Trabajo Futuro

1. **Costo computacional**: El alto costo de llamadas a LLMs generativos sigue siendo un desafío
2. **Calidad de grafos**: Se requiere mayor refinamiento para uso en contenido académico de alta precisión
3. **Direcciones futuras**: 
   - *Escalabilidad*: Mejorar rendimiento y eficiencia del pipeline
   - *Ampliación*: Integrar con más grafos de conocimiento académicos

## Páginas Relacionadas

- [[paper2lkg]] — Pipeline principal
- [[local-knowledge-graph-construction]] — Concepto de construcción
- [[generative-llm]] — Modelos utilizados
- [[mention-extraction]] — Etapa 1
- [[entity-linking]] — Etapa 2
- [[relation-extraction]] — Etapas 3 y 4
- [[taxonomy-generation]] — Etapa 5
- [[hallucination]] — Desafío identificado
- [[graph-based-rag]] — Aplicación evaluada
- [[deep-document-model]] — Modelo de entrada