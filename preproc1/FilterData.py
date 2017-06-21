import pandas as pd
from scipy import signal
import numpy as np

class FilterData():
    def process(self,data,parameters):

        if parameters[0]=='B':   #Bandpass Filter
            if np.array(parameters.split(',')).size==4:

                #Estimate Filter coefficients
                parameter=np.array(parameters.split(','))
                p=np.array(parameter)
                n= int(p[3])
                a = signal.firwin(n, 2*np.float(p[1]))
                b = - signal.firwin(n, 2*np.float(p[2])); b[n/2] = b[n/2] + 1
                d = - (a+b)
                d[n/2] = d[n/2] + 1
                w1, FilterCoef=signal.freqz(d)
                FilterCoefLength= FilterCoef.size

                #Filter Data with estimated coefficients
                Data = np.transpose(np.array(data))
                size=Data.shape
                FilteredData=np.zeros((size[0],size[1]))

                for c in range(0,size[0]):
                    FilteredData[c,:]=signal.lfilter(d,1,Data[c,:])
                result=pd.DataFrame(np.transpose((FilteredData)))
            else:
                result=np.zeros(1000)
                result=pd.DataFrame(np.transpose((result)))


        if parameters[0]=='L':   #LowPass Filter
            if np.array(parameters.split(',')).size==4:

                #Estimate Filter coefficients
                parameter=np.array(parameters.split(','))
                p=np.array(parameter)
                n= int(p[3])
                a = signal.firwin(n, 2*np.float(p[1]))
                w1, FilterCoef=signal.freqz(a)
                FilterCoefLength= FilterCoef.size

                #Filter Data with estimated coefficients
                Data = np.transpose(np.array(data))
                size=Data.shape
                FilteredData=np.zeros((size[0],size[1]))
                for c in range(0,size[0]):
                    FilteredData[c,:]=signal.lfilter(a,1,Data[c,:])
                result=pd.DataFrame(np.transpose((FilteredData)))
            else:
                result=np.zeros(1000)
                result=pd.DataFrame(np.transpose((result)))

        if parameters[0]=='H':   #Highpass Filter
            if np.array(parameters.split(',')).size==4:

                #Estimate Filter coefficients
                parameter=np.array(parameters.split(','))
                p=np.array(parameter)
                n= int(p[3])
                b = - signal.firwin(n, 2*np.float(p[1])); b[n/2] = b[n/2] + 1
                w1, FilterCoef=signal.freqz(b)
                FilterCoefLength= FilterCoef.size

                #Filter Data with estimated coefficients
                Data = np.transpose(np.array(data))
                size=Data.shape
                FilteredData=np.zeros((size[0],size[1]))

                for c in range(0,size[0]):
                    FilteredData[c,:]=signal.lfilter(b,1,Data[c,:])
                result=pd.DataFrame(np.transpose((FilteredData)))
            else:
                result=np.zeros(1000)
                result=pd.DataFrame(np.transpose((result)))

        return result

    def GetSequence(self):
        Seq=[1,2,4,5,6,7,8,9,10,12,13,14]
        return Seq

    def MetaInformation(self,dim_row,dim_col,parameter,OrigHeader):
        header=''
        index=''
        return header,index