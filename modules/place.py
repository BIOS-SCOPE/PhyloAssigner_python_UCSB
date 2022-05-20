#!/Users/fwittmers/miniconda3/envs/PythonAssigner/bin/python

## importing dependencies

import os
import sys
import subprocess
import shutil


## function to run pplacer
def runPPLACER(out_dir, tree_model_refpack, ref_tree, hmmer_res_fasta):
    print("\n")  # adds 2 newlines
    print("starting phylogenetic placement of sequences using pplacer")

    # In a function named func, use the syntax func.variable = value to store value in variable as an attribute of func.
    # To access value outside of func, use func() to run func, then use the syntax function_name.variable to access value.
    runPPLACER.placements = os.path.join(out_dir, "placements.jplace")

    ## ignoring the bin path path (os.path.join(args.bin_path, "pplacer") since installed in PATH on Linux
    pplacer_args = "pplacer -c " + tree_model_refpack + \
               " -o " + runPPLACER.placements + \
               " -t " + ref_tree + \
               " " + hmmer_res_fasta

    print("placing sequences using pplacer as follows:", pplacer_args)

    try:
        subprocess.check_call(pplacer_args, shell=True, stdout=True)
        print("pplacer placed query sequences successfully.")
    except subprocess.CalledProcessError:
        print("pplacer did NOT finish successfully:\n", subprocess.CalledProcessError)
        sys.exit(1)

## function to run EPA-ng
def runEPANG(out_dir, ref_align_epang, query_align_epang, ref_tree, threads, model_raxml_info):
    print("\n")
    print("starting phylogenetic placement of sequences using EPAng")

    epang_args = "epa-ng" + \
                 " --tree " + str(ref_tree) + \
                 " --model " + str(model_raxml_info) + \
                 " --chunk-size 5000" + \
                 " --ref-msa " + str(ref_align_epang) + \
                 " --query " + str(query_align_epang) + \
                 " --out-dir " + str(out_dir) + \
                 " --threads " + str(threads)

    print("placing sequences using EPA-ng as follows:", epang_args)

    try:
        subprocess.check_call(epang_args, shell=True, stdout=True)
        print("EPAng placed query sequences successfully.")
    except subprocess.CalledProcessError:
        print("EPAng did NOT finish successfully:\n", subprocess.CalledProcessError)
        sys.exit(1)

    # get rid of log file. Not needed; auto-created by epang
    os.remove(os.path.join(out_dir, "epa_info.log"))
    # so results can be called after runEPANG() function is run in line
    runEPANG.placements = os.path.join(out_dir, "placements.jplace")
    # rename so that the name of pplacer and epang output are identical
    shutil.move(os.path.join(out_dir, "epa_result.jplace"), runEPANG.placements)
