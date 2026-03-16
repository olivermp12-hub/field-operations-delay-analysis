# Field Operations Delay Analysis
## Alarm System Installation — Communication Gap Case Study

### Overview
Analysis of 114 field installation jobs to identify the root causes of 
operational delays in alarm system installations. This project was built 
from 8 years of firsthand field experience as an alarm systems technician.

> Note: All data has been fabricated to protect company and client privacy 
> while preserving realistic operational patterns.

### Tools Used
- SQL Server Management Studio (SSMS) — data storage and analysis
- Tableau Public — interactive dashboard and visualization
- Google Sheets — initial data collection and structuring

### Key Findings
- **23.7% of jobs experienced delays** across 114 installations
- **Jobs missing documentation had a 100% delay rate** vs 16.35% for 
  jobs with complete floor plans and scope
- **Missing Documentation was the #1 cause of delays** (44% of all 
  delayed jobs)
- **Tech14 had the highest delay rate at 35.29%** but further analysis 
  showed delays were primarily driven by Device Not Ready issues outside 
  their control — not technician performance
- DMP system type showed 0% delays but sample size (8 jobs) is too small 
  to draw conclusions

### Business Recommendation
Implementing a mandatory documentation checklist before job assignment 
could eliminate the majority of preventable delays. Jobs missing both 
floor plans and scope documents were guaranteed to result in a delay.

### Interactive Dashboards

**Dashboard 1 — Operational Overview**
High-level analysis of delay rates, documentation impact, 
and top delay causes across 114 jobs.

**Dashboard 2 — Technician Deep Dive**
Investigates why Tech14 has the highest delay rate, revealing 
Device Not Ready issues as the primary driver rather than 
documentation gaps or performance problems.

[View Both Dashboards on Tableau Public](https://public.tableau.com/app/profile/oliver.maria/viz/FieldOperationsDelayAnalysis-AlarmSystemInstallation/Dashboard1#1)

### SQL Queries
All analysis queries are saved in `fieldops_analysis.sql` in this 
repository.

### Dataset Structure
| Column | Description |
|--------|-------------|
| job_id | Unique job identifier |
| notification_time | Time technician was notified |
| job_start_time | Scheduled job start time |
| system_type | Alarm system type (Honeywell/DMP) |
| had_floor_plans | Whether floor plans were provided |
| had_scope | Whether scope of work was provided |
| delay_occurred | Whether a delay occurred |
| delay_reason | Description of delay cause |
| delay_response | Resolution or follow-up action |
| tech_id | Technician identifier |
| delay_category | Categorized delay type |

### Limitations
- Dataset contains 114 jobs — findings are directional, not statistically 
  conclusive
- DMP sample size too small to compare system types reliably
- Data covers a single time period with no seasonal variation
- Technician names replaced with IDs to protect privacy
