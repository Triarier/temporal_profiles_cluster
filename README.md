# temporal_profiles_cluster
Source Code for 'Discovering Temporal Profiles based on Trace Clustering in Process-Aware Information Systems'

## Info

This repository contains a proof of concept implementation of the approach described in the paper. 


## Data

The data source files for the paper cannot be published in this repository. 
Please go to https://physionet.org/content/mimiciv/2.2/ for the data set.
To generate event logs from this data source, please visit https://github.com/bptlab/mimic-log-extraction

### Data Preparation

This could change: Currently the files generated using the mimic-log-extraction do not work out of the box with pm4py.
Some problems occured importing the logs. First, some elements are coded as date in an event but the same key is associated in a string 
element in another event. The source is probably a missing date value in the data set. To solve this, I changed all these mixed tags to string.
Second, some events are missing the concept:name key. Third, some events are duplicates with equal concept:name and timestamp. The script 
'cleanup.py' is resolving these issues. 
