🧾 Apache Jira Scraper and Transformer
Overview

This project scrapes public issue data from Apache’s Jira instance for selected projects (SPARK, HADOOP, KAFKA) and converts it into structured JSONL suitable for LLM fine-tuning.

Features

Fault-tolerant scraping (retries, rate-limiting, checkpointing)

Structured JSONL output for LLM tasks

Extensible to multiple projects

Setup
pip install requests
python run_pipeline.py

Architecture

jira_scraper.py: Fetches and saves raw issue data.

transform_to_jsonl.py: Transforms raw JSON into clean, text-based JSONL.

run_pipeline.py: Orchestrates the full workflow.

Edge Cases Handled

1. Network & API Failures

Handles HTTP 429 (rate limits) by pausing and retrying automatically.

Retries 5xx server errors (temporary backend issues) after short delays.

Catches network errors and timeouts with retries to prevent crashes.

Logs and skips unexpected response codes safely.

📄 2. Pagination & Completeness

Supports pagination to fetch thousands of issues across multiple API pages.

Uses checkpointing to resume from the last successful batch if interrupted.

Prevents duplication by fetching based on the startAt index.

Stops automatically when no more results are returned.

🧠 3. Data Quality & Schema Handling

Uses .get() for safe access to fields, preventing KeyErrors on missing data.

Cleans and normalizes text to remove HTML tags, whitespace, and noise.

Handles empty or malformed JSON by skipping or retrying those records.

Writes using UTF-8 encoding to avoid character encoding issues.

Aggregates long descriptions and comments safely without breaking format.

💾 4. Reliability & Fault Tolerance

Checkpoint files ensure progress is saved and can resume after crashes.

Writes data incrementally to prevent memory overload.

Skips problematic records instead of halting the pipeline.

Avoids duplicate records by processing one unique page index at a time.

🧩 5. Data Transformation & Output

Ensures consistent JSONL schema with all key fields present (even if empty).

Handles missing descriptions, assignees, or comments gracefully.

Escapes special characters so every line remains valid JSON.

Adds derived LLM tasks (summarization, classification, QnA) for downstream use.

🚀 6. Performance & Ethical Considerations

Includes delays and rate-limit handling to respect Jira’s public API limits.

Allows configurable batch size and issue limits for large projects like Spark.

Works only with publicly available Jira data (no private scraping).

Can be extended for parallel execution or date-based batching for efficiency.

Future Improvements

Add async parallel scraping for more projects.

Store data in cloud storage (S3, GCS).

Add schema validation and deduplication.