# AMEM: Associative Memory for Expectation Maximization

A Python implementation of the AMEM algorithm as described in [arXiv:2502.12110](https://arxiv.org/pdf/2502.12110).

## Installation

```bash
# Install from source
git clone <repository-url>
cd amem
pip install -e ".[dev]"
```

## Quick Start

```python
from amem.container import container
from amem.services.amem_service import AmemService

# Configure the container
container.config.from_dict({
    "memory": {"capacity": 1000, "embedding_dim": 128},
    "em": {"max_iterations": 100, "tolerance": 1e-6}
})

# Get the AMEM service
amem_service: AmemService = container.amem_service()

# Use the service
# TODO: Add usage examples once core implementation is complete
```

## Development

See [CLAUDE.md](CLAUDE.md) for detailed development instructions.

## License

MIT