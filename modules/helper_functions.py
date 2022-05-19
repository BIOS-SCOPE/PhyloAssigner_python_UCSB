#!/Users/fwittmers/miniconda3/envs/PythonAssigner/bin/python

import pandas as pd
from Bio import SeqIO
import os


### collection of different helper functions

# takes input mapping file, placement results and logical argument (yes/no), if want to retain likelihood weight
# ratio (LWR) or not

def merge_mapping(mapping, placement_table, keep_lwr):
    if keep_lwr == "yes":
        merge_mapping.place_tax = placement_table \
            .set_index('edge_num') \
            .join(mapping.set_index('edge_num')) \
            .drop(['distal_length', 'likelihood', 'pendant_length'],
                  axis=1)  # merge mapping information with a placement table
    elif keep_lwr == "no":  # -> drop like_weight_ratio
        merge_mapping.place_tax = placement_table \
            .set_index('edge_num') \
            .join(mapping.set_index('edge_num')) \
            .drop(['distal_length', 'likelihood', 'pendant_length', 'like_weight_ratio'],
                  # also dropping lwr here because always 1 after gappa computed LCA
                  axis=1)  # merge mapping with LCA placements


# takes an input reference alignment, query sequences, an alignment of both query and ref sequences and an output
# directory # splits the alignment of ref and query and creates 2 output alignments in the output directory # all
# input/output sequence files MUST be .fasta format

def split_align(ref_align, query_seqs, both_align, out_dir):
    # getting reference sequence IDs from reference alignment
    ref_fasta = SeqIO.parse(ref_align, "fasta")
    ref_ids = []
    for reference in ref_fasta:
        ref_ids.append(reference.id)

    # get reference sequences out of hmmer alignment file (result file from hmmer alignment.
    # Name might change with other alignment options and will have to be adjusted at some point
    split_align.split_reference = os.path.join(out_dir, "refseq_align.fasta")

    with open(both_align) as seqs, \
            open(split_align.split_reference, 'w') as result:
        record_dict = SeqIO.to_dict(SeqIO.parse(seqs, 'fasta'))
        ref_records = [record_dict[id_]
                       for id_ in ref_ids]
        SeqIO.write(ref_records, result, "fasta")

    # getting query sequence IDs from query sequence fasta
    query_fasta = SeqIO.parse(query_seqs, "fasta")

    query_ids = []
    for query in query_fasta:
        query_ids.append(query.id)

    split_align.split_query = os.path.join(out_dir, "query_align.fasta")

    with open(both_align) as seqs, open(
            split_align.split_query, 'w') as result:
        record_dict = SeqIO.to_dict(SeqIO.parse(seqs, 'fasta'))
        query_records = [record_dict[id_] for id_ in query_ids]
        SeqIO.write(query_records, result, "fasta")
