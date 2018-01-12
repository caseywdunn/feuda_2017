#!/bin/bash
#SBATCH --job-name=jtt_postpred

#SBATCH --partition=general
#SBATCH --constraint=avx2
#SBATCH --ntasks=50

#SBATCH --mem-per-cpu=6G
#SBATCH --time=7-00:00:00


module load PhyloBayes-MPI




srun --mpi=pmi2 readpb_mpi -div -x 200 5 jtt_1 > jtt_1_postpred_div.out
srun --mpi=pmi2 readpb_mpi -div -x 200 5 jtt_2 > jtt_2_postpred_div.out
