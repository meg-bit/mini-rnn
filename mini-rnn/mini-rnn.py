#!/usr/bin/env python

import argparse
import logging
import os

from assembler import NanoporeReadAssembler
from utils import check_int_range


def get_arguments():
    parser = argparse.ArgumentParser(
        prog='mini-rnn',
        description="De novo assembly and error correction for long-read sequencing",
    )  
    parser.add_argument("-i", "--input", dest="input_filename",
                        required=True, type=str, metavar="filename",
                        help="Input Oxford Nanopore filename")
    parser.add_argument("-o", "--out_dir", required=True, type=str,
                        metavar="path", help="Output directory")
    parser.add_argument("-t", "--threads", default=1, metavar="int", 
                        type=lambda v: check_int_range(v, 1, 128),
                        help="Number of parallel computation threads [1]")
    parser.add_argument("-m", "--model", default="r941_min_sup_g507", type=str,
                        help="Name of Medaka model")
    parser.add_argument("--assembly_opts", default="", type=str, metavar="'opts'",
                        help="Additional options to be passed to flye")
    parser.add_argument("--correction_opts", default="", type=str, metavar="'opts'",
                        help="Additional options to be passed to medaka")
    parser.add_argument("--tmp_dir", default='tmp/', type=str, metavar='path',
                        help="Temporary directory for draft assembly files")
    args = parser.parse_args()
    return args


def main(args):
    args = get_arguments()

    # Initialize assembler object
    assembler = NanoporeReadAssembler(
        input_filename=args.input_filename,
        output_dir=args.out_dir,
        tmp_dir=args.tmp_dir,
        n_threads=args.threads,
    )
    print(assembler)

    # Initialize logging
    if not os.path.isdir(args.out_dir):
        os.makedirs(args.out_dir, exist_ok=True)
    log_file = os.path.join(args.out_dir, "mini-rnn.log")
    logging.basicConfig(filename=log_file, level=logging.DEBUG)
    logger = logging.getLogger()

    ### Run the assembly ###
    try:
        logger.info("Starting the assembly...")
        assembler.assemble_reads(args.assembly_opts)
    except Exception as e:
        logger.error(e)
        logger.error("Assembly pipeline aborted")
        return 1
    
    ### Run the correction ###
    try:
        logger.info("Starting the correction...")
        # assembler._assembly = '../tmp/assembly.fasta' # DEBUG
        assembler.create_consensus(args.model, args.correction_opts)
    except Exception as e:
        logger.error(e)
        logger.error("Correction pipeline aborted")
        return 1

    logger.info("Pipeline completed")
    logger.info("Resulting assembly file: " + assembler.get_current_assembly())


if __name__ == "__main__":
    args = get_arguments()
    main(args)
