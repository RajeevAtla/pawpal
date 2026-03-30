"""Compatibility shims for packages expecting a ``core_types`` module."""

from types import CodeType
from types import FrameType
from types import FunctionType
from types import ModuleType
from types import TracebackType

__all__ = [
    "CodeType",
    "FrameType",
    "FunctionType",
    "ModuleType",
    "TracebackType",
]
