"""Command-line interface for the jq tools project."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from .compiler import JQCompiler
from .tooling import JQDebugger, JQFormatter


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="jqtools", description="Compiler-driven jq tooling")
    subparsers = parser.add_subparsers(dest="command", required=True)

    tokenize = subparsers.add_parser("tokenize", help="Print the lexical token stream")
    tokenize.add_argument("source", help="jq source snippet to tokenize")

    parse = subparsers.add_parser("parse", help="Print the parsed AST as JSON")
    parse.add_argument("source", help="jq source snippet to parse")

    format_cmd = subparsers.add_parser("format", help="Format jq source")
    format_cmd.add_argument("source", help="jq source snippet to format")

    debug = subparsers.add_parser("debug", help="Emit token and AST traces")
    debug.add_argument("source", help="jq source snippet to inspect")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    compiler = JQCompiler()

    if args.command == "tokenize":
        print(json.dumps([asdict(token) for token in compiler.tokenize(args.source)], indent=2, default=str))
        return 0
    if args.command == "parse":
        print(json.dumps(asdict(compiler.parse(args.source)), indent=2, default=str))
        return 0
    if args.command == "format":
        print(JQFormatter(compiler).format(args.source))
        return 0
    if args.command == "debug":
        print(json.dumps(asdict(JQDebugger(compiler).trace(args.source)), indent=2))
        return 0

    parser.error(f"Unsupported command: {args.command}")
    return 2
