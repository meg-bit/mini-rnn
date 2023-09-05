#This file is part of mini-rnn
#Released under the MIT License (see LICENSE file)

"""
Run the correction
"""

import logging
import os
import subprocess

logger = logging.getLogger()


class AssembleException(Exception):
    pass

def correct_assembly(
        input_filename, draft_assembly, out_dir, threads,
        model="r941_min_sup_g507", other_args):

    if not os.path.isdir(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    cmd_line = [
        "medaka_consensus",
        "-i", input_filename,
        "-d", draft_assembly,
        "-o", out_dir,
        "-t", str(threads),
        "-m", model,
    ]

    if other_args:
        for arg in other_args.strip().split():
            cmd_line.append(arg.strip())

    try:
        logger.debug("Running: " + " ".join(cmdline))
        subprocess.check_call(cmdline)
    except subprocess.CalledProcessError as e:
        if e.returncode == -9:
            logger.error("Looks like the system ran out of memory")
        raise AssembleException(str(e))
    except OSError as e:
        raise AssembleException

    subprocess.call(cmd_line)
    logger("Correction completed")
