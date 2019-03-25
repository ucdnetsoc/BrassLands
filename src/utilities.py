import os

def RootGameDirectory():
    thisDirPath = os.path.dirname(os.path.realpath(__file__))
    rootDirPath = os.path.abspath(os.path.join(thisDirPath,".."))
    return rootDirPath


def get_path(string):
    return os.path.join(RootGameDirectory(), string)
