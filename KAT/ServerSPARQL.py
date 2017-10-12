from flask import Flask, request, json, jsonify
import urllib2
import pandas as pd
import numpy as np

from MultiRate import resample
import AlgorithmManager as amc
import time
import sys

from collections import Counter

if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

app = Flask(__name__)


@app.route('/AnalyseData', methods=['POST'])
def api_message():
    am=amc.AlgorithmManager()
    # json
    if request.headers['Content-Type'] == 'application/json':
        try:  # Check to see if JSON format is correct
            Requests = json.dumps(request.json)
        except:
            return jsonify(result="Incorrect JSON Format"), 400

        Requests_parsed=json.loads(Requests)

        # Collect the methods and parameters from the http request.
        try:
            Methods=Requests_parsed['Method']
            Parameters=Requests_parsed['Parameters']
            SPARQLquery=Requests_parsed['SPARQLquery']
            SPARQLendpoint=Requests_parsed['SPARQLendpoint']
        except:
            return jsonify(result="Incorrect JSON labels"), 400

        # SPARQLquery=SPARQLquery.replace("\\","")
        # SPARQLquery=SPARQLquery[:-1]

        #Collect Header information
        try:
            userIDstr = str(request.headers['userId'])
        except Exception as e:
            print(e)
            return jsonify(result="userId Header not included"), 400
        try:
            femoIdstr = str(request.headers['femoId'])
        except Exception as e:
            print(e)
            return jsonify(result="femoId Header not included"), 400
        try:
            jobIdstr=str(request.headers['jobId'])
        except Exception as e:
            print(e)
            return jsonify(result="jobId Header not included"), 400
        try:
           iPlanetDirectoryProStr =str(request.headers['iPlanetDirectoryPro'])
        except Exception as e:
            print(e)
            return jsonify(result="iPlanetDirectoryPro  Header not included"), 400

        # SPARQL query at the SPARQL end point to retreive data

        method = "POST"
        handler = urllib2.HTTPHandler()
        opener = urllib2.build_opener(handler)

        #print SPARQLquery
        # print SPARQLendpoint[0]
        try:
            request_sparql = urllib2.Request(str(SPARQLendpoint[0]), data=SPARQLquery[0])
            request_sparql.add_header("Content-Type", 'text/plain')
            request_sparql.add_header("Accept", 'text/csv')
            request_sparql.add_header("iPlanetDirectoryPro", iPlanetDirectoryProStr)
            request_sparql.get_method = lambda: method
            connection = opener.open(request_sparql, timeout=20*60)
        except Exception as e:
            print(e)
            try:
                print iPlanetDirectoryProStr
                request_sparql_backup = urllib2.Request("http://localhost:8080/iot-registry/api/queries/execute", data=SPARQLquery)
                request_sparql_backup.add_header("Accept", 'text/csv')
                request_sparql.add_header("Content-Type", 'text/plain')
                request_sparql.add_header("iPlanetDirectoryPro", iPlanetDirectoryProStr)
                request_sparql_backup.get_method = lambda: method
                connection =opener.open(request_sparql_backup, timeout=20)
            except Exception as e:
                print(e)
                Str = "Unable to connect to SPARQL endpoint"
                SaveFunction(Str, userIDstr, femoIdstr, jobIdstr)
                return jsonify(result="Unable to connect to SPARQL endpoint"), 400

        try:
            RawResponse = connection.read()
        except Exception as e:
            print(e)
            Str="Unable to retrieve data"
            SaveFunction(Str,userIDstr,femoIdstr,jobIdstr)
            return jsonify(result="Unable to retrieve data from IoT Registry"), 200
        try:
            # convert data into correct format from original SPARQL CSV format
            TESTDATA=StringIO(RawResponse)
            df = pd.read_csv(TESTDATA, sep=",")
            # print df
            ResList = list(df['sensingDevice'])
            DataV = list(df['dataValue'])
            TimeStamp = list(df['dateTime'])
            C = Counter(ResList)
            SensorUnique = C.items()
            tprev = 0             # previous time
            SensObsLen=np.zeros(len(SensorUnique))
            for i in range(0,len(SensorUnique)):
                Temp = SensorUnique[i]
                SensObsLen[i]=Temp[1]

            if min(SensObsLen) < 10:
                Str = "Length of data too small"
                SaveFunction(Str, userIDstr, femoIdstr, jobIdstr)
                return jsonify(result="Length of data too small"), 400  # if data length too short return error

            for i in range(0, len(SensorUnique)):
                Temp = SensorUnique[i]
                if i == 0:
                    tempData = [None]*max(SensObsLen)
                    tempTimeStamp = [None]*max(SensObsLen)
                    tempData[tprev:tprev+Temp[1]]=np.array(DataV[tprev:tprev+Temp[1]])
                    tempTimeStamp[tprev:tprev+Temp[1]] = TimeStamp[tprev:tprev+Temp[1]]
                    Data=pd.DataFrame(np.transpose([tempData, tempTimeStamp]), columns=[Temp[0], 'TimeStamp'+str(i+1)])
                else:
                    del tempData
                    del tempTimeStamp
                    tempData = [None]*max(SensObsLen)
                    tempTimeStamp = [None]*max(SensObsLen)
                    tempData[0:Temp[1]] = np.array(DataV[tprev:tprev+Temp[1]])
                    tempTimeStamp[0:Temp[1]] = TimeStamp[tprev:tprev+Temp[1]]
                    Data[Temp[0]] = np.transpose(tempData)
                    Data[2*i+1] = np.transpose(tempTimeStamp)
                tprev = Temp[1]+tprev
        except Exception as e:
            print(e)
            Str = "Unable to obtain data from SPARQL Query"
            SaveFunction(Str, userIDstr, femoIdstr, jobIdstr)
            return jsonify(result="Unable to obtain data from SPARQL Query"), 200

        if len(Data.iloc[1]) % 2 == 0:  # check to see if number of columns is even
            Dim = len(Data.iloc[1])/2

        else:
            Str="Either time stamp or data variable missing"
            SaveFunction(Str, userIDstr, femoIdstr, jobIdstr)
            return jsonify(result="Either time stamp or data variable missing"), 400

        HeaderNames = list(Data.columns.values)
        Header = []
        for i in range(0, len(HeaderNames)/2):
            Header.append(HeaderNames[2*i])

        # function for re-sampling the data to the lowest sampling frequency
        try:
            T1 = Data.iloc[1]
            T2 = Data.iloc[2]
            SampleFreq = np.zeros(Dim)
            for i in range(0, Dim):  # calculate sample period for each sensor
                pattern = '%Y-%m-%dT%H:%M:%S.%f'
                Temp1 = T1[2*i+1]
                Temp2 = T2[2*i+1]
                epoch1 = int(time.mktime(time.strptime(Temp1[:-1], pattern)))
                epoch2 = int(time.mktime(time.strptime(Temp2[:-1], pattern)))
                SampleFreq[i] = 1/float((epoch2-epoch1))

            RealignSamplingFreq = min(SampleFreq)  # re-sample to the lowest sampling frequency
            MinLength = min(SensObsLen)

            for i in range(0, Dim):
                DataFromSensor = list(Data.iloc[:, 2*i])
                # carry out resample of the list
                TempListDataNew = [np.float(ui) for ui in DataFromSensor]
                ResampledData = resample(np.array(TempListDataNew), 1,round(SampleFreq[i]/RealignSamplingFreq))
                MinLengthTemp = len(ResampledData)
                if i == 0:
                    DataResamp = pd.DataFrame(ResampledData[0:MinLength])
                else:
                    if MinLengthTemp < MinLength:
                        DataResamp.drop(DataResamp.index[[MinLengthTemp, MinLength]])
                        MinLength = MinLengthTemp
                    DataResamp[i] = ResampledData[0:MinLength]
        except Exception as e:
            print(e)
            Str = "Unable to Resample Data"
            SaveFunction(Str, userIDstr, femoIdstr, jobIdstr)
            return jsonify(result = "Unable to Resample Data"), 400

        #########################################################################################

        am.CollectData(Dim, DataResamp)
        # initialiase the methods to send
        N = len(Methods)
        MethodSend = ["Non","Non","Non","Non","Non","Non","Non","Non"]
        ParameterSend = [0,0,0,0,0,0,0,0]

        if len(Methods) == len(Parameters):
            for item in range(0, N):
                MethodSend[item] = Methods[item]
                ParameterSend[item] = Parameters[item]
                # Max number of methods 8
            am.CollectMethods(MethodSend[0], MethodSend[1], MethodSend[2], MethodSend[3], MethodSend[4], MethodSend[5], MethodSend[6], MethodSend[7])
            am.CollectParameters(ParameterSend[0], ParameterSend[1], ParameterSend[2], ParameterSend[3], ParameterSend[4], ParameterSend[5], ParameterSend[6], ParameterSend[7])
            FLagMethodNames = am.CheckMethodNames()  # Check if method names are valid
            if int(FLagMethodNames[0]) > 0:
                ErrorString = 'Incorrect Method Name: ' + MethodSend[int(FLagMethodNames[0])-1]
                Str = ErrorString
                SaveFunction(Str, userIDstr, femoIdstr, jobIdstr)
                return jsonify(result=ErrorString), 400
            FlagSequence = am.CheckTechniqueSequence()
            if int(FlagSequence[0]) == 0:  # Error due to incorrect parameters.
                am.LastMethod(MethodSend)
                Output = am.Main()
                try:
                    Output = am.MetaInformation(Header, Output)
                except:
                    Str = "Error"
                    SaveFunction(Str, userIDstr, femoIdstr, jobIdstr)
                    return jsonify(result="Error"), 400
                if Output is None:
                    Str = "Incorrect Method Parameter Specification"
                    SaveFunction(Str, userIDstr, femoIdstr, jobIdstr)
                    return jsonify(result="Incorrect Method Parameter Specification"), 400
                else:
                    OutputCSV = Output.to_csv(index=True, header=True)
                    Out = {"result": OutputCSV}
                    '''try:
                        reqStore = urllib2.Request('https://localhost:8080/experiment-result-store/')  #storage url will change.
                        reqStore.add_header('Content-Type', 'application/json')
                        reqStore.add_header('userId', userIDstr)
                        reqStore.add_header('femoId', femoIdstr)
                        reqStore.add_header('jobId', jobIdstr)
                        response = urllib2.urlopen(reqStore, json.dumps(Out),timeout=60)

                    except:
                        return jsonify(result=["Unable to store/or confirm storage of processed data"]),400'''

                    # return jsonify(result=[])
                    # return jsonify(result=["Data Processed"]),200
                    return jsonify(Out),200
            else:
                Str="Incorrect Sequence of Methods"
                SaveFunction(Str,userIDstr,femoIdstr,jobIdstr)
                return jsonify(result="Incorrect Sequence of Methods"),400
        else: return jsonify(result="No. of parameters not equal to the No. of methods"),400
    else:
        return jsonify(result="Content In the Incorrect Format"),400
'''
@app.route('/AnalysedDataRetrieval/<path:filename>', methods=['GET', 'POST'])
def download_file(filename):
    uploads = os.path.join(app.root_path, app   .config['UPLOAD_FOLDER'])
    return send_from_directory(uploads,filename)#, delete(uploads,filename)
'''


def SaveFunction(Str, userIDstr, femoIdstr, jobIdstr):
    try:
        Out = {"result": Str}
        reqStore = urllib2.Request('https://localhost:8080/experiment-result-store/')  # storage url will change.
        reqStore.add_header('Content-Type', 'application/json')
        reqStore.add_header('userId', userIDstr)
        reqStore.add_header('femoId', femoIdstr)
        reqStore.add_header('jobId', jobIdstr)
        response = urllib2.urlopen(reqStore,json.dumps(Out), timeout=60)

    except:
        return jsonify(result=["Unable to store/or confirm storage of processed data"]), 400
    return
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("8081"), debug=True)
    # app.run(debug=True)
