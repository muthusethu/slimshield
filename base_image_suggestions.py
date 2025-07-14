BASE_IMAGE_SUGGESTIONS = {
    "python": ["python:3.10-slim", "python:3.10-alpine"],
    "node": ["node:18-slim", "node:18-alpine"],
    "ubuntu": ["ubuntu:20.04-minimal"],
    "debian": ["debian:bullseye-slim"],
    "golang": ["golang:1.18-alpine"],
}

def suggest_base_images(dockerfile_path: str):
    base_image = None
    with open(dockerfile_path, 'r') as file:
        for line in file:
            if line.strip().startswith("FROM"):
                base_image = line.strip().split()[1]
                break

    if not base_image:
        print("No base image found.")
        return

    print(f"[+] Base image found: {base_image}")
    base = base_image.split(":")[0]
    suggestions = BASE_IMAGE_SUGGESTIONS.get(base)

    if suggestions:
        print("[*] Suggested minimal base images:")
        for s in suggestions:
            print(f"    → {s}")
    else:
        print("[*] No suggestions available for this base image.")
