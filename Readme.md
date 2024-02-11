# SIESTA utilities

##  Description

I did this package to create a modern source of tools for SIESTA calculations. I mix different dependences like ``ase`` and ``sisl`` which are very versatile tools to explore bands calculations.

## Instalation

You can install this package as follows

```markdown
    cd siesta_tools
    pip install -e .
```

## Usage example

#### geom2siesta function

This function imports the most common geometries files with (``vasp, xyz, quantum_expresso``) to return a siesta file named like: ``siesta_system.fdf``. If your input geometry is a ``xyz`` file, note that the cell in the ``siesta_system.fdf`` file will be filled with zero values, since the ``xyz`` format usually do not provide any cell.

**recomendation: you can add ``%include siesta_system.fdf`` to your main.fdf file to import the geometry and cell**

```python
from siesta_tools.utilities import geom2siesta

geom2siesta(path, 'newgeometrytest', pdheader=False,sort=False)

```

#### plot_bands function

Note that the input is a folder path not a *bands file, the code will search for the *bands file.

```python
from siesta_tools.electronic_utils import plot_bands
plot_bands(band_FOLDER)
```

## Contributing

Feel free to contact me to colaborate with this little project.

## License

See ``License.txt`` file.
