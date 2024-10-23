#!/bin/bash
#$ -N multiple_processes
#$ -l h_rt=20:00:00

MAX_PROCESSES=$1

rm -rf ../../multiple_cores && mkdir -p ../../multiple_cores

for (( CORES=2; CORES<=$MAX_PROCESSES; CORES*=2 )) do
        echo "##### Running simulation with $CORES cores #####"
        cp -f system/decomposeParDict.orig system/decomposeParDict
        sed -i "s/CORES/$CORES/" system/decomposeParDict
        ./cluster_run.sh $CORES
        # Copy results
        mkdir ../../multiple_cores/${CORES}
        cp -rf postProcessing ../../multiple_cores/${CORES}/postProcessing
        cp -rf log ../../multiple_cores/${CORES}/log
        ./Allclean
    done

./Allclean -a
