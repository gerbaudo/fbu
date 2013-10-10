import json
import numpy as np

def array2json(a, outfname) :
    with open(outfname, 'w') as out:
        json.dump(a.tolist(), out)

def json2array(infname) :
    with open(infname) as inp:
        return np.array(json.load(inp))
