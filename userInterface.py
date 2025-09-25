from model import ngramModel
import save
import os

class userInterface:
    def __init__(self):
        pass

    def startInterface(self,model=None):
        while True:
            inputInt = int(input("[1] Load training Data\n[2] Generate Text\n[3] Save the model (Currently requires large amount of RAM with larger models)\n[4] Load a model\n[5] Add dataset\n[6] Exit\n1-6: "))

            if inputInt == 1:
                try:
                    filepath = input("Filepath of unformatted Text: ")
                    n = int(input("Value for N: "))
                    model = ngramModel(n=n)
                    if os.path.isdir(filepath):
                        print("isDir")
                        for file in os.listdir(filepath):
                            print(filepath+"/"+file)
                            model.addDataSet(filepath+"/"+file)
                    else:
                        model.load()
                        model.train()
                    print("Model has been trained")
                except ValueError:
                    print("Invalid value for N")
                #except:
                #    print("File not found")
            elif inputInt == 2:
                if model != None:
                    inputInt = int(input("[1] Generate sentences with context\n[2] Generate sentences without context\n1-2: "))
                    if inputInt == 1:
                        contextString = input("Preceeding text: ")
                        textSize = int(input("Sentence amount: "))
                        print(model.generateAmountOfSentences(textSeed=contextString,sentNum=textSize))
                    elif inputInt == 2:
                        try:
                            wordNum = int(input("Limit the length of the sentence (will stop if '.' is reached): "))
                            print(model.generateSentence(wordNum=wordNum))
                        except ValueError:
                            print("Invalid value for length of the sentence")
                    else:
                        print("Invalid input")
                else:
                    print("No model has been trained or loaded")
            elif inputInt == 3:
                if model != None:
                    filepath = input("Save filepath: ")
                    save.saveModel(model=model,filepath=filepath)
                    print("Model has been saved")
                else:
                    print("No model has been trained or loaded")
            elif inputInt == 4:
                try:
                    filepath = input("Load filepath: ")
                    model = save.loadModel(filepath=filepath)
                    print("Model has been loaded")
                except:
                    print("File not found")
            elif inputInt == 5:
                try:
                    inputString = input("Filepath of unformatted Text: ")
                    model.addDataSet(inputString)
                    print("Dataset added")
                except:
                    print("File not found")
            elif inputInt == 6:
                break
            else:
                print("Invalid input")