import sys
from pathlib import Path

SPIKE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SPIKE))
