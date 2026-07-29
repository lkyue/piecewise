"""Command-line interface for puzzle-analyser."""

import argparse
import sys
import os

from piecewise.analyser import analyze, format_text, format_json, format_markdown
from piecewise.utils.image_utils import load_image


def cmd_analyze(args):
    if not os.path.exists(args.image):
        print(f"Error: image not found — {args.image}", file=sys.stderr)
        sys.exit(1)

    result = analyze(
        image_path=args.image,
        pieces=args.pieces,
        cut=args.cut,
        back=args.back,
        blind=args.blind,
    )

    if args.format == "json":
        print(format_json(result))
    elif args.format == "markdown":
        print(format_markdown(result))
    else:
        print(format_text(result))


def main():
    parser = argparse.ArgumentParser(
        prog="puzzle-analyser",
        description="Analyze jigsaw puzzle difficulty and estimate completion time.",
    )
    sub = parser.add_subparsers(dest="command")

    a = sub.add_parser("analyze", help="Analyze a single puzzle")
    a.add_argument("-i", "--image", required=True, help="Path to puzzle image")
    a.add_argument("-p", "--pieces", type=int, required=True, help="Number of pieces")
    a.add_argument(
        "-c",
        "--cut",
        default="ribbon",
        choices=["ribbon", "random", "irregular"],
        help="Piece cut type (default: ribbon)",
    )
    a.add_argument(
        "-b",
        "--back",
        default="none",
        choices=["none", "alphabet", "pattern"],
        help="Backside hint type (default: none)",
    )
    a.add_argument(
        "--blind",
        action="store_true",
        help="Puzzle has no reference image (blind puzzle)",
    )
    a.add_argument(
        "-f",
        "--format",
        default="text",
        choices=["text", "json", "markdown"],
        help="Output format (default: text)",
    )
    a.set_defaults(func=cmd_analyze)

    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        sys.exit(0)

    args.func(args)


if __name__ == "__main__":
    main()
