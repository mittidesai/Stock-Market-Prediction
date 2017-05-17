# Introduction

Current stock market trading strategies often depend on using the historic financial data for making predictions
about volatility of the future market. However, the historic data reflects only the past actions and not any information about public thought i.e. a major predictor of the market's future. Following
proven research that uses social data to predict other features of the market, we make a pitch for an attempt
to predict stock market volatility, return and trading volume of tech stocks using Semantic Vectors and Google Trends, which reflects real-time popularity of search terms. Our approach comprises of two steps: First, used New York Times API to download ~1 million documents and obtained a set of keywords related to the information technology
domain using semantic vectors. Then, we train a linear regression model to predict the volatility of
a future week using as input Google Trends data for those keywords in the previous week


# Architecture

We started with 20 set of "seed words" ( for example internet, computers, information etc. ) related to technology to query the New York Times (NYT) Article Search API, which allows access to the abstract, title, and content of all articles in the NYT from 1851. We searched published articles from January 1st, 2012 and created a corpus of 1 million articles to be used for semantic vector generation using Google's Word2vec tool. We generated total list of 30287 words each having 300 dimension
vector. We then clustered these vectors together into (k=120) classes to obtain similar set of words. Reason for choosing such a high "K" number is to get less than 500 words per cluster. We then handpicked one cluster which contained all our desired seed words and formed a distinct set of keywords to be used in market prediction.

# Data Processing 
Once we have set of keywords we are intersted in, we then download search volume interest for those words from google trends publicly available service. This serves as one of our input features to predict stock market. Since stock market is generally volatile, to measure the accuracy of the model we are calculating weekly log returns and stock volatility for every week and training a model to predict the same based on search volume interest of above keyword set. 


# Machine Learning
Data format contains stock price information, weekly log returns, stock volatility and search volume indices of ~800 words. Since number of features are very large, there will be possibility of overfitting if we try to build a model directly from the data. Hence we need to look for Principal component analysis for dimensionality reduction. We will also look at correlation factor to remove columns which has less correlation with the response target. 

With all dimensionality reduction, we should get ~40 keywords in our final dataset. It can then be fed to linear regression model to measure RMSE.