#!/bin/bash


day_dir=Day$1

mkdir $day_dir 
touch $day_dir/sample.txt 
touch $day_dir/input.txt 
sed "s/day = .*/day = $1/" run_template.py > $day_dir/run.py
