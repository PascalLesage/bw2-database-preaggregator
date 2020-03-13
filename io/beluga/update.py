import os
from math import ceil
import json
from pathlib import Path
act_list_fp = Path("/home/plesage/scratch/ei36co_balanced_files/preagg_ei36co/common_files/ordered_activity_codes.json")
lci_files_fp = Path("/home/plesage/scratch/ei36co_balanced_files/preagg_ei36co/lci")
with open(act_list_fp, 'r') as f:
    all_activity_codes = json.load(f)
chunks = lambda l, n: [l[i:i + n] for i in range(0, len(l), n)]
number_of_slices = 25
def get_remaining(all_activity_codes, number_of_slices, slice_id, done):
    activities_to_treat = []
    activity_codes = chunks(all_activity_codes, ceil(len(all_activity_codes) / (number_of_slices)))[slice_id]
    for act in activity_codes:
        lci_filename = "{}.npy".format(act)
        if lci_filename not in done:
            activities_to_treat.append(lci_filename)
    return len(activity_codes), activities_to_treat
for i in range(10):
    if not os.path.isdir(lci_files_fp/str(i)):
        total, todo = "n/a", "n/a"
        print("Batch: ", i, "n/a")
    else:
        print("Batch: ", i)
        done = os.listdir(lci_files_fp/str(i))
        for c in range(25):
            total, todo = get_remaining(all_activity_codes, number_of_slices, c, done)
            print("\t", c, total, len(todo))