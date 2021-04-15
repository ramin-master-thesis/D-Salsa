import logging
import os

import starwrap as sw

from star_space import current_directory
from sklearn.model_selection import ParameterGrid


handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log = logging.getLogger('StarSpace')
log.addHandler(handler)
log.setLevel(logging.DEBUG)

if __name__ == "__main__":
    param_grid = {
        "initRandSd": [0.01],
        "adagrad": [True],
        "ngrams": [1],
        "lr": [0.01, 0.05],
        "margin": [0.05],
        "epoch": [20],
        "dim": [100, 300],
        "negSearchLimit": [100],
        "dropoutRHS": [0.5, 0.8],
        "fileFormat": ['labelDoc'],
        "similarity": ['cosine'],
        "minCount": [5],
        "normalizeText": [True, False],
    }

    list_params = list(ParameterGrid(param_grid))
    total_trainings = len(list_params)
    trained = 1

    for param in list_params:
        log.info("Initializing Parameters...")

        arg = sw.args()

        arg.trainFile = f'{current_directory}/../data/StarSpace_data/twitter_train_3M.txt'
        arg.trainMode = 2
        arg.thread = 40
        arg.verbose = True

        log.debug(f"started {param}")
        arg.initRandSd = param.get('initRandSd')
        arg.adagrad = param.get('adagrad')
        arg.ngrams = param.get('ngrams')
        arg.lr = param.get('lr')
        arg.margin = param.get('margin')
        arg.epoch = param.get('epoch')
        arg.dim = param.get('dim')
        arg.negSearchLimit = param.get('negSearchLimit')
        arg.dropoutRHS = param.get('dropoutRHS')
        arg.fileFormat = param.get('fileFormat')
        arg.similarity = param.get('similarity')
        arg.minCount = param.get('minCount')
        arg.normalizeText = param.get('normalizeText')

        log.debug("check if model exists...")
        folder_path = f"{current_directory}/../data/StarSpace_data/models"

        folder_name = f"initRandSd_{arg.initRandSd}_adagrad_{arg.adagrad}_lr_{arg.lr}_margin_{arg.margin}" \
                      f"_epoch_{arg.epoch}_dim_{arg.dim}" \
                      f"_negSerachLimit_{arg.negSearchLimit}_dropoutRHS_{arg.dropoutRHS}" \
                      f"_minCount_{arg.minCount}_normalizeText_{arg.normalizeText}"

        model_location = os.path.join(folder_path, folder_name)

        model_file_path = os.path.join(model_location, "model")
        model_tsv_file_path = os.path.join(model_location, "model.tsv")

        if not os.path.isdir(model_location):
            log.info("model does not exist...")
            os.mkdir(model_location)
        else:
            if os.path.isfile(model_file_path):
                log.info("model already exists...")
                continue

        log.info("Initializing StarSpace...")
        sp = sw.starSpace(arg)
        sp.init()
        sp.train()

        sp.saveModel(model_file_path)
        sp.saveModelTsv(model_tsv_file_path)
        log.info(f"saved model. {total_trainings - trained}/{total_trainings}")
        trained += 1
