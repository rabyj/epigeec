# epiGeEC
- - - -
The **epiGenomic Efficient Correlator** tool is designed to efficiently perform pairwise correlations of thousands of epigenomic datasets. It supports a growing number of file formats and offers the possibility to compute correlations at any resolution on costum or predefined filtered regions.  
  
A galaxy implementation including thousands of pre-computed public datasets is availalble at http://epigeec.genap.ca/galaxy/ and also includes support for the WIG format and Spearman correlation(coming soon to command line version). It also offers [tools](https://bitbucket.org/labjacquespe/geec_analysis/src/master/) for further annotation and analysis of the matrix files created by epiGeEC.

### Installation
- - - -
Linux/x64 is the only OS currently supported

**Dependencies**

You will need pip to install the python package, use the following command if not already installed

	sudo apt-get install python-pip  
	
Pip will attempt to install all dependencies but most likely will fail

See documentation on how to install [pandas](https://github.com/svaksha/PyData-Workshop-Sprint/wiki/linux-install-pandas) and [h5py](http://docs.h5py.org/en/latest/build.html) as they are most likely to fail.

	sudo pip install pandas h5py

You might have more success with

	sudo apt-get install python-h5py python-pandas

**Install epiGeEC**

	sudo pip install epigeec  


### How To Use
- - - -

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

	epigeec to_hdf5 -bw signal/myfile.bw chrom_sizes 10000 hdf5/myfile.hdf5
	epigeec filter hdf5/myfile.hdf5 resource/chrom_sizes filtered/myfile.hdf5 -s sel.bed -e exc.bed
	epigeec correlate filtered_list resource/chrom_sizes mymatrix.mat  

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
