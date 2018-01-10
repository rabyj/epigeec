# epiGeEC
- - - -
The **epiGenomic Efficient Correlator** tool is designed to efficiently perform pairwise correlations of thousands of epigenomic datasets. It supports many genomic signal file formats (bigWig, WIG and bedGraph), and offers the possibility to compute correlations at various resolutions (from 1 kb to 10 Mb) on predefined filtered regions (e.g. whole genome with or without blacklist-ed regions, only genes, TSS) and using the selected correlation metric (Pearson and Spearman), as well as the annotation and analysis of the generated correlation matrices. Most of the wrapping is coded in Python, while the core functionalities requiring high performance are coded in C++ using the openMP API for parallelization.  
    
A galaxy implementation including thousands of pre-computed public datasets is availalble at [http://epigeec.genap.ca/galaxy/](http://epigeec.genap.ca/galaxy/)  
 
### Installation
- - - -
Linux is the only OS currently supported

**Install dependencies**

Requires python2.7

`pip install pandas numpy`

`sudo apt-get install libhdf5-openmpi-dev libssl-devlibsz2 boost`

**Clone repository**

`git clone https://<username>@bitbucket.org/labjacquespe/epigeec.git`

**Install epiGeEC**

	cd epigeec
	python setup.py install

### How To Use
- - - -

Conversion a signal file to hdf5 format  

`usage: epigeec hdf5 [-h] (-bw | -bg) signal chrom_sizes bin hdf5`  

Filter an hdf5 file (optional)  

`usage: epigeec filter [-h] signal chrom_sizes bin hdf5 include exclude`  

Generate an NxN correlation matrix  

`usage: epigeec corr [-h] list chrom_sizes bin mat`  
  
‌‌   
List of filters and assemblies offered in the [resource](resource) folder:

1. hg19  
    * all: usually used as default value for "include"  
    * none: use this as exclude file if you want to work with the entire genome  
    * blklst: blacklisted regions  
    * gene: regions corresponding to genes (refseq)  
    * tss: transcription sites (refseq)  
    
1. hg38  
    * all: usually used as default value for "include"  
    * none: use this as exclude file if you want to work with the entire genome  
    * gene: regions corresponding to genes (refseq)  
    * tss: transcription sites (refseq)  
    
1. mm10  
    * all: usually used as default value for "include"  
    * none: use this as exclude file if you want to work with the entire genome  
    * blklst: blacklisted regions  
    
1. saccer3  
    * all: usually used as default value for "include"  
    * none: use this as exclude file if you want to work with the entire genome  
  
  
### Example
- - - -

Create a directory structure to hold the data

	myfolder  
	├── signal  
	├── hdf5  
	└── filtered  

Start running the tools

	epigeec -bw signal/myfile.bw chrom_sizes 10000 hdf5/myfile.hdf5
	epigeec hdf5/myfile.hdf5 chrom_sizes 10000 filtered/myfile.hdf5 inc.bed exc.bed
	epigeec filtered_list chrom_sizes 10000 mymatrix.mat  

The output is a tab separated matrix file with your correlations

			file1	file2	file3	file4	file5  
	file1	1.0000	0.0225	0.0579	0.0583	0.0603  
	file2	0.0225	1.0000	0.0625	0.0523	0.0642  
	file3	0.0579	0.0625	1.0000	0.7535	0.7917  
	file4	0.0583	0.0523	0.7535	1.0000	0.7754  
	file5	0.0603	0.0642	0.7917	0.7754	1.0000  

### License
- - - -
[GNU General Public License v3](LICENSE)
