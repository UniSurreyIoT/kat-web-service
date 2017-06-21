import pandas as pd
import numpy as np

class FFT():  #Calculates the abosulte value of the Fourier coefficients
    def process(self,data,input):
        Data = np.transpose(np.array(data))
        size=Data.shape
        #FFTOutput=np.zeros((size[0],size[1]))
        FFTOutput=np.zeros((size[0],int(np.ceil(np.float(size[1]+1)/np.float(2)))))
        Temp=[]
        for c in range(0,size[0]):
            #FFTOutput[c,:]=np.abs(np.fft.fft(Data[c,:]))
            Temp=np.abs(np.fft.fft(Data[c,:]-np.mean(Data[c,:])))
            FFTOutput[c,:]=Temp[0:int(np.ceil(np.float(size[1]+1)/np.float(2)))]

        result=pd.DataFrame(np.transpose(FFTOutput))
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
