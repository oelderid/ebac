import pickle
import os

def write_object(file: str, obj):
    with open(os.getcwd() + '/dataset/' + file, 'wb') as fp:
        pickle.dump(obj, fp)

def read_object(file: str):
    with open(os.getcwd() + '/dataset/' + file, 'rb') as fp:
        return pickle.load(fp)