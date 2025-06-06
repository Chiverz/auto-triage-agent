"""Agent responsible for propagating changes across the system."""


from . import AgentBase


class ChangePropagator(AgentBase):
    """Agent that handles updating downstream resources."""

    def __init__(self) -> None:
        super().__init__("ChangePropagator")
