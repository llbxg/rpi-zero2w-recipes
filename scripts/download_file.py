import argparse
import logging
import tarfile
from pathlib import Path

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("download_file")


def download_file(url: str, download_path: Path) -> bool:
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        with download_path.open(mode="wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        logger.info("File downloaded successfully: %s", download_path)
    except requests.RequestException:
        logger.exception("Failed to download file: %s", url)
        return False
    else:
        return True

def extract_tar_file(tar_path: Path, extract_path: Path) -> None:
    with tarfile.open(tar_path, "r:*") as tar:
        first_member = tar.getmembers()[0]
        first_dir = extract_path / first_member.name.split("/")[0]
        if first_dir.exists():
            logger.info("Skipping extraction, directory exists: %s", first_dir)
            return
        tar.extractall(path=extract_path, filter="tar")
        logger.info("File extracted successfully: %s", extract_path)
    tar_path.unlink()
    logger.info("Removed the tar file: %s", tar_path)

def main() -> None:
    parser = argparse.ArgumentParser(description="Download and extract a tar file.")
    parser.add_argument("--url", type=str, help="URL of the tar file")
    parser.add_argument("--download-to", type=str,
                        help="Directory to download the tar file")
    parser.add_argument("--extract-to", type=str,
                        help="Directory to extract the tar file")
    args = parser.parse_args()

    download_dir = Path(args.download_to)
    download_dir.mkdir(parents=True, exist_ok=True)

    extract_dir = Path(args.extract_to)
    extract_dir.mkdir(parents=True, exist_ok=True)

    download_path = download_dir / Path(args.url).name

    if download_path.exists():
        logger.info("File already exists, skipping download: %s", download_path)
    elif not download_file(args.url, download_path):
        return
    extract_tar_file(download_path, extract_dir)

if __name__ == "__main__":
    main()
