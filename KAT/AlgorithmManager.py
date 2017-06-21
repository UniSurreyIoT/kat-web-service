import preproc1.Clean
import preproc1.Correlation
import preproc1.FFT
import preproc1.FilterData
import preproc1.KNN
import preproc1.LinReg
import preproc1.Non
import preproc1.Outlier
import preproc1.PCA
import preproc1.Periodogram
import preproc1.SAX
import preproc1.kmeans


#import SpectralEstimation.FFT.py
from scipy import signal
import sys
#import preproc1.Paa
#import preproc1.corrM
import numpy as np

class AlgorithmManager():

    def __init__(self):
        self.algorithms = {"KNNreg":"KNN","LinReg":"LinReg","PCA":"PCA","FilterData":"FilterData","Periodogram":"Periodogram","FFT":"FFT","Correlation":"Correlation","Kmeans":"kmeans","SAX":"SAX","PAA":"Paa",
                           "Znorm":"Znorm","Outlier":"Outlier","Clean":"Clean","Non":"Non"}
        self.Seq={"KNNreg":"14","LinReg":"13","PCA":"12","FilterData":"11","Periodogram":"10","FFT":"9","Correlation":"8","Kmeans":"7","SAX":" 6","PAA":"5",
                           "Znorm":"4","Outlier":"3","Clean":"2","Non":"1"}

    #Selects the appropriate algorithm based on the users input
    def Main(self):
        try:
            ComboBox_1 = getattr(getattr(preproc1,self.algorithms[self.method_1]), self.algorithms[self.method_1])()
            self.Output=ComboBox_1.process(self.Data,self.param_1)
        except:
            return None
        try:
            ComboBox_2 = getattr(getattr(preproc1,self.algorithms[self.method_2]), self.algorithms[self.method_2])()
            self.Output=ComboBox_2.process(self.Output,self.param_2)
        except:
            return None
        try:
            ComboBox_3 = getattr(getattr(preproc1,self.algorithms[self.method_3]), self.algorithms[self.method_3])()
            self.Output=ComboBox_3.process(self.Output,self.param_3)
        except:
            return None
        try:
            ComboBox_4 = getattr(getattr(preproc1,self.algorithms[self.method_4]), self.algorithms[self.method_4])()
            self.Output=ComboBox_4.process(self.Output,self.param_4)
        except:
            return None
        try:
            ComboBox_5 = getattr(getattr(preproc1,self.algorithms[self.method_5]), self.algorithms[self.method_5])()
            self.Output=ComboBox_5.process(self.Output,self.param_5)
        except:
            return None
        try:
            ComboBox_6 = getattr(getattr(preproc1,self.algorithms[self.method_6]), self.algorithms[self.method_6])()
            self.Output=ComboBox_6.process(self.Output,self.param_6)
        except:
            return None
        try:
            ComboBox_7 = getattr(getattr(preproc1,self.algorithms[self.method_7]), self.algorithms[self.method_7])()
            self.Output=ComboBox_7.process(self.Output,self.param_7)
        except:
            return None
        try:
            ComboBox_8 = getattr(getattr(preproc1,self.algorithms[self.method_8]), self.algorithms[self.method_8])()
            self.Output=ComboBox_8.process(self.Output,self.param_8)
        except:
            return None
        return self.Output

    #Collect the data set from the main window
    def CollectData(self,DataDimension,Data):
        self.Data=Data
        self.DataDimension=DataDimension

    #Collect methods from drop down menus
    def CollectMethods(self,Meth_1,Meth_2,Meth_3,Meth_4,Meth_5,Meth_6,Meth_7,Meth_8):
        self.method_1=str(Meth_1)
        self.method_2=str(Meth_2)
        self.method_3=str(Meth_3)
        self.method_4=str(Meth_4)
        self.method_5=str(Meth_5)
        self.method_6=str(Meth_6)
        self.method_7=str(Meth_7)
        self.method_8=str(Meth_8)

    #Collect Corresponding Parameters
    def CollectParameters(self,Param_1,Param_2,Param_3,Param_4,Param_5,Param_6,Param_7,Param_8):
        self.paramappend=[]
        self.param_1=str(Param_1)
        self.paramappend.append(self.param_1)
        self.param_2=str(Param_2)
        self.paramappend.append(self.param_2)
        self.param_3=str(Param_3)
        self.paramappend.append(self.param_3)
        self.param_4=str(Param_4)
        self.paramappend.append(self.param_4)
        self.param_5=str(Param_5)
        self.paramappend.append(self.param_5)
        self.param_6=str(Param_6)
        self.paramappend.append(self.param_6)
        self.param_7=str(Param_7)
        self.paramappend.append(self.param_7)
        self.param_8=str(Param_8)
        self.paramappend.append(self.param_8)

    #Check to see if the correct sequence of methods is used
    def CheckTechniqueSequence(self):
        ComboBox_1 = getattr(getattr(preproc1,self.algorithms[self.method_1]), self.algorithms[self.method_1])()
        self.Sequence=ComboBox_1.GetSequence()
        Temp= np.where(self.Sequence-np.array(int(self.Seq[self.method_2])) == 0)[0]
        if len(Temp)==0:
            return '2'
        ComboBox_2 = getattr(getattr(preproc1,self.algorithms[self.method_2]), self.algorithms[self.method_2])()
        self.Sequence=ComboBox_2.GetSequence()
        Temp= np.where(self.Sequence-np.array(int(self.Seq[self.method_3])) == 0)[0]
        if len(Temp)==0:
            return '3'
        ComboBox_3 = getattr(getattr(preproc1,self.algorithms[self.method_3]), self.algorithms[self.method_3])()
        self.Sequence=ComboBox_3.GetSequence()
        Temp= np.where(self.Sequence-np.array(int(self.Seq[self.method_4])) == 0)[0]
        if len(Temp)==0:
            return '4'
        ComboBox_4 = getattr(getattr(preproc1,self.algorithms[self.method_4]), self.algorithms[self.method_4])()
        self.Sequence=ComboBox_4.GetSequence()
        Temp= np.where(self.Sequence-np.array(int(self.Seq[self.method_5])) == 0)[0]
        if len(Temp)==0:
            return '5'
        ComboBox_5 = getattr(getattr(preproc1,self.algorithms[self.method_5]), self.algorithms[self.method_5])()
        self.Sequence=ComboBox_5.GetSequence()
        Temp= np.where(self.Sequence-np.array(int(self.Seq[self.method_6])) == 0)[0]
        if len(Temp)==0:
            return '6'
        ComboBox_6 = getattr(getattr(preproc1,self.algorithms[self.method_6]), self.algorithms[self.method_6])()
        self.Sequence=ComboBox_6.GetSequence()
        Temp= np.where(self.Sequence-np.array(int(self.Seq[self.method_7])) == 0)[0]
        if len(Temp)==0:
            return '7'
        ComboBox_7 = getattr(getattr(preproc1,self.algorithms[self.method_7]), self.algorithms[self.method_7])()
        self.Sequence=ComboBox_7.GetSequence()
        Temp= np.where(self.Sequence-np.array(int(self.Seq[self.method_8])) == 0)[0]
        if len(Temp)==0:
            return '8'
        return '0'

    #Check to see if method names are correct
    def CheckMethodNames(self):
        try:
            self.algorithms[self.method_1]
        except KeyError:
            return '1'
        try:
            self.algorithms[self.method_2]
        except KeyError:
            return '2'
        try:
            self.algorithms[self.method_3]
        except KeyError:
            return '3'
        try:
            self.algorithms[self.method_4]
        except KeyError:
            return '4'
        try:
            self.algorithms[self.method_5]
        except KeyError:
            return '5'
        try:
            self.algorithms[self.method_6]
        except KeyError:
            return '6'
        try:
            self.algorithms[self.method_7]
        except KeyError:
            return '7'
        try:
            self.algorithms[self.method_8]
        except KeyError:
            return '8'
        return '0'



    def LastMethod(self,MethodList):  #obtain the last selected method, along with the position
        self.count=0
        for Method in MethodList:
            if Method!='Non':
                self.LastMethodOut=Method
                self.count=self.count+1
        if self.count==0:
            self.LastMethodOut='Non'
        return None




    def MetaInformation(self,OriginalHeader,Data):    #add information regarding the labels of the processed data
        SelfFinalMethod = getattr(getattr(preproc1,self.algorithms[self.LastMethodOut]), self.algorithms[self.LastMethodOut])()
        dimension= Data.shape
        header,index=SelfFinalMethod.MetaInformation(dimension[0],dimension[1],self.paramappend[self.count-1],OriginalHeader)

        if header=='':
            Data.columns=OriginalHeader
        else:
            Data.columns=header

        if index=='':
            None
        else:
            Data.index=index
        return Data