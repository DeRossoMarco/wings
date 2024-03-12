#!/bin/bash
#$ -cwd
#$ -j y
#$ -N mesh_independence
#$ -S /bin/bash
#$ -q all.q             # queueName
#$ -pe mpi 16           # cpuNumber
#$ -l h_rt=20:00:00

module use /software/spack/spack/share/spack/modules/linux-rocky8-sandybridge/
module load openfoam

cd wing

for tuple in 25,16 20,12 15,9 10,6; do
    set -- $tuple
    echo "Running simulation with (Nx, Ny)=($1, $2)"
    cp system/blockMeshDict.orig system/blockMeshDict
    sed -i "s/Nx/$1/; s/Ny/$2/" system/blockMeshDict
    ./cluster_run.sh
    cp -r postProcessing ../postProcessing_${1}_${2}
    ./Allclean
done
