import numpy as np
import sisl
import matplotlib.pyplot as plt
import os
import pandas as pd

def plot_bands(folder, annot=False,shifted=True):
    """

    Parameters
    ----------
    folder :
        The path of the siesta calculation folder (Not the *bands file)
    annot :
        (Default value = False)
        Allows to plot an extra plot showing the indexes of the band.
    fig :
        (Default value = fig)
        Figure related with the plot.
    ax :
        (Default value = ax)
        Axis of the plot.
    shifted :
        (Default value = True)

    Returns
    -------

    
    """
    
    bandfile = '' # this line is just to avoid unound variable in python
    
    ################################## Watching for the band file in the folder
    list_files = os.listdir(folder)
    for i in list_files:
            if '.bands' in i :
                    bandfile = folder+i
                    break
    print(bandfile)
    ################################## Extracting information using sisl
    
    bandas = sisl.io.siesta.bandsSileSiesta(bandfile)
        
    #From the bands
    Ebands       = bandas.read_data()

    hsp_info     = list(Ebands[0])

    
    if len(hsp_info[1]) == 0 :
        hsp_info[1] = [i for i in range(len(hsp_info[0]))]    
        print('Your calculation do not show any high symmetry point key-name;\n The code will replace it with a list of integers')
    else:
        hsp_info[1]  = [r'$\Gamma$'   if i =='Gamma'  else i for i in hsp_info[1]]
        
    #storing the hsp information in a dictionary    
    hsp_info     = {'HSP_VALS':hsp_info[0],'HSP_NAMES': hsp_info[1]}

    banda_siesta = np.array(list(Ebands)[2])
    kpbands      = np.array(list(Ebands)[1])

    if shifted == False:
        eF = 0.0
        
    else:    
        eF = sisl.io.siesta.eigSileSiesta(bandfile[:-5]+'EIG').read_fermi_level()
        
    delta        = 1.5
    
    fig, ax = plt.subplots(figsize=(5,6), tight_layout=True ) 

    for i in range(len(kpbands)):
            ax.plot(kpbands,banda_siesta[:,0,i]+eF, color='blue',lw=0.75)
            try : 
                    ax.plot(kpbands,banda_siesta[:,1,i]+eF, color='red',lw=0.75,ls='--')
                    if i == 0:
                            print('Polarized calculation')
            except:
                    if i == 0:
                            print('Non-polarized calculation')

    ax.set_xlim(np.min(kpbands),   np.max(kpbands));


    ax.set_ylim(eF-delta,eF+delta)
    ax.set_xlim(np.min(kpbands),   np.max(kpbands))

    ax.set_ylabel('Energy (eV)');
    ax.set_xticks(hsp_info['HSP_VALS']);
    ax.set_xticklabels(hsp_info['HSP_NAMES']);


    ax.axhline(eF,color='gray',lw=0.75,ls='--');
    [ax.axvline(float(x)   ,c='gray',lw=0.75) for x in hsp_info['HSP_VALS']];

    fig.savefig(bandfile[:-6]+'Bands.png',format='png',dpi=300)
    
    if annot == True:
        kkk = 126*2
        [ax.annotate('{}'.format(i+1),(kpbands[kkk], banda_siesta[kkk,1,i]+eF),rotation=0,color='red' )  for i in range(   len(banda_siesta[:,1,:])        )];
        [ax.annotate('{}'.format(i+1),(kpbands[kkk], banda_siesta[kkk,0,i]+eF),rotation=0,color='blue' ,alpha=0.5) for i in range(   len(banda_siesta[:,0,:])        )];
        fig.savefig(bandfile[:-6]+'Bands_annot.png',format='png',dpi=200)
        
        
        
def pop_reader(pop_file):
    """

    Parameters
    ----------
    pop_file :
        path of the siesta_out file that contains the population

    Returns
    -------
    Returns a Pandas dataframe with the whole charges and atomic species

    """
    with open(pop_file,'r') as infile:
        lines=infile.readlines()
    for n, i in enumerate(lines):
        if 'Hirshfeld Net Atomic Populations' in i:

            break
    for m, i in enumerate(lines[n:]):
        i = i.split()
        if len(i) ==0 :
            break
    atom   = [int(i.split()[0])  for i in lines[n+2:n+m]]
    charge = [float(i.split()[1])  for i in lines[n+2:n+m]]
    species = [str(i.split()[2])  for i in lines[n+2:n+m]]
    colnames = lines[n+1].replace('#','').split()
    
    try:
        df_hirsh  = pd.DataFrame(columns=colnames)
        df_hirsh[colnames[0]] = atom
        df_hirsh[colnames[1]] = charge
        df_hirsh[colnames[2]] = species
        return df_hirsh
    except:
        return 0
        pass