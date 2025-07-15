import click
from trivy_scanner import scan_with_trivy
from base_image_suggestions import suggest_base_images
import os
import datetime

@click.command()
@click.option('--dockerfile', type=click.Path(), help='Path to Dockerfile')
@click.option('--image', help='Docker image name (e.g., nginx:latest)')
@click.option('--format', type=click.Choice(['json', 'table'], case_sensitive=False), default='table', help='Output format for scan results')
def main(dockerfile, image, format):
    # Create reports directory if needed
    report_path = None
    if format == "json":
        os.makedirs("reports", exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        name_part = os.path.basename(dockerfile or image).replace(":", "_").replace("/", "_")
        report_path = os.path.join("reports", f"{name_part}_{timestamp}.json")

    # Dockerfile scan
    if dockerfile:
        if not os.path.exists(dockerfile):
            print("[-] Dockerfile not found.")
            return
        suggest_base_images(dockerfile)
        scan_with_trivy(dockerfile, is_dockerfile=True, output_path=report_path, output_format=format)
        if report_path:
            print(f"\n✅ Trivy JSON report saved to: {report_path}")

    # Docker image scan
    elif image:
        scan_with_trivy(image, output_path=report_path, output_format=format)
        if report_path:
            print(f"\n✅ Trivy JSON report saved to: {report_path}")
    else:
        print("[-] Please provide either --dockerfile or --image")

if __name__ == "__main__":
    main()
