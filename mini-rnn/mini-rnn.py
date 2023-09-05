#!/usr/bin/env python

import argparse
import logging

from assemble import assemble_reads
from correct import correct_assembly


def get_arguments():
    parser = argparse.ArgumentParser(
        prog='mini-rnn',
        description="De novo assembly and error correction for long-read sequencing",
    )  
    parser.add_argument("-i", "--input", dest="input_filenames", nargs="+",
                        metavar="filename", help="Input Oxford Nanopore filename(s)")
    parser.add_argument("-o", "--out_dir", required=True, metavar="path",
                        help="Output directory")
    parser.add_argument("-t", "--threads", default=1, metavar="int", 
                        type=lambda v: check_int_range(v, 1, 128),
                        help="Number of parallel computation threads [1]")
    parser.add_argument("-m", "--model", default='r941_min_sup_g507',
                        required=True, metavar="str",
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
    args = get_arguments(args)

    reads = [os.path.abspath(f) for f in args.input_filenames]
    out_dir = os.path.abspath(args.out_dir)
    tmp_dir = os.path.abspath(args.tmp_dir)

    # Initialize logging
    log_file = os.path.join(out_dir, "mini-rnn.log")
    logging.basicConfig(filename=log_file)
    logger = logging.getLogger()

    try:
        logger.info("Starting the pipeline...")
        assemble_reads(reads, tmp_dir, args.threads, args.assembly_opts)
        draft_assembly = os.path.join(tmp_dir, "assembly.fasta")
        correct_assembly(reads, draft_assembly, out_dir,
                         args.threads, args.model, args.correction_opts)

    except Exception as e:
        logger.error(e)
        logger.error("Pipeline aborted")
        return 1

    logger("Pipeline completed")


if __name__ == "__main__":
    args = get_arguments()
    main(args)
