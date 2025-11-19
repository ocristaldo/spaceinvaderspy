#!/usr/bin/env python3
"""Setup script for Space Invaders Python Clone."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="spaceinvaderspy",
    version="1.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "": ["*.json", "*.png", "*.wav", "*.ogg"],
    },
    install_requires=[
        "pygame>=2.0",
    ],
    python_requires=">=3.8",
    author="Space Invaders Contributors",
    author_email="your-email@example.com",
    description="A faithful Python recreation of the 1978 Space Invaders arcade game",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/spaceinvaderspy",
    project_urls={
        "Documentation": "https://github.com/yourusername/spaceinvaderspy/tree/master/docs",
        "Source": "https://github.com/yourusername/spaceinvaderspy",
        "Tracker": "https://github.com/yourusername/spaceinvaderspy/issues",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: X11 Applications",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Games/Entertainment :: Arcade",
    ],
)
