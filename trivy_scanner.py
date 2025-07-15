import subprocess

def scan_with_trivy(target, is_dockerfile=False, output_path=None, output_format="table"):
    print(f"[+] Scanning {'Dockerfile' if is_dockerfile else 'Image'}: {target}")
    
    if is_dockerfile:
        cmd = ["trivy", "config", target]
    else:
        cmd = ["trivy", "image", target]

    if output_format == "json" and output_path:
        cmd += ["--format", "json", "--output", output_path]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.stdout and output_format != "json":
            for line in result.stdout.splitlines():
                if "[INFO]" not in line:
                    print(line)

        if result.stderr:
            for line in result.stderr.splitlines():
                if "INFO" in line:
                    print(f"Trivy info: {line}")
                elif "WARN" in line:
                    print(f"Trivy warning: {line}")
                else:
                    print(f"Trivy error: {line}")



    except Exception as e:
        print(f"[-] Trivy scan failed: {e}")
