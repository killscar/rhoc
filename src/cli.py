import argparse


def fetch_cmd(args: argparse.Namespace) -> None:
    """Placeholder for data fetching."""
    print("fetch: not yet implemented")


def analyze_cmd(args: argparse.Namespace) -> None:
    """Placeholder for data analysis."""
    print("analyze: not yet implemented")


def index_cmd(args: argparse.Namespace) -> None:
    """Placeholder for building the episode index."""
    print("index: not yet implemented")


def write_scripts_cmd(args: argparse.Namespace) -> None:
    """Placeholder for script writing."""
    print("write-scripts: not yet implemented")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="RHOC podcast data pipeline")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("fetch", help="Collect raw data").set_defaults(func=fetch_cmd)
    sub.add_parser("analyze", help="Run sentiment/topic analysis").set_defaults(func=analyze_cmd)
    sub.add_parser("index", help="Build aggregated index").set_defaults(func=index_cmd)
    sub.add_parser("write-scripts", help="Generate podcast scripts").set_defaults(func=write_scripts_cmd)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
