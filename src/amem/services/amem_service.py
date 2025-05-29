"""Main AMEM service orchestrating core components.

This module provides the high-level service that combines memory storage
and expectation maximization to implement the full AMEM algorithm.
"""

from typing import Optional

import numpy as np

from amem.core.interfaces import AmemModel, ExpectationMaximizer, MemoryStore
from amem.types import MatrixArray, MemoryState, ModelParameters, VectorArray


class AmemService:
    """Main AMEM service implementing the complete algorithm.
    
    This service orchestrates the memory store and expectation maximization
    components to provide the full AMEM functionality.
    
    Args:
        memory_store: The associative memory storage component.
        expectation_maximizer: The EM algorithm component.
    """

    def __init__(
        self,
        memory_store: MemoryStore,
        expectation_maximizer: ExpectationMaximizer,
    ) -> None:
        """Initialize the AMEM service.
        
        Args:
            memory_store: Injected memory storage implementation.
            expectation_maximizer: Injected EM algorithm implementation.
        """
        self._memory_store = memory_store
        self._expectation_maximizer = expectation_maximizer
        self._is_trained = False
        self._model_parameters: Optional[ModelParameters] = None

    def train(self, data: MatrixArray, n_components: int) -> None:
        """Train the AMEM model on data.
        
        This method combines EM fitting with memory storage to create
        an associative memory enhanced expectation maximization model.
        
        Args:
            data: Training data matrix of shape (n_samples, n_features).
            n_components: Number of mixture components for EM algorithm.
            
        Raises:
            ValueError: If data is empty or n_components is invalid.
        """
        if data.size == 0:
            raise ValueError("Cannot train on empty data")
        if n_components <= 0:
            raise ValueError("Number of components must be positive")

        # Fit EM algorithm
        self._model_parameters = self._expectation_maximizer.fit(data, n_components)
        
        # Store representative patterns in memory
        means = self._model_parameters.means
        weights = self._model_parameters.weights
        
        # Clear existing memory
        self._memory_store.clear()
        
        # Store each component mean with its weight as the value
        for i, (mean, weight) in enumerate(zip(means, weights)):
            # Use the mean as both key and value, scaled by weight
            weighted_value = mean * weight
            self._memory_store.store(mean, weighted_value)
            
        self._is_trained = True

    def predict(self, query: VectorArray) -> VectorArray:
        """Make predictions using the trained model.
        
        Combines memory retrieval with EM-based probability estimation
        to generate predictions for new queries.
        
        Args:
            query: Query vector to predict for.
            
        Returns:
            Prediction vector based on memory retrieval and EM model.
            
        Raises:
            RuntimeError: If model has not been trained yet.
            ValueError: If query has wrong dimensions.
        """
        if not self._is_trained:
            raise RuntimeError("Model must be trained before making predictions")
        if self._model_parameters is None:
            raise RuntimeError("Model parameters not available")

        # Retrieve similar patterns from memory
        similar_entries = self._memory_store.retrieve(query, k=3)
        
        if not similar_entries:
            # Fallback to closest component mean
            means = self._model_parameters.means
            distances = [np.linalg.norm(query - mean) for mean in means]
            closest_idx = np.argmin(distances)
            return means[closest_idx]
        
        # Weighted combination of retrieved memories
        prediction = np.zeros_like(query)
        total_weight = 0.0
        
        for entry in similar_entries:
            prediction += entry.similarity * entry.value
            total_weight += entry.similarity
            
        if total_weight > 0:
            prediction /= total_weight
            
        return prediction

    def update_memory(self, new_data: MatrixArray) -> None:
        """Update the associative memory with new data.
        
        Incrementally updates the memory store with new patterns
        without requiring full retraining.
        
        Args:
            new_data: New data points to add to memory.
            
        Raises:
            RuntimeError: If model has not been trained yet.
        """
        if not self._is_trained:
            raise RuntimeError("Model must be trained before updating memory")

        # For each new data point, store it in memory
        for point in new_data:
            # Use the point as both key and value
            self._memory_store.store(point, point)

    def get_memory_state(self) -> MemoryState:
        """Get the current state of the associative memory.
        
        Returns:
            MemoryState containing current memory information.
        """
        # For now, return basic memory state
        # TODO: Extract capacity and embedding_dim from memory store
        return MemoryState(
            size=self._memory_store.size,
            capacity=1000,  # Should be extracted from memory store
            embedding_dim=128,  # Should be extracted from memory store
            is_trained=self._is_trained
        )