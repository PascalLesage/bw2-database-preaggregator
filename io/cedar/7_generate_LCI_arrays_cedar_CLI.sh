#!/bin/bash
#SBATCH --account=def-ciraig1
#SBATCH --time=23:59:00
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=40
#SBATCH --mem-per-cpu=2G
#SBATCH --array=21, 38, 39

module load python/3.6
virtualenv --no-download $SLURM_TMPDIR/env
source $SLURM_TMPDIR/env/bin/activate
pip install --upgrade pip --no-index
pip install click --no-index
pip install brightway2 --no-index
pip install bw2speedups --no-index
pip install presamples --no-index
pip install -e bw2_preagg

export LANG=en_CA.UTF-8

BRIGHTWAY2_DIR=/home/plesage/projects/def-ciraig1/plesage/bw2dir
export BRIGHTWAY2_DIR=$BRIGHTWAY2_DIR

cd bw2preagg_CLI
python generate_LCI_samples_CLI.py --project_name=ei36co --database_name=ei36co --result_dir=/home/plesage/scratch/preagg_ei36co --samples_batch=7 --parallel_jobs=4 --number_of_slices=$SLURM_ARRAY_TASK_COUNT --slice_id=$SLURM_ARRAY_TASK_ID