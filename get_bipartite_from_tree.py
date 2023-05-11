#!/usr/bin/python3

# get_bipartite_from_tree.py

# Hsin-Ying Chang <hyhazelchang@gmail.com>
# notes: /home/xinchang/notes/python/pytest02_get_bipartite_from_tree.txt
# v1 2022/12/26
# v2 2022/12/28 simplify get_weight function
# v3 2022/04/10 

# Usage: python3 /home/xinchang/pyscript_xin/get_bipartite_from_tree.py --input_dir="/scratch/xinchang/hcyen/out/concatboot" --list_file="/scratch/xinchang/hcyen/list/testlist.list" --output_dir="/scratch/xinchang/hcyen/output"

import argparse
import os
import shutil
import glob

def main():
    parser = argparse.ArgumentParser(
        description=("Get bipartite from consense tree"),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--input_dir",
                        default=None,
                        type=str,
                        help="Directory containing consense.out files. Please provide absolute path.")
    parser.add_argument("--list_file",
                        default=None,
                        type=str,
                        help="Directory of list containing bipartite pairs. Please provide absolute path.")
    parser.add_argument("--output_dir",
                        default="./output",
                        type=str,
                        help="Directory for output files. Please provide absolute path.")

    args = parser.parse_args()

    # List for parsing bipartite pairs
    runs_list = [line.rstrip("\n") for line in open("%s" % args.list_file)]

    # Find input files from specific directory
    inputs = glob.glob(os.path.join("%s" % args.input_dir, "*.out" ))

    # Make output directory
    if not os.path.exists("%s" % args.output_dir):
        output = args.output_dir
        os.system("mkdir -p output")
    else:
        output = args.output_dir

    for in_file in inputs:
        file_name = os.path.basename(in_file)
        # Parse run order into a keys list
        lines, keys, new_count = parse_run_order(in_file)
        # Get weight of each branch
        weights, needed_weight = get_weight(runs_list, lines, keys, new_count)
        # Get index from weights
        branches_indices = get_index(weights, needed_weight)
        # Check results
        final_runs = check_results(keys, branches_indices)
        # Copy the file into output directory
        if set(final_runs) == set(runs_list):
            try:
                shutil.copyfile(in_file, os.path.join("%s" % output, "%s" % file_name))
                print("Copy %s into output file." % file_name)
            except shutil.SameFileError:
                print("Source and destination represents the same file.")
            except IsADirectoryError:
                print("Destination is a directory.")
            except PermissionError:
                print("Permission denied.")
            except:
                print("Error occurred while copying file.")
        else:
            print("%s does not contain the bipartites." % file_name)

def parse_run_order(in_file):
    lines = [line.rstrip("\n") for line in open(in_file)]
    keys = []
    for i in range(len(lines)):
        if lines[i] == "Species in order: ":
            count = i+2
            break   
    for j in range(count, len(lines)):
        if lines[j] == "Sets included in the consensus tree":
            new_count = j+4
            break
        keys.append(lines[j])
    # remove numbers and spaces from keys
    for num in range(len(keys)):
        if keys[num] == "":
            keys.pop(num)
        else:
            keys[num] = keys[num].replace("  "+str(num+1)+". ", "")
    return lines, keys, new_count

def get_weight(runs_list, lines, keys, new_count):
    weights = []
    for k in range(len(keys)):
        weights.append(0)
    for line in range(new_count, len(lines)):
        if lines[line] == "":
            break
        for weight in range(len(line)):
            if lines[line][weight] == "*":
                weights[weight] += 1
                
    sorted_weight = sorted(weights, reverse=True)
    needed_weight = [sorted_weight[weight] for weight in range(len(runs_list))]
    return weights, needed_weight

def get_index(weights, needed_weight):
    branches_indices = []
    for index in range(len(weights)):
        for weight in needed_weight:
            if weights[index] == weight :
                branches_indices.append(index)
                break
    return branches_indices

def check_results(keys, branches_indices):
    final_runs = []
    for index in branches_indices:
        final_runs.append(keys[index])
    return final_runs

if __name__ == "__main__":
    main()
