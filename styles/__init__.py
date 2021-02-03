import os

def compile():
    files = os.listdir('styles')
    retVal = "" 
    for f in files:
        if f[-4:] == '.qss':
            with open(os.path.join('styles', f), 'r') as fp:
                retVal += ('\n' + fp.read())

    return retVal