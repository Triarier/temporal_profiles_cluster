import pm4py
import json
import numpy as np
import os
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from statistics import mean, stdev 
from sklearn.preprocessing import StandardScaler

def transform(ev_tuple):
    return ev_tuple[2]

log = pm4py.read_xes("cleaned_long.xes")

traces = {}
cur = None
for i,row in log.iterrows():
    if not cur or cur != row["case:concept:name"]:
        cur = row["case:concept:name"]
        traces[cur] = []
    #param of interest == case:age
    traces[cur].append((row["concept:name"],row["time:timestamp"],row["case:age"]))

distances = {}
distances_for_cluster = {}
for tr in traces:
    prev = None
    for tups in traces[tr]:
        if prev is None:
            cluster_k = transform(tups)
            prev = tups
            continue
        k = (prev[0],tups[0])
        if k not in distances:
            distances[k] = []
            distances_for_cluster[k] = []
        distances[k].append((tups[1]-prev[1]).total_seconds())
        if not np.isnan(cluster_k):
            distances_for_cluster[k].append([cluster_k,(tups[1]-prev[1]).total_seconds()])

        prev = tups


temp_profile = {}
for k in distances:
    if len(distances[k]) > 1:
        temp_profile[k] = (mean(distances[k]),stdev(distances[k]))
    else:
        temp_profile[k] = (mean(distances[k]),0.0)

num_clusters = 0
num_long_clusters = 0 
for k in distances_for_cluster:
    if len(distances_for_cluster[k])> 2:
        X_ori = np.array(distances_for_cluster[k])
        scale = StandardScaler()
        X = scale.fit_transform(X_ori)
        db_scan = DBSCAN(eps=.45,min_samples=50)
        clustering = db_scan.fit(X)
        counter = Counter(clustering.labels_)
        if(len(counter)>1):
            num_long_clusters += 1
            new_temp_data = {}
            new_temp_age = {}
            try:
                os.mkdir("clusters")
            except OSError:
                pass
            print(counter)  
            print(clustering.labels_)
            for idx, x in enumerate(clustering.labels_):
                if x not in new_temp_data:
                    new_temp_data[x] = []
                    new_temp_age[x] = []
                new_temp_data[x].append(X_ori[idx][1])
                new_temp_age[x].append(X_ori[idx][0])
            temp_profile_c = {}
            for kk in new_temp_data:
                s = new_temp_age[kk]
                s.sort()
                if len(new_temp_data[kk]) > 1:
                    temp_profile_c[kk] = (mean(new_temp_data[kk]),stdev(new_temp_data[kk]),s[0],s[-1])
                else:
                    temp_profile_c[kk] = (mean(new_temp_data[kk]),0.0,s[0],s[-1])
            print("-----LEN")
            th = 2
            cth = 0
            oldh = 0
            #for i in new_temp_data[1]:
            #    z = abs((i-temp_profile_c[1][0])/temp_profile_c[1][1])
            #    print(z)
            #    zo = abs((i-temp_profile[k][0])/temp_profile[k][1])
            #    if z>th:
            #        cth += 1
            #    if zo>th:
            #        oldh += 1
            #print(cth)    
            #print(oldh)    
            #print(k)
            #print(temp_profile_c)
            print(temp_profile[k])
            
            XX =scale.inverse_transform(X)
            plt.scatter(X[:,0],X[:,1],c=clustering.labels_,cmap='viridis')
            plt.xlabel("Age")
            plt.ylabel("Time in seconds")
            title = "cluster"+k[0]+"_"+k[1]
            title = title.replace("/","_")

            plt.savefig("clusters/"+title+".png")
        else:
            num_clusters += 1

print(num_clusters)
print(num_long_clusters)
