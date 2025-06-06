"""Summariser agent for compiling conversation summaries."""


from . import AgentBase


class Summariser(AgentBase):
    """Agent that summarises collected information."""

    def __init__(self) -> None:
        super().__init__("Summariser")
