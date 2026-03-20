# ============================================================
# Field Operations Pipeline
# Google Sheets -> BigQuery Ingestion Script
# Author: Oliver Maria
# Description: Pulls live operational data from Google Sheets,
#              anonymizes PII, and loads into BigQuery.
# ============================================================

import gspread
from google.oauth2.service_account import Credentials
from google.cloud import bigquery
import hashlib
import os

# ============================================================
# CONFIGURATION
# ============================================================

CREDENTIALS_FILE = "credentials.json"   # Must be in the same folder as this script
SHEET_ID         = "12d46wAoo_SdOk1nAKDRZoj6dcMETZy_kbJYAxZwpPVg"
SHEET_TAB        = "Data"
BQ_PROJECT       = "field-ops-pipeline"
BQ_DATASET       = "field_ops"
BQ_TABLE         = "jobs_raw"

# ============================================================
# STEP 1 — CONNECT TO GOOGLE SHEETS
# ============================================================

print("Connecting to Google Sheets...")

scopes = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly"
]

creds  = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=scopes)
client = gspread.authorize(creds)

sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_TAB)
rows  = sheet.get_all_records()

print(f"  Pulled {len(rows)} rows from Google Sheets.")

# ============================================================
# STEP 2 — ANONYMIZE PII
# Replaces any real tech names with a consistent hashed ID
# so the same name always maps to the same anonymous ID.
# ============================================================

print("Anonymizing sensitive fields...")

def anonymize(value: str) -> str:
    """Hash a string to a consistent anonymous ID."""
    return "tech_" + hashlib.md5(str(value).strip().lower().encode()).hexdigest()[:6]

clean_rows = []
for row in rows:
    clean_rows.append({
        "job_id":            str(row.get("job_id", "")).strip(),
        "notification_time": str(row.get("notification_time", "")).strip(),
        "job_start_time":    str(row.get("job_start_time", "")).strip(),
        "system_type":       str(row.get("system_type", "")).strip(),
        "had_floor_plans":   str(row.get("had_floor_plans", "")).strip().upper(),
        "had_scope":         str(row.get(" had_scope",  # matches your column header spacing
                                         row.get("had_scope", ""))).strip().upper(),
        "delay_occurred":    str(row.get("delay_occurred", "")).strip().upper(),
        "delay_reason":      str(row.get("delay_reason", "")).strip() or None,
        "delay_response":    str(row.get("delay_response", "")).strip() or None,
        "tech_id":           anonymize(row.get("tech_id", "")),
    })

print(f"  Anonymized {len(clean_rows)} rows.")

# ============================================================
# STEP 3 — CONNECT TO BIGQUERY
# ============================================================

print("Connecting to BigQuery...")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_FILE
bq = bigquery.Client(project=BQ_PROJECT)

# ============================================================
# STEP 4 — DEFINE TABLE SCHEMA
# ============================================================

schema = [
    bigquery.SchemaField("job_id",            "STRING"),
    bigquery.SchemaField("notification_time", "STRING"),
    bigquery.SchemaField("job_start_time",    "STRING"),
    bigquery.SchemaField("system_type",       "STRING"),
    bigquery.SchemaField("had_floor_plans",   "STRING"),
    bigquery.SchemaField("had_scope",         "STRING"),
    bigquery.SchemaField("delay_occurred",    "STRING"),
    bigquery.SchemaField("delay_reason",      "STRING"),
    bigquery.SchemaField("delay_response",    "STRING"),
    bigquery.SchemaField("tech_id",           "STRING"),
]

# ============================================================
# STEP 5 — LOAD INTO BIGQUERY
# Replaces the table on every run so data stays fresh.
# ============================================================

print("Loading data into BigQuery...")

table_ref = f"{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE}"

job_config = bigquery.LoadJobConfig(
    schema          = schema,
    write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE,  # Replace on every run
)

load_job = bq.load_table_from_json(clean_rows, table_ref, job_config=job_config)
load_job.result()  # Wait for job to complete

table = bq.get_table(table_ref)
print(f"  Successfully loaded {table.num_rows} rows into {table_ref}")
print("Pipeline complete.")
