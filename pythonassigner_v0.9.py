#!/Users/fwittmers/miniconda3/envs/PythonAssigner/bin/python

## importing argument parse libraries
import argparse  # for parsing input arguments
import subprocess  # for running commandline code, for example pplacer binary
import os  # to get working dirctory
import sys  # e.g. for exit with errormessage
import shutil
# import json
import pandas as pd
from pathlib import Path  # used to check if path exists or not
# import pathlib
from Bio import AlignIO

# from Bio import SeqIO

sys.path.append('modules')
from modules.smart_description_formatter import \
    SmartDescriptionFormatter  # import class to add spaces/format  parser description in commandline help output
from modules.place import runPPLACER
from modules.place import runEPANG
from modules.LCA import getLCA
from modules.best import getBEST
from modules.helper_functions import merge_mapping
from modules.helper_functions import split_align

## parsing arguments
parser = argparse.ArgumentParser(
    formatter_class=SmartDescriptionFormatter,
    description="""run PythonAssigner through the command-line. This is an updated version of PhyloAssigner, 
    originally written in 2012 in perl. See: Vergin et al. 2013 supplementary information for more details; Rewritten 
    in python3 by Fabian Wittmers 2021/2022 """
)

parser.add_argument('-o', '--out_dir', required=True,
                    help="output directory were result files should be stored")  # output directory.
parser.add_argument('-r', '--ref_align', required=True, type=Path,
                    help="reference alignment file. Must contain the same sequence identifiers as in the reference "
                         "tree")  # reference alignment
parser.add_argument('-t', '--ref_tree', required=True, type=Path,
                    help="reference tree file (newick formatted). Must contain the same sequence identifiers as in "
                         "the reference alignment")  # reference tree
#parser.add_argument("-b", "--bin_path", required=True, type=Path,
#                    help="absolute or relative path to the binary folder you downloaded from the PythonAssigner "
#                         "github. The folder should include some script(s)")
parser.add_argument("-q", "--query_seqs", required=True, type=Path,
                    help="fasta file of sequences you want to place on reference tree")
parser.add_argument('-m', '--mapping', required=True, type=Path,
                    help="taxonomy mapping file: edge number in first column + corresponding taxonomy in second "
                         "column. If edge is a tip, then tip label in third.")
parser.add_argument('-T', '--threads', required=False, default=1,
                    help="specify the number of threads to use in parallel computation steps")
parser.add_argument("-p", '--placer', default="pplacer",
                    help="specify which placement algorithm to use, choose between 'pplacer' or 'epang'. "
                         "Alternatively, you can run 'compare' mode to compare both placement algorithms")

args = parser.parse_args()  ## args will be a dictionary with the different input arguments

print("")  # "\n" whould insert 2 newlines
print("PROVIDED ARGUMENTS:")
print("-" * 65)
#print("PythonAssigner github binary folder:", args.bin_path)
print("writing results to:", args.out_dir)  # prints the name of the output directory
print("selected reference alignment:", args.ref_align)
print("selected reference tree:", args.ref_tree)
print("query sequences:", args.query_seqs)
print("taxonomy mapping file", args.mapping)
print("-" * 65)
print("")

## check if files in args supplied exists / checking+creating output directories

wd = os.getcwd()  # current working directory

# check if reference alignment exists
print("CHECKING IF ALL FILES EXIST:")
print("-" * 65)
path_to_file = wd / args.ref_align
if path_to_file.is_file():
    print('reference alignment', path_to_file, ' exists')
else:
    print('reference alignment', path_to_file, ' does not exist')
    sys.exit(1)

# check if reference tree exists
path_to_file = wd / args.ref_tree
if path_to_file.is_file():
    print('reference tree', path_to_file, ' exists')
else:
    print('reference tree', path_to_file, ' does not exist')
    sys.exit(1)

# check if query sequences exist
path_to_file = wd / args.query_seqs
if path_to_file.is_file():
    print('query sequence file', path_to_file, ' exists')
else:
    print('query sequence file', path_to_file, ' does not exist')
    sys.exit(1)

# check if mapping file exists
path_to_file = wd / args.mapping
if path_to_file.is_file():
    print('mapping file', path_to_file, ' exists')
else:
    print('mapping file', path_to_file, ' does not exist')
    sys.exit(1)

# check if binary folder from github PythonAssigner exists
# installed in conda env on linux -> should be in wd
# path_to_dir = os.path.join(wd, args.bin_path)
# if os.path.isdir(path_to_dir):
#    print('binary directory', path_to_dir, ' exists')
# else:
#     print(
#         'binary directory', path_to_dir, ' does NOT exist.\n    ERROR: This tool requires that you provide the path ('
#         'absolute or relative) to the binary directory (bin/ folder) with the PythonAssigner dependencies\n')
#     sys.exit(1)

# check if output directory (for results) exists
path_to_dir = os.path.join(wd, args.out_dir)
if os.path.isdir(path_to_dir):
    print(
        'output directory', {path_to_dir}, ' exists.\n    ERROR: This tool does not overwrite existing directories. Please '
        'remove the directory or provide a different directory name and restart the tool.\n')
    sys.exit(1)
else:
    print('output directory', path_to_dir, ' will be created.')

print("-" * 65, "\n")

# check if temporary output directory (for results) exists
path_to_dir = os.path.join(wd, 'temp_pythonassigner_out')
if os.path.isdir(path_to_dir):
    print(
        'temporary output directory', {path_to_dir}, ' exists.\n    ERROR: This tool does not overwrite existing directories.'
        ' Please remove the directory or provide a different directory name and restart the tool.\n')
    sys.exit(1)
else:
    print('temporary output directory', path_to_dir, ' will be created.')

print("-" * 65, "\n")


# create temporary and final output directories
print("CREATING OUTPUT DIRECTORIES:")
print("-" * 65)
out_dir = os.path.join(wd, args.out_dir)
print("creating output directory for final results and key intermediates:", out_dir)
os.mkdir(out_dir)
temp_dir = os.path.join(wd, "temp_pythonassigner_out")
print("creating temporary output directory for intermediate results:", temp_dir)
os.mkdir(temp_dir)
print("-" * 65, "\n")

## create tree stats file (with RAxML)
T = str(args.threads)

raxml_args = "raxmlHPC-AVX2 -f e -s " + \
             os.path.join(wd, args.ref_align) + \
             " -t " + os.path.join(wd, args.ref_tree) + \
             " -n PythonAssigner -m GTRGAMMAX --silent -w " + \
             os.path.join(wd, temp_dir) + \
             " -T " + T

print("running RAxML to compute model statistics as follows:\n", raxml_args)
try:
    subprocess.check_call(raxml_args, shell=True, stdout=False)
    print("RAxML model computation finished successfully.")
except subprocess.CalledProcessError:  # when there is an error while running RAxML:
    print("RAxML did NOT finish successfully:\n", subprocess.CalledProcessError)
    sys.exit(1)

tree_model = os.path.join(wd, temp_dir, "RAxML_info.PythonAssigner")
print("RAxML model info written to", tree_model, "\n")

## create reference stats package (for pplacer) using taxtastic
tree_model_refpack = os.path.join(wd, temp_dir, "PythonAssigner.taxid.refpkg")
taxtastic_args = "taxit create -l 16s_rRNA -P " + \
                 tree_model_refpack + \
                 " --aln-fasta " + \
                 os.path.join(wd, args.ref_align) + \
                 " --tree-stats " + \
                 tree_model + \
                 " --tree-file " + \
                 os.path.join(wd, args.ref_tree)

print("preparing model stats for PythonAssigner as follows:\n", taxtastic_args)
try:
    subprocess.check_call(taxtastic_args, shell=True, stdout=False)
    print("taxtastic prepared pplacer model reference package successfully.")
except subprocess.CalledProcessError:
    print("taxtastic did NOT finish successfully:\n", subprocess.CalledProcessError)
    sys.exit(1)

print("taxtastic reference package for pplacer written to ", tree_model_refpack, "\n")

## create alignment (align ref alignment with query alignment)
# reformat fasta to stockholm
ref_align_stk = os.path.join(wd, temp_dir, "ref_align.stk")
# reformatted query sequences in stockholm format. Stored in temporary working directory

# to_stock_args = "bash " + \
#                os.path.join(args.bin_path, "fasta_to_stockholm.sh") + \
#                " -i " + os.path.join(wd, args.ref_align) + \
#                " -o " + ref_align_stk

# print("preparing reference alignment for HMMER3 alignment as follows:", to_stock_args)
print("preparing reference alignment for HMMER3 alignment")

# try:
#    subprocess.check_call(to_stock_args, stdout=False, shell=True)
#    print("fasta_to_stockholm.sh created stockholm reference alignment file successfully.")
# except subprocess.CalledProcessError:
#    print("fasta_to_stockholm.sh did NOT finish successfully:\n", subprocess.CalledProcessError)
#    sys.exit(1)

alignment = AlignIO.read(open(os.path.join(wd, args.ref_align)), "fasta")
# print("Alignment length %i" % alignment.get_alignment_length())
AlignIO.write(alignment, ref_align_stk, "stockholm")


print("reformatted reference alignment written to ", ref_align_stk)

# recompile reference alignment into hmm file using hmmbuild

ref_align_hmm3 = os.path.join(wd, temp_dir, "ref_align.hmm3")
hmmbuild_args = "hmmbuild " + ref_align_hmm3 + " " + ref_align_stk

print("compressing reference alignment into hmm as follows:", hmmbuild_args)

try:
    subprocess.check_call(hmmbuild_args, shell=True, stdout=False)
    print("hmmbuild created hmm3 compiled version of reference alignment successfully.")
except subprocess.CalledProcessError:
    print("hmmbuild did NOT finish successfully:\n", subprocess.CalledProcessError)
    sys.exit(1)

# compute alignment (HMMER3 for now. Add other aligners as potential options later?)

hmmer_res_sto = os.path.join(wd, temp_dir, "query_ref_align.stk")
hmmalign_args = "hmmalign --trim --informat FASTA --outformat Stockholm --allcol --mapali " + \
                ref_align_stk + \
                " -o " + hmmer_res_sto + \
                " --dna " + ref_align_hmm3 + " " + \
                os.path.join(wd, args.query_seqs)

print("aligning query sequences with hmmer3 as follows:", hmmalign_args)

try:
    subprocess.check_call(hmmalign_args, shell=True, stdout=False)
    print("HMMER3 aligned query sequences to reference alignment successfully.")
except subprocess.CalledProcessError:
    print("HMMER3 did NOT finish successfully:\n", subprocess.CalledProcessError)
    sys.exit(1)

# reformat from stockholm to fasta
# (suffix of resulting alignment file must .fasta for pplacer to accept it).

print("converting HMMER3 results into fasta MSA file")
hmmer_res_fasta = os.path.join(wd, args.out_dir, "ref_query_align.fasta")

alignment = AlignIO.read(open(hmmer_res_sto), "stockholm")
# print("Alignment length %i" % alignment.get_alignment_length())
AlignIO.write(alignment, hmmer_res_fasta, "fasta")

## run placement algorithm
if args.placer == "pplacer":
    print("placeing sequences through pplacer, the default placement algorithm.")
    runPPLACER(out_dir,
               tree_model_refpack=tree_model_refpack,
               ref_tree=os.path.join(wd, args.ref_tree),
               hmmer_res_fasta=hmmer_res_fasta)
    placements = runPPLACER.placements

elif args.placer == "epang":

    # split query and reference sequences from the alignment (not necessary for PPlacer)
    split_align(args.ref_align, args.query_seqs, hmmer_res_fasta, temp_dir)

    # where to find RAxML_info file
    model_raxml_info = os.path.join(temp_dir, "RAxML_info.PythonAssigner")

    # run EPAng placement
    runEPANG(out_dir, split_align.split_reference, split_align.split_query, args.ref_tree, args.threads,
             model_raxml_info)

    placements = runEPANG.placements

elif args.placer == "compare":
    print("comparison mode currently not available as a placement option.")
else:
    print("non viable placement algorithm choosen: ", args.placer)

## run postprocessing of jplace

# extract best placements
getBEST(placements, args.placer)

# assign taxonomy mapping
# mapping file with first column = edge number; second column = taxon

# read in mapping:
mapping = pd.read_csv(args.mapping, sep="\t") \
    .drop(["V3"], axis=1) \
    .set_axis(['edge_num', 'taxon'], axis=1, inplace=False)

# merge taxonomy (ie mapping file) and placement results
merge_mapping(mapping, getBEST.best_placements, "yes")  # "yes" --> keep lwr
# creates: merge_mapping.place_tax which is the csv including the taxonomy

# write merged dataframe as file in output directory
best_file = os.path.join(wd, out_dir, "best_placements.tsv")
merge_mapping.place_tax.to_csv(best_file, sep='\t', na_rep="NA")  # writes best placement output/results

print("Best placement table written to: ", best_file)

## LCA placement computation
print("\n")  # adds 2 newlines
print("starting LCA computation using gappa")

getLCA(out_dir, placements,
       args.threads)  # from lca.py module. Also writes an output .jplace with the LCA nodes as placements

## assign taxonomy to LCA placements
# no filtering of LCA placements necessary. Only 1 LCA placement per placed sequence generated (by gappa)
# this is different from the processing of the best placement results
merge_mapping(mapping, getLCA.LCA_placements, "no")  # "no" -> drop 'lwr' which is always 1 after accumlation by gappa

LCA_file = os.path.join(wd, out_dir, "LCA_placements.tsv")
merge_mapping.place_tax.to_csv(LCA_file,
                               sep='\t', na_rep="NA")  # write best placement output/results

print("LCA placement table written to: ", LCA_file)

## cleaning. Removing temporary data
shutil.rmtree(temp_dir)
# shutil.rmtree(out_dir)  # development / debugging
# print("\nReached end of script") # development / debugging
