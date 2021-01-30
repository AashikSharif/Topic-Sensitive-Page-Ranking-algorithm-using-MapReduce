
#!/usr/bin/env python

import re, sys
from operator import add
from pyspark import SparkContext


def computeContribs(urls, rank):
    num_urls = len(urls)
    for url in urls: yield (url, rank / num_urls)


def parseNeighbors(urls):
    parts = re.split(r'\s+', urls)
    return parts[0], parts[1]


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: pagerank <master> <file> <number_of_iterations> <topicfile>", file=sys.stderr)
        exit(-1)
    sc = SparkContext(sys.argv[1], "TopicSensitive")
    
    lines = sc.textFile(sys.argv[2], 1)
    pages = sc.textFile(sys.argv[4], 1)

    
    links = lines.map(lambda urls: parseNeighbors(urls)).distinct().groupByKey().cache()
    topics = pages.map(lambda urls: urls).distinct().cache().collect()
    nodedata = dict(sc.textFile("../crawlerdata/nodedata.csv").map(lambda line: line.split(",")).filter(lambda line: len(line)>1).map(lambda line: (line[0],line[1])).cache().collect())
    ranks = links.map(lambda url_neighbors: (url_neighbors[0], 1.0))

    #start=time.time()
    for iteration in range(int(sys.argv[3])):
        contribs = links.join(ranks).flatMap(lambda url_urls_rank:
            computeContribs(url_urls_rank[1][0], url_urls_rank[1][1]))
        ranks = contribs.reduceByKey(add).mapValues(lambda rank: rank * 0.85)
        new_ranks = [(v[0], v[1]) for i, v in enumerate(ranks.collect())]

        for number, i in enumerate(new_ranks):
            if i[0] in topics:
                new_ranks[number] = (i[0], i[1]+0.15)
        ranks = sc.parallelize(new_ranks)
    # print("\nIteration "+str(iteration)+" is OVER!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
    topranks = ranks.sortBy(lambda e: e[1], ascending = False)
   # end=time.time()

    def get_key(val):
    	for key, value in nodedata.items():
    		if val == value:
        		return key
    
    # print only top values
    i = 1
    print("\n\n\n**************************************************************\n\nTop 10 pages and ranks\n")
    for (link, rank) in topranks.collect():
        print("%s ----rank for link---- %s." % (rank,get_key(link)))
        if(i == 10): break
        i+=1
    print("\n**************************************************************\n\n\n")
    
#    print("\nTotal time taken - "+str(end-start)+"\n\n")
