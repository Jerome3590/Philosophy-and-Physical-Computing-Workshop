import numpy as np
import piplates.DAQCplate as DAQC
import time
import socket
import os.path
import pickle


data = []

print("Beginning to sample...") 
print("Make sure your potentiometer is turned counterclockwise as far as it will go.")
print("Use the two knobs on the right to set your power supply to 5.0 V.")
raw_input('Press Enter to continue.')
print('\n')

for resistance in ['A','B','C']:
        for voltage in ['X','Y','Z']:
                resample = True
                while resample == True:
                        current = DAQC.getADC(0, 0)
                        temp = [voltage, resistance, current]
                        print('\nYou just took a measurement of current for the {} resistance with voltage {}'.format(resistance, voltage))
                        input_valid = False
                        while not input_valid:
                                choice = raw_input('\nIf you wish to keep it, enter "c". If you wish to remeasure for those conditions, enter "r" (and press Enter).\n')
                                if choice == 'c' or choice == 'r':
                                        input_valid = True
                        if choice == 'c':
                                data.append(temp)
                                resample = False
                if not voltage == 'Z':
                    print("\nAdust the voltage up by +2 V.")
                raw_input('\nPress Enter to continue.')
        if not resistance == 'C':    
            print("\nTurn the potentiometer approximately 30 degrees clockwise.")
            print("\nSet the voltage on your power supply back to 5.0 V.")
            raw_input("\nPress Enter to continue.")
                                
# Pickle the data
# set filename
sample_time = time.ctime()
sample_time = sample_time.replace(' ', '_')
computer_name = socket.gethostname()
filename = ('../../data/output/ohm_law_data_' + computer_name 
        + '.pkl')
if os.path.isfile(filename):
        filename = ('../../data/output/ohm_law_data_qualitative_' + computer_name 
                + '_' + sample_time + '.pkl')

out = open(filename,'wb')
pickle.dump(data, out)
out.close()

print('\nThe following data has been saved:\n')
print(data)
