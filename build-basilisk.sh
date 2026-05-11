#!/bin/bash
# ---------------------------------------------------------------------
# build-basilisk.sh
#
# Convenience script to build and launch the Basilisk container.
#
# Usage: ./build-basilisk.sh
#
# Author:       Anubhav Gupta
# Organization: Infinite Labs
# License:      MIT
# ---------------------------------------------------------------------

set -e

echo "Building Basilisk Docker container..."
docker compose up -d --build

echo "Container built and running."
echo "To open a terminal inside the container:"
echo "  docker exec -it basilisk_gnc bash"