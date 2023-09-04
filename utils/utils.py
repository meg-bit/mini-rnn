from __future__ import absolute_import
import os
import signal
import multiprocessing


def run_cmd(cmd):
    """ Run a command and print the status. """

    log("INFO", "Running: %s" % " ".join(cmd))
    if subprocess.call(cmd) != 0:
        raise RuntimeError("Failed: %s" % " ".join(cmd))
    log("INFO", "Completed: %s" % " ".join(cmd))
    
def check_for_required_tools():
    section_header('Checking requirements')
    explanation('mini-rnn requires Flye and medaka - checking for these tools now.')

#     minimap2_path, minimap2_version, minimap2_status = minimap2_path_and_version('minimap2')
#     if minimap2_status == 'good':
#         log(f'Minimap2 found: {minimap2_path} (v{minimap2_version})')
#     elif minimap2_status == 'not found':
#         sys.exit('Error: minimap2 not found - make sure it is in your PATH before running '
#                  'Minipolish')
#     elif minimap2_status == 'bad':
#         sys.exit('Error: unable to determine minimap2 version')

#     racon_path, racon_version, racon_status = racon_path_and_version('racon')
#     if racon_status == 'good':
#         log(f'Racon found:    {racon_path} (v{racon_version})')
#     elif racon_status == 'not found':
#         sys.exit('Error: racon not found - make sure it is in your PATH before running Minipolish')
#     elif racon_status == 'bad':
#         sys.exit('Error: unable to determine Racon version')

    log()