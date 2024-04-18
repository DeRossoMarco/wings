#!/bin/bash

# Parameters
CORES=16
SPEED=7.5
ANGLE=0
NX=25
NY=16
MAX_PROCESSES=32
MAX_ANGLE=20
ANGLE_STEP=5

# Variables
FLAG_ANGLE=false
FLAG_MESH=false
FLAG_PROCESSES=false

# QSUB parameters
OPTIONS="-cwd -j y -S /bin/bash -q all.q"

help()
{
    echo "Usage: run [-a] [-m] [-p [max_number_of_processes]] [--cores number_of_cores] [--speed speed_of_flow] [--angle angle_of_flow]"
    exit 0
}

SHORT=a::mp::h
LONG=cores:,speed:,angle:,help
VALID_ARGS=$(getopt -o $SHORT --long $LONG -- "$@")
if [[ $? -ne 0 ]]; then
    help
    exit 1;
fi

eval set -- "$VALID_ARGS"
while [ : ]; do
    case "$1" in
        -a)
            FLAG_ANGLE=true
            case "$2" in
                "")
                    shift 2
                    ;;
                *)
                    MAX_ANGLE=$2
                    shift 2
                    ;;
            esac
            ;;
        -m)
            FLAG_MESH=true
            shift
            ;;
        -p)
            FLAG_PROCESSES=true
            case "$2" in
                "")
                    shift 2
                    ;;
                *)
                    MAX_PROCESSES=$2
                    shift 2
                    ;;
            esac
            ;;
        --cores)
            CORES=$2
            shift 2
            ;;
        --speed)
            SPEED=$2
            shift 2
            ;;
        --angle)
            ANGLE=$2
            shift 2
            ;;
        --)
            shift
            break
            ;;
        -h | --help)
            help
            exit 0
            ;;
        :)
            echo -e "Option $1 requires an argument."
            help
            exit 1
            ;;
        *)
            echo -e "Invalid command option $1."
            help
            exit 1
            ;;
    esac
done

if $FLAG_ANGLE; then
    echo "*** RUNNING MULTIPLE ANGLES SIMULATION ***"
    cp wing/system/blockMeshDict.orig wing/system/blockMeshDict
    sed -i "s/NX/$NX/; s/NY/$NY/" wing/system/blockMeshDict
    cp wing/system/decomposeParDict.orig wing/system/decomposeParDict
    sed -i "s/CORES/$CORES/" wing/system/decomposeParDict
    qsub $OPTIONS -pe mpi $CORES multiple_angles.sh

elif $FLAG_MESH; then
    echo "*** RUNNING MESH INDEPENDENCE SIMULATION ***"
    cp wing/0.orig/include/initialConditions.orig wing/0.orig/include/initialConditions
    sed -i "s/ANGLE/$ANGLE/" wing/0.orig/include/initialConditions
    sed -i "s/SPEED/$SPEED/" wing/0.orig/include/initialConditions
    cp wing/system/decomposeParDict.orig wing/system/decomposeParDict
    sed -i "s/CORES/$CORES/" wing/system/decomposeParDict
    qsub $OPTIONS -pe mpi $CORES mesh_independence.sh

elif $FLAG_PROCESSES; then
    echo "*** RUNNING MULTIPLE PROCESSES SIMULATION ***"
    cp wing/0.orig/include/initialConditions.orig wing/0.orig/include/initialConditions
    sed -i "s/ANGLE/$ANGLE/" wing/0.orig/include/initialConditions
    sed -i "s/SPEED/$SPEED/" wing/0.orig/include/initialConditions
    cp wing/system/blockMeshDict.orig wing/system/blockMeshDict
    sed -i "s/NX/$NX/; s/NY/$NY/" wing/system/blockMeshDict
    qsub $OPTIONS -pe mpi $MAX_PROCESSES multiple_processes.sh

else
    echo "*** RUNNING SINGLE SIMULATION ***"
    cp wing/system/blockMeshDict.orig wing/system/blockMeshDict
    sed -i "s/NX/$NX/; s/NY/$NY/" wing/system/blockMeshDict
    cp wing/system/decomposeParDict.orig wing/system/decomposeParDict
    sed -i "s/CORES/$CORES/" wing/system/decomposeParDict
    sed -i "s/CORES/$CORES/" wing/cluster_run.sh
    cp wing/0.orig/include/initialConditions.orig wing/0.orig/include/initialConditions
    sed -i "s/ANGLE/$ANGLE/" wing/0.orig/include/initialConditions
    sed -i "s/SPEED/$SPEED/" wing/0.orig/include/initialConditions
    cd wing
    qsub $OPTIONS -pe mpi $CORES cluster_run.sh
fi
