"""Shared pytest fixtures for all tests."""

import pytest
from dependency_injector import containers, providers

from amem.container import Container


@pytest.fixture
def container() -> Container:
    """Create a test container with test dependencies."""
    test_container = Container()
    test_container.config.from_dict({
        "debug": True,
        "test_mode": True,
    })
    return test_container


@pytest.fixture
def mock_container() -> Container:
    """Create a container with mocked dependencies for isolated testing."""
    container = Container()
    container.config.from_dict({
        "debug": True,
        "test_mode": True,
    })
    # Override providers with mocks as needed
    return container