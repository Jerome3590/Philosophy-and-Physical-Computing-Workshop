import pickle
import numpy as np
import matplotlib.pyplot as plt
from completed_examples import *
import utilities
import getopt
import sys

try:
    filename = sys.argv[1]
except:
    print('python ProcessThermoData.py filename')
    sys.exit(2)

with open(filename, 'rb') as f:
    data = pickle.load(f)

new = []
for row in data:
    new.append([row[1], row[0], row[2]])

out_file = filename[:-4] + '_repaired.pkl'

with open(out_file, 'wb') as f:
    pickle.dump(new, f)
