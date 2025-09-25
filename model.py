from nltk.tokenize import ToktokTokenizer
from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk.lm import MLE
import re

class ngramModel:
    def __init__(self,filepath=None,n=2):
        # Initialize the n-gram model with a specified value of n (default is 2 for bigrams)
        # If the value of n is less than or equal to 0, an exception is raised
        if n <= 0:
            raise Exception("Value of N must be larger than 0")
        else:
            self.n = n
        # instance variables initialization
        self.filepath = filepath
        self.tokenizedText = ''
        self.model = MLE(self.n)
        self.text = ''

    def load(self):
        # Open the text file and save text in a variable
        file = open(self.filepath)
        self.text = file.read()
        
        # Close the file to prevent unintended behaviour
        file.close()

    def train(self,addDataSet=False):
        # Tokenize the training data
        toktok = ToktokTokenizer()
        wordTokenize = toktok.tokenize
        # Save the rules for tokenization. A lambda function and a regular expression are being used to split the training data appropriately
        sentTokenize = lambda x: re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', x)

        # Apply tokenization to every sentence using the rules previously defined
        self.tokenizedText = [list(map(str.lower, wordTokenize(sent))) for sent in sentTokenize(self.text)]

        # delete text that is not needed anymore to optimize model size
        del(self.text)

        # use the padded_everygram_pipeline to pad every sentence with <s> in the beginning and </s> in the end to specify the sentence beginnings and ends
        trainData, paddedSents = padded_everygram_pipeline(self.n, self.tokenizedText)

        # if the user specified to add a dataset to the existing one, the vocabulary must be updated to the new tokens added
        if len(self.model.vocab) > 0 and addDataSet:
            self.model.vocab.update(paddedSents)
            self.model.fit(trainData, paddedSents)
        else:
            self.model.fit(trainData, paddedSents) # train the model on the training data previously generated


        # delete already used training data to optimize model size in RAM and on disk
        del(self.tokenizedText)
        #del(train_data)
        #del(padded_sents)

    def addDataSet(self,filepath):
        # add a dataset to an already trained model
        self.filepath = filepath
        self.load()
        self.train(addDataSet=True)

    def generateSentence(self,wordNum=None,randomSeed=None,textSeed=None):
        # generate a sentence
        sent = []

        # if a wordNum value has been given, only generate so many words
        if wordNum != None:
            for word in self.model.generate(wordNum, random_seed=randomSeed):
                if word == '<s>':
                    continue
                # if the sentence end has been reached, append a '.' and break 
                elif word == '</s>':
                    sent.append('.')
                    break
                sent.append(word)
        # if no limit has been given, generate until a sentence end (</s>) has been reached
        else:
            currentWord = ''
            # Will indefinitely generate words with context of the previous words and sentences until the end of a sentence is reached
            while currentWord != '.':
                currentWord = self.model.generate(text_seed=textSeed.split(' ')+sent,random_seed=randomSeed)
                
                # </s> is being substituted for a '.' to make the text more human friendly 
                if currentWord == '</s>':
                    currentWord = '.'
                
                # <s> is being substituted for an empty string to make the text more human friendly 
                elif currentWord == '<s>':
                    continue
                sent.append(currentWord)
        return sent
    
    def generateAmountOfSentences(self,sentNum=1,textSeed=None,randomSeed=None):
        # simple for loop to generate a specified amount of full sentences
        sent = []
        for i in range(sentNum):
            sent.append(self.generateSentence(textSeed=textSeed,randomSeed=randomSeed))
        return sent