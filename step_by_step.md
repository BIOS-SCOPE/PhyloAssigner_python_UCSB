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

```

```

### 2) Dowloading the reference databases

Download this [github repository](https://github.com/BIOS-SCOPE/PhyloAssigner_python_UCSB) as a zip file (press on the green "code" button and select zip).

### 3) upload it to your cluster



example:

```{bash}
scp -r PhyloAssigner_python_UCSB-main.zip USERNAME@nesh-fe.rz.uni-kiel.de:/gxfs_work1/geomar/smomw421
```

*Note* make ......


### 4) core conda commands 

```{bash}
conda info --envs # gives you a list 
conda list
```


### 5) core slurm commands

```{bash}
squeue #prints all jobs currently submitted
squeue -u USERNAMER #prints all jobs submitted by USERNAME
scancel JOBID #cancels a job
sbatch #to submit a job, see detailed code example below
