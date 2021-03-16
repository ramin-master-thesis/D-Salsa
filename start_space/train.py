import starwrap as sw

from start_space import current_directory

if __name__ == "__main__":
    arg = sw.args()
    arg.trainFile = f'{current_directory}/../data/twitter_train130k.txt'
    arg.trainMode = 2
    arg.initRandSd = 0.01
    arg.adagrad = True
    arg.ngrams = 1
    arg.lr = 0.05
    arg.margin = 0.05
    arg.epoch = 20
    arg.thread = 40
    arg.dim = 300
    arg.negSearchLimit = 100
    arg.dropoutRHS = 0.8
    arg.fileFormat = 'labelDoc'
    arg.similarity = "cosine"
    arg.minCount = 5
    arg.normalizeText = True
    arg.verbose = True

    sp = sw.starSpace(arg)
    sp.init()
    sp.train()

    sp.saveModelTsv(f'{current_directory}/../data/models/model.tsv')
