# ThermoData2CSV.py

import pickle
import socket
import numpy as np
import csv
import sys
import os.path
import time

# Methods: LoadOhm, Pkl2Tetrad

def LoadThermoData(filename):
    pass

def relative_to_absolute_hum(rel_h, temp):
    """ Inverts the Antoine equation as presented on Wikipedia.
    """
    A = 8.07131
    B = 1730.63
    C = 233.426
    Ph20_star = 10 ** (A - B / (C + temp))
    P = rel_h / 100. * Ph20_star
    return P.reshape(-1,1)

def main():
    computer_name = socket.gethostname()

    # verify the input file or choose default
    if len(sys.argv) > 1:
        if os.path.isfile(sys.argv[1]):
            filename = sys.argv[1]
        else:
            raise ValueError("Not a valid file.")

    else:
        filename = '../../data/output/atmo_data_' + computer_name + '.pkl'
 
    
    # Unpickle the data
    f = open(filename, 'rb')
    raw_data = pickle.load(f)
    f.close()

    # Repack data as numpy array
    ndata = np.array(raw_data)

    # Convert relataive humidity to absolute
    h = relative_to_absolute_hum(ndata[:,3], ndata[:,1])
    ndata = np.hstack((ndata[:,:3], h, ndata[:,3:]))

    # Return to list
    data = ndata.tolist()

    # Create a header row
    data = [['t', 'T', 'P', 'H', 'I']]
    data.extend(raw_data)


    # write out the data in a csv file
    if not os.path.isfile('../../data/output/atmo_data_' + computer_name +
            '.csv'):
        outfile = '../../data/output/atmo_data_' + computer_name + '.csv'
    else:
        current_time = time.ctime()
        currenct_time = current_time.replace(' ', '_')
        outfile = '../../data/output/atmo_data_' + computer_name + '_' + current_time + '.csv'

    with open(outfile, 'wb') as csvfile:
        csvwriter = csv.writer(csvfile)
        for row in data:
            csvwriter.writerow(row)


if __name__=="__main__":
    main()



