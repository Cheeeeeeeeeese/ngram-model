from model import ngramModel
import save
import os
import glob

class userInterface:
    def __init__(self):
        # Initialization of the user interface
        pass

    def startInterface(self,model=None):
        # Start the user interface
        while True:
            inputInt = int(input("[1] Load training Data\n[2] Generate Text\n[3] Save model (Currently requires large amount of RAM with larger models)\n[4] Load model\n[5] Add dataset\n[6] Exit\n1-6: "))
            if inputInt == 1:
                try:
                    filepath = input("Filepath of unformatted Text: ")
                    n = int(input("Value for N: "))
                    model = ngramModel(n=n)
                    if os.path.isdir(filepath):
                        if filepath[-1] != "/":
                            filepath += "/"
                        for file in glob.glob(filepath+"*"):
                            print(filepath+"/"+file)
                            model.addDataSet(file)
                    else:
                        model.addDataSet(filepath)
                    print("Model has been trained")
                except ValueError:
                    print("Invalid value for N")
            elif inputInt == 2:
                if model != None:
                    contextString = input("Preceeding text: ")
                    textSize = input("Sentence amount: ")
                    if textSize == "":
                        textSize = 1
                    else:
                        textSize = int(textSize)
                    generatedText = model.generateAmountOfSentences(textSeed=contextString,sentNum=textSize)
                    result = ""
                    for sentence in generatedText:
                        for word in sentence:
                            result += word + " "
                    print(contextString + result)
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