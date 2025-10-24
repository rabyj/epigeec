# syntax=docker/dockerfile:1
FROM custom-manylinux_2_28_x86_64

LABEL description="Building epigeec binaries into custom-manylinux_2_28_x86_64 image."

# Create work directory and copy source tree from build context
WORKDIR /project
COPY . .

# Optional sanity check
RUN echo "--- Source tree ---" && tree -L 2

# Clean, configure, and build
RUN git clean -fdx && \
    cmake . && \
    make -j "$(nproc --all)"

# Default entrypoint
CMD ["/bin/bash"]
