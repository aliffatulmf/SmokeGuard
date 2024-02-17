"""
Meta Logger
"""

import logging

import rich.logging as rlogging


def beauty_logger(level=logging.DEBUG):
    handlers = [rlogging.RichHandler(omit_repeated_times=False, show_path=False)]

    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=handlers
    )
