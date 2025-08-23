"""
This module defines a data models for all samples.
"""
from dataclasses import dataclass

@dataclass
class EventInfo:
    """Data class representing event information.
    
    Attributes:
        id: Unique identifier for the event
        name: Name of the event
    """
    id: int
    name: str
