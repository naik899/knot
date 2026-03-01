---
name: market-analysis
description: Patent-product matching and commercial application analysis to find IP relevant to products or products relevant to patents
allowed-tools: match_patent_to_products, find_product_matches
metadata:
  author: knot
  version: "1.0"
---

# Market Analysis

## Overview

Use this skill when the user wants to connect patents to commercial products — either finding patents relevant to a product or finding products that may use a specific patent.

## When to Use

- User mentions "product match", "commercial application", "licensing opportunity"
- User describes a product and wants to find relevant patents
- User has a patent and wants to find products using it

## Instructions

### 1. Match patents to products (product → patents)

If the user describes a product, use `match_patent_to_products` with:
- `description`: the product description
- `keywords`: relevant technical terms

This finds patents most relevant to the product.

### 2. Find product matches (patent → products)

If the user has a specific patent, use `find_product_matches` with:
- `patent_id`: the patent to analyze

This finds commercial products that may be implementing the patent.

## Output Format

Provide a structured response with:
- **Matched items** ranked by confidence score
- **Evidence** for each match (matched claims, keywords)
- **Summary** of commercial relevance
