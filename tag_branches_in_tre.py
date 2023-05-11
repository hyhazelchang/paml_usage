#!/usr/bin/python3

# tag_branches_in_tre.py

# Hsin-Ying Chang <hyhazelchang@gmail.com>
# notes: /home/xinchang/notes/python/pytest07_tag_branches_in_tre.txt
# v1 2023/05/09

# Usage: python3 /home/xinchang/pyscript/pyscript_xin/tag_branches_in_tre.py --input_dir="/scratch/xinchang/cyano11/cyano11.16/test/new_tree" --list_file="/scratch/xinchang/cyano11/cyano11.16/test/tags.list" --output_dir="/scratch/xinchang/cyano11/cyano11.16/test/tagged_trees"

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
                        help="Directory containing tree files. Please provide absolute path.")
    parser.add_argument("--list_file",
                        default=None,
                        type=str,
                        help="Directory of list containing group. Place groups by order (one group per line); ex: #0 in the first line, #1 in the second line. Please provide absolute path.")
    parser.add_argument("--output_dir",
                        default="./tagged_trees",
                        type=str,
                        help="Directory for output files. Please provide absolute path.")

    args = parser.parse_args()

    # List for groups
    group_ls = args.list_file
    groups = []
    for line in open(group_ls):
        group = line.rstrip("\n").split(",")
        groups.append(group)

    # Find input files from specific directory
    inputs = glob.glob(os.path.join("%s/" % args.input_dir, "*.tre" ))

    # Make output directory
    output = args.output_dir
    if not os.path.exists(output):
        os.system("mkdir -p " + output)
        
    for tre in inputs:
        file_name = os.path.basename(tre).split(".")[0]
        # Parse tree files
        tree = parse_trefile(tre)
        # Tag the branches
        tagged_tree = tag_the_branches(tree, groups)
        # Write into a new tree file
        new_tre = open("%s/%s.tagged.tre" % (output, file_name), "w")
        new_tre.write(tagged_tree)
        new_tre.close()

def parse_trefile(tre):
    for line in open(tre):
        tree = line.rstrip("\n")
    # get branch
    tree = tree.split(",")
    return tree

def tag_the_branches(tree, groups):    
    # tag the branches
    for num in range(len(tree)):
        for i in range(len(groups)):
            for group in groups[i]:
                tag = " #" + str(i)
                if group in tree[num]:
                    tree[num] = tree[num].replace(group, group + tag)

    tagged_tree = ",".join(tree)
    return tagged_tree

if __name__ == "__main__":
    main()
