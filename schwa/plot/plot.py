# Copyright (c) 2015 Faculty of Engineering of the University of Porto
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

""" Module for Plotting """
import matplotlib.pyplot as plt
import numpy as np


class Plot:
    """ Plots a scatter.

    Useful for debugging scientific results.

    Attributes:
        x: A list with ints of x axis.
        y: A list with ints of y axis.
        title: A string with the plot title.
        x_label: A string with the x axis label.
        y_label: A string with the y axis label.
    """
    def __init__(self, x=None, y=None, title=None, x_label=None, y_label=None):
        if not x:
            x = []
        if not y:
            y = []
        self.x = x
        self.y = y
        self.title = title
        self.x_label = x_label
        self.y_label = y_label

    def add_x(self, x):
        self.x.append(x)

    def add_y(self, y):
        self.y.append(y)

    def plot(self):
        x = np.array(self.x)
        y = np.array(self.y)
        plt.scatter(x, y)
        if self.title:
            plt.title(self.title)
        if self.x_label:
            plt.xlabel(self.x_label, fontsize=18)
        if self.y_label:
            plt.ylabel(self.y_label, fontsize=18)
        plt.show()