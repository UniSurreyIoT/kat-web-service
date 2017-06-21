__author__ = 'shirin'
import time

import numpy as np
#import pylab as pl
import pandas as pd
from sklearn.cluster import MiniBatchKMeans, KMeans
#from PyQt4 import QtCore, QtGui
#from scipy.cluster.vq import kmeans2
#from src.MainGUI import Ui_Form

class kmeans():
    def process(self,data,clusterSize):
            Data = np.array(data)
            size=Data.shape
            kmeans = KMeans(int(clusterSize))
            kmeans.fit(Data)
            labels = kmeans.labels_
            result=pd.DataFrame(np.transpose(labels))
            return result

    def GetSequence(self):
        Seq=[1]
        return Seq

    def MetaInformation(self,dim_row,dim_col,parameter,OrigHeader):
        header=['Cluster Label']
        index=''
        return header,index








'''
            result=[]
            kmeans = KMeans(int(clusterSize))
            result_in=pd.DataFrame(index=data.index,columns=data.columns)
            data=pd.DataFrame(data)
            for i in range(data.columns.size):
                x=pd.DataFrame(data.iloc[:,i])
                kmeans.fit(x)
                labels = kmeans.labels_
                result_in.iloc[:,i]=labels
            #msgBox = QtGui.QMessageBox()
            #msgBox.setText('Cluster center for the selected channels: '+str(kmeans.cluster_centers_))
            #msgBox.setWindowTitle ('Inofrmation!' )
            #msgBox.exec_()
            return result_in
            #TODO I added the clusterer as return value will not work with GUI

    def getConfigurationParams(self):
        return {"clusterSize":"2"}
        '''

