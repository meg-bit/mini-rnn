Table of Contents
-----------------

- [Quick usage](#quickusage)
- [Examples](#examples)
- [Supported Input Data](#inputdata)
- [Parameter Descriptions](#parameters)
- [Output](#output)

## <a name="quickusage"></a> Quick usage

```
usage: argseq (--nano-raw | --pacbio-raw) file1 [file_2 ...]
	     --out-dir PATH

	     [--genome-size SIZE] [--threads int] [--iterations int]
	     [--meta] [--polish-target] [--min-overlap SIZE]
	     [--keep-haplotypes] [--debug] [--version] [--help] 
	     [--scaffold] [--resume] [--resume-from] [--stop-after] 
	     [--read-error float] [--extra-params]

Arguments:
  -h, --help            show this help message and exit
  --pacbio-raw path [path ...]
                        PacBio regular CLR reads (<20% error)
  --pacbio-corr path [path ...]
                        PacBio reads that were corrected with other methods (<3% error)
  --pacbio-hifi path [path ...]
                        PacBio HiFi reads (<1% error)
  --nano-raw path [path ...]
                        ONT regular reads, pre-Guppy5 (<20% error)
  --nano-corr path [path ...]
                        ONT reads that were corrected with other methods (<3% error)
  --nano-hq path [path ...]
                        ONT high-quality reads: Guppy5+ SUP or Q20 (<5% error)
  --subassemblies path [path ...]
                        [deprecated] high-quality contigs input
  -g size, --genome-size size
                        estimated genome size (for example, 5m or 2.6g)
  -o path, --out-dir path
                        Output directory
  -t int, --threads int
                        number of parallel threads [1]
  -i int, --iterations int
                        number of polishing iterations [1]
  -m int, --min-overlap int
                        minimum overlap between reads [auto]
  --asm-coverage int    reduced coverage for initial disjointig assembly [not set]
  --hifi-error float    [deprecated] same as --read-error
  --read-error float    adjust parameters for given read error rate (as fraction e.g. 0.03)
  --extra-params extra_params
                        extra configuration parameters list (comma-separated)
  --plasmids            unused (retained for backward compatibility)
  --meta                metagenome / uneven coverage mode
  --keep-haplotypes     do not collapse alternative haplotypes
  --no-alt-contigs      do not output contigs representing alternative
                        haplotypes
  --scaffold            enable scaffolding using graph [disabled by default]
  --trestle             [deprecated] enable Trestle [disabled by default]
  --polish-target path  run polisher on the target sequence
  --resume              resume from the last completed stage
  --resume-from stage_name
                        resume from a custom stage
  --stop-after stage_name
                        stop after the specified stage completed
  --debug               enable debug output
  -v, --version         show program's version number and exit
```

## <a name="examples"></a> Examples

### E. coli Oxford Nanopore Technologies data

The dataset was originally released by the 
[Loman lab](http://lab.loman.net/2015/09/24/first-sqk-map-006-experiment/).

    wget https://zenodo.org/record/1172816/files/Loman_E.coli_MAP006-1_2D_50x.fasta
    argseq --nano-raw Loman_E.coli_MAP006-1_2D_50x.fasta --out-dir out_nano --threads 4


## <a name="inputdata"></a> Supported Input Data

### Oxford Nanopore

### PacBio

## <a name="parameters"></a> Parameter descriptions

## <a name="output"></a> Flye output

The main output files are:

* `assembly.fasta` - Final assembly. Contains contigs and possibly scaffolds (see below).
* `assembly_graph.{gfa|gv}` - Final repeat graph. Note that the edge sequences might be
different (shorter) than contig sequences, because contigs might include multiple
graph edges (see below).
* `assembly_info.txt` - Extra information about contigs (such as length or coverage).