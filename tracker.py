"""Entry point — adds src/ to the module path then delegates to cli.main."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from cli import main

if __name__ == "__main__":
    main()
