
import argparse
import sys
import os

from orgchart import flask_app
from orgchart import constants
from orgchart import graph


def parse_args(args, config):
    """Parse overrides to the config.

    Stores parsed overrides back in the config, and
    returns the parsed args argparse namespace object.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-f',
        '--dotfile',
        default=config[constants.DOTFILE],
        help="The dotfile to load/store the orgchart in.")

    parser.add_argument(
        '-o',
        '--svg',
        default=config[constants.SVG],
        help="The svg output the orgchart to.")

    parsed_args = parser.parse_args(args)

    config[constants.DOTFILE] = parsed_args.dotfile
    config[constants.SVG] = parsed_args.svg

    return parsed_args


def main():
    g = graph.load(flask_app.config[constants.DOTFILE])
    flask_app.config[constants.GRAPH] = g

    # Need a better place for this
    if flask_app.config[constants.REVISION_DIR] is None:
        raise Exception("No directory specified for revision control")

    return flask_app.run()


parse_args(sys.argv[1:], flask_app.config)
sys.exit(main())
