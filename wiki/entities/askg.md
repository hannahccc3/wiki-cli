---
type: entity
title: "ANU Academic Scholarly Knowledge Graph (ASKG)"
tags: ["knowledge-graph", "academic", "research"]
related: ["paper2lkg", "australian-national-university", "knowledge-graph-alignment"]
sources: ["Chen 等 - 2025 - Open Local Knowledge Graph Construction from Academic Papers Using Generative Large Language Models.md"]
created: 2025-01-01
updated: 2025-01-01
---
# ANU Academic Scholarly Knowledge Graph (ASKG)

## Descripción General

El **Academic Scholarly Knowledge Graph (ASKG)** es un grafo de conocimiento académico experimental desarrollado en la Universidad Nacional Australiana (ANU). Almacena artículos de investigación de la universidad y se enfoca en enlazar y organizar metadatos a través de varias fuentes.

## Propósito

ASKG fue diseñado para asistir a investigadores en:

- Recuperar información académica
- Organizar datos de investigación
- Mantener una vista unificada de dominios de investigación

## Limitaciones Identificadas

Aunque ASKG integra conocimiento a través de corpus académicos extensos, alignando conceptos, citas y autoría, tiene una limitación específica:

> *"Carece de una representación semántica profunda de cada artículo, es decir, un sub-grafo local que capture las Entidades y Relaciones dentro."*

Esta limitación es precisamente la que paper2lkg busca abordar.

## Integración con paper2lkg

El pipeline paper2lkg fue diseñado específicamente para:

1. **Enriquecer ASKG**: Agregar representaciones semánticas locales de artículos individuales
2. **Construir nuevos grafos**: Servir como bloques de construcción para grafos académicos más amplios
3. **Mantener diferencias**: Proporcionar una vista unificada de un tema mientras mantiene las diferencias en las discusiones entre artículos

## Relación con Otros Grafos Académicos

ASKG es parte de un ecosistema más amplio de grafos de conocimiento académicos que incluye:

- Open Research Knowledge Graph
- Microsoft Academic Graph
- AMiner

## Páginas Relacionadas

- [[paper2lkg]] — Pipeline diseñado para enriquecer ASKG
- [[australian-national-university]] — Institución desarrolladora
- [[knowledge-graph-alignment]] — Proceso de integración
- [[local-knowledge-graph-construction]] — Concepto relacionado