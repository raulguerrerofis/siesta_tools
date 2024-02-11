import os
import numpy as np
def whichfile(extension='.bands', directory = '~/' ):
    """

    Parameters
    ----------
    extension :
        (Default value = '.bands')
        Here is the extention of the file that you want to extract form the directory.
    directory :
        (Default value = '~/')
        The Directory.

    Returns
    -------
    It returns the name of the full path of the file.
    
    """
    list_files = os.listdir(directory)
    for i in list_files:
            if extension in i :
                    myfile = directory+i
                    break
    return myfile


def extract_pattern(f=str, pattern = 'Total =',indexofvalue=-1,name ='no_name'):
    """

    Parameters
    ----------
    f :
         (Default value = str)
        Path of the file.
    pattern :
        (Default value = 'Total =')
        Pattern to extract from the file
    indexofvalue :
        (Default value = -1)
        Example: If the pattern line contains  3 numbers by default it will takes the last one (-1) but if you want the second one add set 'indexofvalue=1'or 
        'indexofvalue=-2'
    Returns
    -------
    returns a tuple of the (pattern, value)
    
    """
    with open(f,'r') as input:
        lines =  input.readlines()
    ee = []
    for i in lines:
        if pattern in i:
            try:
                ee.append(float(i.split()[indexofvalue]))
                if len(float(i.split()[indexofvalue])) == 0:
                    ee.append(np.nan)
            except:
                ee.append(np.nan)
                
    if name=='no_name':
        name=pattern
    else :
        name=name
    return (name,ee[0])