import argparse
import logging
import shutil
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("setup_overlays_dtbo")

class FileMover:
    def __init__(self, source_directory: str, destination_directory: str) -> None:
        self.source_directory = Path(source_directory)
        if not self.source_directory.exists():
            raise FileNotFoundError

        self.destination_directory = Path(destination_directory)
        self.destination_directory.mkdir(parents=True, exist_ok=True)

    def move_file(self, filename: str) -> None:
        source_path = self.source_directory / filename
        destination_path = self.destination_directory / filename
        shutil.move(str(source_path), str(destination_path))
        logger.info("Moved %s to %s", source_path, destination_path)

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Move .dtbo files from one directory to another.")

    parser.add_argument("--source", required=True, type=str,
                        help="Directory containing the .dtbo files")
    parser.add_argument("--destination", required=True, type=str,
                        help="Destination directory for files")
    parser.add_argument("--path-target-dtbos", required=False, type=str,
                        help="File containing list of dtbo")
    parser.add_argument("dtbos", nargs="*", type=str,
                        help="Relative paths of .dtbo files to process")

    args = parser.parse_args()

    target_dtbos = []

    if args.path_target_dtbos:
        p_target_dtbo = Path(args.path_target_dtbos)
        if not p_target_dtbo.exists():
            logger.error("Error: The file %s was not found.", p_target_dtbo)
            return
        with p_target_dtbo.open("r") as file:
            target_dtbos = [line.strip() for line in file if line.strip()]

    target_dtbos = [*target_dtbos, *args.dtbos]

    if len(target_dtbos) == 0:
        logger.error("No dtbos provided.")
        return

    processor = FileMover(args.source, args.destination)
    try:
        for dtb in target_dtbos:
            processor.move_file(dtb)
    except Exception:
        logger.exception("Failed to process file: %s", dtb)
        raise

if __name__ == "__main__":
    main()
