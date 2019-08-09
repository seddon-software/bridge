import pandas as pd
import sys, os
import re
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
    

def splitIt(s, n):
    s = re.split(r'[()]', s)
    return s[n]

def readExcelFile(excelFile, sheet):
    table = pd.read_excel(excelFile, sheet)
    table = table[['A','B','COUNT']]
    table['text'] = table.apply(lambda row : splitIt(row['A'], 0), raw = True, axis = 1)
    table['ptsE']  = table.apply(lambda row : splitIt(row['A'], 1), raw = True, axis = 1)
    table['ptsW']  = table.apply(lambda row : splitIt(row['B'], 0), raw = True, axis = 1)
    table.drop(['A','B'], axis = 1, inplace = True)
    
#     print(table[table.text == "TNT if 1H makes"])
#     print(table[table.text == "TNT if 2H makes"])
    return table
    

import time

def plotIt(table):
    plt.ion()
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    table.drop(['text'], axis = 1, inplace = True)
    print(table)
    table = table.apply(pd.to_numeric)
    X = table['ptsE'].as_matrix()
    Y = table['ptsW'].as_matrix()
    Z = table['COUNT'].as_matrix()
#    ax.scatter(X, Y, Z)
#    ax.plot_surface(X, Y, Z)
    ax.plot_trisurf(X, Y, Z, cmap='viridis', edgecolor='none')
    ax.set_xlabel('ptsE')
    ax.set_ylabel('ptsW')
    ax.set_zlabel('count')
    plt.show()
    for angle in range(0, 360):
        # ax.view_init(30, angle)
        plt.draw()
        plt.pause(0.001)
        time.sleep(1.0)
    

os.chdir("/Users/Seddon/home/_Bridge/My Articles")
data = readExcelFile("weak_twos.xlsx", "2nd_seat")
plotIt(data)
