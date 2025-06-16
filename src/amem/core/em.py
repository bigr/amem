"""Expectation Maximization implementation for AMEM.

This module provides the concrete implementation of the ExpectationMaximizer
protocol for fitting mixture models using the EM algorithm.
"""

import numpy as np
from scipy.stats import multivariate_normal

from amem.types import MatrixArray, ModelParameters, ResponsibilityMatrix


class ExpectationMaximizer:
    """Concrete implementation of expectation maximization algorithm.
    
    This class implements the EM algorithm for fitting Gaussian mixture models,
    which is a core component of the AMEM algorithm.
    
    Args:
        max_iterations: Maximum number of EM iterations.
        tolerance: Convergence tolerance for log-likelihood improvement.
    """

    def __init__(self, max_iterations: int, tolerance: float) -> None:
        """Initialize the expectation maximizer.
        
        Args:
            max_iterations: Maximum number of iterations before stopping.
            tolerance: Minimum improvement in log-likelihood to continue.
        """
        self._max_iterations = max_iterations
        self._tolerance = tolerance

    def fit(self, data: MatrixArray, n_components: int) -> ModelParameters:
        """Fit the EM algorithm to data.
        
        Args:
            data: Input data matrix of shape (n_samples, n_features).
            n_components: Number of mixture components to fit.
            
        Returns:
            ModelParameters containing fitted parameters with convergence info.
                
        Raises:
            ValueError: If data is empty or n_components is invalid.
        """
        if data.size == 0:
            raise ValueError("Cannot fit EM on empty data")
        if n_components <= 0:
            raise ValueError("Number of components must be positive")
            
        n_samples, n_features = data.shape
        
        # Initialize parameters
        means = np.random.randn(n_components, n_features)
        covariances = np.array([np.eye(n_features) for _ in range(n_components)])
        weights = np.ones(n_components) / n_components
        
        prev_log_likelihood = -np.inf
        
        for iteration in range(self._max_iterations):
            # E-step
            current_params = ModelParameters(
                means=means,
                covariances=covariances,
                weights=weights,
                converged=False,
                n_iterations=iteration
            )
            responsibilities = self.expectation_step(data, current_params)
            
            # M-step
            new_params = self.maximization_step(data, responsibilities)
            means = new_params.means
            covariances = new_params.covariances
            weights = new_params.weights
            
            # Check convergence
            updated_params = ModelParameters(
                means=means,
                covariances=covariances,
                weights=weights,
                converged=False,
                n_iterations=iteration + 1
            )
            log_likelihood = self.log_likelihood(data, updated_params)
            
            if log_likelihood - prev_log_likelihood < self._tolerance:
                return ModelParameters(
                    means=means,
                    covariances=covariances,
                    weights=weights,
                    converged=True,
                    n_iterations=iteration + 1
                )
                
            prev_log_likelihood = log_likelihood
            
        return ModelParameters(
            means=means,
            covariances=covariances,
            weights=weights,
            converged=False,
            n_iterations=self._max_iterations
        )

    def expectation_step(self, data: MatrixArray, parameters: ModelParameters) -> ResponsibilityMatrix:
        """Perform the expectation step.
        
        Args:
            data: Input data matrix.
            parameters: Current parameter estimates containing means, covariances, weights.
            
        Returns:
            Responsibility matrix of shape (n_samples, n_components).
        """
        means = parameters.means
        covariances = parameters.covariances 
        weights = parameters.weights
        
        n_samples, _ = data.shape
        n_components = len(means)
        
        responsibilities = np.zeros((n_samples, n_components))
        
        for k in range(n_components):
            try:
                rv = multivariate_normal(means[k], covariances[k])
                responsibilities[:, k] = weights[k] * rv.pdf(data)
            except np.linalg.LinAlgError:
                # Handle singular covariance matrix
                responsibilities[:, k] = 0
                
        # Normalize responsibilities
        row_sums = responsibilities.sum(axis=1, keepdims=True)
        row_sums[row_sums == 0] = 1  # Avoid division by zero
        responsibilities /= row_sums
        
        return responsibilities

    def maximization_step(self, data: MatrixArray, responsibilities: ResponsibilityMatrix) -> ModelParameters:
        """Perform the maximization step.
        
        Args:
            data: Input data matrix.
            responsibilities: Responsibility matrix from E-step.
            
        Returns:
            Updated ModelParameters.
        """
        n_samples, n_features = data.shape
        n_components = responsibilities.shape[1]
        
        # Update weights
        n_k = responsibilities.sum(axis=0)
        weights = n_k / n_samples
        
        # Update means
        means = np.zeros((n_components, n_features))
        for k in range(n_components):
            if n_k[k] > 0:
                means[k] = (responsibilities[:, k:k+1] * data).sum(axis=0) / n_k[k]
                
        # Update covariances
        covariances = np.zeros((n_components, n_features, n_features))
        for k in range(n_components):
            if n_k[k] > 0:
                diff = data - means[k]
                weighted_diff = responsibilities[:, k:k+1] * diff
                covariances[k] = (weighted_diff.T @ diff) / n_k[k]
                
                # Add regularization to avoid singular matrices
                covariances[k] += 1e-6 * np.eye(n_features)
            else:
                covariances[k] = np.eye(n_features)
                
        return ModelParameters(
            means=means,
            covariances=covariances,
            weights=weights,
            converged=False,  # This is just M-step, convergence determined in fit()
            n_iterations=0    # Not applicable for single M-step
        )

    def log_likelihood(self, data: MatrixArray, parameters: ModelParameters) -> float:
        """Calculate the log likelihood of the data given parameters.
        
        Args:
            data: Input data matrix.
            parameters: Model parameters.
            
        Returns:
            Log likelihood value.
        """
        means = parameters.means
        covariances = parameters.covariances
        weights = parameters.weights
        
        n_samples, _ = data.shape
        n_components = len(means)
        
        log_likelihood = 0.0
        
        for i in range(n_samples):
            sample_likelihood = 0.0
            for k in range(n_components):
                try:
                    rv = multivariate_normal(means[k], covariances[k])
                    sample_likelihood += weights[k] * rv.pdf(data[i])
                except np.linalg.LinAlgError:
                    continue
                    
            if sample_likelihood > 0:
                log_likelihood += np.log(sample_likelihood)
                
        return log_likelihood