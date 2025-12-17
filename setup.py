"""Setup configuration for QWSEngine."""

from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="qwsengine",
    version="0.1.0",
    description="Qt Web Server Engine - Web automation and scripting tool",
    author="Your Name",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=install_requires,
    extras_require={
        "dev": [
            "pytest>=8.0",
            "black>=24.0",
            "pylint>=3.0",
            "isort>=6.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "qwsengine=qwsengine.__main__:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
    ],
)
