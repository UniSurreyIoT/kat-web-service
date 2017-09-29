import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
pca = PCA()

class PCA():
    def process(self,Data,parameter):

            Data = np.array(Data)
            Data=np.nan_to_num(Data)

            pca.fit(Data)
            if parameter=='ExpVar':
                result=pca.explained_variance_ratio_
            elif parameter=='Comp':
                result=pca.components_  #principal component loadings.


            if not result.shape:
                result=pd.DataFrame([1])
            else:
                result=pd.DataFrame(np.array(result.astype(np.float)))
            return result

    def GetSequence(self):
        Seq=[1]
        return Seq

    def MetaInformation(self,dim_row,dim_col,parameter,OrigHeader):
        if parameter=='ExpVar':
            header=['ExplainedVariance']
            index=[]
            for i in range(0,dim_row):
                index.append('ExplainedVariance_' +str(i+1))

        elif parameter=='Comp':
            header=[]
            for i in range(0,dim_col):
                header.append('D' +str(i+1))
            index=''
        return header,index