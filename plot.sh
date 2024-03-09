#!/bin/bash
file1="cdcl.txt"
output="graph.png"
gnuplot << EOFset terminal pngcairo enhanced font 'Arial,12'
set output "$output"set xlabel "Valori sull'asse x"
set ylabel "Valori sull'asse y"plot "$file1" using 1:2 with lines title "f(x)"
EOF
