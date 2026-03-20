[README.md](https://github.com/user-attachments/files/26124800/README.md)
# Field Operations Delay Analysis
## Alarm System Installation — Communication Gap Case Study

> Built from 8 years of firsthand experience as an alarm systems field technician, this analysis identifies the operational patterns that cause installation delays — patterns invisible to analysts who have never been on a jobsite. All data has been anonymized and restructured to protect company and client confidentiality while preserving accurate operational patterns.
Pipeline status: Google Sheets → BigQuery ingestion live and running on 104 rows of operational data.
---

## Overview

Analysis of 104 field installation jobs to identify the root causes of operational delays in alarm system installations. Using SQL for data transformation and analysis and Tableau for visualization, this project surfaces a clear, actionable finding: **documentation failures — not technician performance — are the primary driver of preventable delays.**

This project is also the foundation of a larger analytics pipeline currently in development, ingesting live operational data into BigQuery with dbt transformations and automated Tableau reporting.

---

## Tools Used

- **SQL Server Management Studio 21** — data storage, feature engineering, and analysis
- **Tableau Public** — interactive dashboards and visualization
- **Google Sheets** — initial data collection and structuring

---

## Key Findings

- **23.7% of jobs experienced delays** across 114 installations (27 of 114 jobs)
- **Jobs missing documentation had a 100% delay rate** vs 16.35% for fully documented jobs
- **Missing Documentation was the #1 delay cause**, accounting for 44% of all delayed jobs
- **Tech14 had the highest individual delay rate at 35.29%** — but a deeper analysis revealed delays were driven by Device Not Ready issues outside their control, not technician performance
- **DMP system type showed 0% delays** across 8 jobs — sample size too small for conclusions but warrants continued tracking

---

## Business Recommendation

Implementing a mandatory pre-job documentation checklist before job assignment could reduce delay frequency by an estimated **44%** based on this analysis. Jobs missing both floor plans and scope documents resulted in a delay 100% of the time — making missing documentation not just the most common delay cause, but a fully predictable and preventable one.

A secondary recommendation: procurement and scheduling workflows should be reviewed for jobs flagged as Device Not Ready, as these delays are systemic rather than performance-related.

---

## SQL Highlights

### 1. Overall delay rate
```sql
-- Finding: 23.68% of jobs experienced delays (27 out of 114)
SELECT
    delay_occurred,
    COUNT(*) AS total_jobs,
    CAST(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS DECIMAL(5,2)) AS percentage
FROM dbo.jobs
GROUP BY delay_occurred;
```

### 2. Impact of documentation on delay rate
```sql
-- Finding: Jobs missing both floor plans AND scope had a 100% delay rate
-- vs 16.35% for fully documented jobs
SELECT
    had_floor_plans,
    had_scope,
    COUNT(*) AS total_jobs,
    SUM(CASE WHEN delay_occurred = 'YES' THEN 1 ELSE 0 END) AS delayed_jobs,
    CAST(SUM(CASE WHEN delay_occurred = 'YES' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS delay_rate_pct
FROM dbo.jobs
GROUP BY had_floor_plans, had_scope
ORDER BY delay_rate_pct DESC;
```

### 3. Deep dive into Tech14 — performance or circumstances?
```sql
-- Finding: Tech14's delays are primarily Device Not Ready (3 of 6 delayed jobs)
-- which is outside the technician's control — suggesting a procurement
-- or scheduling issue rather than a performance issue
SELECT
    tech_id,
    delay_category,
    COUNT(*) AS total
FROM dbo.jobs
WHERE delay_occurred = 'YES'
    AND tech_id = 'tech14'
GROUP BY tech_id, delay_category
ORDER BY total DESC;
```

> All 7 analysis queries are available in [`fieldops_analysis.sql`](./fieldops_analysis.sql)

---

## Feature Engineering

A key step in this analysis was building a `delay_category` column from unstructured free-text delay reasons. Using a CASE statement with keyword pattern matching, delay descriptions were classified into five structured buckets:

| Category | Description |
|---|---|
| Missing Documentation | No paperwork, floor plans, scope, or approvals |
| Device Not Ready | Equipment, head end, sensors, or radios not ready |
| Site Not Ready | Walls, ceilings, floors, or access issues |
| Missing/Faulty Wires | Wires not run, buried, cut, or shorted |
| Other | Delays that did not fit defined categories |

This transformation converted raw field notes into analyzable data — the core of the insight that documentation failures are the primary controllable delay driver.

---

## Interactive Dashboards

**Dashboard 1 — Operational Overview**
High-level analysis of delay rates, documentation impact, and top delay causes across 114 jobs.

**Dashboard 2 — Technician Deep Dive**
Investigates why Tech14 has the highest delay rate, revealing Device Not Ready issues as the primary driver rather than documentation gaps or performance problems.

[View Both Dashboards on Tableau Public](https://public.tableau.com/app/profile/oliver.maria/viz/FieldOperationsDelayAnalysis-AlarmSystemInstallation/Dashboard1#1)

---

## Dataset Structure

| Column | Description |
|---|---|
| `job_id` | Unique job identifier |
| `notification_time` | Time technician was notified of next day's job |
| `job_start_time` | Scheduled job start time |
| `system_type` | Alarm system type (Honeywell / DMP) |
| `had_floor_plans` | Whether floor plans were provided |
| `had_scope` | Whether scope of work was provided |
| `delay_occurred` | Whether a delay occurred |
| `delay_reason` | Raw field description of delay cause |
| `delay_response` | Resolution or follow-up action taken |
| `tech_id` | Anonymized technician identifier |
| `delay_category` | Engineered column — structured delay classification |

---

## Limitations

- Dataset contains 114 jobs — findings are directional, not statistically conclusive
- DMP sample size (8 jobs) too small to compare system types reliably
- Data covers a single time period with no seasonal variation
- Technician names replaced with anonymized IDs to protect privacy

---

## About

This project was designed, built, and analyzed independently — not as part of a formal role, but as a self-initiated effort to apply data analysis to real operational problems observed over 8 years in the field. The goal was to answer a question no one was asking but everyone was feeling: *why do so many jobs run into the same problems, and what does the data actually say about it?*

**Connect:** [LinkedIn](https://www.linkedin.com/in/oliver-maria-071707355) | [Tableau Public](https://public.tableau.com/app/profile/oliver.maria)
