#!/bin/bash
#$ -N mesh_independence
#$ -l h_rt=20:00:00

CORES=$1

mkdir -p ../../mesh_independence

OLDIFS=$IFS
IFS=','
for tuple in 30,20 35,24 25,16 20,12 15,9 10,6; do
    set -- $tuple
    echo "##### Running simulation with (NX, NY)=($1, $2) #####"

    # Run
    cp -f system/blockMeshDict.orig system/blockMeshDict
    sed -i "s/NX/$1/; s/NY/$2/" system/blockMeshDict
    ./cluster_run.sh $CORES

    # Copy results
    cp -rf postProcessing ../../mesh_independence/postProcessing_${1}_${2}
    ./Allclean
done
IFS=$OLDIFS

./Allclean -a
