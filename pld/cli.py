import logging as logger
import sys
from pathlib import Path
import configargparse as argparse
from pld.pld import main
from urllib.parse import urlparse
import re


def cli():
    argd = arg_handler(sys.argv[1:])
    logger.basicConfig(
        format="%(asctime)s [%(levelname)s] %(message)s",
        level=logger.INFO if not argd["debug"] else logger.DEBUG,
    )
    logger.debug(argd)
    main(argd)


def arg_handler(argv, description: str | None = None):
    """Patreon link downloader cli"""

    description = description if description is not None else "Patreon link downloader"
    parent_parser = general_parser_factory(description=description)
    subparsers = parent_parser.add_subparsers(
        title="actions",
        help="actions to perform",
        dest="action",
    )

    parser_download = subparsers.add_parser(
        "login",
        help="login to patreon",
    )

    parser_download = subparsers.add_parser(
        "download",
        help="download links",
    )

    parser_download.add_argument(
        "--pages",
        nargs="+",
        required=True,
        default=[],
        type=list_valid_url,
        help="pages to scrape to populate download links",
    )

    parser_download.add_argument(
        "--include-regex",
        nargs="+",
        default=[
            r"https.*patreon\.com\/file.*",
            r"https.*drive\.google\.com\/file.*",
            r"https.*dropbox.com/s.*",
        ],
        type=list_valid_regex,
        help="Regex to define what download links we want to include",
    )

    parser_download.add_argument(
        "--exclude-regex",
        nargs="+",
        default=["$^"],
        type=list_valid_regex,
        help="Regex to define what download links we want to exclude",
    )

    parser_download.add_argument(
        "--output",
        required=True,
        type=Path,
        help="output directory",
    )

    args = vars(parent_parser.parse_args())
    return args


def general_parser_factory(description):
    """Abstracted argument parser for ease of maintenance.

    Args:
        description (str): Description of the parser.

    """
    parser = argparse.ArgumentParser(description=description)
    add_general_params(parser)
    return parser


def add_general_params(parser):
    """Single purpose function to add general purpose args to all commands

    Args:
        parser (argparse.ArgumentParser): Parser to add arguments to.

    Returns:
        None

    """

    parser.add_argument(
        "-c",
        "--config",
        default="./config.yaml",
        env_var="CONFIG",
        is_config_file=True,
        help="Load a non-default config from this path.",
    )

    parser.add_argument(
        "--cookies",
        default="cookies.txt",
        type=Path,
        help="cookie file involved in login.",
    )

    parser.add_argument(
        "-v",
        "--debug",
        "--verbose",
        env_var="DEBUG",
        action="store_true",
        help="Activate debug/ verbose logging.",
    )

    # parser.add_argument(
    #    "--version",
    #    action="version",
    #    version="%(prog)s {version}".format(version=__version__),
    #    help="Show the version and exit.",
    # )

    parser.add_argument(
        "--dry-run",
        env_var="DRY_RUN",
        action="store_true",
        help="Will not make any changes.",
    )


def list_valid_url(urls):
    for url in urls:
        try:
            urlparse(url)
        except AttributeError:
            raise argparse.ArgumentTypeError(f"{url} is not a valid url")
    return urls


def list_valid_regex(regexes):
    for regex in regexes:
        try:
            re.compile(regex)
        except re.error as e:
            raise argparse.ArgumentTypeError(f"{regex} is not a valid regex: {e}")
    return regexes


if __name__ == "__main__":
    cli()
