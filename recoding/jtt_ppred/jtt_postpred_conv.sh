#!/bin/bash
#SBATCH --job-name=jtt_postpred_conv

#SBATCH --partition=general
#SBATCH --constraint=avx2
#SBATCH --ntasks=32

#SBATCH --mem-per-cpu=6G
#SBATCH --time=7-00:00:00


module load PhyloBayes-MPI




srun --mpi=pmi2 readpb_mpi -siteconvprob -x 200 5 jtt_1 > jtt_1_postpred_conv.out
srun --mpi=pmi2 readpb_mpi -siteconvprob -x 200 5 jtt_2 > jtt_2_postpred_conv.out
