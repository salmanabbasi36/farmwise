"""FarmWise: a small, offline-capable maize advisory module for smallholder farmers.

Pure Python standard library. See README.md for usage.
"""

from .advisor import Advisor, Answer

__all__ = ["Advisor", "Answer"]
__version__ = "0.1.0"
