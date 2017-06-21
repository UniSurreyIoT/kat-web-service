__author__ = 'shirin'

import numpy as np
from scipy.stats import norm
import string
import bottleneck as bn
import math
import pandas as pd
# paa tranformation, window = incoming data, string_length = length of outcoming data

class Paa():
    def process(self, data, output_length):
        data = np.array(data)
        data = np.array_split(data, int(output_length))
        result = []
        for section in data:
            if math.isnan(bn.nanmean(section)):
                result.append(0)
            else:
                result.append(bn.nanmean(section))
        result = np.array(result)
        result=pd.DataFrame((result))

        print "paa output shape", result.shape
        return result

    #def getConfigurationParams(self):
        #return {"output_length":"100"}