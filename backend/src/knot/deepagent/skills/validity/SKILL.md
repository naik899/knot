---
name: validity-research
description: Patent validity research and prior art identification to assess whether patent claims are novel and non-obvious
allowed-tools: find_prior_art, validate_patent
metadata:
  author: knot
  version: "1.0"
---

# Validity Research

## Overview

Use this skill when the user wants to challenge or assess the validity of a patent by finding prior art that anticipates or renders obvious the patent's claims.

## When to Use

- User mentions "prior art", "validity", "invalidate", "novel", "obviousness"
- User wants to challenge a specific patent
- User needs prior art search for a technology area

## Instructions

### 1. Find prior art

Use `find_prior_art` with:
- `patent_id`: the specific patent to investigate (if provided)
- `keywords`: technical keywords related to the patent's claims

This searches for publications, patents, and other references predating the filing date.

### 2. Validate the patent

Use `validate_patent` with the patent ID to get a comprehensive validity assessment that considers all found prior art against each claim.

### 3. Assess the findings

Evaluate the strength of the prior art references and their impact on specific claims.

## Output Format

Provide a structured response with:
- **Prior art references** ranked by relevance
- **Claim-by-claim impact** assessment
- **Overall validity opinion** (appears_valid / questionable / likely_invalid)
- **Summary** of the strongest invalidation arguments
