#!/bin.bash
#$ -cwd                 # workingDirectory
#$ -j y
#$ -N wings
#$ -S /bin/bash
#$ -q all.q             # queueName
#$ -pe mpi 32           # cpuNumber
#$ -l h_rt=10:00:00

module use /software/spack/spack/share/spack/modules/linux-rocky8-sandybridge/
module load openfoam

# #!/bin/bash
localDir='/global-scratch/USER/CASE'
