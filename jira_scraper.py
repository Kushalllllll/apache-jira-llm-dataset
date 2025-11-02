import requests
import time
import json
import os

class JiraScraper:
    def __init__(self, project_key, output_dir="data", max_results=50):
        self.project_key = project_key
        self.base_url = "https://issues.apache.org/jira/rest/api/2"
        self.output_dir = output_dir
        self.max_results = max_results
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})
        os.makedirs(output_dir, exist_ok=True)
        self.checkpoint_file = f"{output_dir}/{project_key}_checkpoint.json"

    def _get_checkpoint(self):
        if os.path.exists(self.checkpoint_file):
            with open(self.checkpoint_file, "r") as f:
                return json.load(f).get("startAt", 0)
        return 0

    def _save_checkpoint(self, startAt):
        with open(self.checkpoint_file, "w") as f:
            json.dump({"startAt": startAt}, f)

    def fetch_issues(self):
        startAt = self._get_checkpoint()
        all_issues = []

        while True:
            url = f"{self.base_url}/search?jql=project={self.project_key}&startAt={startAt}&maxResults={self.max_results}"
            try:
                response = self.session.get(url, timeout=15)
                if response.status_code == 429:  # Rate limit
                    print("Rate limit hit. Sleeping for 60s...")
                    time.sleep(60)
                    continue
                elif response.status_code >= 500:
                    print("Server error. Retrying in 10s...")
                    time.sleep(10)
                    continue
                elif response.status_code != 200:
                    print(f"Unexpected status: {response.status_code}")
                    break

                data = response.json()
                issues = data.get("issues", [])
                if not issues:
                    print("No more issues found.")
                    break

                all_issues.extend(issues)
                print(f"Fetched {len(issues)} issues (total: {len(all_issues)})")

                startAt += self.max_results
                self._save_checkpoint(startAt)

                if len(issues) < self.max_results:
                    break  # Last page reached

                time.sleep(1)  # polite delay

            except requests.exceptions.RequestException as e:
                print(f"Network error: {e}, retrying in 10s...")
                time.sleep(10)
                continue

        out_path = f"{self.output_dir}/{self.project_key}_raw.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(all_issues, f, indent=2)
        print(f"Saved raw data to {out_path}")
        return all_issues