# base_image_suggester.py

BASE_IMAGE_SUGGESTIONS = {
    "python": ["python:3.10-slim", "python:3.10-alpine"],
    "node": ["node:18-slim", "node:18-alpine"],
    "ubuntu": ["ubuntu:20.04-minimal"],
    "debian": ["debian:bullseye-slim"],
    "golang": ["golang:1.18-alpine"],
}


def extract_base_image(dockerfile_path: str) -> str | None:
    """
    Extract the base image name from a Dockerfile.
    """
    try:
        with open(dockerfile_path, 'r') as file:
            for line in file:
                if line.strip().startswith("FROM"):
                    return line.strip().split()[1]
    except FileNotFoundError:
        return None
    return None


def suggest_base_images(dockerfile_path, only_suggestions=False, return_suggestions=False):
    base_image = None
    suggestions = []

    with open(dockerfile_path, "r") as f:
        for line in f:
            if line.strip().startswith("FROM"):
                base_image = line.strip().split()[1]
                break

    if base_image:
        if "python" in base_image:
            parts = base_image.split(":")
            if len(parts) == 2:
                tag = parts[1]
                suggestions = [f"{parts[0]}:{tag}-slim", f"{parts[0]}:{tag}-alpine"]
        elif "node" in base_image:
            parts = base_image.split(":")
            if len(parts) == 2:
                tag = parts[1]
                suggestions = [f"{parts[0]}:{tag}-alpine"]

    if return_suggestions:
        return base_image, suggestions

    if only_suggestions:
        return suggestions
    else:
        return base_image
