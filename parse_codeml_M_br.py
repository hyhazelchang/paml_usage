#!/usr/bin/python3

# parse_codeml_M_br.py

# Hsin-Ying Chang <hyhazelchang@gmail.com>
# v1 2023/05/12

# Usage: python3 /home/xinchang/pyscript/pyscript_xin/parse_codeml_M_br.py --M_br_dir="/scratch/xinchang/cyano11/cyano11.16/codeml/M_br" --data_ext="codeml" --output="/scratch/xinchang/cyano11/cyano11.16/codeml/M_br_result.tsv"

import argparse
import os
import glob

def main():
    parser = argparse.ArgumentParser(
        description=("Parse data of codeml branch model."),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--M_br_dir",
                        default=None,
                        type=str,
                        help="Directory containing data file. Please provide absolute path.")
    parser.add_argument("--data_ext",
                        default="codeml",
                        type=str,
                        help="Extension of data files.")
    parser.add_argument("--output",
                        default="./M_br_output",
                        type=str,
                        help="Output directory. Please provide absolute path.")

    args = parser.parse_args()
    M_br_dir = args.M_br_dir
    data_ext = args.data_ext
    output = args.output

    # Find data locations
    data_file = glob.glob(os.path.join(M_br_dir, "*"))

    # Header of the data
    data = [["gene", "lnL", "w0", "w1"]]

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
        if "w (dN/dS) for branches:" in line:
            value = line.split()
            parsing.append(value[4])
            parsing.append(value[5])
    return parsing

if __name__ == "__main__":
    main()
