# Dataset Guide

## Purpose

The Dataset module supports ingestion, visibility, and validation of training data.

## Typical Uses

- load a dataset into the suite
- inspect catalog contents
- review metadata
- validate quality before training

## Workflow

```text
Load Dataset → Validate → Register Metadata → Use in Training
```

## Recommended Checks

- schema consistency
- missing values
- duplicates
- sensitive data / PII indicators
- class balance
- domain coverage
