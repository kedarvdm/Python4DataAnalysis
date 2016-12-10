# Project Title

Data Analysis of NYC Yellow Cab

### Prerequisites

In order to run the project you need following,
* Softwares:
  1. Python 3.x
  2. Jupyter Notebook

* Libraries:
  1. Pandas
  2. Requests
  3. Matplotlib
  4. Seaborn

You can easily install them if you have Anaconda installed. Please make sure you install Anaconda with Administrative permissions.

### Dataset:
  Please download Trip Sheet Data in CSV Format from following website and place in the "Taxi" folder in this project.
http://www.nyc.gov/html/tlc/html/about/trip_record_data.shtml

Few important points about dataset.

* There are few records without location info.
* In some cases, the tip amount is way to higher than usual scenario (e.g fare amount $9.5, tip amount $998.0)
* Tip amount is present only for credit card payments.

I have ignored such cases.

### Pre-Processing
The aim is to process the downloaded data in Taxi folder and getting it ready for analysis.
Steps:
  1. Data extraction from Taxi folder and adding Travel date parameter in the file.
  2. Creating chunks of the extracted data in order to deal with small csv rather than a big one.
  3. Read the GeoJSON and updating the Pick Up and Dropoff areas
  4. Request and store Lyft ride estimates using requests library.

Please run the DataCollection.py file.
  Optional Arguments: 
  1. \-\-venderid (1= Creative Mobile Technologies, LLC; 2= VeriFone Inc.)
  2. \-\-month (The format is YYYY-MM e.g. 2016-01)
```
    python DataCollection.py --venderid=1 --month=2016-01
```
This file will perform certain steps on data and will get it ready for analysis.

## General Statistics

**index**|**passenger\_count**|**trip\_distance**|**fare\_amount**|**extra**|**mta\_tax**|**tip\_amount**|**tolls\_amount**|**improvement\_surcharge**|**total\_amount**
:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:
count|150774.0|150774.0|150774.0|150774.0|150774.0|150774.0|150774.0|150774.0|150774.0
mean|1.48|3.22|12.78|0.3|0.5|1.45|0.26|0.3|15.58
std|0.82|3.73|11.77|0.28|0.04|4.1|1.4|0.0|14.04
min|0.0|0.0|0.0|0.0|0.0|0.0|0.0|0.0|0.0
25%|1.0|1.1|6.5|0.0|0.5|0.0|0.0|0.3|8.15
50%|1.0|1.9|9.0|0.5|0.5|0.98|0.0|0.3|11.3
75%|2.0|3.8|15.0|0.5|0.5|2.0|0.0|0.3|17.75
max|6.0|175.2|998.0|2.0|0.5|998.14|95.54|0.3|1004.94
Sum|222411.0|485329.9|1926663.28|44596.02|74851.0|218746.62|38877.73|45227.4|2348962.05

## Analysis
The py files for performing analysis are located in Analysis folder and its subfolders.
Every analysis file has same optional arguments.
  Optional Arguments: 1) --venderid (So far NYC dataset has 2 venders. 1= Creative Mobile Technologies, LLC; 2= VeriFone Inc.)
                      2) --month (The format is YYYY-MM e.g. 2016-01)
```
    python Analysis1.py --venderid=1 --month=2016-01
```

### Analysis 1- Borough to Borough Revenue Distribution
* The analysis displays the revenue matrix between all the boroughs in New York.
* Group the data by pick up and dropoff area and sum up the total amount.

**Pick-Up**|**Bronx**|**Brooklyn**|**Manhattan**|**Queens**|**Staten Island**
:-----:|:-----:|:-----:|:-----:|:-----:|:-----:
Bronx|4328.69|197.78|2930.96|656.54|0.0
Brooklyn|1184.25|67935.79|40048.17|15083.4|51.3
Manhattan|43725.55|161242.94|1360331.61|213737.8|2033.2
Queens|8138.49|58872.59|175640.55|69512.92|963.15
Staten Island|0.0|46.8|0.0|0.0|11.8

The Cost Heatmap is as below:

![](Analysis/Analysis1/reports/png/All_All_2016_12_10_16_10_54.png?token=AJjBAvueiasEFrC3NGDEI5-qvNdAHPitks5YVZv-wA%3D%3D)

### Analysis 2- Average Credit Vs. Cash Payments Per Borough.
* The analysis displays average Credit Vs. Cash payments Per borough where the trip ended and payment was made.
* Filter the dataframe for cash and credit card payments.
* Group the data by Pickup area and Payment type and calculate the mean.

**Pick-Up Area**|**Payment Type**|**Average**
:-----:|:-----:|:-----:
Bronx|Credit|23.69
Bronx|Cash|14.2
Brooklyn|Credit|20.2
Brooklyn|Cash|14.22
Manhattan|Credit|15.17
Manhattan|Cash|12.16
Queens|Credit|40.45
Queens|Cash|25.32
Staten Island|Credit|46.8
Staten Island|Cash|11.8

The Grouped bar chart is as below:

![](Analysis/Analysis2/reports/png/All_All_2016_12_10_16_11_25.png?token=AJjBAjHEzhY84l8Jbrv2wKgVJRAvVRTUks5YVZzQwA%3D%3D)

### Analysis 3- Avarage Tip Percentage
* This analysis tells us the avarage tip percentage per borough and also displays min and max payment.
* Calculate the tip percentage by using total_amount and tip_amount.
* Group the data by Dropoff area and calculate average tip amount.

**Dropoff Area**|**Average Tip**|**Max Tip**|**Min Tip**
:-----:|:-----:|:-----:|:-----:
Bronx|13.52|59.92|0.0
Brooklyn|18.91|76.05|0.0
Manhattan|18.95|89.39|0.0
Queens|17.96|88.71|0.0
Staten Island|17.17|29.97|0.0

The Bar plot is as below:
![](Analysis/Analysis3/reports/png/All_All_2016_12_10_16_11_46.png?token=AJjBAotkT7Ez9mXpOc2wYDJ8v6dGs06_ks5YVZz4wA%3D%3D)

### Analysis 4- Cash Vs. Credit Payment Distribution For Trips Under $150
* The analysis displays Cash Vs Credit Payment distribution per borough in violin chart. Only trips under $150 are considered for this analysis.
* Filter the dataframe for cash and credit payments.
* Group the data by Dropoff area and Payment Type and calculate average trip amount.

**Dropoff Area**|**Payment Type**|**Amount**
:-----:|:-----:|:-----:
Bronx|Cash|24.83
Bronx|Credit|36.77
Brooklyn|Cash|19.83
Brooklyn|Credit|25.77
Manhattan|Cash|11.2
Manhattan|Credit|14.61
Queens|Cash|23.28
Queens|Credit|32.56
Staten Island|Cash|67.4
Staten Island|Credit|84.37

The violin plot is as below:
![](Analysis/Analysis4/reports/png/All_All_2016_12_10_16_12_04.png?token=AJjBAl1R6SDueVSYMBoTRCQRgrlWxUWHks5YVZ0qwA%3D%3D)

### Analysis 5- Comparison of Lyft Vs Yellow Cab Ride Costs based on Passenger count
* This analysis compares the NYC Yellow cab with Lyft ride estimated costs. The lyft data is collected through Lyft REST API.
* The primetime hike has been deducted while storing the estimated ride costs.
* Also for comparison is performed with following rule:
        1. 0 or 1 passenger compared with Lyft Line estimated cost. (Passenger count cant be O but the dataset has few record where it is given as 0).
        2. 2 to 4 passenger compared with regular Lyft estimated cost.
        3. 5 and above compared with Lyft Plus estimated cost.

**Passenger Count**|**Yellow Cab Cost**|**Lyft Cost**
:-----:|:-----:|:-----:
1|15.04|15.06
2|15.16|15.24
3|15.08|15.15
4|15.3|15.36
5|14.54|14.92
6|13.27|13.91

The Bidirectional Bar plots is as below:
![](Analysis/Analysis5/reports/png/All_All_2016_12_10_16_10_23_bidirectional.png?token=AJjBAntMGVvZLQbbXTd0eSySIS7TvD-mks5YVZ1dwA%3D%3D)

The Grouped Bar chart is as below:
![](Analysis/Analysis5/reports/png/All_All_2016_12_10_16_10_23_bar_plot.png?token=AJjBAmThvCuXNpa-McilCPe39qbnavDOks5YVZ2FwA%3D%3D)
