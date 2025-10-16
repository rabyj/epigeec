#!/bin/bash
set -e

# Clean previous build artifacts
rm -rf build/ dist/ CMakeCache.txt CMakeFiles/ ./*.egg-info ./*/CMakeFiles/

# Build C code
cmake .
make -j "$(nproc --all)"

# Build wheel
pip install build
python -m build --wheel

# Repair wheel with auditwheel (only for platform-specific wheels)
WHEEL=$(ls dist/*.whl)

if [[ $WHEEL == *"none-any"* ]]; then
    echo "ERROR: Built pure Python wheel instead of platform wheel!"
    echo "This means the .so files are not being included."
    echo "Check your setup.py/pyproject.toml configuration."
    exit 1
fi

echo "Repairing wheel: $WHEEL"
auditwheel repair "$WHEEL" -w dist/
rm "$WHEEL"  # Remove unrepaired wheel

echo "Build complete! Repaired wheel is in dist/"
ls -lh dist/
