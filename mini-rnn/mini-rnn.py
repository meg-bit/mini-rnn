#!/usr/bin/env python

import argparse

def main():
    parser = argparse.ArgumentParser(
        prog='mini-rnn',
        description="De novo assembly and error correction for long-read sequencing"
    )  
  
    parser.add_argument("--nano-raw", dest="nano_raw", nargs="+",
                        default=None, metavar="path",
                        help="Oxford Nanopore reads")
    parser.add_argument("-o", "--out-dir", dest="out_dir",
                        default=None, required=True,
                        metavar="path", help="Output directory")
    parser.add_argument("-t", "--threads", dest="threads",
                        type=lambda v: check_int_range(v, 1, 128),
                        default=1, metavar="int", 
                        help="number of parallel threads [1]")
    parser.add_argument("--debug", action="store_true",
                        dest="debug", default=False,
                        help="enable debug output")
    parser.add_argument("--deterministic", action="store_true",
                        dest="deterministic", default=False,
                        help="perform disjointig assembly single-threaded")
    args = parser.parse_args()      

    if not os.path.isdir(args.out_dir):
        os.mkdir(args.out_dir)
    args.out_dir = os.path.abspath(args.out_dir)

    args.reads = [os.path.abspath(r) for r in args.reads]

    # Should add time, etc here for logging
    args.log_file = os.path.join(args.out_dir, "log")

    try:
        aln.check_binaries()
        pol.check_binaries()
        asm.check_binaries()
        repeat.check_binaries()

        if not args.polish_target:
            _run(args)
        else:
            _run_polisher_only(args)

    except (AlignmentException, pol.PolishException,
            asm.AssembleException, repeat.RepeatException,
            ResumeException, fp.FastaError, ConfigException) as e:
        logger.error(e)
        logger.error("Pipeline aborted")
        return 1

    
if __name__ == "__main__":
    main()