import subprocess
import datetime
import os

def scan_with_trivy(target, is_dockerfile=False, output_format=None, log_level="info"):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.basename(target).replace(":", "_")
    os.makedirs("reports", exist_ok=True)

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
        cmd = ["trivy", "config" if is_dockerfile else "image", target]
        output_file = None

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')

        if result.stdout:
            print(result.stdout)

        if result.stderr:
            for line in result.stderr.splitlines():
                level = None
                if "FATAL" in line or "ERROR" in line:
                    level = "error"
                elif "WARN" in line:
                    level = "warning"
                elif "INFO" in line:
                    level = "info"

                if log_level == "info":
                    print(f"Trivy {level}: {line}")
                elif log_level == "warning" and level in ("warning", "error"):
                    print(f"Trivy {level}: {line}")
                elif log_level == "error" and level == "error":
                    print(f"Trivy {level}: {line}")

        if output_file:
            print(f"\n✅ Trivy {output_format.upper()} report saved to: {output_file}")
    except Exception as e:
        print(f"[-] Failed to run Trivy: {str(e)}")
