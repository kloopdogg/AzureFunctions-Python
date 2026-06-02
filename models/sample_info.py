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

    def __post_init__(self):
        self.id = int(self.id)
