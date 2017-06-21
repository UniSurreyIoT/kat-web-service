__author__ = 'shirin'
import pandas as pd
import numpy as np
from scipy import stats


class Outlier():
    def process(self, data,parameter):
        #Winsorizing based outlier removal method
        limit=np.float(parameter)
        Data = np.transpose(np.array(data))
        size=Data.shape
        OutlierOutput=np.zeros((size[0],size[1]))
        for c in range(0,size[0]):
            OutlierOutput[c,:]=stats.mstats.winsorize(Data[c,:],limit)
        result=pd.DataFrame(np.transpose(OutlierOutput))
        return result

    def getConfigurationParams(self):
        return {"output_length":"1"}


    def GetSequence(self):
        Seq=[1,2,4,5,6,7,8,9,10,11,12,13,14]
        return Seq

    def MetaInformation(self,dim_row,dim_col,parameter,OrigHeader):
        header=''
        index=''
        return header,index