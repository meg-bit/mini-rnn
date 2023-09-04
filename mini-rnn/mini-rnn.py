#!/usr/bin/env python

import argparse

from .assemble import assemble
from .correct import correct

def get_arguments():
    parser = argparse.ArgumentParser(
        prog='mini-rnn',
        description="De novo assembly and error correction for long-read sequencing"
    )  
  
    parser.add_argument("--nano-raw", dest="nano_raw", nargs="+",
                        default=None, metavar="path",
                        help="Oxford Nanopore reads")
    parser.add_argument("-i", "--input", dest="input_filename",
                        default=None, required=True,
                        metavar="path", help="Input filename")
    parser.add_argument("-o", "--out-dir", dest="out_dir",
                        default=None, required=True,
                        metavar="path", help="Output directory")
    parser.add_argument("-t", "--threads", dest="threads",
                        type=lambda v: check_int_range(v, 1, 128),
                        default=1, metavar="int", 
                        help="number of parallel threads [1]")
    parser.add_argument("-m", "--model",
                        default='r941_min_sup_g507', required=True,
                        metavar="str", help="Model")
    parser.add_argument("--debug", action="store_true",
                        dest="debug", default=False,
                        help="enable debug output")
    parser.add_argument("--deterministic", action="store_true",
                        dest="deterministic", default=False,
                        help="perform disjointig assembly single-threaded")
    args = parser.parse_args()
    return args

def main(args):
    args = get_arguments(args)
    
    if not os.path.isdir(args.out_dir):
        os.mkdir(args.out_dir)
    args.out_dir = os.path.abspath(args.out_dir)

    args.reads = [os.path.abspath(r) for r in args.reads]

    # Should add time, etc here for logging
    args.log_file = os.path.join(args.out_dir, "log")
    
    assemble(args.input_filename, 
             args.tmp_dir, 
             args.threads)
    correct(args.input_filename, 
            args.tmp_dir, 
            args.out_dir, 
            args.threads,
            args.model)

    except (AlignmentException) as e:
        logger.error(e)
        logger.error("Pipeline aborted")
        return 1
  
if __name__ == "__main__":
    main()