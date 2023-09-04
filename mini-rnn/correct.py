#This file is part of mini-rnn
#Released under the MIT License (see LICENSE file)

"""
Run the correction
"""

import subprocess
import logging

logger = logging.getLogger()


class AssembleException(Exception):
    pass

def correct(
    input_filename, tmp_dir, out_dir, threads,
    model='r941_min_sup_g507'
):
    cmd_line = [
        'medaka_consensus', '-i', input_filename, '-d', tmp_dir/'assembly.fasta', '-o' out_dir '-t'  str(threads), '-m', model,
    ]
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
    # can add the time taken for this process in the log
    log('Correction completed')