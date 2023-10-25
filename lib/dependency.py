import subprocess as sp
import sys

from rich.console import Console

console = Console()

MAMBA_PACKAGES = [
    "pytorch",
    "torchvision",
    "torchaudio",
    "cpuonly",
    "gitpython",
    "matplotlib",
    "numpy",
    "Pillow",
    "psutil",
    "PyYAML",
    "requests",
    "scipy",
    "torchvision",
    "tqdm",
    "pandas",
    "seaborn",
    "rich",
    "pyside6",
]
MAMBA_CHANNELS = ["conda-forge", "pytorch"]
PIP_PACKAGES = ["thop", "opencv-contrib-python"]


class Module:
    def __init__(self):
        pass

    def run_command(self, cmd: list):
        try:
            sp.check_call(cmd)
        except sp.CalledProcessError as e:
            console.log(f"[bold red][ERROR][/bold red] {e}")
            # sys.exit(1)
            exit(1)

    def mamba_command(self, name: str, reinstall: bool = False):
        cmd = [
            "mamba",
            "install",
            "--yes",
            "--strict-channel-priority",
            "--quiet",
            "--name",
            name,
        ]
        if reinstall:
            cmd.append("--force-reinstall")
        for channel in MAMBA_CHANNELS:
            cmd.extend(["-c", channel])
        cmd.extend(MAMBA_PACKAGES)
        return cmd

    def pip_command(self, packages: list[str], reinstall: bool = False):
        cmd = [sys.executable, "-m", "pip", "install", "--quiet"]
        if reinstall:
            cmd.append("--force-reinstall")
        cmd.extend(packages)
        return cmd

    def install_required(self, name: str, reinstall: bool = False):
        mamba = self.mamba_command(name, reinstall)
        pip = self.pip_command(PIP_PACKAGES, reinstall)

        tasks = [
            {
                "log": "[bold green][INSTALL][/bold green] [italic green]MAMBA PACKAGES[/italic green]",
                "command": mamba,
            },
            {
                "log": "[bold green][INSTALL][/bold green] [italic green]PIP PACKAGES[/italic green]",
                "command": pip,
            },
        ]
        with console.status("[bold green]Loading ...[/bold green]") as status:
            while tasks:
                task = tasks.pop(0)
                status.update(task["log"])
                self.run_command(task["command"])

    def install_manual(self):
        pass
