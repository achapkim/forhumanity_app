### How to use t-SNE

To get started, choose a group you want to visualize. Here are the groups available:

- **Noun:** 347 Nouns present in the AI incident summmary reports.
- **Verb:** 111 Verbs present in the AI incident summmary reports.
- **Adjective:** 119 Adjectives present in the AI incident summmary reports. 

You will be offered two ways of displaying the word embeddings:

- **Regular:** All 3000 samples will be shown in scatter dots.
- **Nearest Neighbors:** The 100 closest neighbors of the word selected, in term of Euclidean distances. To select a word, using the dropdown menu for this purpose. The neighbors will be shown in text.

Upon clicking a data point, you will be able to see the 5 closest neighbors of the word you clicked.

###  Word Embeddings

What if we could visualize words, with respect to how often they appear with each other? One way to do so is to visualize word embeddings, which are large collections of text (e.g. Wikipedia Articles, User Tweets, Web Scraped texts) reduced to smaller dimensions (50-d, 100-d, 200-d, etc.) that contain meaningful and compact information about how often words appear with each other, with respect to how often they are used. We used [Word2Vec](https://en.wikipedia.org/wiki/Word2vec) as our means of creating numerical representations of our words. 

### How does this work?

The t-SNE algorithm reduces the number of dimensions given by the Word2Vec algorithm, so that you can visualize it in low-dimensional space, i.e. in 2D or 3D. For each data point, you will now have a position on your plot, which can be compared with other data points to understand how close or far apart they are from each other.

### Choosing the right parameters

The quality of a t-SNE visualization depends heavily on the input parameters when you train the algorithm. Each parameter has a great impact on how well each group of data will be clustered. Here is what you should know for each of them:

- **Number of Iterations:** This is how many steps you want to run the algorithm. A higher number of iterations often gives better visualizations, but more time to train.
- **Perplexity:** This is a value that influences the number of neighbors that are taken into account during the training. According to the [original paper](https://lvdmaaten.github.io/publications/papers/JMLR_2008.pdf), the value should be between 5 and 50.
- **Learning Rate:** This value determines how much weight we should give to the updates given by the algorithm at each step. It is typically between 10 and 1000.

### References 

We were heavily inspired by this github repository to generate this portion [Dash-TSNE-App](https://github.com/plotly/dash-sample-apps/tree/main/apps/dash-tsne).
