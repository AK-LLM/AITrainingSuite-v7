# Scaling Guide

## When To Scale Beyond Default Setup

Consider scaling changes when you hit:

- hundreds of experiments
- slow metadata queries
- larger artifact volumes
- more concurrent users

## First Upgrade Path

Move metadata storage from SQLite to PostgreSQL when experiment volume materially increases.

## Operational Suggestions

- archive older artifacts
- separate raw data from generated outputs
- batch larger workloads
- use more durable storage for long-lived artifacts
