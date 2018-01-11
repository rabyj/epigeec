# epiGeEC
- - - -
The **epiGenomic Efficient Correlator** tool is designed to efficiently perform pairwise correlations of thousands of epigenomic datasets. It supports a growing number of file formats and offers the possibility to compute correlations at any resolution on costum or predefined filtered regions.  
  
A galaxy implementation including thousands of pre-computed public datasets is availalble at http://epigeec.genap.ca/galaxy/ and already includes support for the WIG format and spearman correlation(coming soon to command line version). It also offers tools for further annotation and analysis of the matrix files created by epiGeEC.

### Installation
- - - -
Linux is the only OS currently supported

**Install dependencies**

Requires python2.7

	sudo apt-get install libhdf5-openmpi-dev libssl-devlibsz2 boost

**Install epiGeEC**

	sudo pip install epigeec

### How To Use
- - - -

For more info on each parameter use

	epigeec [tool] --help

Conversion of a signal file to hdf5 format

	usage: epigeec to_hdf5 [-h] (-bw | -bg) signal_file chrom_sizes resolution output_hdf5

Filter an hdf5 file (optional)  

	usage: epigeec filter [-h] [--include INCLUDE] [--exclude EXCLUDE] hdf5 chrom_sizes resolution output_hdf5

Generate an NxN correlation matrix  

	usage: main.py correlation [-h] hdf5_list chrom_sizes resolution output_matrix 
  
‌‌   
List of assemblies and filters offered in the [resource](epigeec/resource) folder:

1. hg19  
    * blklst: blacklisted regions  
    * gene: regions corresponding to genes (refseq)  
    * tss: transcription sites (refseq)  
    
1. hg38    
    * gene: regions corresponding to genes (refseq)  
    * tss: transcription sites (refseq)  
    
1. mm10   
    * blklst: blacklisted regions  
    
1. saccer3 
  
  
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
