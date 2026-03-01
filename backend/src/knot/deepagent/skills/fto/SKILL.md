---
name: fto-analysis
description: Freedom-to-Operate analysis for assessing patent infringement risk against a product or technology description
allowed-tools: analyze_fto, check_patent_risk, search_patents, resolve_assignees, find_prior_art
metadata:
  author: knot
  version: "1.0"
---

# FTO Analysis

## Overview

Use this skill when the user wants to assess whether a product, technology, or process risks infringing existing patents. This includes freedom-to-operate studies, infringement risk assessments, and patent clearance requests.

## When to Use

- User mentions "FTO", "freedom to operate", "infringement risk", "patent clearance"
- User describes a product and asks about patent risks
- User wants to know if a technology is safe to commercialize

## Instructions

### 1. Search for relevant patents

Use `search_patents` with keywords extracted from the product/technology description. Include jurisdiction filters if the user specifies target markets (US, EU, IN, etc.).

### 2. Resolve patent assignees

If the search returns patents, use `resolve_assignees` to identify the actual corporate owners behind patent assignee names. This reveals who holds the IP.

### 3. Run FTO analysis

Use `analyze_fto` with:
- `description`: the product/technology description
- `target_markets`: jurisdictions the user cares about
- `keywords`: relevant technical keywords

This performs claim-by-claim matching and risk scoring.

### 4. Check specific high-risk patents

For any patents flagged as high risk, use `check_patent_risk` to get detailed claim-level analysis with mitigation suggestions.

### 5. Search for invalidating prior art (optional)

If high-risk patents are found, use `find_prior_art` to look for prior art that might invalidate concerning claims.

## Output Format

Provide a structured response with:
- **Overall risk level** (high/medium/low)
- **High-risk patents** with claim details and assignee info
- **Mitigation recommendations** for each risk area
- **Summary** of the FTO landscape
