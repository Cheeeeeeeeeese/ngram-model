from nltk.tokenize import ToktokTokenizer
from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk.lm import MLE
import re
import dill
import pandas as pd

class ngramModel:
    def __init__(self,filepath=None,n=2):
        if n <= 0:
            raise Exception("Value of N must be larger than 0")
        else:
            self.n = n
        self.filepath = filepath
        self.tokenizedText = ''
        self.model = None
        self.text = ''

    def load(self):
        file = open(self.filepath)
        self.text = file.read()
        file.close()
    
    def train(self,addDataSet=False):
        toktok = ToktokTokenizer()
        wordTokenize = toktok.tokenize
        sentTokenize = lambda x: re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', x)

        self.tokenizedText = [list(map(str.lower, wordTokenize(sent))) for sent in sentTokenize(self.text)]
        
        # delete text that is not needed anymore to optimize model size 
        del(self.text)

        trainData, paddedSents = padded_everygram_pipeline(self.n, self.tokenizedText)

        # if new data is being added, do not create new MLE object
        if not addDataSet:
            self.model = MLE(self.n)
        self.model.fit(trainData, paddedSents)

        if addDataSet:
            self.model.vocab.update()

        # delete already used training data to optimize model size in RAM and on disk 
        del(self.tokenizedText)
        #del(train_data)
        #del(padded_sents)

    def addDataSet(self,filepath):
        self.filepath = filepath
        self.load()
        self.train(addDataSet=True)

    def generateSentence(self,wordNum=None,seed=None):
        sent = []
        if wordNum != None:
            for word in self.model.generate(wordNum, random_seed=seed):
                if word == '<s>':
                    continue
                elif word == '</s>':
                    break
                sent.append(word)
            return sent

    def generateTextWithInput(self,wordSeed,wordNum=None,seed=None):
        sent = wordSeed.split(' ')
        for i in range(wordNum):
            word = self.model.generate(text_seed=sent)
            if word == '</s>':
                word = '.'
                sent.append(word)
            elif word == '<s>':
                continue
            else:
                sent.append(word)
        return sent

    
