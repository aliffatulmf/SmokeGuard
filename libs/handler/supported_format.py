from rich.table import Table

from libs.logger import console
from libs.requirements.packages import check_requirements
from validation.model import SUPPORTED_FORMATS


def show_supported_formats():
    check_requirements(["rich"])
    table = Table(
        title="Supported Formats", show_header=True, header_style="bold magenta"
    )
    table.add_column("Format", justify="center", style="cyan")
    table.add_column("Description", justify="center", style="cyan")

    for format in SUPPORTED_FORMATS:
        table.add_row(format[0], format[1])

    console.print(table, justify="center")
