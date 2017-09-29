import pandas as pd
from scipy import signal
import numpy as np

class Periodogram():  #Calculates the abosulte value of the Fourier coefficients
    def process(self,data,parameters):
        Data = np.transpose(np.array(data))
        Data=np.nan_to_num(Data)

        size=Data.shape
        Pxx_den=np.zeros((size[0],int(np.ceil(np.float(size[1]+1)/np.float(2)))))

        for c in range(0,size[0]):
            [f, Pxx_den[c,:]]=signal.periodogram(Data[c,:], int(parameters))
        result=pd.DataFrame(np.transpose((Pxx_den)))
        return result

    def GetSequence(self):
        Seq=[1]
        return Seq

    def MetaInformation(self,dim_row,dim_col,parameter,OrigHeader):
        header=''
        In=np.linspace(0,dim_row-1, dim_row)/(2*dim_row)
        index=[]
        for i in range(0,dim_row):
            index.append(str(In[i]))

        return header,index
