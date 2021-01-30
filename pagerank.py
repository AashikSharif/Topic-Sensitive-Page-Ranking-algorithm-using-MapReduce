
#!/usr/bin/env python

import re, sys
from operator import add
#import time

from pyspark import SparkContext


def computeContribs(urls, rank):
    """Calculates URL contributions to the rank of other URLs."""
    num_urls = len(urls)
    for url in urls: yield (url, rank / num_urls)


def parseNeighbors(urls):
    """Parses a urls pair string into urls pair."""
    parts = re.split(r'\s+', urls)
    return parts[0], parts[1]


if __name__ == "__main__":
    print(sys.argv[1])
    if len(sys.argv) < 3:
        print("Usage: pagerank <master> <file> <number_of_iterations>", file=sys.stderr)
        exit(-1)
    
    # Initialize the spark context.
    sc = SparkContext(sys.argv[1], "PythonPageRank")

    # Loads in input file. It should be in format of:
    #     URL         neighbor URL
    #     URL         neighbor URL
    #     ...
    
    lines = sc.textFile(sys.argv[2], 1)
    
    # Loads all URLs from input file and initialize their neighbors.
    links = lines.map(lambda urls: parseNeighbors(urls)).distinct().groupByKey().cache()
    
    nodedata = sc.textFile("../crawlerdata/nodedata.csv").map(lambda line: line.split(",")).filter(lambda line: len(line)>1).map(lambda line: (line[0],line[1])).collect()
    #print(nodedata)
    # Loads all URLs with other URL(s) link to from input file and initialize ranks of them to one.
    ranks = links.map(lambda url_neighbors: (url_neighbors[0], 1.0))
    # Calculates and updates URL ranks continuously using PageRank algorithm.

    #start=time.time()
    for iteration in range(int(sys.argv[3])):
        # Calculates URL contributions to the rank of other URLs.
        contribs = links.join(ranks).flatMap(lambda url_urls_rank:
            computeContribs(url_urls_rank[1][0], url_urls_rank[1][1]))
        # Re-calculates URL ranks based on neighbor contributions.
        ranks = contribs.reduceByKey(add).mapValues(lambda rank: rank * 0.85 + 0.15)
    # Collects all URL ranks and dump them to console.
    #end=time.time()
    # Sorts the ranks in Descending order
    topranks = ranks.sortBy(lambda e: e[1], ascending = False)
    

    nodedata=dict(nodedata)
    def get_key(val):
    	for key, value in nodedata.items():
    		if val == value:
        		return key
    

    # print only top values
    i = 1
    print("\n\n\n**************************************************************\n\nTop 10 pages and ranks\n")
    for (link, rank) in topranks.collect():
        print("%s ----rank for link---- %s." % (rank,get_key(link)))
        if(i == 11): break
        i+=1
    print("\n**************************************************************\n\n\n")
#
#    print("\nTotal time taken - "+str(end-start)+"\n\n")
