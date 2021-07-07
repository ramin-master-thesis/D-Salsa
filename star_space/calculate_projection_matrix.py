# Import modules
import os
from glob import glob

import numpy as np
import starwrap as sw

from definitions import ROOT_DIR

star_space_data_path = os.path.join(ROOT_DIR, "data", "StarSpace_data")

# Get models
list_models = glob(os.path.join(star_space_data_path, "models", "*", ""))


# Read all sentences
def read_all_train_sentences():
    print("reading train data")
    with open(f'{ROOT_DIR}/data/StarSpace_data/twitter_train_3M.txt', 'r', encoding='utf-8') as items:
        return [x.split('\t')[0] for x in items]


# Import model
def import_model(path):
    arg = sw.args()
    arg.trainMode = 2
    arg.thread = 20
    arg.verbose = True

    sp = sw.starSpace(arg)
    # sp.initFromSavedModel(os.path.join(path, 'model'))
    sp.initFromTsv(os.path.join(path, 'model.tsv'))
    return sp


sentences = read_all_train_sentences()
print("Load all sentences")

for model_path in list_models:
    print(f"Starting with {model_path}")
    if os.path.isfile(os.path.join(model_path, "projection_matrix.npy")):
        print(f"projection matrix exists for {model_path} skipping...")
        continue
    star_space = import_model(model_path)
    X = np.array([np.array(star_space.getDocVector(x, ' '))[0] for x in sentences])

    cov_mat = np.cov(X.T)
    # Compute the eigen values and vectors using numpy
    eig_vals, eig_vecs = np.linalg.eig(cov_mat)

    # Make a list of (eigenvalue, eigenvector) tuples
    eig_pairs = [(np.abs(eig_vals[i]), eig_vecs[:, i]) for i in range(len(eig_vals))]

    # Sort the (eigenvalue, eigenvector) tuples from high to low
    eig_pairs.sort(key=lambda x: x[0], reverse=True)

    # Hardcode it as log(number of partitions)
    num_vec_to_keep = 4

    # Compute the projection matrix based on the top eigen vectors
    num_features = X.shape[1]
    proj_mat = eig_pairs[0][1].reshape(num_features, 1)
    for eig_vec_idx in range(1, num_vec_to_keep):
        proj_mat = np.hstack((proj_mat, eig_pairs[eig_vec_idx][1].reshape(num_features, 1)))

    np.save(os.path.join(model_path, "projection_matrix.npy"), proj_mat)
    print("saved projection matrix")
