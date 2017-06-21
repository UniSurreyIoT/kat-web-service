from flask import Flask, request, json, url_for, redirect, send_from_directory, send_file
import random, httplib, urllib, os, urllib2, csv, uuid
import pandas as pd
import numpy as np
from MultiRate import resample
#from PyQt4 import QtCore, QtGui
import AlgorithmManager as amc
app = Flask(__name__)
import  datetime, time
UPLOAD_FOLDER = os.path.expanduser('~') + '/Desktop/DA_GUI/untitled1/Flask/preproc1/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.run(host="127.0.0.1", port=int("80"), debug=True)


@app.route('/AnalyseData', methods = ['POST'])
def api_message():
    am=amc.AlgorithmManager()
    ###json
    if request.headers['Content-Type'] == 'application/json'  :
        try:  #Check to see if JSON format is correct
            Requests = json.dumps(request.json)
        except:
            return 'Error: Incorrect JSON Format'
        Requests_parsed=json.loads(Requests)

        # Collect the methods and parameters from the http request.
        try:
            Methods=Requests_parsed['Method']
            Parameters=Requests_parsed['Parameters']
            DataPointer=Requests_parsed['DataPointer']
        except:
            return 'Error: Incorrect JSON labels'

        #Connect to data and collect the csv data.
        try:  #check if data link is a valid URL
            Data = pd.read_csv(DataPointer[0])
        except:
            return 'Error: Incorrect Data Link'

        if (len(Data.iloc[1]) % 2 == 0):  #check to see if number of coluns is even
            Dim=len(Data.iloc[1])/2
        else:
            return 'Error: either time stamp or data variable missing '



        HeaderNames= list(Data.columns.values)
        Header=[]
        for i in range(0,len(HeaderNames)/2):
            Header.append(HeaderNames[2*i])


        ###############function for resampling the data to the lowest sampling frequency
        T1=Data.iloc[1]
        T2=Data.iloc[2]
        SampleFreq=np.zeros(Dim)
        for i in range(0,Dim): #calcaulate sample period for each sensor
            pattern = '%Y-%m-%dT%H:%M:%S'
            epoch1 = int(time.mktime(time.strptime(T1[2*i+1], pattern)))
            epoch2 = int(time.mktime(time.strptime(T2[2*i+1], pattern)))
            SampleFreq[i]=1/float((epoch2-epoch1))

        RealignSamplingFreq= min(SampleFreq) #resample to the lowest sampling frequency
        for i in range(0,Dim):
            DataFromSensor=list(Data.iloc[:,2*i])
            count=0
            st=0
            while count<len(Data) and st==0:
                if str(DataFromSensor[count])=="nan":
                    st=1
                count=count+1
            if count==len(DataFromSensor):
                TempListData=DataFromSensor[0:count]
            else:
                TempListData=DataFromSensor[0:count-1]   #Data from each observation extracted along each sensor and time interval

            #carry out resample of the list
            k= np.array(TempListData)
            ResampledData= resample(np.array(TempListData), 1,round(SampleFreq[i]/RealignSamplingFreq))
            if i==0:
                DataResamp=pd.DataFrame(ResampledData)
            else:
                DataResamp[i]=ResampledData

        #########################################################################################

        am.CollectData(Dim,DataResamp)
        #initialiase the methods to send
        N=len(Methods)
        MethodSend=["Non","Non","Non","Non","Non","Non","Non","Non"]
        ParameterSend=[0,0,0,0,0,0,0,0]

        if len(Methods)==len(Parameters):
            for item in range(0,N):
                MethodSend[item]=Methods[item]
                ParameterSend[item]=Parameters[item]
                #Max number of methods 8
            am.CollectMethods(MethodSend[0],MethodSend[1],MethodSend[2],MethodSend[3],MethodSend[4],MethodSend[5],MethodSend[6],MethodSend[7])
            am.CollectParameters(ParameterSend[0],ParameterSend[1],ParameterSend[2],ParameterSend[3],ParameterSend[4],ParameterSend[5],ParameterSend[6],ParameterSend[7])
            FLagMethodNames=am.CheckMethodNames() #Check if method names are valid
            if int(FLagMethodNames[0])>0:
                return 'Error: Incorrect Method Name: '  +  MethodSend[int(FLagMethodNames[0])-1]
            FlagSequence=am.CheckTechniqueSequence()
            if int(FlagSequence[0])==0:  #Error due to incorrect parameters.
                am.LastMethod(MethodSend)
                Output = am.Main()
                try:
                    Output = am.MetaInformation(Header,Output)
                except:
                    return 'Error'
                if Output is None:
                    return 'Error: In parameters, please consult documentation '
                else:
                    OutputCSV= Output.to_csv(index=True,header=True)
                    return OutputCSV
            else:
                return 'Error: Incorrect Sequence of Methods'
        else: return 'Error: No. of parameters not equal to the No. of methods'
    else:
        return 'Error: Content In the Incorrect Format'
'''
@app.route('/AnalysedDataRetrieval/<path:filename>', methods=['GET', 'POST'])
def download_file(filename):
    uploads = os.path.join(app.root_path, app   .config['UPLOAD_FOLDER'])
    return send_from_directory(uploads,filename)#, delete(uploads,filename)
'''


if __name__ == "__main__":
    #app.run(host="127.0.0.1", port=int("80"), debug=True)
    app.run()