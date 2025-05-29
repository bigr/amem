"""Interfaces for core AMEM components following SOLID principles.

This module defines the abstract interfaces that all core AMEM components
must implement, ensuring proper separation of concerns and testability.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

import numpy as np


class IMemoryStore(ABC):
    """Interface for associative memory storage.
    
    This interface defines the contract for storing and retrieving
    key-value pairs in an associative memory system.
    """

    @abstractmethod
    def store(self, key: np.ndarray, value: np.ndarray) -> None:
        """Store a key-value pair in memory.
        
        Args:
            key: The key vector to store.
            value: The value vector associated with the key.
        """

    @abstractmethod
    def retrieve(self, query: np.ndarray, k: int = 1) -> List[Tuple[np.ndarray, np.ndarray, float]]:
        """Retrieve k most similar entries for a query.
        
        Args:
            query: The query vector to search for.
            k: Number of most similar entries to return. Defaults to 1.
            
        Returns:
            List of tuples containing (key, value, similarity_score) for the
            k most similar entries.
        """

    @abstractmethod
    def update(self, key: np.ndarray, value: np.ndarray) -> None:
        """Update an existing memory entry.
        
        Args:
            key: The key vector to update.
            value: The new value vector to associate with the key.
        """

    @abstractmethod
    def clear(self) -> None:
        """Clear all memory entries."""

    @property
    @abstractmethod
    def size(self) -> int:
        """Get the current number of stored entries.
        
        Returns:
            The number of key-value pairs currently stored.
        """


class IExpectationMaximizer(ABC):
    """Interface for expectation maximization operations."""

    @abstractmethod
    def fit(self, data: np.ndarray, n_components: int) -> Dict[str, Any]:
        """Fit the EM algorithm to data."""

    @abstractmethod
    def expectation_step(self, data: np.ndarray, parameters: Dict[str, Any]) -> np.ndarray:
        """Perform the expectation step."""

    @abstractmethod
    def maximization_step(self, data: np.ndarray, responsibilities: np.ndarray) -> Dict[str, Any]:
        """Perform the maximization step."""

    @abstractmethod
    def log_likelihood(self, data: np.ndarray, parameters: Dict[str, Any]) -> float:
        """Calculate the log likelihood of the data given parameters."""


class IAmemModel(ABC):
    """Interface for the main AMEM model."""

    @abstractmethod
    def train(self, data: np.ndarray, n_components: int) -> None:
        """Train the AMEM model on data."""

    @abstractmethod
    def predict(self, query: np.ndarray) -> np.ndarray:
        """Make predictions using the trained model."""

    @abstractmethod
    def update_memory(self, new_data: np.ndarray) -> None:
        """Update the associative memory with new data."""

    @abstractmethod
    def get_memory_state(self) -> Dict[str, Any]:
        """Get the current state of the associative memory."""