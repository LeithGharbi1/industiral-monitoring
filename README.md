# 🏭 Industrial Data Platform (Real-Time Manufacturing Monitoring)

## 🧠 System Overview

This project simulates a real-world industrial data platform designed to ingest, process, and analyze manufacturing machine data in near real-time.

It demonstrates how modern data engineering systems are built in production environments using a layered architecture that separates data generation, ingestion, storage, transformation, and analytics.

The system is designed with scalability, modularity, and cloud-readiness in mind.

---

## 🎯 Business Context

In modern manufacturing environments, industrial machines continuously generate operational data such as:

- Production counts
- Defect occurrences
- Machine downtime
- Sensor readings (temperature, vibration)

This data must be collected reliably, stored efficiently, and transformed into actionable KPIs for operational decision-making and performance monitoring.

---

## ⚙️ Problem Statement

Traditional reporting systems often suffer from:

- Delayed visibility into production issues
- Lack of real-time monitoring capabilities
- Poor scalability for high-frequency machine data
- Fragmented data sources

This project addresses these challenges by simulating a real-time industrial data pipeline.

---

## 🏗️ System Architecture

The system follows a modular event-driven data pipeline architecture:

### 📡 1. Data Generation Layer
Simulates industrial machine events in real-time:
- Production metrics
- Quality defects
- Sensor readings
- Operator and shift metadata

### 🚀 2. Ingestion Layer (FastAPI)
Acts as a real-time ingestion API:
- Receives streaming events via HTTP POST
- Validates incoming data using Pydantic models
- Stores raw events into PostgreSQL

### 🗄️ 3. Storage Layer (PostgreSQL)
Central structured database:
- Stores normalized machine events
- Serves as single source of truth
- Enables analytical queries

### 🔄 4. Transformation Layer (ELT - SQL)
Transforms raw data into analytical models:
- Production per day
- Scrap rate computation
- Machine uptime analysis
- Shift-based performance metrics

### 📊 5. Analytics Layer
Exposes business-ready KPIs for reporting and dashboards.

---

## 🔁 End-to-End Data Flow

Machine data is generated in real-time by a simulation engine, sent via HTTP requests to a FastAPI ingestion service, validated and stored in PostgreSQL, then transformed using SQL-based ELT processes to produce analytical KPIs for monitoring and decision-making.

---

## 🧩 Design Principles

- **Separation of concerns**: each layer has a clear responsibility
- **Scalability-first design**: services are containerized and independent
- **Data consistency**: PostgreSQL used as single source of truth
- **Cloud-ready architecture**: easily deployable to AWS/GCP environments
- **Modularity**: each component can be replaced or scaled independently

---

## ☁️ Cloud-Ready Architecture (Target Design)

The system is designed for cloud deployment with minimal changes.

### Proposed Cloud Architecture:

- Data Generator → Docker container
- Ingestion API → AWS ECS / Kubernetes service
- Database → AWS RDS (PostgreSQL)
- Transformation Layer → dbt / Spark jobs
- Orchestration → Apache Airflow (MWAA or self-hosted)
- Dashboard → Streamlit / Superset / Power BI

### Scalability Features:

- Stateless ingestion service
- Horizontal scaling via containers
- Separation of compute and storage
- Event-driven extensibility (Kafka-compatible design)

---

## 📦 System Modules

### 🔵 ingestion/
FastAPI service responsible for receiving, validating, and storing industrial machine events.

### 🔵 data_generator/
Simulates real-time industrial machine telemetry for testing and pipeline validation.

### 🔵 database/
Contains schema definition and database connection logic.

### 🔵 analytics/
SQL-based transformation layer implementing KPIs and business metrics.

### 🟡 spark/ (planned)
Distributed processing layer for large-scale analytics using PySpark.

### 🟡 airflow/ (planned)
Workflow orchestration for scheduling and managing data pipelines.

### 🟡 dashboard/ (planned)
Visualization layer for operational KPIs and business insights.

---

## ⚙️ Tech Stack

- Python
- FastAPI
- PostgreSQL
- Pandas
- SQL (ELT transformations)
- Docker

Planned:
- Apache Spark
- Apache Airflow
- Streamlit / Power BI
- AWS / Cloud deployment

---

## 🎯 What This Project Demonstrates

This project showcases:

- End-to-end data engineering pipeline design
- Real-time ingestion architecture
- ELT-based transformation modeling
- SQL KPI development
- Containerized microservices (Docker)
- Cloud-ready system design thinking

---

## 🚀 Current Status

✔ Real-time ingestion working  
✔ Cloud deployment on Render  
✔ Supabase PostgreSQL integration  
✔ Streaming simulator active  

---

## 👨‍💻 Author

Leith Gharbi  
Data Engineering & Cloud Computing Enthusiast