import pm4py
import json
from pm4py.algo.discovery.temporal_profile import algorithm as temporal_profile_discovery

log = pm4py.read_xes("cleaned_long.xes")
events  = 0
cases = 0
lens = []
cur = None
c = 0
for i,row in log.iterrows():
    events += 1
    if not cur or cur != row["case:concept:name"]:
        if cur:
            lens.append(c)
            c = 0

        cur = row["case:concept:name"]
        cases += 1
    c+= 1
    #param of interest == case:age

lens.append(c)
print("Min: ", min(lens))
print("Max: ", max(lens))
print("Events: ", events)
print("Cases: ", cases)
process_tree = pm4py.discover_process_tree_inductive(log)
bpmn_model = pm4py.convert_to_bpmn(process_tree)
pm4py.save_vis_bpmn(bpmn_model, "data_set.png")
pm4py.save_vis_process_tree(process_tree, "process_tree.png")
