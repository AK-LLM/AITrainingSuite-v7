# Prediction Guide

## Purpose

The Predict module runs inference using existing trained artifacts.

## Workflow

1. Select a trained model
2. Provide input data
3. Execute prediction
4. Inspect output
5. optionally export results

## Outputs

Prediction artifacts and exports are typically written under:

```text
exports/
```

## Common Failures

- model artifact missing
- incompatible input schema
- no completed training artifact available
