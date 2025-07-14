import subprocess

def scan_with_trivy(target: str, is_dockerfile=False):
    if is_dockerfile:
        print(f"[+] Scanning Dockerfile: {target}")
        cmd = ["trivy", "config", target]
    else:
        print(f"[+] Scanning Docker image: {target}")
        cmd = ["trivy", "image", "--format", "table", target]

    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode('utf-8', errors='replace'))

        stderr_output = result.stderr.decode('utf-8', errors='replace')
        # 🚫 Filter out all INFO logs
        errors = [line for line in stderr_output.splitlines() if "INFO" not in line]
        if errors:
            print("Trivy error:")
            print("\n".join(errors))
    except Exception as e:
        print(f"Error running Trivy: {e}")
