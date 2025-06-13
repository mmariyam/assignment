from setuptools import setup, find_packages

setup(
    name="spacex-tracker",
    version="1.0.0",
    description="A Python application to track and analyze SpaceX launches",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "rich>=13.0.0",
        "pandas>=1.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "typing-extensions>=3.7.4",
        ]
    },
    entry_points={
        "console_scripts": [
            "spacex-tracker=spacex_tracker.cli:main",
        ],
    },
    python_requires=">=3.7",
)