# FIESTA-IoT Analytics  

## Table of Contents  

[TOC]

## Introduction  

In order to maximise the added value of the data being extracted from FIESTA-IoT testbeds for the experimenter, it is important to provide data analysis tools and service. As a result, an analytics web service based on the Knowledge Acquisition Toolkit (KAT) is being developed for FIESTA-IoT in order to provide open access data analysis tools for data consumers as a web service. Such a tool provides the following benefits: namely for novice/beginner data consumer, the tools that would enable them to analyse and obtain useful information. While for the more advanced/experienced user providing the most effective tools for a given data set.  

For example, such a tool would provide relevant documentation for the beginner data consumer, with examples of data processing work flows; while for the more experienced user the most advanced tools developed in academic institutions can be evaluated by a wide range of users and the most useful data analysis tool for a given data set will be identified. Furthermore, by providing data analysis as a web service, FIESTA-IoT enables a wider range of experimenters to access the FIESTA-IoT platform.  

## Background on Data Analysis methods  

### Data Pre-Processing Techniques  
These techniques involve the removal of corrupted or noisy data points from the original raw time series data. There 2 methods that are available through KAT.

- **Digital Filtering** – A finite impulse response (FIR) filter, for lowpass, bandpass and highpass filtering. 
  - That is, the removal of low frequencies (low-pass filtering), between a range of frequencies (band-pass filtering) and the removal of high frequency components (high-pass filtering). 
  - This method is important for the removal of unwanted signal components that corrupt the desired signal. 
  - It should be noted that the user would need to define the type of filtering required (that is lowpass, bandpass etc.) as well as providing the frequency ranges they require to remove.  
- **Outlier Removal** –  an outlier tool that is based on winsorization. 
  - Many machine learning algorithms are sensitive to outliers. 
  - The performance of the methods degrade as the number of outliers increases. 
  - With the tool, the user defines only one parameter that is the percentage of from the highest and lowest value in the data set is clipped.  

### Machine Learning Techniques  

#### Supervised learning  

Supervised learning seeks to identify a functional relationship between the data when an input-output relationship is required by the experimenter for the data set being analysed. 

 - For example, if one considers the output set of data points Y that may correspond for example to data obtained from a sensor measuring air pollution. While the input variable X may be the number of cars. One can then find a functional (either linear or nonlinear) relationship between the output Y with the input X. Such a problem is generally referred to as supervised learning, where training is first carried out in order to identify the parameters of the functional form specified by the experimenter. Such that either inference or prediction can then be carried out. 
 - Examples of supervised learning algorithms that will be initially included in the FIESTA-IoT Analytics platform include the following [18]:

- **Linear Regression** – This supervised learning method seeks to find a linear functional relationship between the output Y and the set of input variables X_p (where the subscript p corresponds to the variable index). 
   - An advantage of linear regression is the relatively simple interpretability of model while maintaining reasonable prediction performance. 
     - For example consider the following example: that is we wish to generate a linear model between the input and output, Y=aX, where a is the linear parameter that relates the input X to the output Y. 
     - As a result, the following inference (interpretation) can be made, if the input variables changes by, ∆X then the output will change by a∆X.  
- **K-Nearest Neighbors (K-NN) regression** – Given the input data (X_(train,) Y_train), we seek to estimate the output ( Y) ̂_test, given the test data X_test (which is a subset of the X_(train,)), by averaging the K output training samples using the corresponding K nearest (using the Euclidean distance) input training data X_(train )points to〖 X〗_(test ).
  - While linear regression may provide an interpretable relationship between the input and output variables. 
  - The performance of the method for predicting the output given the input data points may degrade. 
  - This may arise owing to a non-linear relationship with respect to the model parameters (it should be noted that, transformations of the input variables themselves can be carried out in order to carry out linear regression).  

#### Unsupervised learning  

Unsupervised learning seeks to identify structures and patterns in the data set, where an explicit input-output relationship is not known (or required). 

 - In such problems where only the input data is only available with no explicit output, the challenge is to identify groups or cluster the data in order to understand the relationship between the variables (this is often carried out in exploratory data analysis). 
 - To this end, we have also initially included the following unsupervised learning algorithms:
  - **K-Means Clustering** - This algorithms seeks to identify clusters or subgroups of the data points being analysed. 
    - Clustering is often performed as part of exploratory analysis of data sets, where the experimenter seeks to identify group structure within the data. 
    - K-means clustering seeks to identify a set of K non-overlapping clusters, where each data point is assigned to one of the K clusters. The algorithm achieves this by iteratively estimating the clusters such that the total distance between each point within the K clusters is minimized.  
   - For example, consider Figure # where there are two sensors such that the data has a large variation along one direction (this is illustrated by the red arrow). By projecting the original data of the two sensors along this direction of highest variation (this is referred to the as the principal component scores), we can obtain a lower dimensional representation of the data thus enabling more effective analysis of the original data set.  
  - **Principal Component Analysis** - 

### Other Methods  

- **Fast Fourier Transform (FFT)** - a method for determining the spectral content of a set of data points.  
- **Periodogram** - obtains an estimate of the power of a set of data points for a given frequency. Particularly useful in cases where data is corrupted with unwanted noise.  
- **Correlation** - Estimates the linear dependence between sets of variables/sensors.  

## Methods and Parameters

### Pre-Processing Methods  ("cleaning the data")

| Method  | Parameter    |  Description  | Result | Subsequent Methods  
|---|---|---|---|---|
| Outlier     |  *Thresh* | value between **0** and **1**, selects the percentage of tail values to remove from the ordered time series data.  | {row_number}, {sensor1_outliers_clipped}, {sensor2_outliers_clipped}... {sensorN_outliers_clipped} | Preprocessing, Unsupervised, Supervised, Other Methods 
|FilterData   | *Type* | Select between, **“B”** Bandpass Filter, **“L”** Lowpass filter  and Highpass filter **“H”**.   | {row_number}, {sensor1_post_filter}, {sensor2_post_filter}... {sensorN_post_filter} |
| | *cutoff_1*  |  For the respective filters is the first normalised cutoff frequency, between **0** and **0.5**.  |
| | *cutoff_2*  | For bandpass filter only, the second cutoff frequency.  |
| | *numtaps*  |  Filter length. Usually select **30**.  |

### Unsupervised Learning  

| Method | Parameter     | Description                              | Result                        | Subsequent Methods |
| ------ | ------------- | ---------------------------------------- | ----------------------------- | ------------------ |
| Kmeans | *NumClusters* | The number of clusters to select. An integer value. | {row_number}, {Cluster Label} |                    |
| PCA    | *Mode*        | Select either, ***ExpVar*** the explained variance for the different principal components, or ***Comp*** the principal component loadings that is the direction in the data corresponds to the highest variance. |                               |                    |

### Supervised Learning  

| Method | Parameter   | Description                              | Result                            | Possible Subsequent Methods |
| ------ | ----------- | ---------------------------------------- | --------------------------------- | --------------------------- |
| LinReg | *Type*      | Select between, “***Param***” the estimated parameters of the regression model, and “***Predict***” the estimate of the output given the test data. | {row_number}, {coefficients}      |                             |
|        | *Dependant* | Select the column index corresponding to the dependent variable. |                                   |                             |
|        | *Ratio*     | Select the ratio of the training data to test data. Value between **0** and **1**. |                                   |                             |
| KNNreg | *Num*       | Selects the number of nearest neighbours. | {row_number}, {predicted}, {true} |                             |
|        | *Dependant* | Select the column index corresponding to the dependent variable. |                                   |                             |
|        | *Ratio*     | Select the ratio of the training data to test data. Value between **0** and **1**. |                                   |                             |

### Other Methods  

| Method      | Parameter | Description | Result                                   | Possible Subsequent Methods |
| ----------- | --------- | ----------- | ---------------------------------------- | --------------------------- |
| FFT         | N/A       | N/A         | {frequency}, {sensor1_fft}, {sensor2_fft} |                             |
| Periodogram | N/A       | N/A         | ???                                      |                             |
| Correlation | N/A       | N/A         | {sensor1}, {sensor2_correlation}, {sensor1_correlation} |                             |

## Data Input/Output  

| Input | Output |
| ----- | ------ |
| CSV   | CSV    |

## Workflow  
For the KAT to process a dataset, it needs a dataset in **CSV** format, whereby the columns sequentially correspond a Observation data value and it's corresponding date value (timestamp):

| sensor1DataValue |     sensor1Timestamp | sensor2DataValue |     sensor2Timestamp |
| ---------------: | -------------------: | ---------------: | -------------------: |
|             21.0 | 2017-04-21T13:57:00Z |             22.2 | 2017-04-21T13:57:00Z |
|             21.1 | 2017-04-21T13:58:00Z |             22.3 | 2017-04-21T13:58:00Z |
|             21.2 | 2017-04-21T13:59:00Z |             22.2 | 2017-04-21T13:59:00Z |

It is possible to invoke a SPARQL endpoint to return the result of a query in CSV format.

1. An experimenter discovers sensor devices of interest  
2. Experimenter defines time interval for dataset  

#### Dataset retrieval  

An approach to retrieve data would be to merge both the discovery and retrieval of a dataset with respect to a set of sensing devices.  

```sparql  
PREFIX iot-lite: <http://purl.oclc.org/NET/UNIS/fiware/iot-lite#>
PREFIX m3-lite: <http://purl.org/iot/vocab/m3-lite#>
PREFIX ssn: <http://purl.oclc.org/NET/ssnx/ssn#>
PREFIX geo:  <http://www.w3.org/2003/01/geo/wgs84_pos#>
PREFIX xsd:    <http://www.w3.org/2001/XMLSchema#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dul: <http://www.loa.istc.cnr.it/ontologies/DUL.owl#>
PREFIX time: <http://www.w3.org/2006/time#>
PREFIX sics: <http://smart-ics.ee.surrey.ac.uk/fiesta-iot#>

SELECT  ?sensingDevice ?dataValue ?dateTime
WHERE {
    ?sensingDevice a m3-lite:EnergyMeter .
    ?sensingDevice iot-lite:hasQuantityKind ?qk .
    ?qk a m3-lite:Power .
    ?sensingDevice iot-lite:hasUnit ?unit .
    ?unit a m3-lite:Watt .
    ?sensingDevice iot-lite:isSubSystemOf ?device .
    ?device a ssn:Device .
    ?device ssn:onPlatform ?platform .
    ?platform geo:location ?point .
    ?point geo:lat ?lat .
    ?point geo:long ?long .
    ?observation ssn:observedBy ?sensingDevice .    
    ?observation ssn:observationResult ?sensorOutput .
    ?sensorOutput ssn:hasValue ?obsValue .
    ?obsValue dul:hasDataValue ?dataValue .
    ?observation ssn:observationSamplingTime ?instant .
    ?instant time:inXSDDateTime ?dateTime .
    #set interval
    FILTER ( 
         ( xsd:dateTime(?dateTime) > xsd:dateTime("2017-08-05T14:10:00Z"))
      && ( xsd:dateTime(?dateTime) < xsd:dateTime("2017-08-05T23:10:00Z"))
      ) . 
    #set location bounding box 
    FILTER ( 
         (xsd:double(?lat) >= "0"^^xsd:double) 
      && (xsd:double(?lat) <= "60"^^xsd:double) 
      && ( xsd:double(?long) < "10"^^xsd:double)  
      && ( xsd:double(?long) > "-6"^^xsd:double)
      )  .   
} ORDER BY ?sensingDevice ASC(?dateTime)  
LIMIT 100000
  
```
Example result:  

```csv  
sensingDevice, dataValue, dateTime
http://smart-ics.surrey.ac.uk/fiesta-iot/resource/sc-sics-sp-001-power,0.0E0,2017-05-05T14:11:00Z
http://smart-ics.surrey.ac.uk/fiesta-iot/resource/sc-sics-sp-001-power,0.0E0,2017-05-05T14:12:00Z
http://smart-ics.surrey.ac.uk/fiesta-iot/resource/sc-sics-sp-001-power,0.0E0,2017-05-05T14:13:00Z
http://smart-ics.surrey.ac.uk/fiesta-iot/resource/sc-sics-sp-001-power,0.0E0,2017-05-05T14:14:00Z
http://smart-ics.surrey.ac.uk/fiesta-iot/resource/sc-sics-sp-001-power,0.0E0,2017-05-05T14:15:00Z
http://smart-ics.surrey.ac.uk/fiesta-iot/resource/sc-sics-sp-001-power,0.0E0,2017-05-05T14:16:00Z
http://smart-ics.surrey.ac.uk/fiesta-iot/resource/sc-sics-sp-001-power,0.0E0,2017-05-05T14:17:00Z
http://smart-ics.surrey.ac.uk/fiesta-iot/resource/sc-sics-sp-001-power,0.0E0,2017-05-05T14:18:00Z
http://smart-ics.surrey.ac.uk/fiesta-iot/resource/sc-sics-sp-001-power,0.0E0,2017-05-05T14:19:00Z
http://smart-ics.surrey.ac.uk/fiesta-iot/resource/sc-sics-sp-002-power,9.82058E-1,2017-05-05T14:11:00Z
http://smart-ics.surrey.ac.uk/fiesta-iot/resource/sc-sics-sp-002-power,9.24422E-1,2017-05-05T14:12:00Z
http://smart-ics.surrey.ac.uk/fiesta-iot/resource/sc-sics-sp-002-power,8.06907E-1,2017-05-05T14:13:00Z
http://smart-ics.surrey.ac.uk/fiesta-iot/resource/sc-sics-sp-002-power,7.59163E-1,2017-05-05T14:14:00Z
http://smart-ics.surrey.ac.uk/fiesta-iot/resource/sc-sics-sp-002-power,7.81057E-1,2017-05-05T14:15:00Z
http://smart-ics.surrey.ac.uk/fiesta-iot/resource/sc-sics-sp-002-power,8.71402E-1,2017-05-05T14:16:00Z
http://smart-ics.surrey.ac.uk/fiesta-iot/resource/sc-sics-sp-002-power,8.47793E-1,2017-05-05T14:17:00Z
http://smart-ics.surrey.ac.uk/fiesta-iot/resource/sc-sics-sp-002-power,1.096935E0,2017-05-05T14:18:00Z
http://smart-ics.surrey.ac.uk/fiesta-iot/resource/sc-sics-sp-002-power,9.27258E-1,2017-05-05T14:19:00Z  
```
## FIESTA-IoT Analytics Web Service  

The FIESTA-IoT Web Service can be invoked as shown below:  

![kat-restful-2](https://www.dropbox.com/s/xf0w400gyrbpmk9/kat-restful-2.png?raw=1)  

URL:
```  
POST http://{serverRoot}/AnalyseData
```
Request body (1):
``` json  

{
    "Method": ["FFT"],
    "Parameters":[""],
    "SPARQLquery":["PREFIX iot-lite: <http://purl.oclc.org/NET/UNIS/fiware/iot-lite#>\r\nPREFIX m3-lite: <http://purl.org/iot/vocab/m3-lite#>\r\nPREFIX ssn: <http://purl.oclc.org/NET/ssnx/ssn#>\r\nPREFIX geo:  <http://www.w3.org/2003/01/geo/wgs84_pos#>\r\nPREFIX xsd:    <http://www.w3.org/2001/XMLSchema#>\r\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\r\nPREFIX dul: <http://www.loa.istc.cnr.it/ontologies/DUL.owl#>\r\nPREFIX time: <http://www.w3.org/2006/time#>\r\nPREFIX sics: <http://smart-ics.ee.surrey.ac.uk/fiesta-iot#>\r\n\r\nSELECT  ?sensingDevice ?dataValue ?dateTime\r\nWHERE {\r\n    ?sensingDevice a m3-lite:EnergyMeter .\r\n    ?sensingDevice iot-lite:hasQuantityKind ?qk .\r\n    ?qk a m3-lite:Power .\r\n    ?sensingDevice iot-lite:hasUnit ?unit .\r\n    ?unit a m3-lite:Watt .\r\n    ?sensingDevice iot-lite:isSubSystemOf ?device .\r\n    ?device a ssn:Device .\r\n    ?device ssn:onPlatform ?platform .\r\n    ?platform geo:location ?point .\r\n    ?point geo:lat ?lat .\r\n    ?point geo:long ?long .\r\n    ?observation ssn:observedBy ?sensingDevice .    \r\n    ?observation ssn:observationResult ?sensorOutput .\r\n    ?sensorOutput ssn:hasValue ?obsValue .\r\n    ?obsValue dul:hasDataValue ?dataValue .\r\n    ?observation ssn:observationSamplingTime ?instant .\r\n    ?instant time:inXSDDateTime ?dateTime .\r\n    FILTER ( \r\n         ( xsd:dateTime(?dateTime) > xsd:dateTime(\"2017-05-01T12:10:00Z\"))\r\n      && ( xsd:dateTime(?dateTime) < xsd:dateTime(\"2017-05-01T14:20:00Z\"))\r\n      ) .  \r\n  FILTER ( \r\n       (xsd:double(?lat) >= \"0\"^^xsd:double) \r\n    && (xsd:double(?lat) <= \"60\"^^xsd:double) \r\n    && ( xsd:double(?long) < \"10\"^^xsd:double)  \r\n    && ( xsd:double(?long) > \"-6\"^^xsd:double)\r\n   )  .   \r\n}ORDER BY ?sensingDevice ASC(?dateTime)"],
    "SPARQLendpoint":["http://smart-ics.ee.surrey.ac.uk/srd/sparql/test"]
}
```
- **Method**: A sequence of methods can be selected. Note that the sequences can not be in any order.
- **Parameter**: A set of parameters can be set for each method declared in the same order as the sequence of methods, so that the array index of method 1 should be the same as the array index of parameter 1, and so on.
- **SPARQLquery**: the SPARQL query (including escape characters for double-quotes and carriage returns)  
- **SPARQLendpoint**: the SPARQL endpoint  

The response for the above request would look like:  
```csv  
,http://smart-ics.ee.surrey.ac.uk/fiesta-iot/resource/sc-sics-sp-002-power,http://smart-ics.ee.surrey.ac.uk/fiesta-iot/resource/sc-sics-sp-001-power
0.0,9.880984919163893e-15,2.4424906541753444e-15
0.00819672131148,0.7783786666506537,0.9832946948105892
0.016393442623,0.460068366588671,0.6407791062011362
0.0245901639344,0.5465827765575441,1.6448235918544256
0.0327868852459,0.9407883178169799,0.7477312491096191
0.0409836065574,1.227399470996599,0.10552729931764025
0.0491803278689,0.5596953113530331,0.9696945260416988
0.0573770491803,1.3344798449950006,0.5811979414579715
0.0655737704918,0.8492531349679621,0.5587886846949528
0.0737704918033,1.8443250446945452,1.0398259722146106
0.0819672131148,1.2146292226325448,2.330791043962481
0.0901639344262,0.6801364471846914,1.349631231269907
0.0983606557377,0.9248821311229444,1.8847421684856844
0.106557377049,1.0390665771696894,2.148924836621726
0.114754098361,0.49270521913971854,3.3824120571728664
0.122950819672,1.1875655606859978,0.47064203014504424
0.131147540984,1.3904742220344926,0.8454561298931079
```

## Integration with Experiment Execution Engine (EEE)

The FIESTA-IoT Web Service can be invoked by the EEE to retrieve and analyse a dataset. Normally this could be done in a synchronous manner, whereby the EEE sends a requests and waits until the service finishes the analysis.  Although there are cases where this could take a long time. Therefore the web service could also respond by acknowledging receipt of request, and will then send the result to the Experiment Result Store (ERS).  In order for the ERS to store data for an experimenter, the ERS needs some information with regards to the experiment in order to store the experiment result. This includes:   

* ***userId*** - The username for the experimenter's platform account.  
* ***femoId*** - The FEMO ID for the experiment set.  
* ***jobId***  - The Job ID for the EEE thread.  

This information should appended in the header of the store request.

![kat-restful-3](https://www.dropbox.com/s/cltg3rouax80p6i/kat-restful-3.png?raw=1)  
