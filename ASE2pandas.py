
import pandas as pd
from ase.io import read
def ASE2PANDAS (path=str):
    """Reads Atomic Simulation Environment geometries to Pandas

    Parameters
    ----------
    path    : full path of the geometry.  If a direct Atoms  (ASE) object is given, it also will provide a pandas dataframe.


    Returns
    -------
    Pandas Dataframe with atomic symbols and chemical symbols.
    """
    if "Atoms" in str(path):
        ingeom = path
    else:
        ingeom    = read(path).repeat((1,1,1))
    df        = pd.DataFrame({'symbol':ingeom.get_chemical_symbols(),
            'x':ingeom.get_positions()[:,0],
            'y':ingeom.get_positions()[:,1],
            'z':ingeom.get_positions()[:,2]})
    return df