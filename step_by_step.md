
1) Install conda. 
  + download the installer for linux from: https://docs.conda.io/en/latest/miniconda.html#linux-installers
  + upload this file to your cluster

2) Download this github repository as https://github.com/BIOS-SCOPE/PhyloAssigner_python_UCSB

3) upload it to your cluster

example:
```{bash}
scp -r PhyloAssigner_python_UCSB-main.zip USERNAME@nesh-fe.rz.uni-kiel.de:/gxfs_work1/geomar/smomw421
```
*Note* make 

4) core conda commands 

```{bash}
conda info --envs # gives you a list 
conda list
```


5) core slurm commands

```{bash}
squeue #prints all jobs currently submitted
squeue -u USERNAMER #prints all jobs submitted by USERNAME
scancel JOBID #cancels a job
sbatch #to submit a job, see detailed code example below
