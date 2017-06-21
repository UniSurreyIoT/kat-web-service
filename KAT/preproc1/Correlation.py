import pandas as pd
import numpy as np

class Correlation():
    def process(self,Data,parameter):
            Data = np.transpose(np.array(Data))
            result=np.corrcoef(Data)
            if not result.shape:
                result=pd.DataFrame([1])
            else:
                result=pd.DataFrame(np.array(result.astype(np.float)))
            return result

    def GetSequence(self):
        Seq=[1]
        return Seq

    def MetaInformation(self,dim_row,dim_col,parameter,OrigHeader):

        header=''
        index=OrigHeader
        return header,index