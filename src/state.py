"""
Global application state.
Holds singleton instances that are initialized during app startup.
"""

from sqlalchemy import Engine

# Global singleton instances
engine: Engine | None = None
