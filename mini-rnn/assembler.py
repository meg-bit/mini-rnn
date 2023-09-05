#This file is part of mini-rnn
#Released under the MIT License (see LICENSE file)

import logging
import os
import subprocess

logger = logging.getLogger()


class AssemblyException(Exception):
    pass


class NanoporeReadAssembler:
    """De Novo Assembly of Oxford Nanopore reads.

    Params
    ------
    input_filenames: list
        List of filenames with the sequencing data.

    output_dir: str
        Output directory for the final assembly, after determining the
        consensus sequences and variant calls from nanopore reads.

    tmp_dir: str [Optional]
        Output directory for the initial assembly of the reads.

    n_threads: positive int
        Number of parallel computation threads.
    """

    def __init__(self, input_filenames, output_dir,
                 tmp_dir="tmp/", n_threads=1):
        self.reads = [os.path.abspath(f) for f in input_filenames]
        self.output_dir = os.path.abspath(output_dir)
        self.tmp_dir = os.path.abspath(tmp_dir)
        self.n_threads = n_threads

    def assemble_reads(self, other_args=""):
        """Perform an initial assembly of the reads.

        Params
        ------
        other_args: str
            String of space separated additional arguments to be passed to
            the Flye assembler tool.
        """
        if not os.path.isdir(self.tmp_dir):
            os.makedirs(self.tmp_dir, exist_ok=True)
        
        cmd_line = [
            "flye",
            "--nano-raw", *self.reads,
            "--out-dir", self.tmp_dir,
            "--threads", str(self.n_threads),
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
        
        #assemble_log = os.path.join(self.tmp_dir, "flye.log")
        #with open(assemble_log, "w") as stderr:
        #    subprocess.call(cmd_line, stderr=stderr)

        self._assembly = os.path.join(self.tmp_dir, "assembly.fasta")
        self._assembly_cmdline = cmd_line
        logger("Assembly completed")

    def create_consensus(self, model="r941_min_sup_g507", other_args=""):
        """Determine consensus sequences and variant calls from nanopore reads.

        Params
        ------
        model: str
            Name of the Medaka model to use, based on the base calling.
            Medaka models are named to indicate i) the pore type,
            ii) the sequencing device (MinION or PromethION),
            iii) the basecaller variant, and iv) the basecaller version,
            with the format:
                {pore}_{device}_{caller variant}_{caller version}
            See https://github.com/nanoporetech/medaka#models for details.

        other_args: str
            String of space separated additional arguments to be passed to
            the Medaka correction tool.
        """
        if not hasattr(self, "_assembly"):
            raise ValueError("The reads need to be assembled first with `assemble_reads`.")

        if not os.path.isdir(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)

        cmd_line = [
            "medaka_consensus",
            "-i", *self.reads,
            "-d", self._assembly,
            "-o", self.output_dir,
            "-t", str(self.n_threads),
            "-m", model,
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

        self._consensus = os.path.join(self.output_dir, "consensus.fasta")
        self._consensus_cmdline = cmd_line
        logger("Consensus completed")

    def get_current_assembly(self):
        if hasattr(self, "_consensus"):
            return self._consensus
        elif hasattr(self, "_assembly"):
            return self._assembly
        else:
            return None

    def __repr__(self):
        return (
            f"NanoporeReadAssembler(\n"
            f"    reads={self.reads}\n"
            f"    output_dir={self.output_dir}\n"
            f"    tmp_dir={self.tmp_dir}\n"
            f"    n_threads={self.n_threads}\n)"
        )
