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

### currently available databases

This git contains a collection of placement reference trees build by different members of the WordenLab, Luis Bolanos, and Kevin Vergin.

Currently available databases (and the paper in which they were published) comprise:
+ Global 16S
  + Vergin et al. 2013; "High-resolution SAR11 ecotype dynamics at the Bermuda Atlantic Time-series Study site by phylogenetic placement of pyrosequences"
+ SAR11
  + Bolanos et al. 2021; "Seasonality of the Microbial Community Composition in the North Atlantic"
+ SAR202
  + Landy et al. 2017; "SAR202 Genomes from the Dark Ocean Predict Pathways for the Oxidation of Recalcitrant Dissolved Organic Matter"
+ Chrysophyceae (16S plastid)
  + *Worden Lab; unpublished*
+ Dictyochophyceae (16S plastid)
  + Choi et al. 2017; "Seasonal and Geographical Transitions in Eukaryotic Phytoplankton Community Structure in the Atlantic and Pacific Oceans"
+ Pelagophyceae (16S plastid)
  + Choi et al. 2017; "Seasonal and Geographical Transitions in Eukaryotic Phytoplankton Community Structure in the Atlantic and Pacific Oceans"
+ Stramenopiles (16S plastid)
  + Choi et al. 2017; "Seasonal and Geographical Transitions in Eukaryotic Phytoplankton Community Structure in the Atlantic and Pacific Oceans"
+ Cyanobacteria
  + Sudek et al. 2015; "Cyanobacterial distributions along a physico-chemical gradient in the Northeastern Pacific Ocean" 
+ Prochlorococcus
  + *Worden Lab; unpublished* 
+ Cyanobacteria + Plastid
  + Sudek et al. 2015; "Cyanobacterial distributions along a physico-chemical gradient in the Northeastern Pacific Ocean"
  + Choi et al. 2017; "Newly discovered deep-branching marine plastid lineages are numerically rare but globally distributed"
+ Viridiplantae (16S plastid)
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
    --ref_align databases/Global_16S_refDB/ref.fasta \
    --ref_tree databases/Global_16S_refDB/ref_tree.txt \
    --query_seqs your_ASVs.fasta \
    --mapping databases/Global_16S_refDB/edge.mapping \
    --threads 32 \
    --placer pplacer
```
