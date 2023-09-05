#This file is part of mini-rnn
#Released under the MIT License (see LICENSE file)

"""
Run the assembly
"""

import logging
import os
import subprocess

logger = logging.getLogger()


class AssembleException(Exception):
    pass

def assemble_reads(input_filename, tmp_dir, threads, other_args):
    # the output of the assembly is placed in tmp_dir
    if not os.path.isdir(tmp_dir):
        os.makedirs(tmp_dir, exist_ok=True)

    cmd_line = [
        "flye",
        "--nano-raw", input_filename,
        "--out-dir", tmp_dir,
        "--threads", str(threads),
    ]

    if other_args:
        for arg in other_args.strip().split():
            cmd_line.append(arg.strip())

    try:
        logger.debug("Running: " + " ".join(cmd_line))
        subprocess.check_call(cmd_line)
    except subprocess.CalledProcessError as e:
        if e.returncode == -9:
            logger.error("Looks like the system ran out of memory")
        raise AssembleException(str(e))
    except OSError as e:
        raise AssembleException
    
    assemble_log = os.path.join(tmp_dir, "flye.log")
    with open(assemble_log, "w") as stderr:
        subprocess.call(cmd_line, stderr=stderr)

    logger("Assembly completed")
