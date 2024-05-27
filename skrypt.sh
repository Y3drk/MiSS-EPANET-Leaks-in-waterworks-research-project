#!/bin/bash -l
## sbatch -N 1 --mem-per-cpu=2GB -A plgwtdydoptym-cpu -p plgrid-now -n 48 -t 12:00:00
#SBATCH -N 1
#SBATCH --mem-per-cpu=2GB
#SBATCH -A plgwtdydoptym-cpu
#SBATCH -p plgrid-now 
#SBATCH -n 48 
#SBATCH -t 12:00:00

cd $SCRATCH
module load python/3.11.5-gcccore-13.2.0
module load epanet/2.2.0-gcc-13.2.0 
source ioenv/bin/activate
cd repo
python -m scoop genetic.py 48 10000
