#This file is part of argseq
#Released under the MIT License (see LICENSE file)

"""
Run the assembling process
"""

import subprocess
import logging
import os

from utils.utils import which

logger = logging.getLogger()


class AssembleException(Exception):
    pass

def assemble(
    args, run_params, out_file, 
    log_file, config_path, input_filename, threads, tmp_dir
):
    logger.info("Assembling disjointigs")
    logger.debug("-----Begin assembly log------")
    cmdline = [ASSEMBLE_BIN, "assemble", "--reads", ",".join(args.reads), "--out-asm", out_file,
               "--config", config_path, "--log", log_file, "--threads", str(1 if args.deterministic else args.threads)]
    
    if args.debug:
        cmdline.append("--debug")
    if args.meta:
        cmdline.append("--meta")
    if args.genome_size:
        cmdline.extend(["--genome-size", str(args.genome_size)])

    cmdline.extend(["--min-ovlp", str(run_params["min_overlap"])])
    if run_params["min_read_length"] > 0:
        cmdline.extend(["--min-read", str(run_params["min_read_length"])])

    if args.extra_params:
        cmdline.extend(["--extra-params", args.extra_params])

    try:
        logger.debug("Running: " + " ".join(cmdline))
        subprocess.check_call(cmdline)
    except subprocess.CalledProcessError as e:
        if e.returncode == -9:
            logger.error("Looks like the system ran out of memory")
        raise AssembleException(str(e))
    except OSError as e:
        raise AssembleException
        
    command = [
        'minimap2', '-t', str(threads), '-x', preset, unpolished_filename, read_filename
    'flye' '--nano-raw' input_filename '--out-dir' out_nano '--threads' str(threads)
    ]
    alignments = tmp_dir / (name + '.paf')
    assemble_log = tmp_dir / '_minimap2.log'
    with open(alignments, 'wt') as stdout, open(minimap2_log, 'w') as stderr:
        subprocess.call(command, stdout=stdout, stderr=stderr)
    alignment_count = count_lines(alignments)
    log(f'  alignments: {alignments} ({alignment_count:,} alignments)')