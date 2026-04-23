# MLOps

# MLOps Batch Pipeline Task

## Overview

This project is a simple batch pipeline that processes OHLCV data, calculates a rolling mean on the close price, and generates a basic signal based on it.

The goal was to build something reproducible, observable, and easy to run using Docker.

---

## What it does

* Reads config from a YAML file
* Loads data from CSV
* Computes rolling mean
* Generates signal (1 or 0)
* Outputs metrics in JSON format
* Logs the full process

---

## How to run locally

```bash
python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log
```

---

## How to run using Docker

```bash
docker build -t mlops-task .
docker run --rm mlops-task
```

---

## Files in this project

* run.py → main script
* config.yaml → configuration file (seed, window, version)
* data.csv → dataset
* requirements.txt → dependencies
* Dockerfile → for container setup
* metrics.json → output file
* run.log → logs of execution

---

## Output example

```json
{
  "version": "v1",
  "rows_processed": 9996,
  "metric": "signal_rate",
  "value": 0.4991,
  "latency_ms": 37,
  "seed": 42,
  "status": "success"
}
```

---

## Notes

* First few rows are dropped because rolling mean needs enough data
* Config file is used to keep things flexible
* Logging is added to track each step

---

## Thought process (simple)

Tried to keep things simple and readable, while still handling edge cases like missing columns or empty data. Focus was more on making the pipeline work end-to-end rather than over-optimizing.
