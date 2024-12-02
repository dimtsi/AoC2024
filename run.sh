#!/bin/bash


day_dir=Day$1

clear && export PYTHONPATH=$(pwd) && python $day_dir/run.py
