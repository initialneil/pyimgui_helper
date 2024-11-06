# Useful helpers for pyimgui
# https://github.com/pyimgui/pyimgui
# Developed by Neil Z. SHAO
# https://github.com/initialneil/pyimgui_helper
import os
from pathlib import Path

# Available at setup time due to pyproject.toml
from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup, find_packages

__version__ = "0.1.0"

setup(
    name="imgui_helper",
    version=__version__,
    author="Neil Z. Shao",
    author_email="initialneil@gmail.com",
    url="",
    description="Useful helpers for pyimgui",
    long_description="",
    packages=find_packages(),
    zip_safe=False,
    python_requires=">=3.0",
)
