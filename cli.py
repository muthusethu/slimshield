import click
from trivy_scanner import scan_with_trivy
from base_image_suggestions import suggest_base_images
import os

@click.command()
@click.option('--dockerfile', type=click.Path(), help='Path to Dockerfile')
@click.option('--image', help='Docker image name (e.g., nginx:latest)')
@click.option('--format', type=click.Choice(['json', 'html', 'table']), help='Output format: json, html, or table')
@click.option('--log-level', type=click.Choice(['info', 'warning', 'error']), default='info', help='Log level to control Trivy output')
def main(dockerfile, image, format, log_level):
    if dockerfile:
        if not os.path.exists(dockerfile):
            print("[-] Dockerfile not found.")
            return
        suggest_base_images(dockerfile)
        scan_with_trivy(dockerfile, is_dockerfile=True, output_format=format, log_level=log_level)

    elif image:
        scan_with_trivy(image, output_format=format, log_level=log_level)

    else:
        print("[-] Please provide either --dockerfile or --image")

if __name__ == "__main__":
    main()
