"""Type aliases and data structures for the AMEM package.

This module defines common type aliases and immutable data structures
used throughout the AMEM package following functional programming principles.
"""

from dataclasses import dataclass
from typing import Any

import numpy as np

# Array type aliases with shape documentation
VectorArray = np.ndarray  # Shape: (n_features,)
MatrixArray = np.ndarray  # Shape: (n_samples, n_features)
CovarianceArray = np.ndarray  # Shape: (n_features, n_features)

# EM-specific types
ResponsibilityMatrix = np.ndarray  # Shape: (n_samples, n_components)
ComponentMeans = np.ndarray  # Shape: (n_components, n_features)
ComponentCovariances = np.ndarray  # Shape: (n_components, n_features, n_features)
ComponentWeights = np.ndarray  # Shape: (n_components,)


@dataclass(frozen=True)
class MemoryEntry:
    """Immutable memory entry with key, value, and similarity score."""

    key: VectorArray
    value: VectorArray
    similarity: float


@dataclass(frozen=True)
class ModelParameters:
    """Immutable EM model parameters."""

    means: ComponentMeans
    covariances: ComponentCovariances
    weights: ComponentWeights
    converged: bool
    n_iterations: int


@dataclass(frozen=True)
class MemoryState:
    """Immutable memory state information."""

    size: int
    capacity: int
    embedding_dim: int
    is_trained: bool


# Type aliases using dataclasses
MemoryResults = list[MemoryEntry]
ParameterDict = dict[str, Any]  # Legacy support, prefer ModelParameters