import os
from pathlib import Path
import json

lci_files_fp = Path("/home/plesage/scratch/preagg_ei36co/lci")
for i in range(10):
    batch_dir = lci_files_fp / str(i)
    if batch_dir.is_dir():
        files = os.listdir(batch_dir)
        with open(lci_files_fp/"{}.json".format(i), "w") as f:
            json.dump(files, f)
