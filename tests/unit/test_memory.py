"""Unit tests for the memory store implementation."""

import numpy as np
import pytest

from amem.core.memory import MemoryStore


class TestMemoryStore:
    """Test cases for the MemoryStore class."""

    def test_initialization(self) -> None:
        """Test proper initialization of memory store."""
        store = MemoryStore(capacity=100, embedding_dim=64)
        assert store.size == 0

    def test_store_and_retrieve(self) -> None:
        """Test basic store and retrieve functionality."""
        store = MemoryStore(capacity=10, embedding_dim=3)
        
        key = np.array([1.0, 0.0, 0.0])
        value = np.array([0.0, 1.0, 0.0])
        
        store.store(key, value)
        assert store.size == 1
        
        results = store.retrieve(key)
        assert len(results) == 1
        
        retrieved_key, retrieved_value, similarity = results[0]
        np.testing.assert_array_almost_equal(retrieved_key, key)
        np.testing.assert_array_almost_equal(retrieved_value, value)
        assert similarity == pytest.approx(1.0, abs=1e-6)

    def test_capacity_limit(self) -> None:
        """Test that capacity limit is enforced."""
        store = MemoryStore(capacity=2, embedding_dim=2)
        
        # Store 3 items (exceeds capacity)
        for i in range(3):
            key = np.array([float(i), 0.0])
            value = np.array([0.0, float(i)])
            store.store(key, value)
        
        # Should only have 2 items (capacity limit)
        assert store.size == 2

    def test_retrieve_multiple(self) -> None:
        """Test retrieving multiple similar entries."""
        store = MemoryStore(capacity=10, embedding_dim=2)
        
        # Store several items
        keys = [
            np.array([1.0, 0.0]),
            np.array([0.9, 0.1]), 
            np.array([0.0, 1.0])
        ]
        values = [
            np.array([1.0, 1.0]),
            np.array([2.0, 2.0]),
            np.array([3.0, 3.0])
        ]
        
        for key, value in zip(keys, values):
            store.store(key, value)
        
        # Retrieve top 2 similar to first key
        query = np.array([1.0, 0.0])
        results = store.retrieve(query, k=2)
        
        assert len(results) == 2
        # Results should be sorted by similarity (highest first)
        assert results[0][2] >= results[1][2]

    def test_update_existing(self) -> None:
        """Test updating existing memory entries."""
        store = MemoryStore(capacity=10, embedding_dim=2)
        
        key = np.array([1.0, 0.0])
        original_value = np.array([1.0, 1.0])
        updated_value = np.array([2.0, 2.0])
        
        store.store(key, original_value)
        store.update(key, updated_value)
        
        results = store.retrieve(key)
        _, retrieved_value, _ = results[0]
        np.testing.assert_array_almost_equal(retrieved_value, updated_value)

    def test_clear_memory(self) -> None:
        """Test clearing all memory entries."""
        store = MemoryStore(capacity=10, embedding_dim=2)
        
        # Store some items
        for i in range(3):
            key = np.array([float(i), 0.0])
            value = np.array([0.0, float(i)])
            store.store(key, value)
        
        assert store.size == 3
        
        store.clear()
        assert store.size == 0

    def test_dimension_validation(self) -> None:
        """Test validation of vector dimensions."""
        store = MemoryStore(capacity=10, embedding_dim=3)
        
        # Wrong key dimension
        with pytest.raises(ValueError, match="Key dimension"):
            store.store(np.array([1.0, 0.0]), np.array([1.0, 0.0, 0.0]))
        
        # Wrong value dimension  
        with pytest.raises(ValueError, match="Value dimension"):
            store.store(np.array([1.0, 0.0, 0.0]), np.array([1.0, 0.0]))
            
        # Wrong query dimension
        with pytest.raises(ValueError, match="Query dimension"):
            store.retrieve(np.array([1.0, 0.0]))

    def test_update_empty_memory(self) -> None:
        """Test updating when memory is empty raises error."""
        store = MemoryStore(capacity=10, embedding_dim=2)
        
        key = np.array([1.0, 0.0])
        value = np.array([0.0, 1.0])
        
        with pytest.raises(ValueError, match="Cannot update: no entries in memory"):
            store.update(key, value)

    def test_retrieve_empty_memory(self) -> None:
        """Test retrieving from empty memory returns empty list."""
        store = MemoryStore(capacity=10, embedding_dim=2)
        
        query = np.array([1.0, 0.0])
        results = store.retrieve(query)
        
        assert results == []