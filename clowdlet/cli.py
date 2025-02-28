"""CLI for Clowdlet. Contains the main logic of the module."""
import argparse
import sys
from pathlib import Path

import yaml
from dotenv import dotenv_values

from clowdlet.models.clowdapptemplate import ClowdAppTemplate


def validate_args(args: argparse.Namespace) -> tuple[bool, str]:
    """Check if all required args are present."""
    if not args.file or not Path(args.file).is_file():
        return False, "Expecting existing input file as an argument."
    if not args.output or not Path(args.output).is_dir():
        return False, "Expecting existing output directory as an argument."
    if args.env_file and not Path(args.env_file).is_file():
        return False, "Expecting existing env file as an argument."
    return True, ""


def main() -> None:
    """Run the application."""
    parser = argparse.ArgumentParser(prog="clowdlet")
    parser.add_argument("-f", "--file", help="file with ClowdApp template")
    parser.add_argument("-o", "--output", help="output directory where to put generated Quadlet files")
    parser.add_argument("--env-file", help="file with custom env variables to render in the template")
    args = parser.parse_args()
    args_ok, detail = validate_args(args)

    if not args_ok:
        print(detail, file=sys.stderr)
        sys.exit(1)

    print(f"Loading ClowdAppTemplate file: {args.file}")
    with Path(args.file).open() as template_file:
        template_yaml = yaml.safe_load(template_file)

    custom_env = {}
    if args.env_file:
        print(f"Loading custom env file: {args.env_file}")
        for key, value in dotenv_values(args.env_file).items():
            custom_env[key] = value if value is not None else ""

    try:
        clowdapp_template = ClowdAppTemplate(template_yaml, custom_env)
    except (TypeError, ValueError) as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)

    print()
    print("ClowdApps structure:")
    print("====================")
    for clowdapp in clowdapp_template.clowdapps:
        print(f"{clowdapp.name} (ClowdApp)")
        for deployment in clowdapp.deployments:
            print(f"  • {deployment.name} (Deployment)")
            print(f"      - {deployment.image} (Image)")
            print(f"      - {deployment.command} (Command)")
            print(f"      - {len(deployment.env)} Environment variables")
        print()

    for clowdapp in clowdapp_template.clowdapps:
        clowdapp.write_quadlets(args.output)

    print()
    print("Done.")


if __name__ == "__main__":
    main()
