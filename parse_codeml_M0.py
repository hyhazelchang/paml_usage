#!/usr/bin/python3

# parse_codeml_M0_sh.py

# Hsin-Ying Chang <hyhazelchang@gmail.com>
# v1 2023/05/12
# v2 2023/05/31

# Usage: python3 /home/xinchang/pyscript_xin/parse_codeml_M0.py --M0_dir=/scratch/xinchang/cyano11/cyano11.16/codeml/M0 --data_ext=codeml --output=/scratch/xinchang/cyano11/cyano11.16/codeml/M0_result


import argparse
import os
import glob

def main():
    parser = argparse.ArgumentParser(
        description=("Parse data of codeml M0 model."),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--M0_dir",
                        default=None,
                        type=str,
                        help="Directory containing data file. Please provide absolute path.")
    parser.add_argument("--data_ext",
                        default="codeml",
                        type=str,
                        help="Extension of data files.")
    parser.add_argument("--output",
                        default="./M0_output",
                        type=str,
                        help="Output directory. Please provide absolute path.")

    args = parser.parse_args()
    M0_dir = args.M0_dir
    data_ext = args.data_ext
    output = args.output

    # Find data locations
    data_file = glob.glob(os.path.join(M0_dir, "*"))

    # Header of the data
    data = [["gene", "lnL", "dN/dS"]]

    # Parse data in the files
    for file in data_file:
        filename = os.path.basename(file)
        parsing = parse(file, filename, data_ext)
        data.append(parsing)

    # Write into output
    out = open(output, "w")
    for line in data:
        out.write("\t".join(line) + "\n")
    out.close()

def parse(file, filename, data_ext):
    codeml_file = os.path.join(file + "/" + filename + "." + data_ext)
    codeml = [line.rstrip("\n") for line in open(codeml_file)]
    parsing = []
    parsing.append(filename)
    for line in codeml:
        if "lnL" in line:
            value = line.split()
            parsing.append(value[4])
        if "omega" in line:
            value = line.split()
            parsing.append(value[3])
    return parsing

if __name__ == "__main__":
    main()
