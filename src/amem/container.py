"""Dependency injection container for the AMEM package.

This module provides the main dependency injection container that manages
all component instances and their dependencies following SOLID principles.
"""

from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject

from amem.core.interfaces import MemoryStore as MemoryStoreProtocol, ExpectationMaximizer as EMProtocol
from amem.core.memory import MemoryStore
from amem.core.em import ExpectationMaximizer
from amem.services.amem_service import AmemService


class Container(containers.DeclarativeContainer):
    """Main dependency injection container for AMEM components.
    
    This container manages all component instances and their dependencies,
    ensuring proper instantiation order and configuration.
    """

    # Configuration
    config = providers.Configuration()

    # Core components
    memory_store: providers.Provider[MemoryStoreProtocol] = providers.Singleton(
        MemoryStore,
        capacity=config.memory.capacity.as_(int).provided.or_(1000),
        embedding_dim=config.memory.embedding_dim.as_(int).provided.or_(128),
    )

    expectation_maximizer: providers.Provider[EMProtocol] = providers.Singleton(
        ExpectationMaximizer,
        max_iterations=config.em.max_iterations.as_(int).provided.or_(100),
        tolerance=config.em.tolerance.as_(float).provided.or_(1e-6),
    )

    # Services
    amem_service: providers.Provider[AmemService] = providers.Singleton(
        AmemService,
        memory_store=memory_store,
        expectation_maximizer=expectation_maximizer,
    )


# Global container instance
container = Container()


def get_container() -> Container:
    """Get the global container instance.
    
    Returns:
        The global container instance configured for the application.
    """
    return container


# Dependency injection decorators
def inject_memory_store(func):
    """Decorator to inject memory store dependency.
    
    Args:
        func: The function to decorate with memory store injection.
        
    Returns:
        The decorated function with memory store injected.
    """
    return inject(func, memory_store=Provide[Container.memory_store])


def inject_em(func):
    """Decorator to inject expectation maximizer dependency.
    
    Args:
        func: The function to decorate with EM injection.
        
    Returns:
        The decorated function with expectation maximizer injected.
    """
    return inject(func, expectation_maximizer=Provide[Container.expectation_maximizer])


def inject_amem_service(func):
    """Decorator to inject AMEM service dependency.
    
    Args:
        func: The function to decorate with AMEM service injection.
        
    Returns:
        The decorated function with AMEM service injected.
    """
    return inject(func, amem_service=Provide[Container.amem_service])