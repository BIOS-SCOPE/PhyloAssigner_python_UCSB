# PhyloAssigner_python_UCSB

+ code&instructions by Fabian Wittmers

### background

This repository contains a working version of PhyloAssigner. The tool produces results that are comparable with the original version of this tool as published in 2013 by Kevin Vergin (Vergin et al. 2013). 
It does not rely on any of the old code and is written in fully written in python3, resulting in a more userfriendly application and easier installation.
This rewrite includes a small bugfix on how the old perl-code handled the computation of LCA placements, but runs on the same basic principle as the original PhyloAssigner.

### installation

PhyloAssigner handles alignment, reformatting, placement and output summary all within one command and therefore relies on some dependencies. I advice to run PhyloAssigner on a linux system, idealy a cluster with a good chunk of RAM, although it can run on low RAM systems just fine (will just take longer). It installation is simple, all dependencies can be installed in 1 command by creating a new conda environment to run PhyloAssigner in.

```{bash}
conda env create -f pythonassignler_linux.yml
```

### command structure

```{bash}
usage: pythonassigner_v0.9.py [-h] -o OUT_DIR -r REF_ALIGN -t REF_TREE -q
                              QUERY_SEQS -m MAPPING [-T THREADS] [-p PLACER]

run PythonAssigner through the command-line. This is an updated version of PhyloAssigner, 
    originally written in 2012 in perl. See: Vergin et al. 2013 supplementary information for more details; Rewritten 
    in python3 by Fabian Wittmers 2021/2022 

optional arguments:
  -h, --help            show this help message and exit
  -o OUT_DIR, --out_dir OUT_DIR
                        output directory were result files should be stored
  -r REF_ALIGN, --ref_align REF_ALIGN
                        reference alignment file. Must contain the same
                        sequence identifiers as in the reference tree
  -t REF_TREE, --ref_tree REF_TREE
                        reference tree file (newick formatted). Must contain
                        the same sequence identifiers as in the reference
                        alignment
  -q QUERY_SEQS, --query_seqs QUERY_SEQS
                        fasta file of sequences you want to place on reference
                        tree
  -m MAPPING, --mapping MAPPING
                        taxonomy mapping file: edge number in first column +
                        corresponding taxonomy in second column. If edge is a
                        tip, then tip label in third.
  -T THREADS, --threads THREADS
                        specify the number of threads to use in parallel
                        computation steps
  -p PLACER, --placer PLACER
                        specify which placement algorithm to use, choose
                        between 'pplacer' or 'epang'. Alternatively, you can
                        run 'compare' mode to compare both placement
                        algorithms
```

### currently available databases

This git contains a collection of placement reference trees build by different members of the WordenLab, Luis Bolanos, and Kevin Vergin.

Currently available databases (and the paper in which they were published) comprise:
+ Global 16S
  + Vergin et al. 2013; "High-resolution SAR11 ecotype dynamics at the Bermuda Atlantic Time-series Study site by phylogenetic placement of pyrosequences"
+ SAR11
  + Bolanos et al. 2021; "Seasonality of the Microbial Community Composition in the North Atlantic"
  + see: https://github.com/lbolanos32/NAAMES_2020
+ SAR202
  + Landy et al. 2017; "SAR202 Genomes from the Dark Ocean Predict Pathways for the Oxidation of Recalcitrant Dissolved Organic Matter"
  + see: https://github.com/lbolanos32/NAAMES_2020
+ Dictyochophyceae (16S plastid)
  + Choi et al. 2021; "Seasonal and Geographical Transitions in Eukaryotic Phytoplankton Community Structure in the Atlantic and Pacific Oceans"
+ Pelagophyceae (16S plastid)
  + Choi et al. 2021; "Seasonal and Geographical Transitions in Eukaryotic Phytoplankton Community Structure in the Atlantic and Pacific Oceans"
+ Stramenopiles (16S plastid)
  + Choi et al. 2021; "Seasonal and Geographical Transitions in Eukaryotic Phytoplankton Community Structure in the Atlantic and Pacific Oceans"
+ Cyanobacteria
  + Sudek et al. 2015; "Cyanobacterial distributions along a physico-chemical gradient in the Northeastern Pacific Ocean" 
+ Prochlorococcus
  + *Worden Lab; unpublished* (Strauss&Choi et al. submitted)
+ Cyanobacteria + Plastid
  + Sudek et al. 2015; "Cyanobacterial distributions along a physico-chemical gradient in the Northeastern Pacific Ocean"
  + Choi et al. 2017; "Newly discovered deep-branching marine plastid lineages are numerically rare but globally distributed"
+ Viridiplantae (16S plastid)
  + *Worden Lab; unpublished*
+ Chrysophyceae (16S plastid)
  + *Worden Lab; unpublished*
+ Synechococcus  
  + *Worden Lab; unpublished* 

### command example

PhyloAssigner requires 3 reference files, that are part of each PhyloAssigner database in this git:

+ reference tree
  + reference phylogeny to place the ASVs on 
+ reference alignment
  + alignment that was used to reconstruct the reference tree
+ reference mapping
  + connects each edge in the tree with its corresponding label that shall be printed in the results

Those 3 input files are provided. In addition, the user is required to provide an output directory. Optional arguments include the number of threads to use (for the alignment of query and reference sequences) and what placement algorithm to use. The default placement algorithm is PPLACER, so the user does not have to specify it.

```{bash}
python pythonassigner_v0.9.py \
    --out_dir example_output/ \
    --ref_align databases/Global_16S_refDB/ref.aln \
    --ref_tree databases/Global_16S_refDB/ref_tree.txt \
    --query_seqs your_ASVs.fasta \
    --mapping databases/Global_16S_refDB/edge.mapping \
    --threads 32 \
    --placer pplacer
```

### 16S region compatibility

Most of the reference databases provided here have been created over multiple years and they do differ in the 16S region that they are suitable for. Some alignments are specific to the v1v2 region, while others can be used for the v4 or v4v5 region as well. Here is an overview of which databases can be used for which regions: 

+ Global
  + available: 16S v1v2
  + validated: 16S v1v2
+ SAR11
  + available: 16S full_length
  + validated: 16S v1v2 & 16S v4 (on full length alignment)
  + see [here](https://github.com/lbolanos32/NAAMES_2020) for the originally published database, reformatted for the python3 version of phyloassigner now
+ SAR202
  + available: 16S full_length
  + validated: 16S v1v2 & 16S v4 (on full length alignment)
  + see [here](https://github.com/lbolanos32/NAAMES_2020) for the originally published database, reformatted for the python3 version of phyloassigner now
+ Dictyochophyceae
  + available: 16S full_length
  + validated: 16S v1v2 (on full length alignment)
+ Pelagophyceae
  + available: 16S v1v2 & 16S full_length
  + validated: 16S v1v2
+ Stramenopiles
  + available: 16S v1v2 & 16S full_length
  + validated: 16S v1v2
+ Cyanobacteria
  + available: 16S v1v2 & 16S full_length
  + validated: 16S v1v2
+ Prochlorococcus
  + available: 16S v1v2 & 16S full_length
  + validated: 16S v1v2
+ Cyanobacteria + Plastid
  + available: 16S v1v2 & 16S full_length
  + validated: 16S v1v2
+ Viridiplantae
  + available: 16S v1v2 & 16S full_length
  + validated: 16S v1v2

per default, PhyloAssigner currently runs for the v1v2 region. If you want to run amplicons from a different region, some modifications will be necessary for all reference databases that are not validated for the 16S v1v2 region. If a 16S full_length alignment is available these changes can be implemented so please reach out to the author of this git if this becomes relevant to you.
