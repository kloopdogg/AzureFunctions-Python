"""
This module defines a sample data model.
"""
from dataclasses import dataclass

@dataclass
class SampleInfo:
    """
    Data class representing sample information.
    """
    id: int
    name: str
