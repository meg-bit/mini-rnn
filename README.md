# mini-rnn

Mini-rnn performs de novo assembly and error correction for long-read sequencing data.

### Getting Started
Retrieve the repo with:
```bash
git clone --recurse-submodules https://github.com/meg-bit/mini-rnn.git
```

The tools requires the installation of several tools and their corresponding dependencies. For ease of use, these are readily retrieved as submodules under `tools/`. Each still needs to be independently installed following their respective instructions:
 - [Flye](https://github.com/fenderglass/Flye)
 - [Minimap2](https://github.com/lh3/minimap2)
 - [HTSlib](https://github.com/samtools/htslib)
 - [BCFtools](https://github.com/samtools/bcftools)
 - [samtools](https://github.com/samtools/samtools)

### Manuals
- [Installation instructions](docs/INSTALL.md)
- [Usage](docs/USAGE.md)
