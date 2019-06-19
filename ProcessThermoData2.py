""" ProcessThermoData.py
The column headings for the data are:
    time, temperature, pressure, humidity, light
    """

import pickle
import socket
import numpy as np
import matplotlib.pyplot as plt
from completed_examples import *
import utilities
import getopt
import sys

def relative_to_absolute_hum(rel_h, temp):
    """ Inverts the Antoine equation as presented on Wikipedia.
    """
    A = 8.07131
    B = 1730.63
    C = 233.426
    Ph20_star = 10 ** (A - B / (C + temp))
    P = rel_h / 100. * Ph20_star
    return P.reshape(-1,1)


# Process command line options
linearize = True
use_sample_data = False
try:
    opts, args = getopt.getopt(sys.argv[1:],"uT")
except getopt.GetoptError:
    print('ProcessThermoData.py [-uT]')
    sys.exit(2)
for opt, arg in opts:
    if opt in ('-u'):
        linearize = False
    if opt in ('-T'):
        use_sample_data = True

# Unpickle the data
if use_sample_data:
    filename = '../../data/output/atmo_data_Tesseract.pkl'
else:
    computer_name = socket.gethostname()
    filename = '../../data/output/atmo_data_' + computer_name + '.pkl'
f = open(filename, 'rb')
data = pickle.load(f)
f.close()

# Repack data as numpy array
ndata = np.array(data)

# Convert relataive humidity to absolute
h = relative_to_absolute_hum(ndata[:,3], ndata[:,1])
ndata = np.hstack((ndata[:,:3], h, ndata[:,3:]))

# Plot pressure vs. temperature
f0 = plt.figure(0)
plt.plot(ndata[:,1], ndata[:,2], 'bo')
plt.title('Pressure vs. Temperature')
plt.xlabel('T')
plt.ylabel('P')

# Plot humidity vs. temperature
f1 = plt.figure(1)
plt.plot(ndata[:,1], ndata[:,3], 'bo')
plt.title('Humidity vs. Temperature')
plt.xlabel('T')
plt.ylabel('H')

# Plot light intensity vs. temperature 
f2 = plt.figure(2)
plt.plot(ndata[:,1], -ndata[:,4], 'bo')
plt.title('Light intensity vs. Temperature')
plt.xlabel('T')
plt.ylabel('I')

# Plot humidity vs. pressure
f3 = plt.figure(3)
plt.plot(ndata[:,2], ndata[:,3], 'bo')
plt.title('Humidity vs. Pressure')
plt.xlabel('P')
plt.ylabel('H')

# Plot humidity vs. light intensity
f3 = plt.figure(4)
plt.plot(ndata[:,4], ndata[:,3], 'bo')
plt.title('Humidity vs. Light intensity')
plt.xlabel('I')
plt.ylabel('H')

# Process for perceptron demo (classify humidity using temperature and light)
humidity = ndata[:,3]
temperature = ndata[:,1].reshape(len(ndata[:,1]),1)
pressure = ndata[:,2].reshape(len(ndata[:,2]),1)
norm_temperature = (temperature - np.mean(temperature)) / np.max(np.abs(temperature 
    - np.mean(temperature)))
norm_pressure = (pressure - np.mean(pressure)) / np.max(np.abs(pressure - np.mean(pressure)))

temp = np.hstack((norm_temperature, norm_pressure))
X = []
y = []
m = np.mean(humidity)

if linearize:
    s = np.std(humidity) / 2.
    
    for i, h in enumerate(humidity):
        if h > m + s:
            y.append(1.)
            X.append(temp[i,:])
        elif h < m - s:
            y.append(-1.)
            X.append(temp[i,:])
else:
    for i, h in enumerate(humidity):
        if h > m:
            y.append(1.)
            X.append(temp[i,:])
        elif h <= m:
            y.append(-1.)
            X.append(temp[i,:])


y = np.array(y)
X = np.array(X)

# Fit perceptron
p = Perceptron()
p.fit(X, y)

# Display results
f4 = plt.figure(5)
utilities.plot_decision_regions(X, y, p, title='Humid or Dry',
xlabel='normalized temperature', ylabel='normalized pressure')

