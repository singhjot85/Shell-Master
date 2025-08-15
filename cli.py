import argparse
from jq_core.formatter import format_jq

def main():
    parser = argparse.ArgumentParser(description="Format JQ programs like black for Python.")
    parser.add_argument("file", help="Path to the JQ file or '-' for stdin.")
    parser.add_argument("-i", "--indent", type=int, default=4, help="Indentation width (default 4).")
    args = parser.parse_args()

    if args.file == "-":
        jq_code = input()
    else:
        with open(args.file, "r", encoding="utf-8") as f:
            jq_code = f.read()

    formatted = format_jq(jq_code, indent_width=args.indent)
    print(formatted)

if __name__ == "__main__":
    main()
