#!/bin/bash
set -e

docker run --rm -v "$(pwd)":/io quay.io/pypa/manylinux2014_x86_64 bash -c '
    set -e
    cd /io
    yum install -y hdf5-devel boost-devel

    # Using python 3.11 since 3.8-3.10 already EOL or soon to be
    export PATH=/opt/python/cp311-cp311/bin:$PATH
    export PIP_ONLY_BINARY=:all:

    bash build_wheel.sh

    chown -R $(id -u):$(id -g) /io
'

echo "Build complete! Wheel is in dist/"
