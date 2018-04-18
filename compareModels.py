#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, argparse, os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

"""
Simple program for visual comparison of TLUSTY models
More about TLUSTY http://nova.astro.umd.edu/
https://arxiv.org/abs/1706.01937
---------------------------------------------------------
example call  >> python3 compareModels.py fort.7 -t -d -e
"""

def readModel(filename):
    model=pd.DataFrame()
    deepPoints=[]
    NDEPTH=0;NUMPAR=0;
    with open(filename) as f:
        line = f.readline()
        [NDEPTH,NUMPAR]=[int(s) for s in line.split()]
        while len(deepPoints) < NDEPTH:
            line = f.readline()
            l=[float(s.replace('D', 'E')) for s in line.split()]
            deepPoints.extend(l)
        dfSpectrum = pd.read_table(f,header=None,delim_whitespace=True)
        dfSpectrum = dfSpectrum.applymap(lambda x: float(x.replace('D', 'E')))
        model=np.transpose(dfSpectrum.values.flatten().reshape((-1,NUMPAR)))
        #model contains
        # in model[0,:] - Temperature
        # in model[1,:] - Electron density
        # in model[1,:] - Mass density
        # in the rest populations (unless it is model of acretion disc)
    return (NDEPTH,NUMPAR,deepPoints,model)


def main():

    descStr="""
    Show TLUSTY models for comparison.\n
    """
    parser=argparse.ArgumentParser(description=descStr)

    parser.add_argument(nargs='+',dest='fileName',help="Models to display",type=str)
    parser.add_argument('-t','--temperature',dest='ifTemp',action='store_true', required=False, default=False, help="Display temperatures")
    parser.add_argument('-e','--electron',dest='ifElec',action='store_true', required=False, default=False, help="Display electron density")
    parser.add_argument('-d','--density',dest='ifDens',action='store_true', required=False, default=False, help="Display mass density")
    args=parser.parse_args()

    #======== READ DATA AND PLOT
    if not (args.ifTemp or args.ifElec or args.ifDens):
        print("Choose quantity to print. Check --help")
        return

    plots={}
    if args.ifTemp:
        plots["TEMP"]= plt.subplots(1)
        plots["TEMP"][1].set_title('Temperature')
        plots["TEMP"][1].set_ylabel('T [K]')
        plots["TEMP"][1].set_xlabel('Column mass [g cm-2]')
    if args.ifElec:
        plots["ELECTRON"]= plt.subplots(1)
        plots["ELECTRON"][1].set_title('Electron density')
        plots["ELECTRON"][1].set_ylabel('n_e [cm-3]')
        plots["ELECTRON"][1].set_xlabel('Column mass [g cm-2]')
    if args.ifDens:
        plots["DENSITY"]= plt.subplots(1)
        plots["DENSITY"][1].set_title('Mass density')
        plots["DENSITY"][1].set_ylabel('rho [g cm-3]')
        plots["DENSITY"][1].set_xlabel('Column mass [g cm-2]')

    for i, f in enumerate(args.fileName):
        if not os.path.isfile(f):
            continue
        NDEPTH,NUMPAR,deepPoints,model=readModel(f)
        if args.ifTemp:
            y=model[0,:]
            plots["TEMP"][1].semilogx(deepPoints,y,label=f)
        if args.ifElec:
            y=model[1,:]
            plots["ELECTRON"][1].semilogx(deepPoints,y,label=f)
        if args.ifDens:
            y=model[2,:]
            plots["DENSITY"][1].semilogx(deepPoints,y,label=f)
    for name,(f,ax) in plots.items():
        ax.legend(loc=1)
    plt.show()

if __name__=='__main__':
    main()
