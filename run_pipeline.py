from jira_scraper import JiraScraper
from transform_to_jsonl import transform_issues

projects = ["SPARK", "HADOOP", "KAFKA"]

for project in projects:
    print(f"=== Processing project: {project} ===")
    scraper = JiraScraper(project)
    raw_data = scraper.fetch_issues()
    transform_issues(project, f"data/{project}_raw.json", f"data/{project}_clean.jsonl")
