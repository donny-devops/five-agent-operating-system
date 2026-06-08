"""Root conftest.py — add src/ to sys.path so tests can import src.multi_agent_os.*"""

from __future__ import annotations

import sys
from pathlib import Path

# Insert the repo root so `from src.multi_agent_os import ...` works without installation.
sys.path.insert(0, str(Path(__file__).parent))
