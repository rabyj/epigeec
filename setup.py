from setuptools import setup

# This tells setuptools we have platform-specific binary content
setup(
    has_ext_modules=lambda: True,
)
