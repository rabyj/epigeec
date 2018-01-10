# epiGeEC
- - - -
The **epiGenomic Efficient Correlator** tool is designed to efficiently perform pairwise correlations of thousands of epigenomic datasets. It supports many genomic signal file formats (bigWig, WIG and bedGraph), and offers the possibility to compute correlations at various resolutions (from 1 kb to 10 Mb) on predefined filtered regions (e.g. whole genome with or without blacklist-ed regions, only genes, TSS) and using the selected correlation metric (Pearson and Spearman), as well as the annotation and analysis of the generated correlation matrices. Most of the wrapping is coded in Python, while the core functionalities requiring high performance are coded in C++ using openMP for parallelization.  
  
A galaxy implementation including thousands of pre-computed public datasets is availalble at [http://epigeec.genap.ca/galaxy/](http://epigeec.genap.ca/galaxy/)  

### Installation
- - - -
Linux is the only OS currently supported

**Clone repository**

`git clone https://<username>@bitbucket.org/labjacquespe/epigeec.git`

**Install dependencies**

Requires python2.7

`pip install pandas numpy`

`sudo apt-get install libhdf5-openmpi-dev libssl-devlibsz2 boost`

### How To Use
- - - -

All tools require 2 parameters, a list of signal filenames and a config file

`python <tool> mylist.txt myconfig.conf`

A sample config file can be found [here](epigeec/python/example.conf)

**Config parameters:**

* sig_folder: a folder with all your signal files

* hdf5_folder: path to folders that will hold your hdf5

* filtered_folder: filtered path to folders that will hold your filtered hdf5 files

* assembly: the assembly of your data (see below for list of available assembly)

* include: name of the precomputed filter of regions to include (see below for list of available filters)

* exclude: name of the precomputed filter of regions to excl (see below for list of available filters)

    *note: in case of conflict, exclude takes priority*

* resolution: the size of the bins used

* corr_path: path for the matrix file

* mat_path: path for the correlation file

‌‌   
List of available filters and assemblies:

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

*note: it is possible to add aditional filters by adding them to the resource/filter folder they must follow the assembly.filtername.bed naming convension*

### Example
- - - -

Create a directory structure to hold the data

	myfolder  
	├── signal  
	├── hdf5  
	├── filtered  
	└── example.conf  

The next step is to generate a list of the signal files to correlate, the following command can be used to take every file in the folder

	cd /my/signal/folder  
	ls > mylist.txt  

Start running the tools

	python /path/to/epigeec/epigeec/python/core/to_hdf5.py mylist.txt example.conf  
	python /path/to/epigeec/epigeec/python/core/filter_hdf5.py mylist.txt example.conf  
	python /path/to/epigeec/epigeec/python/core/geec_corr.py mylist.txt example.conf  

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
