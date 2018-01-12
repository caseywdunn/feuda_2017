#!/bin/bash
#SBATCH --job-name=jtt_2

#SBATCH --partition=scavenge
#SBATCH --constraint=avx2
#SBATCH --ntasks=200

#SBATCH --ntasks-per-node=16
#SBATCH --mem-per-cpu=6G
#SBATCH --time=7-00:00:00


module load PhyloBayes-MPI

srun --mpi=pmi2 pb_mpi -jtt -ncat 1 -dgam 4 -d WhelanD20_AA.phy jtt_2
