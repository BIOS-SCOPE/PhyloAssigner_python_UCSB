#!/Users/fwittmers/miniconda3/envs/PythonAssigner/bin/python
import pandas as pd
import json

## creates getBEST.best_placements objects which has only the best placements retained.
## Inbut placements must be .jplace file

def getBEST(placements, placer):
    # best placement computation (see jupyter notebook)
    fh = open(placements, "r")
    jplace = json.load(fh)
    fh.close()
    # tree_json = jplace['tree'] #get tree from json file
    placements_json = jplace['placements']  # get placement results from json file
    colnames_json = jplace['fields']  # get column names of placement results

    all_placements = pd.DataFrame()  # create empty dataframe

    for pp_queries in placements_json:
        placement_lwr = pp_queries['p']
        # convert json list of lists into dataframe, also adding column names (from json file 'fields' section)
        placement = pd \
            .DataFrame(placement_lwr) \
            .set_axis(colnames_json,
                      axis=1,
                      inplace=False)

        # depending on what placer is used the Key for the name section of the .JSON output differs between 'nm' (
        # pplacer) and 'n' (EPA-ng) also, pplacer stores the result name in a nested list while EPA-ng stores the
        # name in a single list
        if placer == "pplacer":
            taxid_list = pp_queries['nm']  # get ASV_id of placement
            placement['ASV_id'] = taxid_list[0][0]  # add taxid of placement to placement table
        elif placer == "epang":
            taxid_list = pp_queries['n']
            placement['ASV_id'] = taxid_list[0]  # add taxid of placement to placement table

        frames = [all_placements, placement]  # determine the 2 frames to concat
        all_placements = pd \
            .concat(frames)  # concat new and previous loop iteration placements together

    getBEST.best_placements = all_placements. \
        sort_values(by=['ASV_id', 'like_weight_ratio'],
                    ascending=False) \
        .drop_duplicates('ASV_id',
                         keep='first')