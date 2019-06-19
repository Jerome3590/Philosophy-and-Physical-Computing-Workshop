'''
Copyright 2017 Colin R. Shea-Blymyer

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files
(the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''


import numpy as np
import matplotlib.pyplot as plt
from utilities.PlotDecisionRegions import plot_decision_regions

class Perceptron(object):

    def __init__(self, c=0.01, n_iter=10):
        self.c = c
        self.n_iter = n_iter
        self._w = 0


    def net_input(self, x):
        return np.dot(x, self._w)


    def predict(self, x):
        x = np.insert(x, 0, 1., axis=1)
        data = self.net_input(x)
        return np.where(data >= 0, 1, -1)


    def fit(self, X, y):
        """Fit training data.

        Parameters
        ----------
        X : {array-like}, shape = [n_samples, n_features]
            Training vectors, where n_samples is the number of samples
            and n_features is the number of features.
        y : array-like, shape = [n_samples]
            Target values.

        Returns
        -------
        self : object
        """

        x = np.insert(X, 0, 1., axis=1)
        self._w = np.zeros(len(x[0,:]))

        for i in range(self.n_iter):
            choices = np.random.randint(0, len(X), self.n_iter)
            index = choices[i]
            sample = x[index]

            t = y[index]
            a = self.predict(X)[index]
            self._w += self.c * (t - a) * sample

        return self


    def stream_fit_demo(self, X, y, num):
        """Fit training data.

        Parameters
        ----------
        X : {array-like}, shape = [n_features]
            First training vector, where n_features is the number of
            features.
        y : First training vector's true class.

        Returns
        -------
        self : object
        """

        for i in range(num):
            datum = 2 * np.random.sample(2) - 1
            X = np.insert(X, len(X), datum, axis = 0)
            t = self.truth(datum)
            y = np.insert(y, len(y), t)
            a = self.predict(X)[-1]
            sample = np.insert(datum, 0, 1)
            self._w += self.c * (t - a) * sample
            try:
                input("continue: ")
            except:
                print("\n")
            plt.clf()
            plot_decision_regions(X, y, self)
            r = np.arange(-2, 3)
            f = eval('-r')
            plt.plot(r, f)
            dw = self._w[1:]/3.
            plt.arrow(0, -self._w[0], dw[0], dw[1])

        try:
            input("finish: ")
        except:
            print("\n")

        return self


    def terminal_input_fit(self, dims):
        print("New Sample: ")
        cont = "y"
        X = []
        y = []
        while cont != "n":
            xs = []
            for i in range(dims):
                try:
                    el = input("x_" + str(i) + ": ")
                    xs.append(float(el))
                except:
                    print("Input Error: breaking.")
                    cont = "n"
                    return 0

            xs = np.array(xs)
            X.append(xs)
            t = self.truth(xs)
            y.append(t)
            a = self.predict(X)[-1]
            sample = np.insert(xs, 0, 1)
            self._w += self.c * (t - a) * sample

            plt.clf()
            plot_decision_regions(np.array(X), np.array(y), self)
            r = np.arange(-2, 3)
            f = eval('-r')
            plt.plot(r, f)
            dw = self._w[1:]/3.
            plt.arrow(0, -self._w[0], dw[0], dw[1])
            mag = np.sqrt((dw[0]**2.)+((dw[1]+self._w[0])**2.))
            mag_text = "Mag: {0:.4f}".format(mag)
            plt.text(dw[0], (dw[1] - self._w[0]), mag_text)

            print("New Sample: ")


    def click_input_fit(self, X, y):
        pass



    def truth(self, sample):
        if (sample[1] >= -sample[0]):
            return 1
        else:
            return -1


class ClickPerceptron:
    def __init__(self, line, c=0.5):
        self.line = line
        self.xs = list(line.get_xdata())
        self.ys = list(line.get_ydata())
        self.cid = line.figure.canvas.mpl_connect('button_press_event', self)
        self.pt = line.figure
        self.X = []
        self.y = []
        self.perc = Perceptron(c, n_iter=50)

    def __call__(self, event):
        print('click', event)
        x1 = event.xdata
        x2 = event.ydata
        if x1 is None or x2 is None: return
        sample = np.array([x1, x2])
        self.X.append(sample)
        print(sample)
        t = self.perc.truth(sample)
        self.y.append(t)
        a = self.perc.predict(self.X)[-1]
        xs = np.insert(sample, 0, 1)
        self.perc._w += self.perc.c * (t - a) * xs
        self.pt.clf()
        plot_decision_regions(np.array(self.X), np.array(self.y), self.perc)
        r = np.arange(-10, 11)
        f = eval('-r')
        plt.plot(r, f)
        dw = self.perc._w[1:]/3.
        plt.arrow(0, -self.perc._w[0], dw[0], dw[1])
        mag = np.sqrt((dw[0]**2.)+((dw[1]+self.perc._w[0])**2.))
        mag_text = "Mag: {0:.4f}".format(mag)
        plt.text(dw[0], (dw[1] - self.perc._w[0]), mag_text)

def setup_ClickPerceptron(c=0.5):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    line, = ax.plot([0], [0])
    clack = ClickPerceptron(line, c)
    plt.show()
