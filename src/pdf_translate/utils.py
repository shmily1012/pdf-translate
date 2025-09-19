"""Utility helpers for running shell commands and working with files."""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import List, Sequence


class CommandError(RuntimeError):
    def __init__(self, command: Sequence[str], exit_code: int, stderr: str) -> None:
        super().__init__(f"Command {' '.join(command)} failed with exit code {exit_code}: {stderr}")
        self.command = list(command)
        self.exit_code = exit_code
        self.stderr = stderr


def run_command(args: Sequence[str], cwd: Path | None = None) -> None:
    process = subprocess.run(
        args,
        cwd=str(cwd) if cwd else None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if process.returncode != 0:
        raise CommandError(args, process.returncode, process.stderr)


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
