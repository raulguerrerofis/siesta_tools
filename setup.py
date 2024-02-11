from setuptools import setup, find_packages

setup(
    author      = "Dr. Raúl Guerrero",
    description = "Set of packages oriented to improve Density Functional Theory Analysis and manipulation of geometries.",
    long_description_content_type='text/markdown',
    name        = "siesta_tools",
    version     = '0.1.4',
    packages    = find_packages(include=["utilities","utilities.*","electronic_utils","electronic_utils*","ASE2pandas","filemanipulation","findfiles","geometry_utils","interatomicsticks"]),
    install_requires=[
        "pandas>=1.5.3",
        "numpy>=1.23.5",
        "ase>=3.22.1",
        "sisl>=0.13",
        "ipykernel>=6.25.2"
    ],
    python_requires='>=3.8',
)