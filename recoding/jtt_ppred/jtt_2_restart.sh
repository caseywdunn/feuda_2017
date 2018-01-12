#!/bin/bash
#SBATCH --job-name=jtt_2

#SBATCH --partition=scavenge
#SBATCH --constraint=avx2
#SBATCH --ntasks=200

#SBATCH --mem-per-cpu=6G
#SBATCH --time=7-00:00:00


module load PhyloBayes-MPI

srun --mpi=pmi2 pb_mpi jtt_2
