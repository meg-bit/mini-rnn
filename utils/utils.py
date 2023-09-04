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