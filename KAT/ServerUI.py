from flask import Flask, request, json, url_for, redirect, send_from_directory, send_file,jsonify,abort,render_template
import random, httplib, urllib, os, urllib2, csv, uuid
import pandas as pd
import numpy as np
from MultiRate import resample
#from PyQt4 import QtCore, QtGui
import AlgorithmManager as amc
import werkzeug.exceptions as ex
app = Flask(__name__)
import  datetime, time
UPLOAD_FOLDER = os.path.expanduser('~') + '/Desktop/DA_GUI/untitled1/Flask/preproc1/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.run(host="127.0.0.1", port=int("80"), debug=True)
import sys
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO
from collections import Counter


@app.route('/analytics-toolkit')
def root1():

    return render_template('KAT_index.html')


@app.route('/analytics-toolkit/results', methods = ['POST'])
def api_message():
        am=amc.AlgorithmManager()
    ###json
        data= request.form
        try:  #Check to see if JSON format is correct
                method1=str(data['method1'])
                method2=str(data['method2'])
                method3=str(data['method3'])
                method4=str(data['method4'])
                parameter1=str(data['parameter1'])
                parameter2=str(data['parameter2'])
                parameter3=str(data['parameter3'])
                parameter4=str(data['parameter4'])
                SPARQLquery=str(data['myTextBox2'])
        except:
                return render_template('KAT_index.html', Result="Incorrect JSON Format")

        try:
            Methods=[method1,method2,method3,method4]
            Parameters=[parameter1,parameter2,parameter3,parameter4]
        except:
            return  render_template('KAT_index.html', Result="Incorrect JSON Labels")




        #SPARQL query at the SPARQL end point to retreive data
        method = "POST"
        handler = urllib2.HTTPHandler()
        opener = urllib2.build_opener(handler)

        iPlanetDirectoryProStr="AQIC5wM2LY4SfcyR8RgVHVfeuigA_rC4XbuiNHxc83yhug4.*AAJTSQACMDEAAlNLABMxMDcwOTI2MDg3MTM4MzQ1MjYzAAJTMQAA*"
        SPARQLendpoint="http://localhost:8080/iot-registry/api/queries/execute/global"

        try:
            request_sparql = urllib2.Request(SPARQLendpoint, data=SPARQLquery)
            request_sparql.add_header("Accept", 'text/csv')
            request_sparql.add_header("Content-Type", 'text/plain')
            # request_sparql.add_header("iPlanetDirectoryPro", iPlanetDirectoryProStr)
            request_sparql.get_method = lambda: method
            connection = opener.open(request_sparql, timeout=20*60)
        except:
            try:
                request_sparql_backup = urllib2.Request("http://localhost:8080/iot-registry/api/queries/execute/global", data=SPARQLquery)
                request_sparql_backup.add_header("Accept", 'text/csv')
                request_sparql.add_header("Content-Type", 'text/plain')
                request_sparql.add_header("iPlanetDirectoryPro", iPlanetDirectoryProStr)
                request_sparql_backup.get_method = lambda: method
                connection =opener.open(request_sparql_backup, timeout=20)
            except:
                Str="Unable to connect to SPARQL endpoint"
                return render_template('KAT_index.html',Result=Str)

                #return jsonify(result=[]),400

        try:
            RawResponse = connection.read()
            print RawResponse
        except:
            Str="Unable to retrieve data"
            return render_template('KAT_index.html',Result=Str)
        try:
        #####  convert data into correct format from original SPARQL CSV format
            TESTDATA=StringIO(RawResponse)
            df = pd.read_csv(TESTDATA, sep=",")
            ResList = list(df['sensingDevice'])
            DataV = list(df['dataValue'])
            TimeStamp = list(df['dateTime'])
            C = Counter(ResList)
            SensorUnique = C.items()
            tprev = 0             #previous time
            SensObsLen=np.zeros(len(SensorUnique))
            for i in range(0,len(SensorUnique)):
                Temp = SensorUnique[i]
                SensObsLen[i]=Temp[1]
            if min(SensObsLen)<1:
                Str="Length of data too small"
                return render_template('KAT_index.html',Result=Str)  #if data length too short return error

            for i in range(0,len(SensorUnique)):
                Temp=SensorUnique[i]
                if i==0:
                    tempData = [None]*max(SensObsLen)
                    tempTimeStamp = [None]*max(SensObsLen)
                    tempData[tprev:tprev+Temp[1]]=np.array(DataV[tprev:tprev+Temp[1]])
                    tempTimeStamp[tprev:tprev+Temp[1]] =TimeStamp[tprev:tprev+Temp[1]]
                    Data = pd.DataFrame(np.transpose([tempData,tempTimeStamp]), columns=[Temp[0], 'TimeStamp'+str(i+1)])
                else:
                    print "hello"
                    del tempData
                    del tempTimeStamp
                    tempData=[None]*max(SensObsLen)
                    tempTimeStamp=[None]*max(SensObsLen)
                    tempData[0:Temp[1]]=np.array(DataV[tprev:tprev+Temp[1]])
                    tempTimeStamp[0:Temp[1]] =TimeStamp[tprev:tprev+Temp[1]]
                    Data[Temp[0]] = np.transpose(tempData)
                    Data[2*i+1]=np.transpose(tempTimeStamp)
                tprev=Temp[1]+tprev        ####
        except:
            Str = "Unable to obtain data from SPARQL Query"
            return render_template('KAT_index.html',Result=Str)

        if (len(Data.iloc[1]) % 2 == 0):  #check to see if number of coluns is even
            Dim=len(Data.iloc[1])/2

        else:
            Str="Either time stamp or data variable missing"
            return render_template('KAT_index.html',Result=Str)


        HeaderNames= list(Data.columns.values)
        Header=[]
        for i in range(0,len(HeaderNames)/2):
            Header.append(HeaderNames[2*i])


        ###############function for resampling the data to the lowest sampling frequency
        try:
            T1=Data.iloc[1]
            T2=Data.iloc[2]
            SampleFreq=np.zeros(Dim)
            for i in range(0,Dim): #calcaulate sample period for each sensor
                pattern = '%Y-%m-%dT%H:%M:%S'
                Temp1=T1[2*i+1]
                Temp2=T2[2*i+1]
                epoch1 = int(time.mktime(time.strptime(Temp1[:-1], pattern)))
                epoch2 = int(time.mktime(time.strptime(Temp2[:-1], pattern)))
                SampleFreq[i]=1/float((epoch2-epoch1))


            RealignSamplingFreq= min(SampleFreq) #resample to the lowest sampling frequency
            MinLength=min(SensObsLen)

            for i in range(0,Dim):
                DataFromSensor=list(Data.iloc[:,2*i])
                #carry out resample of the list
                TempListDataNew=[np.float(ui) for ui in DataFromSensor]
                ResampledData= resample(np.array(TempListDataNew), 1,round(SampleFreq[i]/RealignSamplingFreq))
                MinLengthTemp=len(ResampledData)
                if i==0:
                    DataResamp=pd.DataFrame(ResampledData[0:MinLength])
                else:
                    if MinLengthTemp<MinLength:
                        DataResamp.drop(DataResamp.index[[MinLengthTemp,MinLength]])
                        MinLength=MinLengthTemp
                    DataResamp[i]=ResampledData[0:MinLength]
        except:
            Str="Unable to Resample Data"
            return render_template('KAT_index.html',Result=Str)

        #########################################################################################
        print 'hello'
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
                ErrorString='Incorrect Method Name: '  +  MethodSend[int(FLagMethodNames[0])-1]
                Str=ErrorString
                return render_template('KAT_index.html',Result=Str)
            FlagSequence=am.CheckTechniqueSequence()
            if int(FlagSequence[0])==0:  #Error due to incorrect parameters.
                am.LastMethod(MethodSend)
                Output = am.Main()
                try:
                    Output = am.MetaInformation(Header,Output)
                except:
                    Str="Error"
                    return render_template('KAT_index.html',Result=Str)
                if Output is None:
                    Str="Incorrect Method Parameter Specification"
                    return render_template('KAT_index.html',Result=Str)
                else:
                    OutputCSV= Output.to_csv(index=True,header=True)
                    '''try:
                        reqStore = urllib2.Request('https://localhost:8080/experiment-result-store/')  #storage url will change.
                        reqStore.add_header('Content-Type', 'application/json')
                        reqStore.add_header('userId', userIDstr)
                        reqStore.add_header('femoId', femoIdstr)
                        reqStore.add_header('jobId', jobIdstr)
                        response = urllib2.urlopen(reqStore, json.dumps(Out),timeout=60)

                    except:
                        return jsonify(result=["Unable to store/or confirm storage of processed data"]),400'''

                    #return jsonify(result=[])
                    #return jsonify(result=["Data Processed"]),200
                  #  htmlcode = HTML.table(table_data)
                    return render_template('KAT_index.html',Result=OutputCSV)
            else:
                Str="Incorrect Sequence of Methods"
                return render_template('KAT_index.html',Result=Str)
        else: return render_template('KAT_index.html',Result="No. of parameters not equal to the No. of methods")

'''
@app.route('/AnalysedDataRetrieval/<path:filename>', methods=['GET', 'POST'])
def download_file(filename):
    uploads = os.path.join(app.root_path, app   .config['UPLOAD_FOLDER'])
    return send_from_directory(uploads,filename)#, delete(uploads,filename)
'''
def SaveFunction(Str,userIDstr,femoIdstr,jobIdstr):
    try:
        Out={"result": Str}
        reqStore = urllib2.Request('https://localhost:8080/experiment-result-store/')  #storage url will change.
        reqStore.add_header('Content-Type', 'application/json')
        reqStore.add_header('userId', userIDstr)
        reqStore.add_header('femoId', femoIdstr)
        reqStore.add_header('jobId', jobIdstr)
        response = urllib2.urlopen(reqStore,json.dumps(Out),timeout=60)

    except:
        return jsonify(result=["Unable to store/or confirm storage of processed data"]), 400
    return
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5001"), debug=True)
    # app.run()
