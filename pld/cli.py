import logging as logger
import sys
from pathlib import Path
import configargparse as argparse
from pld.pld import main

def cli():
    argd = arg_handler(sys.argv[1:])
    logger.basicConfig(
        format="%(asctime)s [%(levelname)s] %(message)s",
        level=logger.INFO if not argd["debug"] else logger.DEBUG,
    )
    logger.debug(argd)
    main(argd)

def arg_handler(argv, description: str|None = None):
    """Patreon link downloader cli"""

    description = (
        description
        if description is not None
        else "Patreon link downloader"
    )
    parent_parser = general_parser_factory(description=description)
    subparsers = parent_parser.add_subparsers(
        title="actions",
        help="actions to perform",
        dest="action",
    )

    parser_download = subparsers.add_parser(
        "download",
        help="download links",
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
        "-v",
        "--debug",
        "--verbose",
        env_var="DEBUG",
        action="store_true",
        help="Activate debug/ verbose logging.",
    )

    #parser.add_argument(
    #    "--version",
    #    action="version",
    #    version="%(prog)s {version}".format(version=__version__),
    #    help="Show the version and exit.",
    #)

    parser.add_argument(
        "--dry-run",
        env_var="DRY_RUN",
        action="store_true",
        help="Will not make any changes.",
    )

if __name__ == "__main__":
    cli()
