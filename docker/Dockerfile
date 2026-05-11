# ---------------------------------------------------------------------
# ./docker/Dockerfile
#
# Docker image for containerized Basilisk GN&C simulation workflows.
#
# Author:       Anubhav Gupta
# Affiliation:  University of Colorado Boulder
#               In Orbit Aerospace Inc.
# Organization: Infinite Labs
# License:      MIT
# ---------------------------------------------------------------------

FROM ubuntu:22.04

ARG BASILISK_COMMIT=87cb4116e09694ddf6587f61a7f4196d2e720c43
LABEL basilisk_commit=${BASILISK_COMMIT}

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=America/Los_Angeles

RUN apt update && \
    apt-get install -y \
    git git-lfs build-essential \
    python3-setuptools python3-dev \
    python3-tk python3-pip python3-venv \
    swig libgtk2.0-0 libzmq3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN git clone https://github.com/AVSLab/basilisk.git && \
    cd basilisk && \
    git checkout ${BASILISK_COMMIT} && \
    git lfs pull && \
    python3 -m pip install --upgrade pip && \
    python3 -m pip install --no-cache-dir \
        "conan>=2.0.5,<=2.15.1" \
        "cmake>=3.26,<4.0" \
        "setuptools>=70.1.0,<=78.1.0" \
        "wheel>=0.45.1,<=0.46.1" \
        "setuptools-scm>=8.0,<=8.2.1" \
        "numpy>=1.24.4,<2.4.0" \
        "pandas>=2.0.3,<=2.3.3" \
        "matplotlib>=3.7.5,<=3.10.7" \
        "bokeh>=3.4.0,<=3.8.0" \
        "scipy>=1.10.1,<2.0" \
        "pyyaml>=6.0,<7.0" \
        "pillow>=10.4.0,<=12.0.0" \
        "requests>=2.32.3,<=2.32.5" \
        "packaging>=24,<26" \
        "tqdm==4.67.1" \
        "pytest>=8.3.5,<=9.0.1" \
        "pytest-html==4.1.1" \
        "pytest-xdist>=3.6.1,<=3.8.0" \
        "pytest-timeout==2.4.0" \
        "pytest-rerunfailures>=13.0,<=16.1" \
        "pre-commit>=3.5.0,<=4.5.0" \
        "clang-format>=20.1.0,<=21.1.6" \
        "psutil>=7.0.0,<=7.1.3" \
        "swig>=4.4.1,<5" \
        "protobuf>=5.29.4,<=6.33.1" \
        "libclang>=15.0.6.1,<=18.1.1" \
        "colorama" \
        "ipykernel" && \
    python3 conanfile.py \
        --buildProject False \
        --vizInterface True \
        --managePipEnvironment False && \
    cd dist3 && \
    make -j"$(nproc)"

WORKDIR /app/workspace