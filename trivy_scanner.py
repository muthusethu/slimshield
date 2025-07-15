import subprocess
import datetime
import os
import re


def scan_with_trivy(target, is_dockerfile=False, output_format=None, quiet=False, fail_on_secrets=False):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.basename(target).replace(":", "_").replace("/", "_")
    os.makedirs("reports", exist_ok=True)

    output_file = None
    secrets_found = False

    # Format-specific setup
    if output_format == "json":
        output_file = f"reports/{filename}_{timestamp}.json"
        cmd = [
            "trivy",
            "config" if is_dockerfile else "image",
            "--format", "json",
            "--output", output_file,
            target
        ]
    elif output_format == "html":
        output_file = f"reports/{filename}_{timestamp}.html"
        template_path = os.path.join("templates", "html.tpl")
        cmd = [
            "trivy",
            "config" if is_dockerfile else "image",
            "--format", "template",
            "--template", f"@{template_path}",
            "--output", output_file,
            target
        ]
    else:
        # Plain table format
        cmd = ["trivy", "config" if is_dockerfile else "image", target]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')

        if not quiet and result.stdout:
            print(result.stdout)

        # Detect secrets from stderr
        if result.stderr:
            for line in result.stderr.splitlines():
                if "secret" in line.lower():
                    secrets_found = True

                if not quiet:
                    if "ERROR" in line or "FATAL" in line:
                        print(f"Trivy error: {line}")
                    elif "WARN" in line:
                        print(f"Trivy warning: {line}")
                    elif "INFO" in line:
                        print(f"Trivy info: {line}")

        # Detect secrets from stdout (Dockerfile mode)
        if is_dockerfile and result.stdout:
            secret_env_pattern = re.compile(r'ENV\s+([A-Z_]+)=["\']?([^\s"\']+)["\']?', re.IGNORECASE)
            for match in secret_env_pattern.finditer(result.stdout):
                var_name = match.group(1)
                var_value = match.group(2)
                if any(secret in var_name.lower() for secret in ["secret", "key", "token", "pass"]):
                    secrets_found = True
                    if not quiet:
                        print(f"\n🔐 Potential secret detected: {var_name}=\"****\"")

        if output_file:
            print(f"\n✅ Trivy {output_format.upper() if output_format else 'scan'} report saved to: {output_file}")

        if fail_on_secrets and secrets_found:
            print("\n❌ Secrets detected. Exiting with error due to --fail-on-secrets flag.")
            exit(1)

        return output_file, secrets_found

    except Exception as e:
        print(f"[-] Failed to run Trivy: {str(e)}")
        return None, False
