import pandas as pd
import numpy as np
from sklearn import   linear_model

regr = linear_model.LinearRegression()


class LinReg():
    def process(self,Data,parameter):

            paramArray=  np.array(parameter.split(','))
            Data = np.transpose(np.array(Data))
            L=Data.shape
            Li=np.floor(L[1]*np.float(paramArray[2]))

            #train data
            Ytrain=Data[int(paramArray[1])-1,0:int(Li)]
            Xtemp=np.delete(Data,int(paramArray[1])-1,0)
            Xtrain=Xtemp[:,0:int(Li)]

            #test data
            Ytest=Data[int(paramArray[1])-1,int(Li):L[1]]
            Xtest=Xtemp[:,int(Li):L[1]]

            regr.fit(np.transpose(Xtrain),np.transpose(Ytrain))

            if paramArray[0]=='Param':
                result=regr.coef_
                result=pd.DataFrame(result)
            elif paramArray[0]=='Predict':
                res=np.zeros((2,len(Ytest)))
                res[0,:]=regr.predict(np.transpose(Xtest))
                res[1,:]=Ytest
                result=pd.DataFrame(np.transpose(res))

            return result

    def GetSequence(self):
        Seq=[1]
        return Seq

    def MetaInformation(self,dim_row,dim_col,parameter,OrigHeader):
        paramArray=  np.array(parameter.split(','))
        if paramArray[0]=='Param':
            header=['Coefficients']
            index=''
        elif paramArray[0]=='Predict':
            header=['Predicted '+OrigHeader[int(paramArray[1])-1],'True '+OrigHeader[int(paramArray[1])-1]]
            index=''

        return header,index