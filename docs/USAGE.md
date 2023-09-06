Table of Contents
-----------------

- [Quick usage](#quickusage)
- [Examples](#examples)
- [Supported Input Data](#inputdata)
- [Parameter Descriptions](#parameters)
- [Output](#output)

## <a name="quickusage"></a> Quick usage

```
usage: argseq --nano-raw input-file
	     --out-dir PATH

	     [--genome-size SIZE] [--threads int] [--iterations int]
	     [--meta] [--polish-target] [--min-overlap SIZE]
	     [--keep-haplotypes] [--debug] [--version] [--help] 
	     [--scaffold] [--resume] [--resume-from] [--stop-after] 
	     [--read-error float] [--extra-params]

Arguments:
  -h, --help            show this help message and exit
  --nano-raw path [path ...]
                        ONT regular reads
  -v, --version         show program's version number and exit
```

## <a name="examples"></a> Examples

### E. coli Oxford Nanopore Technologies data

The dataset was originally released by the 
[Loman lab](http://lab.loman.net/2015/09/24/first-sqk-map-006-experiment/).

    python3 mini-rnn/mini-rnn/mini-rnn.py -i data/Loman_E.coli_MAP006-1_2D_50x.fasta -o out_consensus -t 4

## <a name="inputdata"></a> Supported Input Data

### Oxford Nanopore

### PacBio

## <a name="parameters"></a> Parameter descriptions

## <a name="output"></a> Flye output

The main output files are:

* `assembly.fasta` - Desription.
* `consensus.fasta` - Desription.