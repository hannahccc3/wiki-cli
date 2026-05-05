---
type: entity
title: "Deep Document Model (DDM)"
tags: ["model", "document-representation", "rdf"]
related: ["paper2lkg", "australian-national-university"]
sources: ["Chen 等 - 2025 - Open Local Knowledge Graph Construction from Academic Papers Using Generative Large Language Models.md"]
created: 2025-01-01
updated: 2025-01-01
---
# Deep Document Model (DDM)

## Descripción General

El **Modelo de Documento Profundo** (Deep Document Model, DDM) es una representación semiestructurada utilizada como entrada para el pipeline paper2lkg. Transforma documentos académicos sin formato, como PDFs, en una estructura que puede ser procesada eficientemente por algoritmos de NLP.

## Características Principales

### Estructura RDF-Graph

El DDM está basado en la estructura de grafo RDF, lo que permite:

- Representación estructurada de información
- Fácil navegación y acceso a partes específicas del documento
- Compatibilidad con estándares de la web semántica

### Jerarquía Documental

El modelo organiza un documento académico en una jerarquía de niveles:

```
Artículo
├── Metadatos
├── Sección 1
│   ├── Párrafo 1
│   │   ├── Oración 1
│   │   └── Oración 2
│   └── Párrafo 2
└── Sección 2
    └── ...
```

### Metadatos Incluidos

El DDM incluye metadatos del artículo como:
- Título
- Autores
- Palabras clave
- Información de citas

## Función en paper2lkg

El DDM sirve como entrada al pipeline paper2lkg, permitiendo:

1. **Recorrido eficiente**: Los algoritmos pueden atravesar el documento eficientemente
2. **Acceso específico**: Se pueden acceder partes específicas para tareas de NLP
3. **Preservación estructural**: Mantiene la estructura jerárquica del documento original

## Complemento de Salida

La salida de paper2lkg es el DDM más la representación de grafo de conocimiento local del artículo, donde:
- Las entidades se vinculan a oraciones específicas
- Las menciones se referencian a ubicaciones precisas
- Las relaciones mantienen contexto documental

## Repositorio

Más detalles sobre DDM están disponibles en: https://w3id.org/kgcp/DDM

## Páginas Relacionadas

- [[paper2lkg]] — Pipeline que utiliza DDM como entrada
- [[mention-extraction]] — Proceso que usa la estructura del DDM
- [[relation-extraction]] — Extracción basada en contexto del DDM