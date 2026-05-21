# QE Control Plane

Cloud-native API automation framework built using Python, Pytest, Docker, Kubernetes, and Jenkins.

Designed with scalable automation architecture principles including:

* reusable API client layer
* centralized configuration management
* distributed-safe execution
* Kubernetes-based orchestration
* CI/CD integration
* enterprise-grade reporting and artifact management

---

# Tech Stack

* Python 3.12
* Pytest
* Pytest-xdist
* Requests
* JSON Schema Validation
* Allure Reporting
* Docker
* Docker Compose
* Kubernetes
* Jenkins

---

# Framework Features

## API Automation Architecture

* Reusable `BaseClient` implementation
* Request/Response abstraction layer
* API-specific client implementations
* ReqRes API integration
* Centralized request execution flow

Supported capabilities:

* headers
* query params
* payload handling
* retries
* authentication
* response validation

---

## Authentication Layer

Implemented centralized authentication handling with:

* `x-api-key` support
* auth header management
* retry-safe auth handling
* token refresh handling support
* `_handle_auth_failure()` implementation
* Idempotency-Key support for safe retries

---

## Configuration Management

Environment-based configuration system using YAML files.

Supported environments:

* dev
* nqa
* future scalable environment support

Centralized configuration handling for:

* base URLs
* authentication
* status codes
* execution configs
* environment-specific properties

---

## Request / Response Models

Implemented reusable request and response models using Pydantic.

Features:

* request validation
* response parsing
* type-safe models
* optional field handling
* reusable API contract layer

---

## Validation Layer

Implemented JSON Schema validation layer for API response verification.

Features:

* schema-based validation
* centralized schema management
* automatic validation failure handling
* reusable schema utilities
* response contract verification

---

## Logging & Execution Metadata

Centralized logger implementation with:

* timestamped logs
* structured logging
* execution summaries
* runtime metadata tracking
* execution lifecycle visibility

Generated execution artifacts:

* logs
* aggregated_results.json
* execution_summary.json
* junit reports
* allure reports

---

## Execution Context & Traceability

Implemented centralized `ExecutionContext` for runtime coordination across:

* local execution
* Docker execution
* Kubernetes execution
* parallel workers

Features:

* centralized `RUN_ID` propagation
* correlation ID support
* worker-safe execution tracking
* parallel worker identification
* runtime artifact isolation
* distributed-safe execution coordination

Execution metadata includes:

* run_id
* worker_id
* execution timestamps
* environment
* execution summaries

Supports distributed-safe traceability across parallel executions.

---

# Parallel Execution

Implemented distributed-safe execution using:

* `pytest-xdist`
* worker-safe artifact handling
* centralized RUN_ID propagation

Supports:

* parallel test execution
* isolated artifact generation
* distributed-safe reporting
* scalable execution orchestration

---

# Reporting

Integrated:

* Allure Reporting
* JUnit XML Reporting

Generated artifacts:

```text id="a2f7vx"
artifacts/runs/<run_id>/
```

Contains:

* allure-report
* allure-results
* logs
* junit reports
* execution summaries
* aggregated execution results

---

# Docker Support

Framework supports containerized execution using Docker.

Features:

* custom execution image
* Allure CLI integration
* isolated execution environment
* mounted artifact persistence
* reproducible execution setup

Build:

```bash id="t9m4hz"
docker build -t qe-control-plane -f docker/Dockerfile .
```

Run:

```bash id="y5q8lc"
docker run --rm qe-control-plane
```

---

# Docker Compose Support

Declarative local orchestration using Docker Compose.

Supports:

* container orchestration
* environment management
* volume management
* reusable execution configuration
* simplified local execution

Run:

```bash id="g2w7pk"
docker compose up
```

---

# Kubernetes Support

Framework supports Kubernetes Job-based execution.

Implemented:

* Kubernetes Job manifests
* containerized execution
* artifact extraction
* pod log inspection
* orchestration automation
* distributed execution support

Execution flow:

```text id="k4m1vz"
Kubernetes Job
    ↓
Pytest Execution
    ↓
Artifact Generation
    ↓
Artifact Extraction
```

Kubernetes capabilities:

* Job-based execution
* parallel execution support
* pod log inspection
* runtime orchestration
* containerized workload management

---

# Jenkins CI/CD Integration

Integrated with Jenkins Pipeline.

Pipeline stages:

* Docker image build
* Kubernetes execution
* artifact collection
* report publishing

Supports:

* pipeline-as-code
* artifact archiving
* JUnit publishing
* scalable CI/CD execution
* automated orchestration

---

# Project Structure

```text id="m8q2vc"
framework/
tests/
configs/
docker/
k8s/
jenkins/
scripts/
artifacts/
```

---

# Execution Commands

## Local Execution

```bash id="r6t1hy"
python -m scripts.execution.run_tests
```

---

## Kubernetes Execution

```bash id="w3m9pk"
python -m scripts.execution.k8s_execution
```

---

# Future Enhancements

* Helm deployment support
* Prometheus metrics integration
* Grafana dashboards
* Slack notifications
* Dynamic environment provisioning
* Test impact analysis
* Distributed execution scaling
* Centralized artifact storage
* GitHub Actions integration
* Cloud-native observability support

---

# Author

Shiv Sharma
