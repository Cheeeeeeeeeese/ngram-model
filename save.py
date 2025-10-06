import dill

# use dill to save model on disk
def saveModel(model, filepath):
    with open(filepath, 'wb') as fout:
        dill.dump(model, fout)

# use dill to load model from disk
def loadModel(filepath):
    with open(filepath, 'rb') as fin:
        model = dill.load(fin)
    return model