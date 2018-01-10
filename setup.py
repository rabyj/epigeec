
import os
from setuptools import setup

setup(
    name = "epigeec",
    version = "0.9",
    author = "Jonathan Laperle",
    author_email = "jonathan.laperle@usherbrooke.ca",
    description = ("TODO"),
    scripts=["bin/epigeec"],
    install_requires=["pandas", "numpy"],
    license = "GPL",
)
