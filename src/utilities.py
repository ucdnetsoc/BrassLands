import os
import config

def RootGameDirectory():
    thisDirPath = os.path.dirname(os.path.realpath(__file__))
    rootDirPath = os.path.abspath(os.path.join(thisDirPath,".."))
    return rootDirPath
