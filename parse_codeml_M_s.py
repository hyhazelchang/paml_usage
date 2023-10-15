#!/usr/bin/python3

# parse_codeml_M_s.py

# Hsin-Ying Chang <hyhazelchang@gmail.com>
# v1 2023/05/19
# v2 2023/05/30 modify the parsing results

# Usage: python3 /home/xinchang/pyscript_xin/parse_codeml_M_s.py --M_s_dir=/scratch/xinchang/cyano11/cyano11.17/codeml/Ms --data_ext=codeml --NSsites="1 2 7 8" --output=/scratch/xinchang/cyano11/cyano11.17/codeml/Ms_result

import argparse
import os
import glob

def main():
    parser = argparse.ArgumentParser(
        description=("Parse data of codeml site models."),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--M_s_dir",
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
    M_s_dir = args.M_s_dir
    models = args.NSsites.split()
    data_ext = args.data_ext
    output = args.output

    # Find data locations
    data_file = glob.glob(os.path.join(M_s_dir, "*"))

    # Check output directory
    if not os.path.exists(output):
        os.system("mkdir -p " + output)

    # Parse the models setting
    for i in range(len(models)):
        models[i] = "NSsites Model " + models[i]
    print(models)

    # Parse data in the files
    for model in models:
        if model == "NSsites Model 1":           
            data = [["gene", "lnL", "dN/dS"]]  # headers
            for file in data_file:
                filename = os.path.basename(file)
                parsing_M1a = parse_M1a(file, filename, data_ext, model)
                data.append(parsing_M1a)
            # Write into output
            M1a_output = output + "/M1a_result.tsv"
            out = open(M1a_output, "w")
            for line in data:
                out.write("\t".join(line) + "\n")
            out.close()

        if model == "NSsites Model 2":
            data = [["gene", "lnL", "p0", "p2", "w0", "w2"]]  # headers
            for file in data_file:
                filename = os.path.basename(file)
                parsing_M2a = parse_M2a(file, filename, data_ext, model)
                data.append(parsing_M2a)
            # Write into output
            M2a_output = output + "/M2a_result.tsv"
            out = open(M2a_output, "w")
            for line in data:
                out.write("\t".join(line) + "\n")
            out.close()

        if model == "NSsites Model 7":           
            data = [["gene", "lnL", "p", "q"]]  # headers
            for file in data_file:
                filename = os.path.basename(file)
                parsing_M7 = parse_M7(file, filename, data_ext, model)
                data.append(parsing_M7)
            # Write into output
            M7_output = output + "/M7_result.tsv"
            out = open(M7_output, "w")
            for line in data:
                out.write("\t".join(line) + "\n")
            out.close()

        if model == "NSsites Model 8":
            data = [["gene", "lnL", "p", "q", "w"]]  # headers
            for file in data_file:
                filename = os.path.basename(file)
                parsing_M8 = parse_M8(file, filename, data_ext, model)
                data.append(parsing_M8)
            # Write into output
            M8_output = output + "/M8_result.tsv"
            out = open(M8_output, "w")
            for line in data:
                out.write("\t".join(line) + "\n")
            out.close()

def parse_M1a(file, filename, data_ext, model):
    codeml_file = os.path.join(file + "/" + filename + "." + data_ext)
    codeml = [line.rstrip("\n") for line in open(codeml_file)]
    parsing_M1a = []
    parsing_M1a.append(filename)
    for line in codeml:
        if model in line:
            count = codeml.index(line)
            count += 3
            if "check convergence" in codeml[count]:
                count += 1
            value = codeml[count].split()
            parsing_M1a.append(value[4])
            count += 28
            value = codeml[count].split()    
            parsing_M1a.append(value[4])
    return parsing_M1a

def parse_M2a(file, filename, data_ext, model):
    codeml_file = os.path.join(file + "/" + filename + "." + data_ext)
    codeml = [line.rstrip("\n") for line in open(codeml_file)]
    parsing_M2a = []
    parsing_M2a.append(filename)
    for line in codeml:
        if model in line:
            count = codeml.index(line)
            count += 3
            if "check convergence" in codeml[count]:
                count += 1
            value = codeml[count].split()
            parsing_M2a.append(value[4])
            count += 21
            while codeml[count] != '':
                p_w = codeml[count].split()
                parsing_M2a.append(p_w[1])
                parsing_M2a.append(p_w[3])                
                count += 1
                if "note" in codeml[count]:
                    count += 1
                    break
    return parsing_M2a

def parse_M7(file, filename, data_ext, model):
    codeml_file = os.path.join(file + "/" + filename + "." + data_ext)
    codeml = [line.rstrip("\n") for line in open(codeml_file)]
    parsing_M7 = []
    parsing_M7.append(filename)
    for line in codeml:
        if model in line:
            count = codeml.index(line)
            count += 3
            if "check convergence" in codeml[count]:
                count += 1   
            value = codeml[count].split()
            parsing_M7.append(value[4])
        if line == "Parameters in M7 (beta):":
            count = codeml.index(line)
            count += 1
            value = codeml[count].split()    
            parsing_M7.append(value[2])
            parsing_M7.append(value[5])
    return parsing_M7

def parse_M8(file, filename, data_ext, model):
    codeml_file = os.path.join(file + "/" + filename + "." + data_ext)
    codeml = [line.rstrip("\n") for line in open(codeml_file)]
    parsing_M8 = []
    parsing_M8.append(filename)
    for line in codeml:
        if model in line:
            count = codeml.index(line)
            count += 3
            if "check convergence" in codeml[count]:
                count += 1
            value = codeml[count].split()
            parsing_M8.append(value[4])
        if line == "Parameters in M8 (beta&w>1):":
            count = codeml.index(line) + 1
            p_w = codeml[count].split()
            parsing_M8.append(p_w[5])
            parsing_M8.append(p_w[8])                
            count += 1
            value = codeml[count].split()
            parsing_M8.append(value[5])
    return parsing_M8

if __name__ == "__main__":
    main()