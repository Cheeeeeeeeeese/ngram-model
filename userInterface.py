from model import ngramModel
import save
import os

class userInterface:
    def __init__(self):
        pass

    def startInterface(self,model=None):
        while True:
            inputInt = int(input("[1] Load training Data\n[2] Generate Text\n[3] Save model (Currently requires large amount of RAM with larger models)\n[4] Load model\n[5] Add dataset\n[6] Exit\n1-6: "))

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
                    contextString = input("Preceeding text: ")
                    textSize = input("Sentence amount: ")
                    if textSize == "":
                        textSize = 1
                    print(model.generateAmountOfSentences(textSeed=contextString,sentNum=textSize))
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