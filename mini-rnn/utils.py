import argparse
import logging

logger = logging.getLogger()


def check_int_range(value, min_val, max_val, require_odd=False):
    ival = int(value)
    if ival < min_val or ival > max_val:
        raise argparse.ArgumentTypeError("value should be in the "
                        "range [{0}, {1}]".format(min_val, max_val))
    if require_odd and ival % 2 == 0:
        raise argparse.ArgumentTypeError("should be an odd number")
    return ival

def run_cmd(cmd):
    """ Run a command and print the status. """

    logger("INFO", "Running: %s" % " ".join(cmd))
    if subprocess.call(cmd) != 0:
        raise RuntimeError("Failed: %s" % " ".join(cmd))
    logger("INFO", "Completed: %s" % " ".join(cmd))
