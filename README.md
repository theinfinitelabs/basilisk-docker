# basilisk-docker

Docker-based containerization workflow for the 
[Basilisk](https://hanspeterschaub.info/basilisk) 
astrodynamics simulation framework.

## Overview

This repository provides a containerized deployment 
environment for Basilisk GN&C simulations, including 
Docker configuration files and example simulation scripts. 
The workflow encapsulates the complete Basilisk build 
environment within a portable Docker container, eliminating 
dependency conflicts and enabling consistent simulation 
execution across heterogeneous development systems.

This repository accompanies the paper:

> Gupta, A. "Basilisk and Docker for Reproducible GN&C Simulation: A Workflow Reference." *arXiv*, 2026. 
> [DOI: XXXX](https://arxiv.org/abs/2605.XXXX)

The original workshop presentation is available on Zenodo:  
[https://doi.org/10.5281/zenodo.15008785](https://doi.org/10.5281/zenodo.15008785)

## Repository Structure
```
basilisk-docker/
├── docker/
│   └── Dockerfile
├── examples/
├── .env
├── build-basilisk.sh
├── CITATION.cff
├── docker-compose.yml
├── LICENSE
└── README.md
```

## Requirements

- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [VS Code](https://code.visualstudio.com/) (recommended)

## Quick Start

```bash
git clone https://github.com/infinitelabs/basilisk-docker
cd basilisk-docker
./build-basilisk.sh
```

Or manually:

```bash
docker compose up -d --build
```

To open a terminal inside the running container:

```bash
docker exec -it basilisk_gnc bash
```

## Notes

- Compatible with Ubuntu 22.04 and Python 3.10
- First-time build takes approximately 15-20 minutes
- Subsequent rebuilds use Docker layer caching 
  and are significantly faster
- The `de430.bsp` SPICE ephemeris file is not included 
  due to size; see Section 3 of the companion paper 
  for retrieval instructions
- Running each scenario generates a .bin file in the same
  directory, which can be opened in Vizard for 3D visualization.

## Development History

The Docker configuration in this repository originated 
from simulation environment work begun in 2021. The 
workflow was formalized and presented as a workshop at 
the 46th Rocky Mountain AAS GN&C Conference in February 
2024, and is documented in the companion paper listed above.

## License

MIT License. See [LICENSE](LICENSE) for details.

## Citation

If you use this workflow in your research, please cite:

```bibtex
@misc{gupta2026basilisk,
  author       = {Gupta, Anubhav},
  title        = {Basilisk and Docker for Reproducible 
                  {GN\&C} Simulation: A Workflow Reference},
  year         = {2026},
  note         = {arXiv preprint},
  url          = {https://arxiv.org/abs/XXXX}
}
```

## Acknowledgments

The author thanks Dr. Hanspeter Schaub and the AVS 
Laboratory at the University of Colorado Boulder for 
developing Basilisk.