import logging
import sys

from src import CallMainWindow


def run():
    def parseargs():
        import argparse

        parser = argparse.ArgumentParser(description="This script allows you to configure the device, model, source, and save and verbose options for running an inference", prog="control_panel.py run")
        parser.add_argument("--device", choices=["cpu", "cuda"], default="cuda", help="specify the device to be used for inference. options are 'cpu' or 'cuda'. by default, 'cuda' is used. if 'cuda' is unavailable, 'cpu' is used")
        parser.add_argument("--single", action="store_true", help="specify whether to use a single model for inference. if specified, a single model is used")
        parser.add_argument("--half", action="store_true", help="specify whether to use half precision for inference. if specified, half precision is used")
        parser.add_argument("--source", default="0", help="specify the source for inference. the default value is 0")
        parser.add_argument("--verbose", action="store_true", help="specify whether to display verbose output. if specified, verbose output is displayed")
        return parser

    parser = parseargs()
    args = parser.parse_args(sys.argv[2:])
    
    if args.verbose:
        logging.debug("Running inference with the following arguments:")
        for arg in vars(args):
            logging.debug(f"{arg}: {getattr(args, arg)}")
            
    CallMainWindow(**vars(args))


def cleaner():
    def parserargs():
        import argparse

        parser = argparse.ArgumentParser(description="This script allows you to clean the python cache", prog="control_panel.py clean")
        parser.add_argument("--exclude", nargs="+", default=[], help="specify the directories to be excluded from the cleaning process. the default value is []")
        parser.add_argument("--verbose", action="store_true", help="specify whether to display verbose output. if specified, verbose output is displayed")
        return parser
    
    parser = parserargs()
    args = parser.parse_args(sys.argv[2:])
    
    from meta.cache import delete_cache
    delete_cache(exclude=args.exclude, verbose=args.verbose)