#!/usr/bin/python3

# parse_codeml_M_br_s.py

# Hsin-Ying Chang <hyhazelchang@gmail.com>
# v1 2023/05/12

# Usage: python3 /home/xinchang/pyscript/pyscript_xin/parse_codeml_M_br_s.py --M_br_s_dir="/scratch/xinchang/cyano11/cyano11.16/codeml/M_br_s" --data_ext="codeml" --output="/scratch/xinchang/cyano11/cyano11.16/codeml/M_br_s_result"

import argparse
import os
import glob

def main():
    parser = argparse.ArgumentParser(
        description=("Parse data of codeml branch-site model."),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--M_br_s_dir",
                        default=None,
                        type=str,
                        help="Directory containing data file. Please provide absolute path.")
    parser.add_argument("--data_ext",
                        default="codeml",
                        type=str,
                        help="Extension of data files.")
    parser.add_argument("--output",
                        default="./M_br_s_output",
                        type=str,
                        help="Output directory. Please provide absolute path.")

    args = parser.parse_args()
    M_br_s_dir = args.M_br_s_dir
    data_ext = args.data_ext
    output = args.output

    # Find data locations
    data_file = glob.glob(os.path.join(M_br_s_dir, "*"))

    # Header of the data
    data = [["gene", "lnL", "p0", "p1", "p2a", "p2b", "w0", "w1", "w2", "p2 is zero", "sites (p value > 0.95)", "sites (p value > 0.99)"]]

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
    site_95 = []
    site_99 = []
    parsing.append(filename)
    for line in codeml:
        if "lnL" in line:
            value = line.split()
            parsing.append(value[4])
        if "proportion" in line:
            value = line.split()
            parsing.append(value[1])
            parsing.append(value[2])
            parsing.append(value[3])
            parsing.append(value[4])
        if "foreground w" in line:
            fore_omega = line.split()
            parsing.append(fore_omega[2])
            parsing.append(fore_omega[3])
            parsing.append(fore_omega[4])
            parsing.append("1")
        if "note that p[2] is zero" in line:
            parsing[8] = "0"
        if "Bayes Empirical Bayes (BEB) analysis" in line:
            count = codeml.index(line) + 2
            while codeml[count] != '':
                site = codeml[count].split()
                site[2] = site[2].rstrip("*")
                if float(site[2]) > float(0.95):
                    site_95.append("".join(site[0:2]))
                if float(site[2]) > float(0.99):
                    site_99.append("".join(site[0:2]))                 
                count += 1
            parsing.append(", ".join(site_95))
            parsing.append(", ".join(site_99))
    return parsing

if __name__ == "__main__":
    main()
