# This is free software licensed under the MIT license.
# Copyright (c) 2021 Samarth Ramesh <samarthr1@outlook.com>
# You should have recived a copy of the MIT license with this file. In case you ahve not, visit https://github.com/samarth-ramsh/mtlaucher

import os

def compile():
    files = os.listdir('styles')
    retVal = "" 
    for f in files:
        if f[-4:] == '.qss':
            with open(os.path.join('styles', f), 'r') as fp:
                retVal += ('\n' + fp.read())

    return retVal