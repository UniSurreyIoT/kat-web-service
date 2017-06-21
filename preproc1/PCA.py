import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
pca = PCA()

class PCA():
    def process(self,Data,parameter):

            Data = np.array(Data)
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