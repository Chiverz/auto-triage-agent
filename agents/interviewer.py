"""Interviewer agent responsible for asking follow-up questions."""


from . import AgentBase


class Interviewer(AgentBase):
    """Agent that asks follow-up questions."""

    def __init__(self) -> None:
        super().__init__("Interviewer")
