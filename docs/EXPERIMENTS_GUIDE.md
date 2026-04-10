# Experiments Guide

## Purpose

Experiments are the system-of-record for model runs inside AITrainingSuite v7.

## Experiment Record Includes

- dataset used
- model/configuration
- metrics
- timestamps
- artifact references

## Supported Operations

- inspect run history
- compare experiments
- replay runs
- trace lineage into reports

## Storage

Experiment metadata is typically stored in SQLite:

```text
data/experiments.db
```
