import argparse
import logging
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("check_args")


def main() -> None:
    parser = argparse.ArgumentParser(description="Checks and processes input values.")
    parser.add_argument("inputs", nargs="+", type=str, help="Non-empty input values.")
    parser.add_argument(
        "--model_name", type=str, help="Optional model name (zero2w or cm4).")

    args = parser.parse_args()

    if any(not arg.strip() for arg in args.inputs):
        logger.error("Empty input detected.")
        sys.exit(1)

    if args.model_name is not None:
        if args.model_name not in ("zero2w", "cm4"):
            logger.error(
                "Invalid model_name: %s (must be 'zero2w' or 'cm4')", args.model_name)
            sys.exit(1)
        logger.info("Model name: %s", args.model_name)


    logger.info("Processing complete.")

if __name__ == "__main__":
    main()
