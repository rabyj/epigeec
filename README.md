# epiGeEC
- - - -
The **epiGenomic Efficient Correlator** tool is designed to efficiently perform pairwise correlations of thousands of epigenomic datasets. It supports a growing number of file formats and offers the possibility to compute correlations at any resolution on costum or predefined filtered regions. Please refer to the following paper for a description of epiGeEC : https://academic.oup.com/bioinformatics/article/35/4/674/5058096
  
A galaxy implementation including thousands of pre-computed public datasets is availalble at http://epigeec.genap.ca/galaxy/ and also includes support for the WIG format and Spearman correlation(coming soon to command line version). It also offers [tools](https://bitbucket.org/labjacquespe/epigeec_analysis/src/master/) for further annotation and analysis of the matrix files created by epiGeEC.

### Installation
- - - -
Linux/x64 is the only OS currently supported

**Install epiGeEC**

	pip install epigeec  

**Dependencies**

You will need pip to install the python package, use the following command if not already installed

	sudo apt-get install python-pip  
	
Pip will attempt to install all dependencies but might fail

See documentation on how to install [pandas](https://github.com/svaksha/PyData-Workshop-Sprint/wiki/linux-install-pandas) and [h5py](http://docs.h5py.org/en/latest/build.html).

	pip install pandas h5py

You might have more success with

	sudo apt-get install python-h5py python-pandas


### How To Use
- - - -

The process is done in 2 or 3 steps, conversion to hdf5, filtering(optional) and correlation.

The signal files (bedgraph, wig or bigwig) need to first be converted to hdf5 format, this will require a chromSizes file(available [here](epigeec/resource) or from UCSC) for the assembly used by your signal files. The chromSizes file can be tuncated. For example, keeping only canonical chromosomes will work even if the bigwig countains non-cannonical chromosomes. You will also need to choose a resolution, we suggest a resolution of 1000 or 10000 base pair to obtain biologically interesting results.  

The hdf5 files can be filtered over certain regions (such as regions corresponding to genes) using your own bed files or those available [here](epigeec/resource).  

The final step, the correlation itself, will require a list of all hdf5 files to be correlated(one file path per line) as well as the chromSizes file used to generate the hdf5 files. It is not possible to correlate files from different assemblies.  

For more info on each parameter use the help flag

	epigeec [tool] --help

Conversion of a signal file to the hdf5 format

	usage: epigeec to_hdf5 [-h] (-bw | -bg) signalFile chromSizes resolution outHdf5

Filter an hdf5 file (optional)  

	usage: epigeec filter [-h] [--select SELECT] [--exclude EXCLUDE] hdf5 chromSizes outHdf5

Generate an NxN Pearson correlation matrix  

	usage: epigeec correlate [-h] [--concat] [--desc] hdf5List chromSizes outMatrix 
  
‌‌   
List of assemblies and filters offered in the [resource](epigeec/resource) folder:

1. hg19  
    * blklst: blacklisted regions from [here](https://sites.google.com/site/anshulkundaje/projects/blacklists)  
    * gene: regions corresponding to genes (from refSeq annotation)  
    * tss: transcription sites (from refSeq annotation)  
    
1. hg38    
    * gene: regions corresponding to genes (from refSeq annotation)  
    * tss: transcription sites (from refSeq annotation)  
    
1. mm10   
    * blklst: blacklisted regions from [here](https://sites.google.com/site/anshulkundaje/projects/blacklists)   
    
1. saccer3 
  
  
### Example
- - - -

Create a directory structure to hold the data

	myfolder  
	├── signal  
	├── hdf5  
	├── filtered
	└── resource 

Start running the tools

	epigeec to_hdf5 -bw signal/myfile.bw resource/chrom_sizes 1000 hdf5/myfile.hdf5
	epigeec filter hdf5/myfile.hdf5 resource/chrom_sizes filtered/myfile.hdf5 -s resource/sel.bed -e resource/excl.bed
	epigeec correlate filtered_list resource/chrom_sizes mymatrix.mat --desc 5dts_1kb 

The output is a tab separated matrix file with your correlations

	5dts_1kb	file1	file2	file3	file4	file5  
	file1	1.0000	0.0225	0.0579	0.0583	0.0603  
	file2	0.0225	1.0000	0.0625	0.0523	0.0642  
	file3	0.0579	0.0625	1.0000	0.7535	0.7917  
	file4	0.0583	0.0523	0.7535	1.0000	0.7754  
	file5	0.0603	0.0642	0.7917	0.7754	1.0000  

### License
- - - -
[GNU General Public License v3](LICENSE)
