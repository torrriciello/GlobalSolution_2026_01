"""IgnisRoute — ponto de entrada da aplicação."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ui.layouts.command_center import render_command_center


def main() -> None:
    render_command_center()


if __name__ == "__main__":
    main()
