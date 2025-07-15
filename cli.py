import click
import os
from trivy_scanner import scan_with_trivy
from base_image_suggestions import suggest_base_images

@click.command()
@click.option('--dockerfile', type=click.Path(), help='Path to Dockerfile')
@click.option('--image', help='Docker image name (e.g., nginx:latest)')
@click.option('--format', type=click.Choice(['json', 'html', 'table']), help='Output format: json, html, or table')
@click.option('--quiet', is_flag=True, help='Suppress Trivy logs')
@click.option('--fail-on-secrets', is_flag=True, help='Exit with error if secrets are detected')
def main(dockerfile, image, format, quiet, fail_on_secrets):
    if dockerfile:
        if not os.path.exists(dockerfile):
            print("[-] Dockerfile not found.")
            return

        click.echo("\n╭" + "─" * (50) + "╮")
        click.echo(f"│ 📄 Dockerfile Scan: {dockerfile.ljust(33)} │")
        click.echo("╰" + "─" * (50) + "╯")

        suggest_base_images(dockerfile)
        report_path, secrets_found = scan_with_trivy(
            dockerfile,
            is_dockerfile=True,
            output_format=format,
            quiet=quiet
        )

    elif image:
        click.echo("\n╭" + "─" * (40) + "╮")
        click.echo(f"│ 🐳 Docker Image Scan: {image.ljust(25)} │")
        click.echo("╰" + "─" * (40) + "╯")

        report_path, secrets_found = scan_with_trivy(
            image,
            is_dockerfile=False,
            output_format=format,
            quiet=quiet
        )
    else:
        print("[-] Please provide either --dockerfile or --image")
        return

    if fail_on_secrets and secrets_found:
        print("❌ Secrets detected. Exiting with error due to --fail-on-secrets flag.")
        exit(1)

if __name__ == "__main__":
    main()
