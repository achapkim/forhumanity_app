import os
import pathlib
from sklearn.manifold import TSNE
import numpy as np
import pandas as pd

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

iterations_ls = [250, 500, 750, 1000]
perplexity_ls = [3, 10, 30, 50, 100]
learning_rate_ls = [10, 50, 100, 200]

def generate_embedding(
    iterations, perplexity, learning_rate
):
    path = f"iterations_{iterations}_perplexity_{perplexity}_learning_rate_{learning_rate}.csv"

    vocab = pd.read_csv(DATA_PATH.joinpath("vocabulary_clean.csv"), index_col = 0)
    coords = pd.read_csv(DATA_PATH.joinpath("vector_coordinates.csv"),converters={"vector": lambda x: x.strip("[]").replace("\n", "").split()}, index_col = 0)
    coords['vector'] = coords['vector'].apply(lambda lst: [float(x) for x in lst if x])


    tsne = TSNE(
        n_components=2,
        n_iter=iterations,
        learning_rate=learning_rate,
        perplexity=perplexity,
        random_state=1131,
    )
    
    embedding = tsne.fit_transform(np.array([l for l in coords.vector]))
    
    coords['x'] = embedding[:,0]
    coords['y'] = embedding[:,1]
    
    coords= coords.merge(vocab.reset_index(), on='term_str')
    coords= coords.set_index('term_str')
    
    coords.to_csv(DATA_PATH.joinpath(path))


for iterations in iterations_ls:
    for perplexity in perplexity_ls:
        for learning_rate in learning_rate_ls:
            generate_embedding(
                    iterations,
                    perplexity,
                    learning_rate,
                )