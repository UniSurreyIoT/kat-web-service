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
    def process(self,data,parameter):

            paramArray=  np.array(parameter.split(','))
            clusterSize=paramArray[0]
            Data = np.array(data)
            size=Data.shape
            kmeans = KMeans(int(clusterSize))
            kmeans.fit(Data)
            labels = kmeans.labels_
            centers=kmeans.cluster_centers_
            if paramArray[1]=='CL':
                result=pd.DataFrame(np.transpose(labels))
            elif paramArray[1]=='Cent':
                result=pd.DataFrame(centers)
            return result

    def GetSequence(self):
        Seq=[1]
        return Seq

    def MetaInformation(self,dim_row,dim_col,parameter,OrigHeader):
        paramArray=  np.array(parameter.split(','))
        if paramArray[1]=='CL':
            header=['Cluster_Label']
            index=''
        elif paramArray[1]=='Cent':
            header=[]
            for i in range(0,dim_col):
                header.append('D' +str(i+1))
            index=[]
            for i in range(0,dim_row):
                index.append('Cluster ' +str(i))

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

