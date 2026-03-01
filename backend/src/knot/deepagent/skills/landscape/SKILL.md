---
name: landscape-analysis
description: Patent landscape analysis to identify clusters, white spaces, and innovation opportunities in a technology domain
allowed-tools: analyze_landscape, find_white_spaces
metadata:
  author: knot
  version: "1.0"
---

# Landscape Analysis

## Overview

Use this skill when the user wants to understand the patent landscape for a technology domain — who is filing, where the clusters are, and where the opportunities lie.

## When to Use

- User mentions "landscape", "white space", "opportunity", "gap", "trend"
- User asks about patent activity in a domain
- User wants to find innovation opportunities

## Instructions

### 1. Analyze the landscape

Use `analyze_landscape` with:
- `domain`: the technology area (e.g., "IoT sensors", "battery technology")
- `keywords`: specific technical terms to focus the analysis

This clusters existing patents and identifies key players.

### 2. Identify white spaces

Use `find_white_spaces` with the same domain and keywords to find areas with low patent coverage that represent innovation opportunities.

### 3. Synthesize findings

Combine the cluster data and white space analysis into a coherent picture of the domain's IP landscape.

## Output Format

Provide a structured response with:
- **Patent clusters** with labels, descriptions, and patent counts
- **White spaces** with opportunity scores and suggested keywords
- **Ranked opportunities** with competitive intensity assessment
- **Summary** of the landscape and strategic recommendations
