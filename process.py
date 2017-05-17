import pandas as pd
import glob
import nltk
import logging
import numpy as np
from gensim.models import Word2Vec
import re

DIRECTORY = "./data/articles"


# removing stop words is optional since it is required to generate good word2vec model

def preprocessing_text_wordlist(article,remove_stopwords=False):

    # remove non-letters
    words = re.sub("[^a-zA-Z]"," ", article)

    # convert words to lower case and split them
    words = words.lower().split()

    if remove_stopwords:
        stops = set(stopwords.words("english"))
        words = [w for w in words if not w in stops]

    return (words)



def preprocessing_text_sentence(article, tokenizer, remove_stopwords = False):
    # Function to split a review into parsed sentences.

    # 1. Use the nltk tokenizer to split the paragraph into sentences
    raw_sentences = tokenizer.tokenize(article.decode('utf8').strip())

    # 2. Loop over each sentence
    sentences = []
    for raw_sentence in raw_sentences:
        # if a sentences empty, skip it
        if len(raw_sentence) > 0 :
            # otherwise, call review_to_wordlist to get list of words
            sentences.append(preprocessing_text_wordlist( raw_sentence, remove_stopwords))

    # return the list of sentences ( each sentence is list of words, so this returns a list of lists )
    return sentences


if __name__ == '__main__':
    # read all csv files inside the directory and combine into one
    allFiles = glob.glob(DIRECTORY+"/*.csv")
    frame = pd.DataFrame()
    list_ = []

    for file_ in allFiles:
        df = pd.read_csv(file_, index_col = None, header = 0)
        list_.append(df)

    frame = pd.concat(list_)

    print frame.columns


    # Load the punkt tokenizer
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    print(type(tokenizer))

    sentences = []
    print "Parsing sentences from training set"
    for text in frame["text"]:
        sentences += preprocessing_text_sentence(text, tokenizer)


    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.INFO)

    # Set values for various parameters
    num_features = 300          # Word vector dimensionality
    min_word_count = 40         # Minimum word count
    num_workers   = 4           # Number of threads to run parallel
    context       = 10          # context window size
    downsampling  = 1e-3        # downsampling setting for frequent words

    # initialize the train model
    print "Training Word2Vec model"
    model = Word2Vec(sentences, workers = num_workers, size = num_features,
                min_count = min_word_count, window = context, sample = downsampling, seed = 1)

    model.init_sims(replace=True)

    model_name = "300features_40minwords_10context"
    model.save(model_name)

    print "finish"

