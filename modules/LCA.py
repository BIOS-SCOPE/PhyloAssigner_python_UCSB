#!/Users/fwittmers/miniconda3/envs/PythonAssigner/bin/python
import pandas as pd
import subprocess
import sys
import os
import json

def getLCA(out_dir, placements, threads):
    # path for the LCA output = os.path.join(out_dir)
    LCA_placements_path = os.path.join(out_dir)
    gappa_args = "gappa edit accumulate --jplace-path " + \
                placements + \
                " --threshold 0.90 --out-dir " \
                + LCA_placements_path + \
                " --threads " + \
                threads + \
                " --file-prefix LCA_gappa_"
    print("computing last common ancestor using gappa as follows:", gappa_args)

    try:
        subprocess.check_call(gappa_args, shell=True, stdout=False)
        print("gappa computed LCA successfully.")
    except subprocess.CalledProcessError:
        print("gappa did NOT finish successfully:\n", subprocess.CalledProcessError)
        sys.exit(1)

    # getting placement table from gappa jplace
    print("exporting placements from gappa jplace")
    fh = open(os.path.join(LCA_placements_path,"LCA_gappa_accumulated.jplace"), "r")
    jplace_gappa = json.load(fh)
    fh.close()

    placements_json = jplace_gappa['placements']  # get placement results from json file
    colnames_json = jplace_gappa['fields']  # get column names of placement results

    getLCA.LCA_placements = pd.DataFrame()  # create empty dataframe

    for pp_queries in placements_json:
        placement_lwr = pp_queries['p']
        # convert json list into dataframe, also adding column names (from json file 'fields' section) this works
        # identical for list or list of lists (as it is the case when pplacer placements, with 1, but potentially
        # more than 1 placements)
        placement = pd \
            .DataFrame(placement_lwr) \
            .set_axis(colnames_json,
                    axis=1,
                    inplace=False)
        taxid_list = pp_queries['n']
        # get ASV_id of placement. This is 'nm' for pplacer output but 'n' for gappa output here taxid_list[] instead
        # of taxid_list[0][0] because gappa produces list instead of list of lists (like pplacer does)
        # add taxid of placement to placement table.
        placement['ASV_id'] = taxid_list[0]

        frames = [getLCA.LCA_placements, placement]  # determine the 2 frames to concat

        getLCA.LCA_placements = pd.concat(frames) # concat new and previous loop iteration placements together