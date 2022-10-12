import requests
import click
import yaml
import logging
import py7zr
import os


def extract_zip(archive_path, target_path):
    """
    The extract_zip function extracts a zip file to the target path.

    :param archive_path: Specify the path to the archive that is to be extracted
    :param target_path: Specify the path where the extracted files will be stored
    """
    with py7zr.SevenZipFile(archive_path, mode='r') as zip_file:
        zip_file.extractall(path=target_path)
    logger.info(f'Archive {archive_path} has been extracted to {target_path}...')


@click.command()
@click.option(
    "-cf",
    "--config_path",
    type=click.Path(exists=True),
    help="Path to config file",
    required=True,
)
def download_dataset(config_path):
    """
    The download_dataset function downloads the Stack Overflow dataset from an URL and saves it to disk.

    :param config_path: Specify the path to the configuration file
    """
    with open(config_path) as conf_file:
        config = yaml.safe_load(conf_file)

    response = requests.get(config['data']['so_dataset_url'])
    logger.info('Dataset has been downloaded...')

    filename = 'stack_overflow_posts.7z'
    dataset_7z_path = f"{config['data']['so_dataset_path']}/{filename}"
    with open(dataset_7z_path, "wb") as f:
        f.write(response.content)
    logger.info(f'Archive {filename} has been created...')

    extract_zip(
        archive_path=dataset_7z_path,
        target_path=config['data']['so_dataset_path'],
    )
    os.remove(dataset_7z_path)


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    logger = logging.getLogger(__name__)
    download_dataset()
