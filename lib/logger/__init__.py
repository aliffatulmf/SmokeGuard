from lib.logger.default import Logger


class VerboseLogger(Logger):
    def __init__(self, verbose: bool):
        self.verbose = verbose

    def print_verbose(self, level: str, message: str):
        if self.verbose:
            self.log(message, level)


console = Logger()
