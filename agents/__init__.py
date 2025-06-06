"""Business requirement agents used throughout the application."""


class AgentBase:
    """Base class for agent stubs used during development."""

    def __init__(self, name: str) -> None:
        self.name = name

    async def run(self, prompt: str) -> str:
        return f"{self.name} received: {prompt}"
