#!/usr/bin/python3

# parse_codeml_M0_M3.py

# Hsin-Ying Chang <hyhazelchang@gmail.com>
# v1 2023/05/19
# v2 2023/05/31 modify the parsing results

# Usage: python3 /home/xinchang/pyscript_xin/parse_codeml_M0_M3.py --M0_M3_dir=/scratch/xinchang/cyano11/cyano11.17/codeml/M0_M3 --data_ext=codeml --NSsites="0 3" --output=/scratch/xinchang/cyano11/cyano11.17/codeml/M0_M3_result

import argparse
import os
import glob

def main():
    parser = argparse.ArgumentParser(
        description=("Parse data of codeml site models."),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--M0_M3_dir",
                        default=None,
                        type=str,
                        help="Directory containing data file. Please provide absolute path.")
    parser.add_argument("--data_ext",
                        default="codeml",
                        type=str,
                        help="Extension of data files.")
    parser.add_argument("--NSsites",
                        default=None,
                        type=str,
                        help="Please provide the NSsites setting in control setting.")
    parser.add_argument("--output",
                        default="./M_s_output",
                        type=str,
                        help="Output directory. Please provide absolute path.")

    args = parser.parse_args()
    M0_M3_dir = args.M0_M3_dir
    models = args.NSsites.split()
    data_ext = args.data_ext
    output = args.output

    # Find data locations
    data_file = glob.glob(os.path.join(M0_M3_dir, "*"))

    # Check output directory
    if not os.path.exists(output):
        os.system("mkdir -p " + output)

    # Parse the models setting
    for i in range(len(models)):
        models[i] = "NSsites Model " + models[i]
    print(models)

    # Parse data in the files
    for model in models:
        if model == "NSsites Model 0":           
            data = [["gene", "lnL", "dN/dS"]]  # headers
            for file in data_file:
                filename = os.path.basename(file)
                parsing_M0 = parse_M0(file, filename, data_ext, model)
                data.append(parsing_M0)
            # Write into output
            M0_output = output + "/M0_result.tsv"
            out = open(M0_output, "w")
            for line in data:
                out.write("\t".join(line) + "\n")
            out.close()

        if model == "NSsites Model 3":
            data = [["gene", "lnL"]]  # headers
            for file in data_file:
                filename = os.path.basename(file)
                parsing_M3 = parse_M3(file, filename, data_ext, model)
                data.append(parsing_M3)
            # Write into output
            M3_output = output + "/M3_result.tsv"
            out = open(M3_output, "w")
            for line in data:
                out.write("\t".join(line) + "\n")
            out.close()

def parse_M0(file, filename, data_ext, model):
    codeml_file = os.path.join(file + "/" + filename + "." + data_ext)
    codeml = [line.rstrip("\n") for line in open(codeml_file)]
    parsing_M0 = []
    parsing_M0.append(filename)
    for line in codeml:
        if model in line:
            count = codeml.index(line)
            count += 3
            if "check convergence" in codeml[count]:
                count += 1
            value = codeml[count].split()
            parsing_M0.append(value[4])
        if "omega (dN/dS)" in line:
            omega = line.split()
            parsing_M0.append(omega[3])            
    return parsing_M0

def parse_M3(file, filename, data_ext, model):
    codeml_file = os.path.join(file + "/" + filename + "." + data_ext)
    codeml = [line.rstrip("\n") for line in open(codeml_file)]
    parsing_M3 = []
    parsing_M3.append(filename)
    for line in codeml:
        if model in line:
            count = codeml.index(line)
            count += 3
            if "check convergence" in codeml[count]:
                count += 1
            value = codeml[count].split()
            parsing_M3.append(value[4])
    return parsing_M3

if __name__ == "__main__":
    main()