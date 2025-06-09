import numpy as np
from sklearn.preprocessing import OneHotEncoder, normalize
from annoy import AnnoyIndex
import faiss


def train_model(df, features, target_column):
    X = df[features]
    y = df[target_column].reset_index(drop=True)
    encoder = OneHotEncoder(handle_unknown='ignore')
    X_encoded = encoder.fit_transform(X).toarray().astype(np.float32)
    X_encoded = normalize(X_encoded, axis=1)
    index = faiss.IndexFlatIP(X_encoded.shape[1])
    index.add(X_encoded)
    return encoder, index, y

def new_model(df, features, target_column):
    X = df[features]
    y = df[target_column].reset_index(drop=True)

    encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    X_encoded = encoder.fit_transform(X).astype(np.float32)

    X_encoded = normalize(X_encoded, axis=1)

    quantizer = faiss.IndexFlatIP(X_encoded.shape[1])
    index = faiss.IndexIVFFlat(quantizer, X_encoded.shape[1], nlist=100)
    index.train(X_encoded)
    index.add(X_encoded)

    return encoder, index, y



def train_annoy_model(df, features, target_column, n_trees=10):
    X = df[features]
    y = df[target_column].reset_index(drop=True)

    encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    X_encoded = encoder.fit_transform(X).astype(np.float32)
    X_encoded = normalize(X_encoded, axis=1)

    dims = X_encoded.shape[1]
    index = AnnoyIndex(dims, metric='angular') 

    for i, vec in enumerate(X_encoded):
        index.add_item(i, vec)

    index.build(n_trees)
    return encoder, index, y
