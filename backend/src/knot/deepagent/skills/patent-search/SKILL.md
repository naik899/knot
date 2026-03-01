---
name: patent-search
description: Search patents by keywords, domain, or jurisdiction across USPTO, EPO, and CGPDTM databases
allowed-tools: search_patents
metadata:
  author: knot
  version: "1.0"
---

# Patent Search

## Overview

Use this skill when the user wants to search for patents by keywords or within specific jurisdictions. This is often the first step before deeper analysis.

## When to Use

- User asks to "search", "find", or "look up" patents
- User provides keywords and wants matching patents
- User wants patents filtered by jurisdiction (US, EU, IN)

## Instructions

### 1. Extract search parameters

Parse the user's query to identify:
- `keywords`: technical terms, product names, or technology descriptions
- `jurisdictions`: any mentioned countries or regions (US, EU, IN, etc.)

### 2. Search patents

Use `search_patents` with:
- `keywords`: list of relevant terms
- `jurisdictions`: optional jurisdiction filters

### 3. Present results

Organize the search results by relevance, highlighting key patents and their assignees.

## Output Format

Provide a structured response with:
- **Total matches** found
- **Top results** with title, assignee, filing date, and jurisdiction
- **Summary** of the patent landscape for the searched terms
