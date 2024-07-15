import argparse
import logging
import lzma
import shutil
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("setup_modules")

class FileMoverAndDecompressor:
    def __init__(self, source_directory: str, destination_directory: str) -> None:
        self.source_directory = Path(source_directory)
        if not self.source_directory.exists():
            raise FileNotFoundError

        self.destination_directory = Path(destination_directory)
        self.destination_directory.mkdir(parents=True, exist_ok=True)

    def _move_file(self, source_path: Path, destination_path: Path) -> None:
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source_path), str(destination_path))
        logger.info("Moved %s to %s", source_path, destination_path)

    def _decompress_file(self, compressed_path: Path) -> Path:
        decompressed_path = compressed_path.with_suffix("")
        with lzma.open(compressed_path, "rb") as xz_file:  # noqa: SIM117
            with decompressed_path.open(mode="wb") as decompressed_file:
                shutil.copyfileobj(xz_file, decompressed_file)
        logger.info("Decompressed %s to %s", compressed_path, decompressed_path)
        return decompressed_path

    def move_and_decompress(self, module_relative_path: str) -> None | Path:
        source_path = self.source_directory / module_relative_path
        if not source_path.exists():
            logger.error("File not found: %s", source_path)
            return None

        destination_path = self.destination_directory / module_relative_path

        self._move_file(source_path, destination_path)

        decompressed_path = self._decompress_file(destination_path)

        destination_path.unlink()

        return decompressed_path

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Move and decompress .xz files from one directory to another.")

    parser.add_argument("--source", required=True, type=str,
                        help="Directory containing the .xz files")
    parser.add_argument("--destination", required=True, type=str,
                        help="Destination directory for decompressed files")
    parser.add_argument("--path-target-modules", required=False, type=str,
                        help="File containing list of modules")
    parser.add_argument("modules", nargs="*", type=str,
                        help="Relative paths of .xz files to process")

    args = parser.parse_args()

    target_modules = []

    if args.path_target_modules:
        p_target_modules = Path(args.path_target_modules)
        if not p_target_modules.exists():
            logger.error("Error: The file %s was not found.", p_target_modules)
            return
        with p_target_modules.open("r") as file:
            target_modules = [line.strip() for line in file if line.strip()]

    target_modules = [*target_modules, *args.modules]

    if len(target_modules) == 0:
        logger.error("No modules provided.")
        return

    processor = FileMoverAndDecompressor(args.source, args.destination)
    try:
        for module in target_modules:
            decompressed_path = processor.move_and_decompress(module)
            logger.info("Decompressed to %s", decompressed_path)
    except Exception:
        logger.exception("Failed to process file: %s", module)
        raise

if __name__ == "__main__":
    main()
