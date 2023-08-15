#!/bin/bash
#SBATCH --error=errors/%J.err --output=out_files/%J.out
#SBATCH --nodes=1
#SBATCH -J SDSS
#SBATCH -t 2:00:00
#SBATCH -C cpu
#SBATCH --qos=regular
#SBATCH --account=desi

cd /global/u2/c/crisjagq/
source ~/.bashrc

# set up for problem & define any environment variables here
cd /pscratch/sd/c/crisjagq/1er_Taller_DESI/TAD/Bloque2/demo/my_likelihood/
cosmodesi

# adding extra things
export OMP_PLACES=threads
export OMP_NUM_THREADS=256
export OMP_PROC_BIND=spread
export SETUPTOOLS_USE_DISTUTILS=stdlib
export OMPI_MCA_opal_cuda_support=0

# execute code
srun -n 4 cobaya-run BAORSD_lcdm.yaml -f