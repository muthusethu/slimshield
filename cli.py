import click
from trivy_scanner import scan_with_trivy
from base_image_suggestions import suggest_base_images
import os

@click.command()
@click.option('--dockerfile', type=click.Path(), help='Path to Dockerfile')
@click.option('--image', help='Docker image name (e.g., nginx:latest)')
def main(dockerfile, image):
    if dockerfile:
        if not os.path.exists(dockerfile):
            print("[-] Dockerfile not found.")
            return
        suggest_base_images(dockerfile)
        scan_with_trivy(dockerfile, is_dockerfile=True)
    elif image:
        scan_with_trivy(image)
    else:
        print("[-] Please provide either --dockerfile or --image")

if __name__ == "__main__":
    main()
