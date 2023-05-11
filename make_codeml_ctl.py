#!/usr/bin/python3

# make_codeml_ctl.py

# Hsin-Ying Chang <hyhazelchang@gmail.com>
# v1 2023/05/10

# Usage: python3 /home/xinchang/pyscript/pyscript_xin/make_codeml_ctl.py --aln_dir="/scratch/xinchang/cyano11/cyano11.16/phylip" --tre_dir="/scratch/xinchang/cyano11/cyano11.16/new_trees" --out_dir="/scratch/xinchang/cyano11/cyano11.16/codeml/M0" --sh_dir="/scratch/xinchang/cyano11/cyano11.16/codeml/M0/sh" --aln_file_ext="phylip" --tree_file_ext="tre" --icode=0 --verbose=1 --model=0 --NSsites=0 --n_job=5


import argparse
import os
import glob

def main():
    parser = argparse.ArgumentParser(
        description=("Make the control files for codeml"),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--aln_dir",
                        default=None,
                        type=str,
                        help="Directory containing sequence alignmnet files. Please provide absolute path.")
    parser.add_argument("--tre_dir",
                        default=None,
                        type=str,
                        help="Directory containing tree files. Please provide absolute path.")
    parser.add_argument("--out_dir",
                        default=None,
                        type=str,
                        help="Directory for outputs. Please provide absolute path.")
    parser.add_argument("--sh_dir",
                        default="0",
                        type=str,
                        help="Directory for shell scripts. Please provide absolute path.")
    parser.add_argument("--aln_file_ext",
                        default="phylip",
                        type=str,
                        help="Extension of alignment sequence file")
    parser.add_argument("--tree_file_ext",
                        default="tre",
                        type=str,
                        help="The name of aln and tree should be the same!")
    parser.add_argument("--icode",
                        default="0",
                        type=str,
                        help="0: universal code. 1: mammalian mt. 2-10...")
    parser.add_argument("--verbose",
                        default="1",
                        type=str,
                        help="verbose")
    parser.add_argument("--model",
                        default="0",
                        type=str,
                        help="Enable 2 or more omega for branches, max = 8")
    parser.add_argument("--NSsites",
                        default="0",
                        type=str,
                        help="Based on the site model settings")
    parser.add_argument("--n_job",
                        default=1,
                        type=int)

    args = parser.parse_args()
    aln_dir = args.aln_dir
    tre_dir = args.tre_dir
    out_dir = args.out_dir
    sh_dir = args.sh_dir
    aln_file_ext = args.aln_file_ext
    tree_file_ext = args.tree_file_ext
    icode = args.icode
    verbose = args.verbose
    model = args.model
    NSsites = args.NSsites
    n_job = args.n_job

    # Find alignment files
    seqfiles = glob.glob(os.path.join(aln_dir, "*." + aln_file_ext))

    # Make output directory
    if not os.path.exists(out_dir):
        os.system("mkdir -p " + out_dir)

    # Get file names
    count = 0
    codeml_cmd = []
    for aln in seqfiles:
        count += 1
        aln_name = os.path.basename(aln).split(".")[0]
        os.system("mkdir -p " + out_dir + "/" + aln_name)
        ctl = open(out_dir + "/" + aln_name + "/" + aln_name + ".ctl", "w")
        ctl.write(
            "seqfile = " + aln + "\n" +
            "treefile = " + tre_dir + "/" + aln_name + "." + tree_file_ext + "\n" +
            "outfile = " + out_dir + "/" + aln_name + "/" + aln_name + ".codeml\n" +
            "noisy = 0\n" +
            "verbose = " + verbose + "\n" +
            "runmode = 0\n" +
            "seqtype = 1\n" +
            "CodonFreq = 2\n" +
            "clock = 0\n" +
            "aaDist = 0\n" +
            "model = " + model + "\n" +
            "NSsites = " + NSsites + "\n" +
            "icode = " + icode + "\n" +
            "Mgene = 0\n" + 
            "fix_kappa = 0\n" + 
            "kappa = 2\n" +
            "fix_omega = 0\n" + 
            "omega = .4\n" +
            "fix_alpha = 1\n" + 
            "alpha = 0.\n" +
            "Malpha = 0\n" + 
            "ncatG = 8\n" + 
            "getSE = 0\n" + 
            "RateAncestor = 1\n" + 
            "Small_Diff = .5e-6\n" +
            "cleandata = 1\n" + 
            "method = 0"
        )
        ctl.close()
        codeml_cmd.append("codeml " + out_dir + "/" + aln_name + "/" + aln_name + ".ctl")

    # print out job scripts
    os.system("mkdir -p " + sh_dir)
    quo = int(count / n_job)
    mod = int(count % n_job)
    for n in range(n_job):
        if (n + 1) == n_job:
            head = int(quo * n)
            tail = int(quo * (n+1) + mod - 1)
        else:
            head = int(quo * n)
            tail = int(quo * (n+1))
        job = open(sh_dir + "/job" + str(n+1) + ".sh" , "w")
        for num in range(head, tail):
            job.write(codeml_cmd[num] + "\n")
        job.close()

if __name__ == "__main__":
    main()