"""
convert original topo to formats for geoclaw
"""

import numpy as np
import geotools.topotools as gt
import pylab
import os

def maketopo():
    infile = 'mars_500m_XYZ.dat' #topo file
    outfile = 'Mars_500m_topo.tt2'
    converttopo(infile,outfile)


def converttopo(infile,outfile):
    """
    convert from 3-column, x,y,z, to single column with header for spacing
    """

    if (os.path.exists(outfile)):
        print (' '+outfile+' already exists...skipping')
        print ' To recreate delete file and then rerun maketopo.py\n'
    else:
        print (' converting '+(infile)+' to '+(outfile))
        print ' output format contains a header and single column of data'


        a = np.loadtxt(infile,skiprows=9)

        xdiff=np.diff(a[:,0])
        inddiff=pylab.find(xdiff<0)
        xlength=inddiff[0]+1
        ylength=len(a[:,0])/xlength
        x=a[:,0]
        y=a[:,1]
        z=a[:,2] + 3500.0 # + 4680.1

        X=np.reshape(x,(ylength,xlength))
        Y=np.reshape(y,(ylength,xlength))
        Z=np.reshape(z,(ylength,xlength))

        #Y=np.flipud(Y)
        #Z=np.flipud(Z)

        gt.griddata2topofile(X,Y,Z,outfile)
        print ' file conversion complete\n'

if __name__=='__main__':
    maketopo()