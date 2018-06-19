#!/bin/bash
#SBATCH --job-name=jtt_postpred

#SBATCH --partition=general
#SBATCH --constraint=avx2
#SBATCH --ntasks=100

#SBATCH --mem-per-cpu=6G
#SBATCH --time=7-00:00:00


module load PhyloBayes-MPI

for filename in ./*_mod_*.phy; do
  filename=$(basename "$filename")
	base="${filename%.*}"
	echo "processing $filename"
	srun --mpi=pmi2 pb_mpi  -x 1 5000 -cat -gtr -dgam 4 -d $filename $base.chain
	srun --mpi=pmi2 readpb_mpi -allppred -x 200 5 $base.chain > $base.ppred.out
done
