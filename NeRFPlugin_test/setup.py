from setuptools import setup, find_packages

setup(
    name="nerf_cli",
    version="0.1",
    packages=find_packages(include=["nerf_cli", "pipeline", "nerf_cli.*", "pipeline.*"]),
    entry_points={
        "console_scripts": [
            "nerf_cli = nerf_cli.__main__:main"
        ]
    },
)
