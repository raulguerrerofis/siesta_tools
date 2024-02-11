def replaceinfile(pattern=True,line_number=int,opatt=str,dpatt=str, mainpath=str,ofilename=str,dfilename=str,verbose=False):
    """opatt = Original pattern
       dpatt = Destiny pattern

    Parameters
    ----------
    pattern :
          (Boolean)
          True: If you need to change a 
          False: If you need to replace a full line  you can add an extra argument to this function showing the number of line.
    line_number:
          (Default value = int)
          
          Aviable only if pattern == False
          'line_number' and 'pattern == True' will change the full line for the 'dpatt' that you provide.
          The index must start from one, i.e., first line_number is 1 and so on.
    opatt :
         (Default value = str)
         The string original pattern (the one to replace).
    dpatt :
         (Default value = str)
         The string destiny pattern (the one to delete).
    mainpath :
         (Default value = str)
         The path of the directory where the file is located.
    ofilename :
         (Default value = str)
         The name of the original file. Including the extention.
    dfilename :
         (Default value = str)
         The name of the destiny file. Including the extention.
         

    Returns
    -------
     No returns, just the new file
    """
    with open(mainpath+ofilename,'r') as infile:
        lines =  infile.readlines()
    if pattern==True:
          
          outfile = open(mainpath+dfilename,'w+')
          
          [outfile.write(i.replace(opatt,dpatt))  if opatt in i else outfile.write(i) for i in lines];
          
          outfile.close()
          
    elif pattern == False:
          
          lines[line_number-1] = dpatt
          
          outfile = open(mainpath+dfilename,'w+')
          
          [outfile.write(i) for i in lines];
          
          outfile.close()
          
    
    if verbose==True:
         return print('Destiny file -> ',mainpath+dfilename)