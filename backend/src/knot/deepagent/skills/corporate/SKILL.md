---
name: corporate-intel
description: Corporate ownership resolution and assignee network mapping to identify who controls patent portfolios
allowed-tools: resolve_parent_company, get_ownership_graph, resolve_assignees
metadata:
  author: knot
  version: "1.0"
---

# Corporate Intelligence

## Overview

Use this skill when the user wants to understand corporate ownership structures behind patents — who owns what, subsidiary relationships, and portfolio consolidation.

## When to Use

- User mentions "parent company", "ownership", "subsidiary", "assignee"
- User wants to know who really owns a patent portfolio
- User needs to resolve patent assignee names to corporate entities

## Instructions

### 1. Resolve assignee names

If working with patent assignee names, use `resolve_assignees` with the list of names to map them to canonical company entities.

### 2. Find parent companies

Use `resolve_parent_company` with:
- `company_name`: the entity to investigate
- `company_id`: or the company ID if known

This traverses ownership chains to find the ultimate parent.

### 3. Get ownership graph

Use `get_ownership_graph` with the company ID to visualize the full corporate structure including subsidiaries and ownership percentages.

## Output Format

Provide a structured response with:
- **Ultimate parent** company identification
- **Ownership chain** from subsidiary to parent
- **Related entities** and their patent holdings
- **Summary** of the corporate IP landscape
