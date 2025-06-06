"""Vector store helper functions."""


from typing import Iterable, Tuple


class VectorStore:
    """In-memory vector store placeholder."""

    def __init__(self) -> None:
        self.vectors: list[Tuple[str, list[float]]] = []

    def add(self, key: str, vector: Iterable[float]) -> None:
        self.vectors.append((key, list(vector)))
