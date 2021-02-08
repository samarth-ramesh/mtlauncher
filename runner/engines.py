import sqlite3
import json
import os


def GetEngines():
    engParentPath = os.path.join(os.getcwd(), 'runners')
    engs = []
    with os.scandir(engParentPath) as it:
        for pth in it:
            if os.path.isdir(pth.path):
                if os.path.isfile(os.path.join(pth.path, 'engine.json')):
                    with open(os.path.join(pth.path, 'engine.json')) as fp:
                        engineData = json.load(fp)
                        if engineData.get('fname') == pth.name:
                            engs.append((engineData, engineData.get('name')))
    return engs


def writeEngineConfig(engines):
    ...
