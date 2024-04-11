#!/bin/bash
#$ -cwd
#$ -j y
#$ -N mesh_independence
#$ -S /bin/bash
#$ -q all.q             # queueName
#$ -pe mpi CORES        # cpuNumber
#$ -l h_rt=20:00:00

cd wing

OLDIFS=$IFS
IFS=','
for tuple in 30,20 35,24 25,16 20,12 15,9 10,6; do
    set -- $tuple
    echo "Running simulation with (Nx, Ny)=($1, $2)"

    # Run
    cp system/blockMeshDict.orig system/blockMeshDict
    sed -i "s/Nx/$1/; s/Ny/$2/" system/blockMeshDict
    ./cluster_run.sh

    # Copy results
    cp -r postProcessing ../../mesh_independence/postProcessing_${1}_${2}
    ./Allclean
done
IFS=$OLDIFS
