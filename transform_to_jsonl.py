import json
import re

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def transform_issues(project_key, input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        issues = json.load(f)

    with open(output_file, "w", encoding="utf-8") as out:
        for issue in issues:
            fields = issue.get("fields", {})
            comments = fields.get("comment", {}).get("comments", [])
            all_comments = " ".join(clean_text(c.get("body", "")) for c in comments)

            record = {
                "project": project_key,
                "issue_key": issue.get("key"),
                "title": clean_text(fields.get("summary")),
                "status": fields.get("status", {}).get("name"),
                "priority": fields.get("priority", {}).get("name") if fields.get("priority") else None,
                "reporter": fields.get("reporter", {}).get("displayName") if fields.get("reporter") else None,
                "assignee": fields.get("assignee", {}).get("displayName") if fields.get("assignee") else None,
                "created": fields.get("created"),
                "updated": fields.get("updated"),
                "description": clean_text(fields.get("description")),
                "comments": all_comments,
                "derived_tasks": {
                    "summarization": f"Summarize the issue titled '{fields.get('summary')}'",
                    "classification": "Classify this issue by type and severity",
                    "qna": "Generate a QnA pair from the description and comments"
                }
            }
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"✅ Transformed data saved to {output_file}")
