============
epiGeEC
============

The **epiGenomic Efficient Correlator** tool is designed to efficiently perform pairwise correlations of thousands of epigenomic datasets. It supports many genomic signal file formats (bigWig, WIG and bedGraph), and offers the possibility to compute correlations at various resolutions (from 1 kb to 10 Mb) on predefined filtered regions (e.g. whole genome with or without blacklist-ed regions, only genes, TSS) and using the selected correlation metric (Pearson and Spearman), as well as the annotation and analysis of the generated correlation matrices. Most of the wrapping is coded in Python, while the core functionalities requiring high performance are coded in C++ using the openMP API for parallelization.  
    
A galaxy implementation including thousands of pre-computed public datasets is availalble at http://epigeec.genap.ca/galaxy/

For more information see the official repository for the epiGeEC tool at https://bitbucket.org/labjacquespe/epigeec 
  