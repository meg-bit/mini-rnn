#!/usr/bin/env python

import argparse

def main():
    parser = argparse.ArgumentParser(
        prog='Argseq',
        description="Assembly of long reads"
    )
    
    # Set the group - input files
    read_group = parser.add_mutually_exclusive_group(required=True)
    read_group.add_argument("--nano-raw", dest="nano_raw", nargs="+",
                            default=None, metavar="path",
                            help="Oxford Nanopore reads")
    read_group.add_argument("--pacbio-raw", dest="pacbio_raw", nargs="+",
                            default=None, metavar="path",
                            help="PacBio reads")
    
    # Set other arguments
    parser.add_argument("-o", "--out-dir", dest="out_dir",
                        default=None, required=True,
                        metavar="path", help="Output directory")
    parser.add_argument("-g", "--genome-size", dest="genome_size",
                        metavar="size", required=False, default=None,
                        help="estimated genome size (for example, 5m or 2.6g)")
    parser.add_argument("-t", "--threads", dest="threads",
                        type=lambda v: check_int_range(v, 1, 128),
                        default=1, metavar="int", 
                        help="number of parallel threads [1]")
    parser.add_argument("-i", "--iterations", dest="num_iters",
                        type=lambda v: check_int_range(v, 0, 10),
                        default=1, metavar="int", 
                        help="number of polishing iterations [1]")
    parser.add_argument("-m", "--min-overlap", dest="min_overlap", metavar="int",
                        type=lambda v: check_int_range(v, 1000, 10000),
                        default=None, help="minimum overlap between reads [auto]")
    parser.add_argument("--asm-coverage", dest="asm_coverage", metavar="int",
                        default=None, help="reduced coverage for initial "
                        "disjointig assembly [not set]", type=int)
    parser.add_argument("--hifi-error", dest="hifi_error", metavar="float",
                        default=None, help="[deprecated] same as --read-error", type=float)
    parser.add_argument("--read-error", dest="read_error", metavar="float",
                        default=None, 
                        help="adjust parameters for read error rate (as fraction e.g. 0.03)", 
                        type=float)
    parser.add_argument("--extra-params", dest="extra_params",
                        metavar="extra_params", required=False, default=None,
                        help="extra configuration parameters list (comma-separated)")
    parser.add_argument("--meta", action="store_true",
                        dest="meta", default=False,
                        help="metagenome / uneven coverage mode")
    parser.add_argument("--keep-haplotypes", action="store_true",
                        dest="keep_haplotypes", default=False,
                        help="do not collapse alternative haplotypes")
    parser.add_argument("--no-alt-contigs", action="store_true",
                        dest="no_alt_contigs", default=False,
                        help="do not output contigs representing alternative haplotypes")
    parser.add_argument("--scaffold", action="store_true",
                        dest="scaffold", default=False,
                        help="enable scaffolding using graph [disabled by default]")
    parser.add_argument("--polish-target", dest="polish_target",
                        metavar="path", required=False,
                        help="run polisher on the target sequence")
    parser.add_argument("--resume", action="store_true",
                        dest="resume", default=False,
                        help="resume from the last completed stage")
    parser.add_argument("--resume-from", dest="resume_from", metavar="stage_name",
                        default=None, help="resume from a custom stage")
    parser.add_argument("--stop-after", dest="stop_after", metavar="stage_name",
                        default=None, help="stop after the specified stage completed")
    parser.add_argument("--debug", action="store_true",
                        dest="debug", default=False,
                        help="enable debug output")
    parser.add_argument("--deterministic", action="store_true",
                        dest="deterministic", default=False,
                        help="perform disjointig assembly single-threaded")
    args = parser.parse_args()

    if args.asm_coverage and (args.genome_size is None):
        parser.error("--asm-coverage option requires genome size estimate (--genome-size)")

    if args.asm_coverage and args.meta:
        parser.error("--asm-coverage is incompatible with --meta")

    if args.hifi_error and not args.read_error:
        args.read_error = args.hifi_error
        
    if args.read_error and (args.pacbio_raw or args.nano_raw):
        parser.error("--read-error can only be used with corr/hq/hifi modes")
        
    if args.read_error and args.read_error > 1:
        parser.error("--read-error expressed as a decimal fraction, e.g. 0.01 or 0.03")

    def _add_extra_param(param):
        if args.extra_params:
            args.extra_params += "," + param
        else:
            args.extra_params = param

    if args.read_error:
        hifi_str = "assemble_ovlp_divergence={0},repeat_graph_ovlp_divergence={0}".format(args.read_error)
        _add_extra_param(hifi_str)

    if args.no_alt_contigs:
        _add_extra_param("remove_alt_edges=1")

    if args.keep_haplotypes:
        _add_extra_param("aggressive_dup_filter=0")

    ##### nano_raw of pacbio_raw #####
    if args.nano_raw:
        args.reads = args.nano_raw
        args.platform = "nano"
        args.read_type = "raw"
    
    if args.pacbio_raw:
        args.reads = args.pacbio_raw
        args.platform = "pacbio"
        args.read_type = "raw"
    ##################################        

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