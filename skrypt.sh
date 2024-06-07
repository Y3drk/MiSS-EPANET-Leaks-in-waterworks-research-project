#!/bin/bash -l
#SBATCH -N 1
#SBATCH --mem-per-cpu=2GB
#SBATCH -A plgwtdydoptym-cpu
#SBATCH -p plgrid 
#SBATCH -n 48 
#SBATCH -t 72:00:00
cd $SCRATCH
module load python/3.11.5-gcccore-13.2.0
module load epanet/2.2.0-gcc-13.2.0 
source ioenv/bin/activate
cd repo
python -m scoop genetic.py 48 10000
