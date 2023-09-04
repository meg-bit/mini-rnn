#This file is part of mini-rnn
#Released under the MIT License (see LICENSE file)

"""
Run the assembly
"""

import subprocess
import logging

logger = logging.getLogger()


class AssembleException(Exception):
    pass

def assemble(input_filename, tmp_dir, threads):
    
    # the output of the assembly is placed in tmp_dir
    cmd_line = [
        'flye', '--nano-raw', input_filename,
        '--out-dir', tmp_dir, '--threads', str(threads),
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
    
    assemble_log = tmp_dir / 'flye.log'
    with open(assemble_log, 'w') as stderr:
        subprocess.call(cmd_line, stderr=stderr)
    # can add the time taken for this process in the log
    log('Assembly completed')