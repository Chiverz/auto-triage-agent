"""Coordinator agent orchestrating the workflow."""


from . import AgentBase


class Coordinator(AgentBase):
    """High-level coordinator for sub-agents."""

    def __init__(self) -> None:
        super().__init__("Coordinator")
