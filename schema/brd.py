"""Pydantic model representing a Business Requirements Document."""


from pydantic import BaseModel


class BusinessRequirement(BaseModel):
    """Simple schema for a single business requirement."""

    title: str
    description: str
    priority: int = 0
