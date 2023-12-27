import logging

from .requirements import check_requirements, is_package_installed


class Logger:
    def __init__(self):
        if not is_package_installed("rich"):
            try:
                check_requirements(["rich"], auto_install=True)
            except Exception as e:
                raise Exception("The 'rich' package is required but could not be installed.") from e

        from rich.console import Console
        from rich.logging import RichHandler
        
        self.logger = logging.getLogger()
        self.logger.handlers.clear()
        self.logger.addHandler(RichHandler(show_path=True, markup=True))
        self.logger.setLevel(logging.ERROR)
        
        self.console = Console()

    def print(self, message, justify="left", **kwargs):
        self.console.print(message, justify=justify, **kwargs)
