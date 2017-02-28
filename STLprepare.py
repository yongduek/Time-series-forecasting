'''
 read datafile, apply STL decomposition, save data for further processing
'''
thisfilename = 'STLprepare.py'

import numpy as np
import csv
import rpy2
from pylab import plot, show, bar

with open ('cif-dataset.txt') as csvfile :
    cr = csv.reader (csvfile, delimiter=';')
    for row in cr:
        val = int (row[1]) # horizon of forecast
        if val == 12:
            seq = np.array(row[3:])
            print (row)
            print (seq)
            #plot (seq)
            #show()


print ('Finished ', thisfilename)