"""Protocols for core AMEM components following SOLID principles.

This module defines the structural interfaces (Protocols) that all core AMEM 
components must implement, ensuring proper separation of concerns and testability.
Uses Protocol instead of ABC for structural typing following modern Python practices.
"""

from typing import Generic, Mapping, Protocol, TypeVar

from amem.types import (
    MatrixArray,
    MemoryResults,
    MemoryState,
    ModelParameters,
    ResponsibilityMatrix,
    VectorArray,
)

T = TypeVar('T')


class MemoryStore(Protocol):
    """Protocol for associative memory storage.
    
    This protocol defines the contract for storing and retrieving
    key-value pairs in an associative memory system.
    """

    def store(self, key: VectorArray, value: VectorArray) -> None:
        """Store a key-value pair in memory.
        
        Args:
            key: The key vector to store.
            value: The value vector associated with the key.
        """
        ...

    def retrieve(self, query: VectorArray, k: int = 1) -> MemoryResults:
        """Retrieve k most similar entries for a query.
        
        Args:
            query: The query vector to search for.
            k: Number of most similar entries to return. Defaults to 1.
            
        Returns:
            List of MemoryEntry objects for the k most similar entries.
        """
        ...

    def update(self, key: VectorArray, value: VectorArray) -> None:
        """Update an existing memory entry.
        
        Args:
            key: The key vector to update.
            value: The new value vector to associate with the key.
        """
        ...

    def clear(self) -> None:
        """Clear all memory entries."""
        ...

    @property
    def size(self) -> int:
        """Get the current number of stored entries.
        
        Returns:
            The number of key-value pairs currently stored.
        """
        ...


class ExpectationMaximizer(Protocol):
    """Protocol for expectation maximization operations."""

    def fit(self, data: MatrixArray, n_components: int) -> ModelParameters:
        """Fit the EM algorithm to data."""
        ...

    def expectation_step(self, data: MatrixArray, parameters: ModelParameters) -> ResponsibilityMatrix:
        """Perform the expectation step."""
        ...

    def maximization_step(self, data: MatrixArray, responsibilities: ResponsibilityMatrix) -> ModelParameters:
        """Perform the maximization step."""
        ...

    def log_likelihood(self, data: MatrixArray, parameters: ModelParameters) -> float:
        """Calculate the log likelihood of the data given parameters."""
        ...


class AmemModel(Protocol):
    """Protocol for the main AMEM model."""

    def train(self, data: MatrixArray, n_components: int) -> None:
        """Train the AMEM model on data."""
        ...

    def predict(self, query: VectorArray) -> VectorArray:
        """Make predictions using the trained model."""
        ...

    def update_memory(self, new_data: MatrixArray) -> None:
        """Update the associative memory with new data."""
        ...

    def get_memory_state(self) -> MemoryState:
        """Get the current state of the associative memory."""
        ...