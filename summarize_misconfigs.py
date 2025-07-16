# summarize_misconfigs.py

import json
import os

def summarize_misconfigs(json_path):
    if not os.path.exists(json_path):
        print("[-] JSON scan report not found.")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    issues = []

    results = data.get("Results", [])
    for result in results:
        misconfigs = result.get("Misconfigurations", [])
        for mis in misconfigs:
            title = mis.get("Title", "")
            id_ = mis.get("ID", "")
            severity = mis.get("Severity", "")
            msg = f"{severity} - {title} (ID: {id_})"
            issues.append((severity, title, id_))

    if not issues:
        print("✅ No critical Dockerfile misconfigurations found.")
        return

    print("\n🚨 Misconfiguration Summary:")
    print("──────────────────────────────────────────────")
    for severity, title, id_ in issues:
        icon = "❌" if severity.upper() == "HIGH" else "⚠️"
        print(f"- {icon} {title} ({id_})")
