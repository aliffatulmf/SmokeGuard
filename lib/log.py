from rich.console import Console

console = Console()


def log_fatal(message: str):
    console.log(f"[bold red][ERROR][/bold red] {message}")
    exit(1)


def log_error(message: str):
    console.log(f"[bold red][ERROR][/bold red] {message}")


def log_warning(message: str):
    console.log(f"[bold yellow][WARNING][/bold yellow] {message}")


def log_info(message: str):
    console.log(f"[bold blue][INFO][/bold blue] {message}")


def log_success(message: str):
    console.log(f"[bold green][SUCCESS][/bold green] {message}")


def log_debug(message: str):
    console.log(f"[bold purple][DEBUG][/bold purple] {message}")
