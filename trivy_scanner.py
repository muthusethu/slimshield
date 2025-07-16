import os
import subprocess
import datetime
import json
import re


def run_trivy_command(command, output_format="table", quiet=False):
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        if not quiet:
            if output_format != "json":  # Avoid printing raw JSON to stdout
                print(result.stdout)
            if result.stderr:
                print(result.stderr)
        return result.stdout, result.returncode
    except Exception as e:
        print(f"[!] Error running Trivy command: {e}")
        return None, 1


def save_report(scan_output, target, output_format="json"):
    if not os.path.exists("reports"):
        os.makedirs("reports")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    sanitized_target = target.replace("/", "_").replace(":", "_")
    filename = f"{sanitized_target}_{timestamp}.{output_format}"
    path = os.path.join("reports", filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(scan_output)
    print(f"\n✅ Trivy {output_format.upper()} report saved to: {path}")
    return path


def extract_secrets_from_output(output):
    secret_matches = []
    for match in re.finditer(r'(?i)(?P<key>API[_-]?KEY|SECRET|TOKEN)[^\n]{0,100}', output):
        context = match.group(0)
        redacted = re.sub(r'=[^\s"]+', '=******', context)
        secret_matches.append({
            "matched_string": context.strip(),
            "redacted": redacted.strip(),
            "line": output[:match.start()].count("\n") + 1
        })
    return secret_matches


def scan_with_trivy(target, is_dockerfile=True, output_format="table", quiet=False,
                    fail_on_secrets=False, fail_on_high=False, fail_on_licenses=False):
    report_format = output_format.lower()
    command = ["trivy"]

    if is_dockerfile:
        command += ["config"]
    else:
        command += ["image", "--scanners", "vuln,secret,license,misconfig"]

    if report_format == "html":
        template_path = os.path.join("templates", "html.tpl")
        if not os.path.exists(template_path):
            print(f"❌ HTML template not found at: {template_path}")
            return None, 1
        command += ["--format", "template", "--template", template_path]
    else:
        command += ["--format", report_format]

    command.append(target)

    scan_output, return_code = run_trivy_command(command, output_format=report_format, quiet=quiet)
    if scan_output is None:
        return None, 1

    report_path = None
    if report_format in ("json", "html"):
        report_path = save_report(scan_output, os.path.basename(target), report_format)

    # === JSON Logic ===
    if report_format == "json":
        try:
            parsed = json.loads(scan_output)
        except json.JSONDecodeError:
            print("❌ Failed to parse Trivy JSON output.")
            return report_path, 1

        results = parsed.get("Results", [])
        secrets = []
        risky_licenses = []
        high_vulns = []

        for result in results:
            if "Secrets" in result:
                for secret in result["Secrets"]:
                    secrets.append({
                        "file": result.get("Target", target),
                        "line": secret.get("StartLine", "-"),
                        "redacted": re.sub(r'(?<=.{2}).(?=.*.{2})', '*', secret.get("SecretID", "")),
                        "description": secret.get("Title")
                    })
            if "Vulnerabilities" in result:
                for vuln in result["Vulnerabilities"]:
                    if vuln.get("Severity") in ["HIGH", "CRITICAL"]:
                        high_vulns.append(vuln)
            if "Licenses" in result:
                for lic in result["Licenses"]:
                    name = lic.get("License", "")
                    if any(risk in name for risk in ["GPL", "LGPL", "AGPL"]):
                        risky_licenses.append(name)

        if secrets:
            print("\n🔐 Secrets Insight")
            for s in secrets:
                print(f"- {s['file']} [Line {s['line']}]: {s['description']} → {s['redacted']}")
            if fail_on_secrets:
                print("❌ Secrets detected. Exiting with error due to --fail-on-secrets flag.")
                return report_path, 1

        if fail_on_high and high_vulns:
            for v in high_vulns:
                print(f"❌ {v['Severity']} CVE: {v['VulnerabilityID']} in {v['PkgName']}")
            return report_path, 1

        if fail_on_licenses and risky_licenses:
            print(f"❌ Risky licenses detected: {', '.join(set(risky_licenses))}")
            return report_path, 1

    # === Table fallback logic ===
    elif report_format == "table":
        secrets = extract_secrets_from_output(scan_output)
        if secrets:
            print("\n🔐 Secrets Insight (regex fallback)")
            for secret in secrets:
                print(f"- Line {secret['line']}: {secret['redacted']}")
            if fail_on_secrets:
                print("❌ Secrets detected. Exiting with error due to --fail-on-secrets flag.")
                return report_path, 1

        if fail_on_high and ("HIGH" in scan_output or "CRITICAL" in scan_output):
            print("❌ High or critical vulnerabilities detected. Exiting due to --fail-on-high flag.")
            return report_path, 1

        if fail_on_licenses and any(l in scan_output for l in ["GPL", "LGPL", "AGPL"]):
            print("❌ Risky licenses detected. Exiting due to --fail-on-licenses flag.")
            return report_path, 1

    return report_path, 0


def analyze_image_size(image_name):
    try:
        result = subprocess.run(
            ["docker", "history", "--no-trunc", "--format", "{{.Size}}: {{.CreatedBy}}", image_name],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        lines = result.stdout.strip().splitlines()
        total_size = 0
        layer_info = []

        for line in lines:
            if ':' not in line:
                continue
            size_str, created_by = line.split(":", 1)
            size_str = size_str.strip()
            created_by = created_by.strip()

            if size_str.endswith("B"):
                size_bytes = size_str_to_bytes(size_str)
                total_size += size_bytes
                layer_info.append({
                    "size": size_str,
                    "created_by": created_by
                })

        print("\n📦 Image Size Breakdown:")
        for layer in layer_info:
            print(f"- {layer['size']} → {layer['created_by']}")

        print(f"\n🧮 Total Image Size: {round(total_size / (1024 * 1024), 2)} MB")
    except Exception as e:
        print(f"[!] Failed to analyze image size: {e}")


def size_str_to_bytes(size_str):
    size_str = size_str.strip().upper()
    if size_str.endswith("GB"):
        return float(size_str[:-2]) * 1024 * 1024 * 1024
    elif size_str.endswith("MB"):
        return float(size_str[:-2]) * 1024 * 1024
    elif size_str.endswith("KB"):
        return float(size_str[:-2]) * 1024
    elif size_str.endswith("B"):
        return float(size_str[:-1])
    return 0
