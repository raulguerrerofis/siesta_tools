import numpy as np
import matplotlib.pyplot as plt

    
def  intersticks(dmin=0.01,dmax=1.42,dist=[],ax=None,axis='xy',scale=1):   
    """Creates the plot of bondings between chemical species 

    Parameters
    ----------
    dmin    : float (Angstrom)
        (Default value 0.01)
        Minimum distance between atoms.
    dmax    : float (Angstrom)
        (Default value 1.42 [Carbon-Carbon distance])
        Maximum distance between atoms.
        
    dist    :
        (Default value = [])
        Array atomic positions
    ax      :
        (Default value = None)
        Matplotlib axis
    axis    :
        (Default value 'xy')
        Point of view to see the plot xy, xz  or yz.
    scale   :
        (Default value, 1)
        Scale the atomic positions to enlarge the resolution of fitting when plotting above an 'experimental image'.
    Returns
    -------
    It just plot the bonding sticks.
    """
    for n,i in  enumerate(dist):
        for m,j in enumerate(dist):
            i = i*scale
            j = j*scale
            d = np.linalg.norm(j-i)
            if n >= m and dmin < d <= dmax:
                if axis   == 'xy':
                    ax.plot([i[0],j[0]],[i[1],j[1]], color='gray',alpha=0.55,zorder=0)
                elif axis == 'xz':
                    ax.plot([i[0],j[0]],[i[2],j[2]], color='gray',alpha=0.55,zorder=0)
                elif axis == 'yz':
                    ax.plot([i[1],j[1]],[i[2],j[2]], color='gray',alpha=0.55,zorder=0)
                    
    return