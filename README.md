# Topic-Sensitive-Page-Ranking-algorithm-using-MapReduce



#### This README file is written by 

Aashik Sharif B  
121003003  
B.Tech CSE  
SASTRA Deemed to be University  

# for the reference of how to run this project in a standalone system.
_________________________________________________________________________________

I assume that you have installed **spark**,**pyspark**,**Gephi** and reqired **python packages**.  

## To run the program:  
## 1) Crawler  

   **SCRAPY** python package is used.  
   Change to the required format and path of FEED_FORMAT and FEED_URI in settings.py present inside sitegraph folder.  
   open command prompt as administrator and change directory to sitegraph/sitegraph.   
   *(Optional) Change the allowed domain and start url to whatever domains you want.*  
   Run this command `scrapy crawl graphspider`  

## 2) Pre-Processing
   
   Change the path of file that is read where you saved crawlerdata.  
   Change the path to where you want to save all the output files (pre-processed data).  
   Run the converter.py files to get preprocess data.  
   
## 3) Visualizing graph  
 
   **GEPHI** tool is used for visualization.  
   Open gephi and input the required edgelist from the pre-processed data. Visualise and play with the graph.   
   Try calculating pagerank and other algorithms present in its right.   

   *Make sure the allocation size for GEPHI is high so that it doesn't lag to render the graph for bigger dataset.*  

## 4) Mapreduce implementation of pagerank.py and topic_sensitive.py  
   
   To run pagerank.py execute the command in spark bin folder using command prompt. Syntax is given below    

   `spark-submit path\to\file\from\bin\folder\pagerank.py local[<number of threads>] path\to\file\from\bin\folder\<Edge_list_file> <Number_of_Iterations>`  

   Sample example is Given below.  
   
   `spark-submit ..\pagerank.py local[1] ..\crawlerdata\mylist.txt 10`  

   To run pagerank.py execute the command in spark bin folder using command prompt. Syntax is given below.    

   `spark-submit path\to\file\from\bin\folder\topic_sensitive.py local[<number of threads>] path\to\file\from\bin\folder\<Edge_list_file> <Number_of_Iterations> path\to\file\from\bin\folder\<Topics_file>`  

   It's Sample example is given below.  
   
   `spark-submit ..\topic_sensitive.py local[1] ..\crawlerdata\mylist.txt 10 ..\crawlerdata\Topics.txt`    

_________________________________________________________________________________


## [OUTPUTS](OUTPUTS/)

The outputs have been as per orderly manner of the steps proceeded to run the project.  
View and visualize output data as per the given order.  

The sample file gives a simple interpretation of files and was run still step 3 (i.e to visualize the graph using gephi and calculated the page rank using the gephi app)  

_________________________________________________________________________________

For futher queries or doubts:  
* mailto: ashiktcy.s@gmail.com  
* LinkedIn: [AashikSharif](https://www.linkedin.com/in/aashik-sharif-b-44ba40b5/)

_________________________________________________________________________________














