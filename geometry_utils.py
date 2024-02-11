from ase import Atoms
from ase.io import read, write
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from ase.visualize import view
from ase.visualize.plot import plot_atoms
from  my_packages.SIESTA_UTILS.siesta_tools.utilities import geom2siesta
from  my_packages.SIESTA_UTILS.siesta_tools.findfiles import whichfile

def subset_rotation(path1 = str,ang1=int,ang2=int,left=[],right=[],savein='./',save_format='vasp',name_file='system', plott=False):
    # print('Reading from : {}'.format(path1))
    infile = read(path1)
    pos    = infile.get_positions()
    chem   = infile.get_chemical_symbols()
    # print(chem)
    # print(len(pos))

    def subset( indexes, ang, axiss=None, celda=None, pos=pos):
        """"Select only the atoms with we want to rotate in the whole structure. The rotation axis is determined y the fist two atom indexes of indexes list"""
        if len(indexes):
            chem1  = [chem[i] for i in indexes]
            pos1   = pos[indexes]
            b      =  Atoms(chem1,pos1, cell = celda,pbc =True)
            v      =  pos1[0] - pos1[1]
            c      = ( pos1[0] + pos1[1])*0.5
            b.rotate(ang,v,center=c,rotate_cell=False)
            return b
        else :
            print('The index is empty')
            return 0

    bz1indx  = right    
    bz2indx  = left     

    b1 = subset(bz1indx,ang1,axiss=bz1indx[:2],    celda=infile.get_cell())
    b2 = subset(bz2indx,ang2,axiss=bz2indx[:2],    celda=infile.get_cell())

    pp = pos
    for n,i in enumerate(pp):
        for j,k in zip(bz1indx,b1.get_positions()):
            if j == n:
                pp[n] = k

    for n,i in enumerate(pp):
        try:
            for j,k in zip(bz2indx,b2.get_positions()):
                if j == n:
                    pp[n] = k
        except:
            print('The second subsystem is empty')
            break
    outgeom = Atoms(chem, positions=pp, cell = infile.get_cell(), pbc=True)


    if plott == True:
        
        _ , ax = plt.subplots(figsize=(15,20),nrows=3)
        
        plot_atoms(outgeom,rotation='0x,0y,0z',ax=ax[0])
        
        plot_atoms(outgeom,rotation='-90x,0y,0z',ax=ax[1])
        
        plot_atoms(infile,rotation='0x,0y,0z',ax=ax[2])
        
    # display(ase.visualize.ngl.view_ngl(outgeom, w=1500, h=500))
    
    # [print('{:3.7f}     {:3.7f}      {:3.7f}'.format(i,j,k)) for i,j,k in outgeom.get_cell()]

    system     = outgeom
    uniquechem = np.unique(system.get_chemical_symbols())
    indexlist  = dict(zip(uniquechem,list(range(1,len (uniquechem)+1))))

    realindex= [int(j) for n, (p,c) in enumerate(zip(system.get_positions(),system.get_chemical_symbols()),1) for i,j in indexlist.items() if c == i]

    char1                = '#,'*len(realindex)
    char1                = char1.split(',')
    data1                = pd.DataFrame()
    data1['x']           = system.get_positions()[:,0]
    data1['y']           = system.get_positions()[:,1]
    data1['z']           = system.get_positions()[:,2]
    data1['index']       = realindex
    data1['comment']     = char1[:-1]
    data1['Symbol']      = system.get_chemical_symbols()
    data1                = data1.sort_values(by=['index','Symbol'])
    data1['atom number'] = np.arange(1,len(realindex)+1)
    
    # namefile = '{}_{:3.1f}{}'.format(name_file, str(ang1).zfill(3), save_format)
    namefile = name_file
    # .format(str(i).zfill(3))
    
    if ang1 < 0:
        ang_aux = str(ang1).replace('-','m')
        namefile = '{}_{}{}'.format(name_file,ang_aux,save_format)
        
    
    if save_format  =='siesta':
        namefile = namefile.replace('siesta','_siesta_geom')
        geom2siesta(outgeom,savein+namefile,pdheader=False)
        
    elif save_format =='vasp':
        aaa  = savein+namefile
        aaa  = aaa.replace('vasp','.vasp')
        print('destination file name ',aaa)
        write(aaa, outgeom,format='vasp', direct=False)
        
    elif save_format == 'none':
        print('Not saved by subset_rotation function')
        
    return outgeom

def read_siesta_format(filepath=str,out_format='vasp'):
    
    print(filepath)
    with open(filepath, 'r') as infile1:
        lines= infile1.readlines()
    N = 0
    pos = []
    for n1,i in enumerate(lines):
        if 'NumberOfAtoms' in i:
            N = int(i.split()[-1])
    for n2,i in enumerate(lines):
        if 'AtomicCoordinatesAndAtomicSpecies' in i:
            break
    for n3,i in enumerate(lines):
        if 'LatticeVectors' in i:
            break
    pos  = np.genfromtxt(lines[n2+1:n2+N+1],dtype=float)[:,:3]
    sym  = np.array([ i.split()[5]   for i in  lines[n2+1:n2+N+1]],dtype = str)
    cell = np.genfromtxt(lines[n3+1:n3+4])
    
    asegeom = Atoms(symbols=sym,positions=pos,cell=cell)
    outgeompath = filepath.replace('_siesta','')+'.vasp'
    
    if out_format == None:
        pass
    else:
        write(outgeompath,asegeom,format=out_format,direct=False)
    
    return asegeom, outgeompath

