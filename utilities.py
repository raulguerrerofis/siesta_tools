from ase.io import read 
import pandas as pd
import numpy as np

def geom2siesta(filepath,outfilename,sort=False,pdheader=True):
    """This function creates a siesta file from many other formats by using ASE.
    You can use the %include tag from siesta or directly copy the result in the main *fdf file

    Parameters
    ----------
    filepath    : str
        Complete path of the geometry to convert.
    outfilename : str
        The name of the file. The file will follows the path of the ``filepath``.
        
    sort :
        (Default value = False)
        If is needed the function will sort the rows by the atomic symbol. 
        Setting to True, the function will bring 2 extra commented columns in the *fdf file,
        the older order and the new order of the atomic positions. Use this function in single point
        calculations, for other cases, try to keep it False because if you are relaxing by fixin atoms
        the index will change.
    pdheader :
        (Default value = True)
        If needed the function will print a header considering each column
    Returns
    -------
    Automatically saves the siesta *fdf file and returns a tuple with dataframe with the geometry 
    and a dataframe with the cell readed, i.e., (geometry_df, cell_df)
   
    """
    system = read(filepath)
    uniquechem = np.unique(system.get_chemical_symbols())
    indexlist  = dict(zip(uniquechem,list(range(1,len (uniquechem)+1))))

    realindex= [int(j) for n, (p,c) in enumerate(zip(system.get_positions(),system.get_chemical_symbols()),1) for i,j in indexlist.items() if c == i]

    char1          = '#,'*len(realindex)
    char1          = char1.split(',')
    df             = pd.DataFrame()
    df['x']        = system.get_positions()[:,0]
    df['y']        = system.get_positions()[:,1]
    df['z']        = system.get_positions()[:,2]
    df['index']    = realindex
    df['comment']  = char1[:-1]
    df['symbol']   = system.get_chemical_symbols()
    
    # display(data1.head(20))
    
    if sort==True:
        df['old_atm_num'] = np.arange(1,len(realindex)+1)
        df = df.sort_values( by = 'symbol')
        df['new_atm_num'] = np.arange(1,len(realindex)+1)
    else:
        df['atm_num'] = np.arange(1,len(realindex)+1)
    # [print('{:3.6f}   {:3.6f}    {:3.6f} '.format(system.get_cell()[i][0],system.get_cell()[i][1],system.get_cell()[i][2])) for i in range(3)]
   
    # display(data1.head(20))
    filepath = '/'.join(filepath.split('/')[:-1])+'/'
    print(filepath)
    outfilepath = filepath+outfilename+'.fdf'
    with open(outfilepath,'w') as ff:
        if pdheader == True:
            ff.write('#')
            ff.write('     '.join(df.columns))
            ff.write('\n')
        
        ff.write('%block AtomicCoordinatesAndAtomicSpecies\n')
        ll = df.to_string(header=pdheader, index=False,  justify='right',col_space=5)
        ff.write(ll)
        ff.write('\n%endblock AtomicCoordinatesAndAtomicSpecies\n')
        
    with open(outfilepath,'a') as outfile:
        outfile.write('\n%block LatticeVectors\n')
        dfcell = pd.DataFrame(system.get_cell(),columns=['a1','a2','a3'])
        llc = dfcell.to_string(header=False, index=False, justify='right', col_space=5)
        outfile.write(llc)
        outfile.write('\n%endblock LatticeVectors\n')
    return (df,dfcell)
