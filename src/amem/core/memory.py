"""Memory store implementation for AMEM associative memory.

This module provides the concrete implementation of the IMemoryStore interface
using numpy arrays for efficient storage and similarity computation.
"""

import numpy as np
from scipy.spatial.distance import cosine

from amem.core.interfaces import IMemoryStore
from amem.types import MemoryResults, VectorArray


class MemoryStore(IMemoryStore):
    """Concrete implementation of associative memory storage.
    
    This class provides efficient storage and retrieval of key-value pairs
    using cosine similarity for finding the most relevant entries.
    
    Args:
        capacity: Maximum number of entries to store.
        embedding_dim: Dimension of the key and value vectors.
    """

    def __init__(self, capacity: int, embedding_dim: int) -> None:
        """Initialize the memory store.
        
        Args:
            capacity: Maximum number of entries that can be stored.
            embedding_dim: Expected dimension of key and value vectors.
        """
        self._capacity = capacity
        self._embedding_dim = embedding_dim
        self._keys: list[VectorArray] = []
        self._values: list[VectorArray] = []

    def store(self, key: VectorArray, value: VectorArray) -> None:
        """Store a key-value pair in memory.
        
        Args:
            key: The key vector to store.
            value: The value vector associated with the key.
            
        Raises:
            ValueError: If key or value dimensions don't match expected dimensions.
        """
        if key.shape[0] != self._embedding_dim:
            raise ValueError(f"Key dimension {key.shape[0]} doesn't match expected {self._embedding_dim}")
        if value.shape[0] != self._embedding_dim:
            raise ValueError(f"Value dimension {value.shape[0]} doesn't match expected {self._embedding_dim}")
            
        self._keys.append(key.copy())
        self._values.append(value.copy())
        
        # Remove oldest entry if capacity exceeded
        if len(self._keys) > self._capacity:
            self._keys.pop(0)
            self._values.pop(0)

    def retrieve(self, query: VectorArray, k: int = 1) -> MemoryResults:
        """Retrieve k most similar entries for a query.
        
        Args:
            query: The query vector to search for.
            k: Number of most similar entries to return. Defaults to 1.
            
        Returns:
            List of tuples containing (key, value, similarity_score) for the
            k most similar entries, sorted by similarity (highest first).
            
        Raises:
            ValueError: If query dimension doesn't match expected dimension.
        """
        if query.shape[0] != self._embedding_dim:
            raise ValueError(f"Query dimension {query.shape[0]} doesn't match expected {self._embedding_dim}")
            
        if not self._keys:
            return []
            
        similarities = []
        for i, key in enumerate(self._keys):
            # Calculate cosine similarity (1 - cosine distance)
            similarity = 1.0 - cosine(query, key)
            similarities.append((key, self._values[i], similarity))
        
        # Sort by similarity (highest first) and return top k
        similarities.sort(key=lambda x: x[2], reverse=True)
        return similarities[:k]

    def update(self, key: VectorArray, value: VectorArray) -> None:
        """Update an existing memory entry.
        
        Finds the most similar key and updates its associated value.
        
        Args:
            key: The key vector to update.
            value: The new value vector to associate with the key.
            
        Raises:
            ValueError: If no entries exist in memory to update.
        """
        if not self._keys:
            raise ValueError("Cannot update: no entries in memory")
            
        # Find most similar key
        similarities = [1.0 - cosine(key, stored_key) for stored_key in self._keys]
        best_idx = np.argmax(similarities)
        
        # Update the value
        self._values[best_idx] = value.copy()

    def clear(self) -> None:
        """Clear all memory entries."""
        self._keys.clear()
        self._values.clear()

    @property
    def size(self) -> int:
        """Get the current number of stored entries.
        
        Returns:
            The number of key-value pairs currently stored.
        """
        return len(self._keys)