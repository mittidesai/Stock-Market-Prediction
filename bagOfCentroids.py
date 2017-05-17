from gensim.models import Word2Vec
from sklearn.cluster import KMeans
import time
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from bs4 import BeautifulSoup
import re
from nltk.corpus import stopwords
import numpy as np
import os




if __name__ == '__main__':
    model = Word2Vec.load("300features_40minwords_10context")

    # Run k means on the word vectors and print a few clusters

    start = time.time()
    # set k clusters to be 1/100th of the vocabulary size or average 100 words per cluster

    word_vectors  = model.wv.syn0
    print word_vectors.shape
    num_clusters  = word_vectors.shape[0] / 250
    print num_clusters

    # initialize k-means object and use it to extract centroids
    print 'Running k means'
    kmeans_clustering = KMeans( n_clusters = num_clusters)
    idx = kmeans_clustering.fit_predict(word_vectors)

    end = time.time()
    elapsed = end - start

    print "Time taken for K Means clustering: ", elapsed, "Seconds"

    #Create a word / index dictionary, mapping each vocabulary word to a cluster number
    word_centroid_map = dict(zip( model.wv.index2word, idx))
    f = open('output','w')

    # print first 1000 clusters
    for cluster in xrange(0,num_clusters):
        # print the cluster number

        print "Cluster %d" %cluster
        f.write("\nCluster %d\n"%cluster)
        words = []
        for i in xrange(0, len(word_centroid_map.values())):
            if ( word_centroid_map.values()[i] == cluster):
                words.append(word_centroid_map.keys()[i])
        #print words
        f.write(','.join(words))
        f.flush()
    f.close()
