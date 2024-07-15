import argparse
import logging
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("check_args")


def main() -> None:
    parser = argparse.ArgumentParser(description="Checks and processes input values.")
    parser.add_argument("inputs", nargs="+", type=str, help="Non-empty input values.")

    args = parser.parse_args()

    if any(not arg.strip() for arg in args.inputs):
        logger.error("Empty input detected.")
        sys.exit(1)

    logger.info("Processing complete.")

if __name__ == "__main__":
    main()
