import socket
import pickle
import numpy as np


def relative_to_absolute_hum(rel_h, temp):
    """ Inverts the Antoine equation as presented on Wikipedia.
    """
    A = 8.07131
    B = 1730.63
    C = 233.426
    Ph20_star = 10 ** (A - B / (C + temp))
    P = rel_h / 100. * Ph20_star
    return P.reshape(-1,1)


def hlt_prep(source='default'):
    """ Opens the stored data from the atmospheric measurement experiment, and
    preps data on light intensity, temperature, and humidity for
    classification.
    """
    # Unpickle the data
    if source == 'default':
        computer_name = socket.gethostname()
        filename = '../../data/output/atmo_data_' + computer_name + '.pkl'
    elif source == 'tesseract':
        filename = '../../data/output/atmo_data_Tesseract.pkl'
    else:
        raise ValueError(
                "Acceptable arguments are nothing, or 'source=tesseract'")

    f = open(filename, 'rb')
    data = pickle.load(f)
    f.close()

    # Repack data as numpy array
    ndata = np.array(data)
    
    # Shuffle the data
    np.random.shuffle(ndata)

    # Convert relataive humidity to absolute
    h = relative_to_absolute_hum(ndata[:,3], ndata[:,1])
    ndata = np.hstack((ndata[:,:3], h, ndata[:,3:]))

    # Process for regressing humidity on temperature and light
    humidity = ndata[:,3]
    temperature = ndata[:,1].reshape(len(ndata[:,1]),1)
    light = ndata[:,4].reshape(len(ndata[:,4]),1)
#    norm_temperature = (temperature - np.mean(temperature)) / np.max(np.abs(temperature 
#        - np.mean(temperature)))
#    norm_light = (light - np.mean(light)) / np.max(np.abs(light - np.mean(light)))
    
#    temp = np.hstack((norm_temperature, norm_light))
#    X = []
#    y = []
#    m = np.mean(humidity)
#    
#    for i, h in enumerate(humidity):
#        if h >= m:
#            y.append(1.)
#            X.append(temp[i,:])
#        elif h < m:
#            y.append(-1.)
#            X.append(temp[i,:])
    
    y = humidity
    X = np.hstack((temperature, light))

    index = 8*len(y)/10

    y_train = y[0:index]
    X_train = X[0:index, :]

    y_test = y[index:len(y)]
    X_test = X[index:len(y),:]
    
    return X_train, y_train, X_test, y_test

