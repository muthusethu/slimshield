import click
import os
from trivy_scanner import scan_with_trivy, analyze_image_size
from base_image_suggestions import suggest_base_images
from utils import print_header


@click.command()
@click.option('--dockerfile', type=click.Path(), help='Path to Dockerfile to scan')
@click.option('--image', help='Docker image name to scan')
@click.option('--format', default='table', help='Output format: table, json, html')
@click.option('--quiet', is_flag=True, help='Suppress Trivy logs')
@click.option('--fail-on-secrets', is_flag=True, help='Fail if secrets are detected')
@click.option('--fail-on-high', is_flag=True, help='Fail if high or critical CVEs are found')
@click.option('--fail-on-licenses', is_flag=True, help='Fail if risky licenses (GPL/AGPL/LGPL) are found')
def main(dockerfile, image, format, quiet, fail_on_secrets, fail_on_high, fail_on_licenses):
    if dockerfile:
        print_header(f"📄 Dockerfile Scan: {dockerfile}")
        if not os.path.exists(dockerfile):
            click.secho("[-] Dockerfile not found.", fg="red")
            return

        base_image, suggestions = suggest_base_images(dockerfile, return_suggestions=True)
        if base_image:
            click.secho(f"[+] Base image found: {base_image}", fg="green")
        if suggestions:
            click.secho("[*] Suggested minimal base images:", fg="yellow")
            for s in suggestions:
                click.echo(f"    → {s}")


        _, exit_code = scan_with_trivy(
            dockerfile,
            is_dockerfile=True,
            output_format=format,
            quiet=quiet,
            fail_on_secrets=fail_on_secrets,
            fail_on_high=fail_on_high,
            fail_on_licenses=fail_on_licenses
        )
        exit(exit_code)

    elif image:
        print_header(f"🐳 Docker Image Scan: {image}")
        _, exit_code = scan_with_trivy(
            image,
            is_dockerfile=False,
            output_format=format,
            quiet=quiet,
            fail_on_secrets=fail_on_secrets,
            fail_on_high=fail_on_high,
            fail_on_licenses=fail_on_licenses
        )
        analyze_image_size(image)
        exit(exit_code)

    else:
        click.secho("[-] Please provide either --dockerfile or --image.", fg="red")


if __name__ == '__main__':
    main()
