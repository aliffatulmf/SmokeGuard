from libs.logger.level import *
from libs.requirements.packages import check_requirements


class Logger:
    def __init__(self):
        check_requirements(["rich"])
        from rich.console import Console

        self.console = Console(log_path=False)

    def log_color_level(self, level: str) -> str:
        if level == FATAL:
            return "[bold red][FATAL][/bold red]"
        elif level == ERROR:
            return "[bold red][ERROR][/bold red]"
        elif level == WARNING:
            return "[bold yellow][WARNING][/bold yellow]"
        elif level == INFO:
            return "[bold blue][INFO][/bold blue]"
        elif level == SUCCESS:
            return "[bold green][SUCCESS][/bold green]"
        elif level == DEBUG:
            return "[bold purple][DEBUG][/bold purple]"
        else:
            return "[bold blue][INFO][/bold blue]"

    def __call__(self, message: str, level: str, **kwargs):
        self.log(message, level, **kwargs)

    def log(self, message: str, level: str, **kwargs):
        kwstr = " ".join(f"{k}={v}" for k, v in kwargs.items())
        self.console.log(f"{self.log_color_level(level)} {message} {kwstr}")

    def fatal(self, message: str, stop: bool = True, **kwargs):
        self.log(message, FATAL, **kwargs)
        if stop:
            exit(1)

    def error(self, message: str, **kwargs):
        self.log(message, ERROR, **kwargs)

    def warning(self, message: str, **kwargs):
        self.log(message, WARNING, **kwargs)

    def info(self, message: str, **kwargs):
        self.log(message, INFO, **kwargs)

    def success(self, message: str, **kwargs):
        self.log(message, SUCCESS, **kwargs)

    def debug(self, message: str, **kwargs):
        self.log(message, DEBUG, **kwargs)

    def custom(self, message: str, header: str, **kwargs):
        self.console.log(f"[bold blue][{header}][/bold blue] {message}", **kwargs)

    def print(self, message: str, **kwargs):
        self.console.print(message, **kwargs)
