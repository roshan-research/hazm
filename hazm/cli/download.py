from io import BytesIO
from zipfile import ZipFile

import click
import requests
from github import Github

from .base import app

RESOURCES_CHOICES = ['all', 'hazm', 'stanford']


@app.command('download-resources')
@click.argument('name',
                type=click.Choice(RESOURCES_CHOICES),
                default='hazm')
@click.argument('extract_path',
                default='resources')
def download_resources_command(name, extract_path):
    """
    This command aims to easily download latest resources (tagger
    and parser models).

    \b
    Parameters
    ----------
    name: Resource name to be downloaded. Available choices: `all`, `hazm`, `stanford`
    extract_path: The extract path for the downloaded file to be extracted. Default: `resources`
    """
    download_resources(name, extract_path)


def download_resources(name, extract_path):
    """
    Function version of `download_resources_command` to be available in
    the package.

    Parameters
    ----------
    name: str
        Resource name to be downloaded

    extract_path: str
        The extract path for the downloaded file to be extracted
    """
    if name == 'all':
        for resource_name in RESOURCES_CHOICES[1:]:
            asset = get_latest_resources_asset(resource_name)
            download_and_extract_asset(asset, extract_path)
    else:
        asset = get_latest_resources_asset(name)
        download_and_extract_asset(asset, extract_path)


def get_latest_resources_asset(name):
    """
    Searches through hazm's releases and find latest release that contains
    resources.

    Parameters
    ----------
    name: str
        The resource name

    Returns
    -------
    asset: GitReleaseAsset
        The resources asset
    """
    g = Github()
    repo = g.get_repo('sobhe/hazm')

    for release in repo.get_releases():
        for asset in release.get_assets():
            name_second_part = release.tag_name[1:] if name == 'hazm' else name
            if asset.name.startswith(f'resources-{name_second_part}'):
                return asset


def download_and_extract_asset(asset, extract_path):
    """
    Downloads a github asset file and extract it.

    Parameters
    ----------
    asset: `GitReleaseAsset`
        The github asset to be downloaded

    extract_path: `str`
        The extract path for the downloaded file to be extracted
    """
    chunk_size = 1024*1024
    with click.progressbar(length=asset.size,
                           label=f'Downloading {asset.name} ...') as progress:
        with requests.get(url=asset.browser_download_url,
                          stream=True) as r:
            with BytesIO() as io_file:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    io_file.write(chunk)
                    progress.update(chunk_size)
                with ZipFile(io_file) as zip_file:
                    zip_file.extractall(path=extract_path)
    click.echo('Download completed.')
