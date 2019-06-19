""" ProcessOhmData.py
    """

import pickle
import socket
import numpy as np
import csv
import sys
import os.path
import time

# Methods: LoadOhm, Pkl2Tetrad

def LoadOhm(filename):
    pass

def main():
    computer_name = socket.gethostname()

    # verify the input file or choose default
    if len(sys.argv) > 1:
        if os.path.isfile(sys.argv[1]):
            filename = sys.argv[1]
        else:
            raise ValueError("Not a valid file.")

    else:
        filename = '../../data/output/ohm_law_data_' + computer_name + '.pkl'
 
    # Unpickle the data
    f = open(filename, 'rb')
    raw_data = pickle.load(f)
    f.close()

    # Create a header row
    data = [['voltage', 'resistance', 'current']]
    data.extend(raw_data)

    # write out the data in a csv file
    if not os.path.isfile('../../data/output/ohm_data_csv_' + computer_name +
            '.csv'):
        outfile = '../../data/output/ohm_data_csv_' + computer_name + '.csv'
    else:
        current_time = time.ctime()
        currenct_time = current_time.replace(' ', '_')
        outfile = '../../data/output/ohm_data_csv_' + computer_name + '_' + current_time + '.csv'

    with open(outfile, 'wb') as csvfile:
        csvwriter = csv.writer(csvfile)
        for row in data:
            csvwriter.writerow(row)


if __name__=="__main__":
    main()



