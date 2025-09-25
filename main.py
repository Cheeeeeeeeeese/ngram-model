from model import ngramModel
import save

myModel = None
while True:
    inputInt = int(input("[1] Load training Data\n[2] Generate Text\n[3] Save the model (Currently requires large amount of RAM with larger models)\n[4] Load a model\n[5] Add dataset\n[6] Exit\n1-6: "))

    if inputInt == 1:
        try:
            filepath = input("Filepath for unformatted Text: ")
            n = int(input("Value for N: "))
            myModel = ngramModel(filepath=filepath,n=n)
            myModel.load()
            myModel.train()
            print("Model has been trained")
        except ValueError:
            print("Invalid value for N")
        except:
            print("File not found")
    elif inputInt == 2:
        if myModel != None:
            inputInt = int(input("[1] Generate text with context\n[2] Generate singular sentence\n1-2: "))
            if inputInt == 1:
                contextString = input("Preceeding text: ")
                textSize = int(input("Text size: "))
                print(myModel.generateTextWithInput(contextString,wordNum=textSize))
            elif inputInt == 2:
                wordNum = int(input("Length of the sentence: "))
                print(myModel.generateSentence(wordNum=wordNum))
            else:
                print("Invalid input")
        else:
            print("No model has been trained or loaded")
    elif inputInt == 3:
        if myModel != None:
            filepath = input("Save filepath: ")
            save.saveModel(model=myModel,filepath=filepath)
            print("Model has been saved")
        else:
            print("No model has been trained or loaded")
    elif inputInt == 4:
        try:
            filepath = input("Load filepath: ")
            myModel = save.loadModel(filepath=filepath)
            print("Model has been loaded")
        except:
            print("File not found")
    elif inputInt == 5:
        try:
            inputString = input("Filepath for unformatted Text: ")
            myModel.addDataSet(inputString)
            print("Dataset added")
        except:
            print("File not found")
    elif inputInt == 6:
        break
    else:
        print("Invalid input")