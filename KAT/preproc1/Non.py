__author__ = 'shirin'
import pandas as pd

class Non():
    def process(self, data,output_length):

        result=data
        return result

    def getConfigurationParams(self):
        return {"output_length":"1"}

    def GetSequence(self):
        Seq=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        return Seq

    def MetaInformation(self,dim_row,dim_col,parameter,header):
        header=''
        index=''
        return header,index