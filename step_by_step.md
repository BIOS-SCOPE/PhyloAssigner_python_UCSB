## STEP by STEP guide - PhyloAssigner for absolute beginners

### 1) Install conda

if you have conda already installed, e.g. if you used it to install a pipline like Qiime2 through conda, you can move on to step 2).

Download the installer for linux from: https://docs.conda.io/en/latest/miniconda.html#linux-installers

How? 
One easy way of achieving this can be the tool wget. Log into your linux machine / cluster. 
Most clusters do have 'wget' pre-installed, so this line should work if you just copy-paste it: 

```{bash}
wget https://repo.anaconda.com/miniconda/Miniconda3-py39_4.12.0-Linux-x86_64.sh
```

This will download a file called 'Miniconda3-py39_4.12.0-Linux-x86_64.sh' into whatever directory you are currently in. 
Next, install conda:

```{bash}
bash Miniconda3-py39_4.12.0-Linux-x86_64.sh
```

After you have finished the installation process (you can press yes whenever conda asks you something during this), you should see "(base)" at the beginning of your commandline handle. If not, log out and in again. If you still don't see the "(base)" at the beginning of the command-line, try:

```{bash}
conda activate base
```

Now you should have conda installed and activated on your system. Conda is called a 'package manager', it does handle all the annoying parts of installing a bioinformatics tool on your machine for you, so you don't have to worry about all of PhyloAssigners dependencies and having to make sure that they have been installed with the correct version and path, etc.


### 2) Dowloading the reference databases

At some later point, this step will become obsolete, but for now, you have to download all the PhyloAssigner reference databases from github and get them on your machine.
Download this [github repository](https://github.com/BIOS-SCOPE/PhyloAssigner_python_UCSB) as a zip file (press on the green "code" button and select zip).


### 3) upload it to your cluster

If you are planning to run PhyloAssigner on a cluster, you will have to upload this git onto your account. I recommend using 'scp' for this. Open a Terminal window and do NOT log into your cluster account. Go into your downloads folder (the path to that differs between maschines, but for Mac '~/Downloads/' will often do the trick. Make sure you are in the same folder as the ZIP file you downloaded. Then, run 'scp' to upload the ZIP file.

example:

```{bash}
scp -r PhyloAssigner_python_UCSB-main.zip USERNAME@SERVERADRESSE:DIRECTORY/
```

*Note*: you have to edit the command above to contain your username and serveradresse. If you log into your cluster using 'ssh' your username and adresse used there will be identical to what you have to fill in here. Then, after the colon, you have to provide the path on the cluster you want to save the ZIP folder to. If you don't know your path, log into your cluster account and enter: 'pwd'. This will print your current location, you can copy paste that behind the colon, replacing 'DIRECTORY/'.


### 4) creating the PhyloAssigner environment

Go into your terminal where you are logged into your cluster account / machine. Move to the directory where you uploaded the ZIP folder and unpack it:

```{bash}
unzip PhyloAssigner_python_UCSB-main.zip
```
Now, move into the folder you just unpacked. If you list the contents of that directory, you should see a few files, included a *.yml* and a *.py* file:

```{bash}
cd PhyloAssigner_python_UCSB-main
ls
#databases  modules  pythonassigner_v0.9.py  pythonassignler_linux.yml  README.md
```

The *yml* file is what we will use to install PhyloAssigner and all it's dependencies. The *py* file is the actual PhyloAssigner tool that we will run later on. Please keep the other files, included the two folders included in the git (modules and databases). They contain all the reference databases and python code that the tool is using and relying on.

Us the *.yml* script to install the correct virtual environment for PhyloAssigner:

```
conda env create -f pythonassignler_linux.yml
```

This will take a few minutes and there will be a lot of hashtags on your screens. In the end, conda will tell you how to activate your now newly created environment:

```{bash}
conda activate pythonassigner
```

Whenever you want to run PhyloAssigner, you have to make sure you activate this environment before. You will see it at the beginning of your commandline, just like the '(base)' environment before. If that is not the case, PhyloAssigner will crash directly and not do anything.
If you forget the name of the correct environment and to get an overview of all your environments, use:

```{bash}
conda info --envs
conda list
```
The first command will list all available environments, which can be turned on by using 'conda activate'. 'conda list' will give a list of all tools installed in your currently activated environment. To deactivate an environment, use 'conda deactivate'.


### 5) running a test

if you finished setting up your conda environment you are good to use PhyloAssigner. When running the script, make sure you call the script in the folder, or direct python to the folder, if you are not. It is not a global variable like some other tools, so you have to let python know where PhyloAssigner is (this will change with a later version of the tool, too).
For example, if you are in a directory that contains the folder 'PhyloAssigner_python_UCSB-main', to start PhyloAssigner, you have to run:

```{bash}
python PhyloAssigner_python_UCSB-main/pythonassigner_v0.9.py -h
```

If you are in the folder PhyloAssigner_python_UCSB-main, meaning you are in the same directory as 'pythonassigner_v0.9.py', you can start PhyloAssigner like this:

```{bash}
python pythonassigner_v0.9.py -h
```

Both of these commands will print the PhyloAssigner help message.

To run a real test, with a few sample ASVs, try:

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

If you want to run a different reference database, you can switch out the name of the database in the example command. If you want to run your own ASVs, just direct PhyloAssigner to those and it will use them instead. I recommend sticking to 'PPlacer' as your placement tool here, since EPA-ng is not tested in this version. You can of course also change the name of your output directory to whatever you prefer. Note: If you run PhyloAssiger in the same directory without changing the output directory name or without deleting the old output directory it will crash since PhyloAssigner does NOT overwrite directories that already exist.

Your PhyloAssinger output directory should have multiple output files. It contains some files only used for more advanced questions, but the two relevant files for you are: 

best_placements.tsv, which looks something like this:
```
edge_num  like_weight_ratio  ASV_id  taxon
1253      0.541737014346     seq5    SAR_11;SAR11_Ib
324       0.333517737163     seq4    NA
2026      0.200078267914     seq3    Subsection_I;Prochlorococcus
1248      0.305134196819     seq2    SAR_11;SAR11_Ia
1225      0.142857232731     seq1    SAR_11;SAR11_Ia
```

and LCA_placements.tsv, which looks slightly different:

```
edge_num  ASV_id  taxon
2028      seq3    Subsection_I;Prochlorococcus
1250      seq2    SAR_11;SAR11_Ia
1255      seq5    SAR_11;SAR11_Ib
1225      seq1    SAR_11;SAR11_Ia
326       seq4    NA
```

The main difference is column two in the best_placements file. This column does not exist in the LCA_placements file. It can be interpreted as something like 'confidence', ranging between 0 and 1, with 1 beeing the best/highest confidence in a placement. The LCA placement is a more conservative approach and can be less exact (say, SAR11 instead of SAR11-1a in the best_placements), but is a bit more reliable. What you use for your analysis depends a bit on your question, but I am happy to discuss details on what sets these two appart.


### 6) running PhyloAssigner in SLURM

SLURM is an acronym, but I forgot the meaning. It does really matter, you can use it to submit jobs on computational cluster, including the systems used at UCSB and GEOMAR. It is fairly widespread but I don't know if your universities system relies on the same job manager or not, please check your IT departments website for this, or contact your institutions helpdesk. These websites generally also have a good chunk of how-to-use comments. Just very briefly, SLURM enables you to submit jobs to remote notes. You can then log out of your account and the job will keep running. To submit your phyloassigner command as a SLURM job, there can be many ways. A all-in-one approach can be this monstrocity:

```{bash}
sbatch \
	--job-name=phyloassigner \
	--nodes=1 \
	--tasks-per-node=1 \
	--cpus-per-task=1 \
	--mem=100G \
	--time=5:00:00 \
	--output=phyloassigner_out \
	--error=phyloassigner_err \
	--wrap="python pythonassigner_v0.9.py \
    --out_dir example_output/ \
    --ref_align databases/Global_16S_refDB/ref.aln \
    --ref_tree databases/Global_16S_refDB/ref_tree.txt \
    --query_seqs your_ASVs.fasta \
    --mapping databases/Global_16S_refDB/edge.mapping \
    --threads 32 \
    --placer pplacer"
```

Please let me know if you run into issues with this or if you need more context for a part of this STEP by STEP guide.

### BONUS: subsetting fasta files

I included all available PhyloAssigner databases in this git repostitory. Note that you should not place all of your ASVs on a database made only for SAR11. Instead, place your ASVs on the Global tree, pull out all SAR11 placements, and place only those on the SAR11 tree, to get higher resolution for their taxonomy than what the Global tree can provide.

To subset all SAR11 ASVs from the test ASV file provided in this git, try:

```{bash}
cat example_output/LCA_placements.tsv | grep "SAR11" | awk '{print $2}' | seqtk subseq your_ASVs.fasta  - > SAR11.fasta
```

You will have to install 'seqtk' for this. This should be straight forward: 'conda install -c bioconda seqtk' 

-> have fun! And never forget: Crying & working in the command-line go hand in hand
