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
    parser.add_argument("-i", "--input", dest="input_filenames",
                        required=True, nargs="+", metavar="filename",
                        help="Input Oxford Nanopore filename(s)")
    parser.add_argument("-o", "--out_dir", required=True, metavar="path", type=str,
                        help="Output directory")
    parser.add_argument("-t", "--threads", default=1, metavar="int", 
                        type=lambda v: check_int_range(v, 1, 128),
                        help="Number of parallel computation threads [1]")
    parser.add_argument("-m", "--model", default="r941_min_sup_g507", type=str,
                        help="Name of Medaka model")
    parser.add_argument("--assembly_opts", default="", type=str, metavar="'opts'",
                        help="Additional options to be passed to flye")
    parser.add_argument("--correction_opts", default="", type=str, metavar="'opts'",
                        help="Additional options to be passed to medaka")
    parser.add_argument("--tmp_dir", default='tmp/', metavar='path',
                        help="Temp directory for draft assembly files")
    args = parser.parse_args()
    return args


def main(args):
    args = get_arguments()

    # Initialize assembler object
    assembler = NanoporeReadAssembler(
        input_filenames=args.input_filenames,
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

    try:
        logger.info("Starting the pipeline...")
        assembler.assemble_reads(args.assembly_opts)
        assembler.create_consensus(args.model, args.correction_opts)

    except Exception as e:
        logger.error(e)
        logger.error("Pipeline aborted")
        return 1

    logger("Pipeline completed")
    logger("Assembly file is: " + assembler.get_current_assembly())


if __name__ == "__main__":
    args = get_arguments()
    main(args)
