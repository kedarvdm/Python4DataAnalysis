# Project Title

Data Analysis of NYC Yellow Cab

### Prerequisites

In order to run the project you need following,
Softwares:
  1) Python 3.x
  2) Jupyter Notebook

Libraries:
  1) Pandas
  2) Requests
  3) Matplotlib
  4) Seaborn
You can easily install them if you have Anaconda installed. Please make sure you install Anaconda with Administrative permissions.

Dataset:
  Please download Trip Sheet Data in CSV Format from following website and place in the "Taxi" folder in this project.
http://www.nyc.gov/html/tlc/html/about/trip_record_data.shtml

### Pre-Processing
The aim is to process the downloaded data in Taxi folder and getting it ready for analysis.
Please run the DataCollection.py file.
  Optional Arguments: 1) --venderid (So far NYC dataset has 2 venders. 1= Creative Mobile Technologies, LLC; 2= VeriFone Inc.)
                      2) --month (The format is YYYY-MM e.g. 2016-01)
```
    python DataCollection.py --venderid=1 --month=2016-01
```
This file will perform certain steps on data and will get it ready for analysis.

## Analysis
The py files for performing analysis are located in Analysis folder and its subfolders.
Every analysis file has same optional arguments.
  Optional Arguments: 1) --venderid (So far NYC dataset has 2 venders. 1= Creative Mobile Technologies, LLC; 2= VeriFone Inc.)
                      2) --month (The format is YYYY-MM e.g. 2016-01)
```
    python Analysis1.py --venderid=1 --month=2016-01
```

1) Analysis 1- Borough to Borough Revenue Distribution
    The analysis displays the revenue matrix between all the boroughs in New York.
    
    ![Image](Analysis/Analysis1/reports/png/1_2016-01_2016_12_10_01_29_41.png?raw=true)

2) Analysis 2- Average Credit Vs. Cash Payments Per Borough.
    The analysis displays average Credit Vs. Cash payments Per borough where the trip ended and payment was made.
    
    ![Image](Analysis/Analysis2/reports/png/1_2016-01_2016_12_10_01_30_42.png?raw=true)

3) Analysis 3- Avarage Tip Percentage
    This analysis tells us the avarage tip percentage per borough and also displays min and max payment.
    
    ![Image](Analysis/Analysis3/reports/png/1_2016-01_2016_12_10_01_31_30.png?raw=true)

4) Analysis 4- Cash Vs. Credit Payment Distribution For Trips Under $150
    The analysis displays Cash Vs Credit Payment distribution per borough in violin chart. Only trips under $150 are considered for this analysis.
    
    ![Image](Analysis/Analysis4/reports/png/1_2016-01_2016_12_10_01_32_28.png?raw=true)
    
5) Analysis 5- Comparison of Lyft Vs Yellow Cab Ride Costs based on Passenger count
    This analysis compares the NYC Yellow cab with Lyft ride estimated costs. The lyft data is collected through Lyft REST API.
    The primetime hike has been deducted while storing the estimated ride costs.
    Also for comparison is performed with following rule:
        1) 0 or 1 passenger compared with Lyft Line estimated cost. (Passenger count cant be O but the dataset has few record where it is given as 0).
        2) 2 to 4 passenger compared with regular Lyft estimated cost.
        3) 5 and above compared with Lyft Plus estimated cost.
        
    ![Image](Analysis/Analysis5/reports/png/1_2016-01_2016_12_10_01_34_55_bidirectional.png?raw=true)
    
    ![Image](Analysis/Analysis5/reports/png/1_2016-01_2016_12_10_01_34_55_bar_plot.png?raw=true)

Each analysis subfolder has reports folder. The CSV out put and PNG output of the graphs is being stored there.
   
