"""Command-line interface for the smartphone recommendation tools."""

from __future__ import annotations

import argparse

from .tools import compare_smartphones, recommend_smartphones, review_smartphone


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Query the bundled smartphone dataset.")
    commands = parser.add_subparsers(dest="command", required=True)

    review = commands.add_parser("review", help="Show details for a smartphone.")
    review.add_argument("model", help="Full or partial model name.")

    compare = commands.add_parser("compare", help="Compare two smartphones.")
    compare.add_argument("model_1", help="First full or partial model name.")
    compare.add_argument("model_2", help="Second full or partial model name.")

    recommend = commands.add_parser("recommend", help="Find phones matching your criteria.")
    recommend.add_argument("--max-price", type=int, required=True, help="Maximum price in INR.")
    recommend.add_argument("--min-rating", type=float, required=True, help="Minimum rating from 0 to 100.")
    recommend.add_argument("--require-5g", action="store_true", help="Return only phones that support 5G.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "review":
        result = review_smartphone(args.model)
    elif args.command == "compare":
        result = compare_smartphones(args.model_1, args.model_2)
    else:
        result = recommend_smartphones(args.max_price, args.min_rating, args.require_5g)
    print(result)


if __name__ == "__main__":
    main()
