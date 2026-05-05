---
type: entity
title: "BAAI–bgem3"
tags: ["embedding", "model", "encoder"]
related: ["paper2lkg", "generative-llm", "taxonomy-generation"]
sources: ["Chen 等 - 2025 - Open Local Knowledge Graph Construction from Academic Papers Using Generative Large Language Models.md"]
created: 2025-01-01
updated: 2025-01-01
---
# BAAI–bgem3

## Descripción General

**BAAI–bgem3** es un modelo de codificador de embeddings desarrollado por BAAI (Beijing Academy of Artificial Intelligence). Se utiliza en paper2lkg específicamente para la Etapa 5 de Generación de Taxonomía.

## Especificaciones

| Parámetro | Valor |
|-----------|-------|
| **Tipo** | Codificador de embeddings |
| **Límite de contexto** | 8192 tokens |
| **Proveedor** | BAAI |
| **Uso en pipeline** | Etapa 5: Generación de Taxonomía |

## Función en paper2lkg

En la Etapa 5, BAAI–bgem3 se utiliza para:

### Generación de Embeddings

1. **Embeddings de descripciones**: Convierte descripciones de tipos de entidades y predicados en vectores
2. **Cálculo de similitud**: Utiliza similitud de coseno para detectar tipos padre similares
3. **Agrupación de predicados**: Detecta predicados similares para resolución

### Proceso de Taxonomía

```
Para cada Entidad:
    Para cada Tipo Padre Potencial:
        Generar descripción con LLM
        Convertir a embedding con BAAI-bgem3
        
    Para cada par de entidades:
        Si similitud(embeddings) > umbral:
            Crear enlace taxonómico
```

## Ventajas

- **Alta dimensionalidad**: Captura relaciones semánticas complejas
- **Contexto amplio**: 8192 tokens permite descripciones extensas
- **Optimizado para español**: Funciona bien con contenido multilingüe

## Comparación

BAAI–bgem3 se complementa con BAAI–bge-base-env1.5, utilizado en otras etapas del pipeline.

## Páginas Relacionadas

- [[paper2lkg]] — Pipeline que lo utiliza
- [[taxonomy-generation]] — Etapa donde se usa
- [[generative-llm]] — Modelos generativos complementarios